# import dependencies
from pathlib import Path
import yaml
import os
import shutil
import docker
import json, requests
import pickle

# internal imports
from pydproc.scripts.definitions import docker_base_path, saved_images_path, \
    saved_data_path, run_dict_path

# load client for docker. This requires user set env variables $DOCKER_USERNAME and $DOCKER_PASSWORD
client = docker.from_env()
# Maps image name to containers running it
containers = {}

if run_dict_path.exists():
    with run_dict_path.open('r+b') as run_dict_file:
        if os.stat(run_dict_path).st_size > 0:
            containers = pickle.load(run_dict_file)

# Defines default values for YAML file
default_values = {'api_key': 'a4b7b2df254a30de3f19c89b8f8be2b9', 'city_name': 'Seattle'}


def make_docker_dir(specs):
    """
    Makes a docker directory to build image from

    :param specs: python dictionary containing all relevant information from user-specified YAML file
    """

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
    Start docker container and mount new saved_data/run_name folder for the run

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
                                      volumes={str(new_save_dir): {'bind': '/saved_data', 'mode': 'rw'}}, stream=True,
                                      detach=True, remove=True)
    # os.system("docker run --rm -v $PWD/saved_data:/workdir/saved_data pydproc_weather")

    # Save logs
    with open(new_save_dir / (run_name + ".log"), "w+") as log_file:
        log_file.write(str(container.logs()))

    containers[proc_name][run_name] = {"container": container.id, "paused": False}
    update_containers()


def stop(run_name):
    """
    Pauses a specified docker container

    :param run_name: name corresponding to single docker container
    """
    # stop the container in containers[proc_name][run_name]
    proc_name = run_name[:run_name.rfind('-')]
    client.containers.get(containers[proc_name][run_name]["container"]).pause()
    containers[proc_name][run_name]["paused"] = True
    print("Pausing docker container " + run_name)
    update_containers()


def remove(run_name):
    """
    Removes a running docker container by force

    :param run_name: is name corresponding to single docker container
    """
    # removes running docker container forcefully, leaves image
    sure = input("Are you sure you want to remove this container? y/n : ")

    if (sure == "n"):
        return
    elif (sure != "y"):
        return

    proc_name = run_name[:run_name.rfind('-')]
    client.containers.get(containers[proc_name][run_name]["container"]).remove(force=True)

    containers[proc_name][run_name]["container"] = None
    containers[proc_name][run_name]["paused"] = None

    print("Removed docker container " + run_name)
    update_containers()


def restart(run_name):
    """
    Unpauses a running docker container

    :param run_name: is name corresponding to single docker container
    """
    # Unpauses the container in containers[proc_name][run_name]
    proc_name = run_name[:run_name.rfind('-')]
    client.containers.get(containers[proc_name][run_name]["container"]).unpause()
    containers[proc_name][run_name]["paused"] = False
    print("Unpausing docker container " + run_name)
    update_containers()


def get_data(run_name, destination):
    """
    Copies data files produced by docker container associated with run_name into
    specified destination on local computer

    :param run_name: is name corresponding to a single docker container
    :param destination: is filepath on local machine
    """

    # search saved_data_path for run_name and shutil.copytree() it to destination
    if Path(destination).exists():
        print("Destination must be a directory that does not exist.")
        return
    shutil.copytree(saved_data_path / run_name, destination)
    print("Files in " + run_name + " Copied to " + destination)


def list_containers(run_name=None):
    """
    list containers and their run_names

    :params run_name: is name corresponding to a single docker container
    """
    if (run_name != None):
        proc_name = run_name[:run_name.rfind('-')]
        listed = containers[proc_name][run_name]["container"]

        if (listed != None):
            listedc = client.containers.get(listed)
            print(f'Run name: {run_name}, ID: {listed}, Image: {listedc.image}, \
                  Status: {listedc.status}, Paused: {containers[proc_name][run_name]["paused"]}')
    else:
        for item in containers.items():
            container_dict = item[1]

            for container in container_dict.items():
                if (container[1]["container"] != None):
                    listedc = client.containers.get(container[1]["container"])
                    print(f'Run name: {container[0]}, ID: {container[1]["container"]}, Image: {listedc.image}, \
                          Status: {listedc.status}, Paused: {container[1]["paused"]}')


