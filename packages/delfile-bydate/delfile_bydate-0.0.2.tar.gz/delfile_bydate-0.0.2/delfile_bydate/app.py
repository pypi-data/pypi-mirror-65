import os
from datetime import datetime


def delete(part, years='*', months='*', days='*'):
    text = 'cannot find path'
    if bool(part):
        entries = os.listdir(part)
        for entry in entries:
            created = os.stat(f'{part}/{entry}').st_ctime
            date = str(datetime.fromtimestamp(created)).split(' ')
            item = date[0].split('-')
            if years == '*' and months == '*' and days == '*':
                os.remove(f'{part}/{entry}')
                text = 'success'
            elif years != '*' and months == '*' and days == '*':
                if item[0] == years:
                    os.remove(f'{part}/{entry}')
                    text = 'success'
            elif years != '*' and months != '*' and days == '*':
                if item[0] == years and item[1] == months:
                    os.remove(f'{part}/{entry}')
                    text = 'success'
            elif years != '*' and months != '*' and days != '*':
                if item[0] == years and item[1] == months and item[2] == days:
                    os.remove(f'{part}/{entry}')
                    text = 'success'
    return text
