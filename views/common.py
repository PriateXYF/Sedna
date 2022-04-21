# coding: utf-8

from leancloud import Object
from leancloud import Query
from leancloud import LeanCloudError
from flask import Blueprint
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template
import pytz

class Common(Object):
    pass

common_view = Blueprint('common', __name__)

@common_view.route('')
def show():
    res = []
    try:
        commons = Query(Common).descending('createdAt').limit(50).find()
        for common in commons:
            res.append({
                'date' : common.get('date').astimezone(pytz.timezone('Asia/Shanghai')).strftime('%m-%d %H:%M'),
                'content' : common.get('content')
            })
    except LeanCloudError as e:
        if e.code == 101:  # Class does not exist on the cloud. 
            res = []
        else:
            raise e
    return render_template('common.html', commons=res)