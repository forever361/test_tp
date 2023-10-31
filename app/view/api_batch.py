import json

import requests
from flask import Blueprint, render_template, request, jsonify, session

import os
import sys

from app.util.permissions import permission_required
from app.view import user

basePath = os.path.join(os.path.join(os.path.dirname(__file__)))
configPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(configPath)

web = Blueprint('api_batch', __name__, template_folder='templates/api')

@web.route('/api_batch', methods=['GET', 'POST'])
@user.login_required
# @permission_required(session.get('groupname'))
def api_batch():
    return render_template('api/api_batch.html',)

@web.route('/api_batch_suite', methods=['GET', 'POST'])
@user.login_required
# @permission_required(session.get('groupname'))
def api_batch_suite():
    return render_template('api/api_batch_suite.html',)


@web.route('/api_batch_case', methods=['GET', 'POST'])
@user.login_required
# @permission_required(session.get('groupname'))
def api_batch_case():
    return render_template('api/api_batch_case.html',)


@web.route('/api_batch_job', methods=['GET', 'POST'])
@user.login_required
# @permission_required(session.get('groupname'))
def api_batch_job():
    return render_template('api/api_batch_job.html',)