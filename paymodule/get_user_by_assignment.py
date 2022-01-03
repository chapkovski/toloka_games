import pandas as pd
from dotenv import load_dotenv
from csv import DictWriter

load_dotenv()  # take environment variables from .env.
"""
What do we do here:
1. Read csv with the follwoing columns: assignment id, payoff, message
1.2. Read log
2. loop through and pay bonuses for each user in assigment id. Prior: check if assignment is not in log
3. log them into a log
"""
from toloka import TolokaClient
from pprint import pprint

client = TolokaClient(sandbox=False)


def accept_assignment(assignment_id):
    resp = client.accept_assignment(assignment_id)
    return resp


log_columns = [ 'assignment_id','worker_id']

file_name = 'old_assignments.csv'
log_name = f'logs_user_ids_{file_name}'
open(f'logs/{log_name}', 'a').close()


def get_assignment_info(assignment_id):
    resp = client.get_assignment_info(assignment_id)
    return resp

def get_users_from_file():
    raw = pd.read_csv(f'data/{file_name}', sep='|')
    raw.rename(columns={'participant_label':'assignment_id'}, inplace=True)
    print(raw.columns)
    # return

    logs = pd.read_csv(f'logs/{log_name}', header=None, names=log_columns)
    df = pd.concat([raw, logs]).drop_duplicates(keep=False, subset=['assignment_id'])
    print(df.shape, '''------''')

    # return
    with open(f'logs/{log_name}', 'a') as f_object:
        writer = DictWriter(f_object, fieldnames=log_columns)
        counter = 0
        for index, row in df.iterrows():
            worker_id = get_assignment_info(row.assignment_id).get('user_id')
            print(f'{counter}: Worker  {worker_id} ;; assignment {row. assignment_id}')
            writer.writerow(dict(worker_id=worker_id, assignment_id=row.assignment_id))
            counter += 1
            # if counter > 10:
            #     return

if __name__ == '__main__':
    get_users_from_file()
