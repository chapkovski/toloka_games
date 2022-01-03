"""
This module reads a csv file with assignments (usually obtained from oTree),
gets a user id from the assignment id, and using this user id, obtains the full information available in this user
Toloka profile.

"""
import logging
import glob
from pprint import pprint
from datetime import datetime
from dotenv import load_dotenv
from csv import DictWriter
import os
import requests
import pandas as pd
import sys
import json
"""
To get basic info about user <ID>:
We need to send a GET request of the following format
https://toloka.yandex.com/api/new/requester/workers/<ID>/
And we will get a response in a form of: 

{
    "workerId": "<ID>",
    "gender": "FEMALE",
    "age": 22,
    "education": "BASIC",
    "languages": [
        "EN",
        "RU",
        "UK"
    ],
    "country": "UA",
    "cityId": 10343,
    "citizenship": "UA"
}
"""

"""
Calculable attributes  can be obtained similarly with a GET request to:

https://toloka.yandex.com/api/new/requester/workers/<ID>>/attributes
with the typical response:

[
    {
        "key": "user_agent_version_major",
        "value": 21
    },
    {
        "key": "user_agent_version_minor",
        "value": 11
    },
    {
        "key": "user_agent_version",
        "value": 21.11
    },
    {
        "key": "device_category",
        "value": "PERSONAL_COMPUTER"
    },
    {
        "key": "client_type",
        "value": "BROWSER"
    },
    {
        "key": "user_agent_type",
        "value": "BROWSER"
    },
    {
        "key": "user_agent_version_bugfix",
        "value": 3
    },
    {
        "key": "user_agent_family",
        "value": "YANDEX_BROWSER"
    },
    {
        "key": "os_family",
        "value": "WINDOWS"
    },
    {
        "key": "region_by_ip",
        "value": [
            10000,
            10001,
            225,
            17,
            10842,
            121016,
            20117
        ]
    },
    {
        "key": "os_version_minor",
        "value": 0
    },
    {
        "key": "os_version",
        "value": 10.0
    },
    {
        "key": "os_version_bugfix",
        "value": 0
    },
    {
        "key": "os_version_major",
        "value": 10
    },
    {
        "key": "minimal_wage",
        "value": 1.81
    },
    {
        "key": "region_by_phone",
        "value": [
            10000,
            10001,
            225
        ]
    },
    {
        "key": "rating",
        "value": 313.8538301
    }
]
"""

BASE_PATH = os.path.abspath(__file__)
error_log_file = f"{os.path.join(BASE_PATH, 'logs')}/error.log"
logging.basicConfig(format='Date-Time : %(asctime)s : Line No. : %(lineno)d - %(message)s',
                    level=logging.ERROR,
                    # filename=error_log_file
                    )

load_dotenv()  # take environment variables from .env.

TOLOKA_API_KEY = os.getenv('TOLOKA_API')
headers = {
    'Authorization': f'OAuth {TOLOKA_API_KEY}',
    'Content-Type': 'application/json'
}


def write_data(fname, value):
    log_columns = ['time', 'timestamp', 'fname', 'value']
    cleaned_fname = fname.split('.')[0]

    path_to_log = f'./data/toloka_rt_data.csv'
    full_path_to_log = os.path.join(BASE_PATH, path_to_log)
    # open(full_path_to_log, 'a').close()
    with open(path_to_log, 'a') as f_object:
        writer = DictWriter(f_object, fieldnames=log_columns)
        now = datetime.utcnow()
        what_to_write = dict(time=now,
                             timestamp=now.timestamp(),
                             fname=cleaned_fname,
                             value=value)
        writer.writerow(what_to_write)


def user_from_assignment(assignment_id):
    url = f'https://toloka.yandex.com/api/v1/assignments/{assignment_id}'
    response = requests.request("GET", url, headers=headers)
    return (response.json().get('user_id'))


def get_attributes(user_id):
    url = f"https://toloka.yandex.com/api/new/requester/workers/{user_id}/attributes"
    response = requests.request("GET", url, headers=headers)
    return response.json()


def get_profile(user_id):
    url = f"https://toloka.yandex.com/api/new/requester/workers/{user_id}"
    response = requests.request("GET", url, headers=headers)
    return response.json()


def item_retrieval(l, k):
    try:
        v = next(item for item in l if item["key"] == k).get('value')
    except StopIteration:
        v = None
    return {k: v}

def wrapper(assignment_id):
    res = dict(assignment_id=assignment_id)
    user_id = user_from_assignment(assignment_id)
    res.update(get_profile(user_id))
    attributes = get_attributes(user_id)
    attrs_to_get = ['rating', 'device_category', 'os_family','region_by_ip','user_agent_type','user_agent_family']
    for a in attrs_to_get:
        res.update(item_retrieval(attributes, a))
    return res


if __name__ == '__main__':

    columns = ['assignment_id', 'workerId', 'gender', 'age', 'education', 'languages', 'country', 'cityId',
               'citizenship', 'rating', 'device_category', 'os_family','region_by_ip','user_agent_type','user_agent_family']

    assignments = pd.read_csv(f'assignments.csv')
    with open('user_data.csv', 'a') as f_object:
        writer = DictWriter(f_object, fieldnames=columns)
        for index, row in assignments.iterrows():
            print(index, row.assignment_id)
            writer.writerow(wrapper(row.assignment_id))

    f_object.close()
