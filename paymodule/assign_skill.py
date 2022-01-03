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


log_columns = [ 'worker_id']

file_name = 'to_pay.csv'
log_name = f'logs_skills_assigned_{file_name}'
open(f'logs/{log_name}', 'a').close()
skill_id_to_assign = '33839'


def assign_skill(worker_id, skill_id):
    pass
    reason = 'Assigned for those who participated in first IRT wave'
    resp = client.assign_skill(worker_id=worker_id, skill_id=skill_id, value=100, reason=reason)
    return resp


def assign_skills_from_file():
    raw = pd.read_csv(f'data/{file_name}', sep='|')
    print(raw.columns)
    return

    logs = pd.read_csv(f'logs/{log_name}', header=None, names=log_columns)
    df = pd.concat([raw, logs]).drop_duplicates(keep=False, subset=['worker_id'])
    print(df.shape, '''------''')

    # return
    with open(f'logs/{log_name}', 'a') as f_object:
        writer = DictWriter(f_object, fieldnames=log_columns)
        counter = 0
        for index, row in df.iterrows():
            print(assign_skill(worker_id=row.worker_id, skill_id=skill_id_to_assign))
            print(f'{counter}: Worker  {row.worker_id} get skill {skill_id_to_assign} assigned')
            writer.writerow(dict(worker_id=row.worker_id))
            counter += 1



if __name__ == '__main__':
    assign_skills_from_file()
