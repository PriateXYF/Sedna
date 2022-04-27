import requests
import os
from urllib.parse import urlencode
def bark(title, content):
    barkURL = None
    if 'BARK_URL' not in os.environ:
        return False
    barkURL = os.environ['BARK_URL']
    params = {
        "title" : title,
        "body" : content[:200],
        'group' : 'Sedna'
    }
    res = requests.post(barkURL, params)
    return True