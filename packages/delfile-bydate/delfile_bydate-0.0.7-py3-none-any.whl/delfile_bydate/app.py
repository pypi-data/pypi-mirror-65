import os
from datetime import datetime


def delete(part, date):
    token_date = date.split('/')
    text = 'cannot find path'
    if bool(part):
        text = 'Empty file for delete'
        entries = os.listdir(part)
        for entry in entries:
            created = os.stat(f'{part}/{entry}').st_ctime
            date = str(datetime.fromtimestamp(created)).split(' ')
            item = date[0].split('-')
            if len(token_date) == 1 and token_date[0] == item[0]:
                os.remove(f'{part}/{entry}')
                text = 'success'
            elif len(token_date) == 2 and token_date[0] == item[0] and token_date[1] == item[1]:
                os.remove(f'{part}/{entry}')
                text = 'success'
            elif len(token_date) == 3 and token_date[0] == item[0] and token_date[1] == item[1] and token_date[2] == item[2]:
                os.remove(f'{part}/{entry}')
                text = 'success'
    return text