def validate(path):
    """
    Ensures url_params and fields_to_save specs in yml file are correct and exist when return API
    data
    
    :param path: path to yml file
    """

    def recur_fields(api_call, desired_fields):
        """
        Reads through API data to make sure client desired data is present

        :param api_call: is the working API data in a dict
        :param desired_fields: is the client desired data in a dict
        """
        for element in desired_fields:
            if isinstance(element, dict):
                keys = list(element.keys())
                try:
                    for k in keys:
                        cur1 = element[k]
                        cur2 = api_call[k]
                        recur_fields(cur1, cur2)
                except:
                    raise Exception('WARNING: Incorrect desired data')
            else:
                for l in desired_fields:
                    if l not in api_call:
                        print(desired_fields)
                        print(api_call)
                        raise Exception('WARNING: desired data ' + l + ' not present in desired data')

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

    while len(url_params) != 0:
        try:
            c1 = desired_params.pop(0)
            c2 = url_params.pop(0)
            if desired_params.pop(0) != url_params.pop(0):
                print('WARNING: incorrect paramters, replacing ' + c1 + ' with ' + c2 + 'with default value ' +
                      default_values[c2])
                ymlspecs[url_params][c2] = default_values[c2]
        except:
            print('WARNING: Missing required URL parameters.')
            while len(url_params) != 0:
                cur = url_params.pop(0)
                print('Filling in ' + cur + 'with default value ' + default_values[cur])
                ymlspecs[url_params][cur] = default_values[cur]

    while len(desired_params) != 0:
        print("WARNING: unused parameter " + desired_params.pop(0))

    api_call = requests.get(base_url.format(**ymlspecs['url_params'])).json()
    try:
        desired_fields = ymlspecs['fields_to_save']
        print(desired_fields)
        print('Validating data...')
        recur_fields(api_call, desired_fields)
        print('Validation passed with no errors.')
    except:
        print('missing fields to save, using all data from api call')

    with open(path, 'w') as f:
        f.write(yaml.dump(ymlspecs))
    return ymlspecs


def buildspecs():
    """
    Build specs

    :return: a dictionary representing the specs
    """

    def is_int(s):
        """
        Simple helper method to check if a string can be cast to an int

        :param: s: string that you want to check
        :return: boolean as to whether or not it can be cast to an int
        """
        try:
            int(s)
            return True
        except ValueError:
            return False

    def create_dict():
        """
        Helper method used to take user input and build a tiered dictionaries
        """
        l = []
        keep_adding = True

        while keep_adding:
            return_dict = {}
            field_name = input('Input data field name: ')
            if is_int(field_name):
                field_name = int(field_name)

            nested_dict = input('Do you want to map a dictionary to this data? (\'y\'/\'n\') ')
            while nested_dict != 'y' and nested_dict != 'n':
                print('Response must be a \'y\' or \'n\'!')
                nested_dict = input('Do you want to map a dictionary to this data? (\'y\'/\'n\') ')

            if nested_dict == 'y':
                return_dict[field_name] = create_dict()
                l.append(return_dict)
            elif nested_dict == 'n':
                l.append(field_name)

            cont_add = input('Continue adding data on this level? (\'y\'/\'n\') ')
            while cont_add != 'y' and cont_add != 'n':
                print('Response must be a \'y\' or \'n\'!')
                cont_add = input('Continue adding data on this level? (\'y\'/\'n\') ')

            if cont_add == 'y':
                keep_adding = True
            elif cont_add == 'n':
                keep_adding = False

        return l

    yml_dict = {'base_url': '', 'url_params': {}, 'fields_to_save': [], 'time_interval': 0, 'max_requests': 0}

    yml_dict['base_url'] = input("Input API URL with API fields present in the URL enclosed with {}  ")

    need_fields = input('Are there fields required for calling the API? (\'y\'/\'n\') ')
    while need_fields != 'y' and need_fields != 'n':
        print('Response must be a \'y\' or \'n\'!')
        need_fields = input('Are there fields required for calling the API? (\'y\'/\'n\') ')

    if need_fields == "y":
        stop = True
    else:
        stop = False

    while stop:
        field_name = input('Input API field name: ')
        if is_int(field_name):
            field_name = int(field_name)

        field = input('Input API field: ')
        if is_int(field):
            field = int(field)

        yml_dict['url_params'][field_name] = field

        cont_api = input('Continue inputting API fields? (\'y\'/\'n\') ')
        while cont_api != 'y' and cont_api != 'n':
            print('Response must be a \'y\' or \'n\'!')
            cont_api = input('Continue inputting API fields? (\'y\'/\'n\') ')

        if cont_api == 'n':
            stop = False
        elif cont_api == 'y':
            stop = True

    keep_all = input('Do you want to keep all data pulled from the API? (\'y\'/\'n\') ')
    while keep_all != 'y' and keep_all != 'n':
        print('Response must be a \'y\' or \'n\'!')
        keep_all = input('Do you want to keep all data pulled from the API? (\'y\'/\'n\') ')

    if keep_all != 'y':
        l = create_dict()
        yml_dict['fields_to_save'] = l

    yml_dict['time_interval'] = int(input("Input time interval between API calls in hours: "))

    yml_dict['max_requests'] = int(input("Input number of desired API requests: "))

    return yml_dict


def update_containers():
    with open(run_dict_path, 'w+b') as run_dict_file:
        pickle.dump(containers, run_dict_file)


if __name__ == "__main__":
    # Tests for development
    fromyml("../examples/weather.yml")
    start("weather")
