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
DEFAULT_TITLE = 'Спасибо за ваше участие!'


def get_assignment_info(assignment_id):
    resp = client.get_assignment_info(assignment_id)
    return resp


def pay_bonus(user_id, bonus, message, title=DEFAULT_TITLE):
    bonus = client.pay_bonus(user_id, bonus=bonus, message=message, title=title)
    return bonus


def accept_assignment(assignment_id):
    resp = client.accept_assignment(assignment_id)
    return resp


log_columns = ['assignment_id', 'user_id']

file_name = 'fullq_assignments.csv'
log_name = f'logs_paid_{file_name}'
open(f'logs/{log_name}', 'a').close()


def accept_and_pay():
    raw = pd.read_csv(f'data/{file_name}')
    raw = raw[["assignment_id"]]
    print(raw.columns)


    logs = pd.read_csv(f'logs/{log_name}', header=None, names=log_columns)
    df = pd.concat([raw, logs]).drop_duplicates(keep=False, subset=['assignment_id'])
    print(df.shape, '''------''')

    # return
    with open(f'logs/{log_name}', 'a') as f_object:
        writer = DictWriter(f_object, fieldnames=log_columns)
        counter = 0
        for index, row in df.iterrows():
            newrow = dict(row)
            user_id = get_assignment_info(row.assignment_id).get('user_id')
            newrow['user_id'] = user_id
            accept_assignment(row.assignment_id)
            # if row.bonus>10:
            #     print(row)
            #     raise Exception('too large bonus')
            # pay_bonus(user_id=user_id, bonus=row.bonus, title='Спасибо', message=row.msg)
            print(f'{counter}: Assignment {row.assignment_id} accepted, paid to user {user_id}')
            writer.writerow(newrow)
            counter += 1
            # if counter > 100:
            #     return


if __name__ == '__main__':
    accept_and_pay()
