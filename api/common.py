import requests,json,os
import leancloud
import time
from datetime import datetime
import pytz as pytz
import re


def get_config(id):
    Config = leancloud.Object.extend('Config')
    query = Config.query
    config = query.get(id)
    return config

# 普遍适用的签到
def common_checkin(id):
    now = datetime.fromtimestamp(int(time.time()), pytz.timezone('Asia/Shanghai'))
    C = get_config(id)
    if not C.get('config'):
        return {
            "name" : "Error",
            "msg" : "Config ID 404!",
            'date': str(now),
            'status' : "error"
        }
    config = C.get('config')
    status = response = None
    
    if 'proxies' in config.keys():
        proxies = config['proxies']
    else:
        proxies = {}
    if config['method'] == 'GET':
        response = requests.get(config['url'], headers=config['headers'], params=config['bodies'], proxies=proxies, verify=False)
    elif config['method'] == 'POST':
        response = requests.post(config['url'], headers=config['headers'], data=config['bodies'], proxies=proxies, verify=False)
    content = response.text
    for result in config['result']:
        if re.findall(config['result'][result], response.text) != []:
            status = result
            break
    if not status:
        status = "error"
    Log = leancloud.Object.extend('Log')
    log = Log()
    log.set('name', config['name'])
    log.set('content', content)
    log.set('date', now)
    log.set('status', status)
    log.set('url', config['url'])
    log.set('config', C)
    log.set('host', C.get('host'))
    log.save()
    return {
        "name" : config['name'],
        "msg" : content,
        'date': str(now),
        'status' : status
    }

if __name__ == '__main__':
    pass
    # APP_ID = os.environ['LEANCLOUD_APP_ID']
    # APP_KEY = os.environ['LEANCLOUD_APP_KEY']
    # MASTER_KEY = os.environ['LEANCLOUD_APP_MASTER_KEY']
    # leancloud.init(APP_ID, app_key=APP_KEY, master_key=MASTER_KEY)
    # leancloud.use_master_key(False)
    # common_checkin("626065c88c99e04b3adfd0bd")