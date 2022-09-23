from secrets import token_hex
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash

db = SQLAlchemy()



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    apitoken = db.Column(db.String, default=None, nullable=True)

    

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.apitoken = token_hex(16)

    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'token': self.apitoken
        }
    
    def saveToDB(self):
        db.session.commit()

  


class Songs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_url =db.Column(db.String(500))

    def __init__(self, song_url):
        self.song_url=song_url
        
    def save(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def to_dict(self):
            return {
                'song_url':self.song_url
                
            }


class Folder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename=db.Column(db.String(400), nullable=False)
    foldername= db.Column(db.String(100), nullable=False)
    url= db.Column(db.String(500), nullable=False)

    def __init__(self, user_id, filename, foldername, url):
        self.user_id = user_id
        self.filename = filename
        self.foldername = foldername
        self.url=url
    def save(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def to_dict(self):
            return {
                'user_id': self.user_id,
                'filename': self.filename,
                'foldername': self.foldername,
                'url':self.url
            }