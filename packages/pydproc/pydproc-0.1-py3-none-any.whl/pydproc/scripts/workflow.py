# import dependencies
from pathlib import Path
import yaml
import os
import shutil
import docker
import json, requests

# internal imports
from pydproc.scripts.definitions import docker_base_path, saved_images_path, saved_data_path

# load client for docker. This requires user set env variables $DOCKER_USERNAME and $DOCKER_PASSWORD
client = docker.from_env()
# Maps image name to containers running it
containers = {}
# Defines default values for YAML file
default_values = {'api_key':'a4b7b2df254a30de3f19c89b8f8be2b9', 'city_name': 'Seattle'}

def make_docker_dir(specs):
    new_image_path = saved_images_path / specs['proc_name']
    if new_image_path.exists():
        shutil.rmtree(new_image_path)

    # Copy docker dir template
    shutil.copytree(docker_base_path, new_image_path)

    # Overwrite proc.yml
    with open(new_image_path / "proc.yml", "w+") as f:
        f.write(yaml.dump(specs))

    # Rewrite build and run scripts
    with open(new_image_path / "build.sh", "r+") as f:
        build_script = f.read().format(IMAGE_NAME=specs['proc_name'])
    with open(new_image_path / "build.sh", "w") as f:
        f.write(build_script)

    with open(new_image_path / "run.sh", "r+") as f:
        run_script = f.read().format(IMAGE_NAME=specs['proc_name'])
    with open(new_image_path / "run.sh", "w") as f:
        f.write(run_script)


def fromyml(spec_file: str):
    """
    Build docker image from yml file as input
    :param spec_file: path to spec file
    :return:
    """
    spec_file = Path(os.path.abspath(spec_file))

    # Check if spec file exists
    if not spec_file.exists():
        raise FileNotFoundError(f"No file found at {spec_file}")

    # Load and process spec_file
    with open(spec_file, "r+") as f:
        specs = yaml.safe_load(f)
        if not "proc_name" in specs: specs["proc_name"] = os.path.basename(spec_file).strip(".yml")

    # Make new docker dir
    make_docker_dir(specs)

    # Build and tag new docker image
    build_pathway = os.path.abspath(saved_images_path / specs['proc_name'])
    client.images.build(path=build_pathway, tag=f"pydproc/{specs['proc_name']}")
                        
    # os.system("docker build -t pydproc/weather " + build_pathway)

def start(proc_name: str):
    """
    Start docker container and mounts saved_data folder
    :param proc_name: name of image in pydproc repo
    """
    image_name = f'pydproc/{proc_name}:latest'
    if not image_name in [i.tags[0] for i in client.images.list() if len(i.tags) > 0]:
        print(f'ERROR: pydproc/{proc_name} docker image has not been built yet.')
        return

    if not proc_name in containers.keys():
        containers[proc_name] = {}

    run_name = f'{proc_name}-{len(containers[proc_name])}'
    new_save_dir = saved_data_path / run_name
    os.mkdir(new_save_dir)

    print(f'Starting new run {run_name}')
    container = client.containers.run(image_name, 'python run_proc.py',
        volumes={str(new_save_dir): {'bind': '/saved_data', 'mode': 'rw'}}, stream=True, detach=True, remove=True)
     # os.system("docker run --rm -v $PWD/saved_data:/workdir/saved_data pydproc_weather")
                        
    # Save logs
    with open(new_save_dir / (run_name + ".log"), "w+") as log_file:
        log_file.write(str(container.logs()))

    containers[proc_name][run_name] = container

def stop(run_name):
    # stop the container in containers[proc_name][run_name]
    proc_name=run_name[:run_name.rfind('-')]
    containers[proc_name][run_name].pause()
    print("Pausing docker container " + run_name)

def remove(run_name):
    sure = input("Are you sure you want to remove this container? y/n : ")

    if (sure == "n"):
        return
    elif (sure != "y"):
        return
    
    proc_name=run_name[:run_name.rfind('-')]
    containers[proc_name][run_name].remove(force=True)
    print("Removed docker container " + run_name)

def restart(run_name):
    # TODO parse run_name for proc_name
    # TODO stop the container in containers[proc_name][run_name]
    pass

def get_data(run_name, destination):
    # TODO search saved_data_path for run_name and shutil.copytree() it to destination
    pass

def validate(path):
    with open(path) as f:
        ymlspecs = yaml.safe_load(f)

    base_url = ymlspecs['base_url']
    url_params = list(ymlspecs['url_params'].keys())
    desired_params = []

    for i in range(0, len(base_url)):
        if base_url[i] == '{':
            i += 1
            in1 = i
            while base_url[i] != '}':
                i += 1
            in2 = i
            desired_params.append(base_url[in1:in2])

    # TODO: update yaml file with any changed parameters if required
    while len(url_params) != 0:
        try:
            c1 = desired_params.pop(0)
            c2 = url_params.pop(0)
        except:
            print('WARNING: Missing required URL parameters.')
            while len(url_params) != 0:
                cur = url_params.pop(0)
                print('Filling in ' + cur + 'with default value ' + default_values[cur])
        if desired_params.pop(0) != url_params.pop(0):
              print('WARNING: incorrect paramters, replacing ' + c1 + ' with ' + c2 + 'with default value ' + default_values[c2]) 

    while len(desired_params) != 0:
        print("WARNING: unused parameter " + desired_params.pop(0))
    
    api_call = requests.get(base_url.format(**ymlspecs['url_params'])).json()
    desired_fields = ymlspecs['fields_to_save']
    print('Validating data...')
    __recur_fields(desired_fields, api_call)
    print('Validation passed with no errors.')
                      

if __name__ == "__main__":
    # TODO Uncomment this for when we create cli
    # globals()[sys.argv[1]]()

    fromyml("./examples/weather.yml")
    start("weather")
