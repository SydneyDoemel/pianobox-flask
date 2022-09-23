from fileinput import filename
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_cors import CORS, cross_origin
# from .forms import LoginForm, UserCreationForm
from app.apiauthhelper import basic_auth, token_auth, token_required
#import login funcitonality
# from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
import json

# import models
from app.models import Folder, User

auth = Blueprint('auth', __name__, template_folder='authtemplates')

from app.models import db




##### API ROUTES #########

@auth.route('/api/signup', methods=["POST"])
@cross_origin()
def apiSignMeUp():
    data = request.json   
    username = data['username']
    email = data['email']
    password = data['password']
    user = User(username, email, password)
    # add instance to our db
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
        # check password
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


@auth.route('/api/folder', methods=["POST"])
@cross_origin()
@token_required
def apiFolder(user):
    data = request.json
    filename = data['filename']
    foldername = data['foldername']
    url = data['url']
    # add user to database
    folder = Folder(user.id, filename, foldername, url)

    # add instance to our db
    db.session.add(folder)
    db.session.commit()
    return {
        'status': 'ok',
        'message': f"Successfully added file: {filename} to folder: {foldername}"
    }

@auth.route('/api/myfolders/<string:user>')
def apigetFolder(user):
    thisuser = User.query.filter_by(username=user).first()
    myfolders = Folder.query.filter_by(user_id=thisuser.id)
    folders = [s.to_dict() for s in myfolders]
    print(f"length: {len(folders)}")
    folder_name=[]
    file_name=[]
    new_dict={}
    url_name=[]
    for item in folders:
        folder_name.append(item['foldername'])
        file_name.append(item['filename'])
        url_name.append(item['url'])
    for each in folders:
        folder=each['foldername']
        file=[each['filename']]
        url=[each['url']]
        if folder not in new_dict:
            new_dict['folder']=folder
            new_dict['file']=[{'filename':file, 'url':url}]
            print('hi')
        else:
            new_dict['file'].append({'filename':file, 'url':url})
            print('no')
    print(new_dict,"!!!!!!!!!!!!!")
    print(folders)
    folder_name=set(folder_name)
    folder_name=list(folder_name)
    if folders:
        return {
            'status': 'ok',
            'total_results': len(folders),
            "folder_info": folders,
            "folders":folder_name,
            "files":file_name
            }
    else:
        return {
            'status': 'not ok',
            'message': "No folders found"
        }

@auth.route('/api/myfolder/<string:user>/<string:folder>')
def apigetFolderInfo(user, folder):
    thisuser = User.query.filter_by(username=user).first()
    myfolders = Folder.query.filter_by(user_id=thisuser.id, foldername=folder)
    folders = [s.to_dict() for s in myfolders]
    print(f"length: {len(folders)}")
    folder_name=[]
    file_name=[]
    new_dict={}
    url_name=[]
    for item in folders:
        folder_name.append(item['foldername'])
        file_name.append(item['filename'])
        url_name.append(item['url'])
    print(folders)
    if folders:
        return {
            'status': 'ok',
            'total_results': len(folders),
            "folder_info": folders,
            "folder_name": folder_name
            }
    else:
        return {
            'status': 'not ok',
            'message': "No folders found"
        }
@auth.route('/api/remove', methods=["POST"])
@cross_origin()
@token_required
def apiRemove(user):
    thisuser = User.query.filter_by(username=user.username).first()
    data = request.json
    filename = data['filename']
    foldername= data['foldername']
    myfile = Folder.query.filter_by(user_id=thisuser.id, filename=filename, foldername = foldername).first()
    # add instance to our db
    db.session.delete(myfile)
    db.session.commit()
    return {
        'status': 'ok',
        'message': f"Successfully removed {filename} from folder {foldername}"
    }
