import os
from flask import Flask
from flask import jsonify
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate

BASEDIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"+\
    os.path.join(BASEDIR, "app.db")
db = SQLAlchemy(app)
migrate =  Migrate(app,db)

db.init_app(app)
CORS(app)


class User(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text,nullable=False, unique=True)
    email = db.Column(db.Text, nullable = False, unique= True)
    prueba = db.Column(db.Text)
    posts = db.relationship('Post', backref='post', lazy = True)

    def __repr__(self) -> str:
        return "<User %r>" % self.username

    def serialize(self):
        return{
            "id":self.id,
            "username":self.username,
            "email":self.email,
            "followers":self.followers
        }

class Post(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable= False, unique= True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= False)

    def __repr__(self) -> str:
        return "<Post %r>"
    
    def serialize(self):
        return{
            "id":self.id,
            "message":self.message,
            "user_id":self.user_id
        }

followers= db.Table('followers',db.Model.metadata,
    db.Column('user_id',db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('follower_id',db.Integer, db.ForeignKey('user.id'), primary_key=True),
)

@app.route('/createUser',methods=['POST'])
def instert_user():
    try:
        user= User()
        user.id=request.json.get("id")
        user.username= request.json.get("name")
        user.email=request.json.get("email")
        db.session.add(user)
        db.session.commit()
        return jsonify({"msg":"ok"})
    except Exception:
        return jsonify({"msg":"no ok"})

if __name__=="__main__":
    app.run(debug=True)
