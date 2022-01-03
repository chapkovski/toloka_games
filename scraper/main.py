"""
What do we do here:

"""
import logging
import glob
from pprint import pprint
from datetime import datetime
from dotenv import load_dotenv
from csv import DictWriter
import os
import requests
import json
import sys
from requests.exceptions import ConnectionError

BASE_PATH = os.path.abspath(__file__)
error_log_file = f"{os.path.join(BASE_PATH, 'logs')}/error.log"
logging.basicConfig(format='Date-Time : %(asctime)s : Line No. : %(lineno)d - %(message)s',
                    level=logging.ERROR,
                    # filename=error_log_file
                    )

load_dotenv()  # take environment variables from .env.

TOLOKA_API_KEY = os.getenv('TOLOKA_API')


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


def get_value(filename):
    url = "https://toloka.yandex.com/api/adjuster/adjustments/?mode=RELATIVE_TOP_N&ratio=1"
    just_fn = os.path.basename(filename)
    with open(f"{filename}", "r") as f:
        jsondata = json.load(f)

    payload = json.dumps(jsondata)
    headers = {
        'Authorization': f'OAuth {TOLOKA_API_KEY}',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
    except ConnectionError:
        logging.error(f'No connect for file {just_fn}')
        return
    try:
        value = response.json().get('parameters').get('value')
        write_data(just_fn, value)
    except AttributeError:
        logging.error(f'something wrong with the file {just_fn}')


if __name__ == '__main__':

    allpayloads = glob.glob('./payloads/*.json')
    for j, i in enumerate(allpayloads):
        print(f'{j} {i} out of {len(allpayloads)}::: ')
        get_value(i)
