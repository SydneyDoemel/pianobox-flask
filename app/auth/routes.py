from fileinput import filename
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_cors import CORS, cross_origin
from app.apiauthhelper import basic_auth, token_auth, token_required
from werkzeug.security import check_password_hash
import json
from app.models import Folder, User

auth = Blueprint('auth', __name__, template_folder='authtemplates')

from app.models import db





@auth.route('/api/signup', methods=["POST"])
@cross_origin()
def apiSignMeUp():
    data = request.json   
    username = data['username']
    email = data['email']
    password = data['password']
    user = User(username, email, password)
    db.session.add(user)
    db.session.commit()
    return {
        'status': 'ok',
        'message': f"Successfully created user {username}"
    }


@auth.route('/token', methods=['POST'])
@basic_auth.login_required
def getToken():
    user = basic_auth.current_user()
    return {
                'status': 'ok',
                'message': "You have successfully logged in",
                'data':  user.to_dict()
            }


@auth.route('/api/login', methods=["POST"])
@cross_origin()
def apiLogMeIn():
    data = request.json
    username = data['username']
    password = data['password']
    user = User.query.filter_by(username=username).first()
    if user:
        if check_password_hash(user.password, password):
            return {
                'status': 'ok',
                'message': "You have successfully logged in",
                'data':  user.to_dict()
            }
        return {
            'status': 'not ok',
            'message': "Incorrect password."
        }
    return {
        'status': 'not ok',
        'message': 'Invalid username.'
    }
@auth.route('/api/changepass', methods=["POST"])
@cross_origin()
@token_required
def apiChangePass(user):
    data = request.json   
    password = data['password']
    user = User.query.filter_by(id=user.id).first()
    user.password= password
    db.session.commit()
    return {
        'status': 'ok',
        'message': f"Successfully changed password"
    }

@auth.route('/api/changeusername', methods=["POST"])
@cross_origin()
@token_required
def apiChangeUsername(user):
    data = request.json   
    username = data['username']
    user = User.query.filter_by(id=user.id).first()
    user.username= username
    db.session.commit() 
    return {
        'status': 'ok',
        'message': f"Successfully created changed username"
    }
@auth.route('/api/changeemail', methods=["POST"])
@cross_origin()
@token_required
def apiChangeEmail(user):
    data = request.json   
    email = data['email']
    user = User.query.filter_by(id=user.id).first()
    user.email= email
    db.session.commit() 
    return {
        'status': 'ok',
        'message': f"Successfully created changed email"
    }
@auth.route('/api/deleteuser', methods=["POST"])
@cross_origin()
@token_required
def apiDeleteUser(user):
    data = request.json   
    myfolders = Folder.query.filter_by(user_id=user.id)
    for each in myfolders:
        db.session.delete(each)
        db.session.commit()
    user = User.query.filter_by(id=user.id).first()
    db.session.delete(user)
    db.session.commit() 
    return {
        'status': 'ok',
        'message': f"Successfully deleted"
    }

