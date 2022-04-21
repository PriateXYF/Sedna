import leancloud
from leancloud import LeanCloudError
import pytz
from urllib.parse import urlparse

def query(keyword="", limit=30):
    res = []
    try:
        Log = leancloud.Object.extend('Log')
        logs = Log.query.matched('name', f'.*?{keyword}.*?', ignore_case=True).descending('createdAt').limit(limit).find()
        # print(commons)
        for log in logs:
            url = urlparse(log.get('url'))
            res.append({
                'id' : log.get('config').id,
                'name' : log.get('name'),
                'date' : log.get('date').astimezone(pytz.timezone('Asia/Shanghai')).strftime('%m月%d日%H:%M'),
                'content' : log.get('content'),
                'status' : log.get('status'),
                'url' : f"{url.scheme}://{url.netloc}"
            })
    except LeanCloudError as e:
        if e.code == 101:  # Class does not exist on the cloud. 
            res = []
        else:
            raise e
    return res