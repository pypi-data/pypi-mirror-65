# this is the python script that runs inside docker container

# import dependencies
import yaml
import requests, json
import time


def load_specs(filename="proc.yml"):
    """
    Load specs from yaml file

    :param filename: spec_file
    :return: dictionary
    """
    with open("proc.yml", "r+") as f:
        specs = yaml.safe_load(f)
    return specs


def get_data(url):
    """
    Returns JSON data from url or {} if 404 error

    :param url: string that has JSON data
    :return: dictionary
    """
    response = requests.get(url)
    x = response.json()
    if x["cod"] != 404:
        return x
    else:
        print("404 Error: url not found.")
        return {}


def filter_data(data, fields):
    """
    Removes keys in data that are not part of fields

    :param data: dict of data
    :param fields: graph representing the keys/indexes to be saved
    """

    # TODO: Implement function, see examples/weather.yml for fields example
    to_filter = []
    while len(to_filter) > 0:
        next = to_filter.pop()

        if isinstance(next, dict):
            return


def main():
    # Load specs from file
    specs = load_specs()
    print(f"Specs loaded from proc.yml: {specs}")

    # Convert time interval in hours to milliseconds
    h_interval = specs["time_interval"]
    s_interval = h_interval * 60 * 60
    print(f"Time interval in seconds computed to be {s_interval}")

    # Get url
    complete_url = specs["base_url"].format(**specs["url_params"])
    print(f"Complete url for requests: {complete_url}")

    # Main loop
    for i in range(specs["max_requests"]):
        # Get new data
        new_data = get_data(complete_url)

        # Save data to file
        with open(f"/saved_data/{time.time()}-data.yml", "w+") as f:
            f.write(yaml.dump(new_data))

        # Wait for next time interval
        time.sleep(s_interval)


if __name__ == "__main__":
    main()
