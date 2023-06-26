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

web = Blueprint('docs', __name__, template_folder='templates/docs')

@web.route('/docs/intro', methods=['GET', 'POST'])
@user.login_required
# @permission_required(session.get('groupname'))
def intro():
    return render_template('docs/introduction.html',)