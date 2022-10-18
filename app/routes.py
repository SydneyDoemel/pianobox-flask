from flask_login import current_user
from app import app
from flask import request
from app.apiauthhelper import token_required
from flask_cors import CORS, cross_origin
from werkzeug.security import check_password_hash
import json
from app.models import Folder, User


from app.models import db
from .models import User

import requests


@app.route('/api/folder', methods=["POST"])
@cross_origin()
@token_required
def apiFolder(user):
    data = request.json
    filename = data['filename']
    foldername = data['foldername']
    url = data['url']
    folder = Folder(user.id, filename, foldername, url)
    db.session.add(folder)
    db.session.commit()
    return {
        'status': 'ok',
        'message': f"Successfully added file: {filename} to folder: {foldername}"
    }

@app.route('/api/myfolders/<string:user>')
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
    print(new_dict)
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

@app.route('/api/myfolder/<string:user>/<string:folder>')
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
@app.route('/api/remove', methods=["POST"])
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
