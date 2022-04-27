# coding: utf-8
import sys
import os
import datetime

import leancloud
from flask import Flask, jsonify, request, session, redirect
from flask import render_template
from flask_sockets import Sockets
from leancloud import LeanCloudError
from api.query import query
from api.common import common_checkin
from api.common import get_config
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=20)

sockets = Sockets(app)

# routing
# app.register_blueprint(glados_view, url_prefix='/glados')
# app.register_blueprint(xiuno_view, url_prefix='/xiuno')
# app.register_blueprint(discuz_view, url_prefix='/discuz')
# app.register_blueprint(common_view, url_prefix='/common')
	

@app.route('/', methods=['GET'])
def index():
	data = query()
	return render_template('index.html', data=data)

@app.route('/query', methods=['POST'])
def search():
	keyword = request.form['keyword']
	limit = int(request.form['limit'])
	res = query(keyword, limit)
	return jsonify(res)

@app.route('/config', methods=['POST'])
def getConfig():
	cid = request.form['id']
	try:
		C = get_config(cid)
		res = {
			'success' : True,
			"id" : C.id,
			'config': C.get('config'),
			'host' : C.get('host'),
			'message' : '获取配置成功!'
		}
	except Exception as e:
		res = {
			"success" : False,
			"message" : "获取配置失败，请传入正确的ID!",
		}
	return jsonify(res)

# 模板
@app.route('/config', methods=['GET'])
def config():
	cid = request.args.get("id")
	return render_template('config.html', id=cid)

@app.route('/checkin', methods=['POST'])
def doCheckin():
	_id = request.form['id']
	try:
		res = common_checkin(_id)
	except Exception as e:
		res = {
			"name" : "Failure",
			"msg" : "签到失败，请传入正确的ID!",
			'date': "",
			'status' : "失败"
		}
	return jsonify(res)

@app.route('/login', methods=['GET'])
def error():
	return render_template('error.html')

@app.route('/login', methods=['POST'])
def login():
	password = request.form['password']
	key = '123456'
	if 'WEB_PASSWORD' in os.environ:
		key = os.environ['WEB_PASSWORD']
	if password == key:
		session['is_login'] = 'true'
		return redirect('/')
	else:
		return render_template('error.html')

@app.before_request
def before():
	url = request.path
	pass_list = ['/login']
	suffix = url.endswith('.png') or url.endswith('.jpg') or url.endswith('.css') or url.endswith('.js')
	if url in pass_list or suffix:
		pass
	# elif session.get('is_login', '') != 'true':
	# 	return redirect('/login')
	# else:
	# 	pass