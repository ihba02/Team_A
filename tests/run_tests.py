import requests
import threading
import time

def quick_check(base='http://127.0.0.1:5000'):
    try:
        r = requests.get(base + '/tables')
        print('/tables', r.status_code)
        print(r.json())
    except Exception as e:
        print('Error connecting to API:', e)

if __name__ == '__main__':
    print('Run the API first (python src/app.py), then run this script to do a quick smoke check.')
