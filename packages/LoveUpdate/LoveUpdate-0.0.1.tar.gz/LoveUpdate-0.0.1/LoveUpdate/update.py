import os
import sys
import subprocess
from datetime import date
import pickle
import requests

def checkaccess(pack):
    url='https://fast.com/pt/'
    timeout=1
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        print("Connection error - moving on")
    return False

def uppack(pack):
    print('Updating '+pack+':')
    return subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', pack])

def getdate():
    today=date.today()
    return today.strftime('%m/%d/%Y')

def update(pack, lastupdate):
    tdy=getdate()
    if lastupdate!=tdy:
        code=checkaccess(pack)
        if not code:
            print('Error fetching internet connection for autoupdate. Moving on')
            return True
        code=uppack(pack)
        if code:
            print('Error autoupdating package from pip. Moving on')
            return True
        return False, tdy