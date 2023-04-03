from flask import Blueprint, render_template, request, jsonify

from app.util.crypto_ECB import AEScoder
from app.view import viewutil

web = Blueprint("othertools", __name__)

@web.route('/encrypt',methods=['GET'])
def encrypt_page():
        return render_template('encrypt.html')


@web.route('/encrypt.json',methods=['POST'])
def encrypt():
    info = request.values
    name = viewutil.getInfoAttribute(info, 'name')
    encr_name = AEScoder().encrypt(name)
    result = jsonify({'code': 200, 'name': name, 'encr_name': encr_name})
    # print(result)
    return result, {'Content-Type': 'application/json'}


