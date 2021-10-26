import requests
import json


if __name__ == "__main__":
    with open('darknet_scripts.json') as json_file:
        config = json.load(json_file)
    response = requests.post(config['request_server'], data='Object detected!')
