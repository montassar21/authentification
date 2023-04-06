from flask import Flask,redirect,url_for,request,flash,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api,Resource,reqparse
from models import UserModel,db
from sqlalchemy import select
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import jwt
import datetime

app=Flask(__name__)
CORS(app)
app.secret_key = 'Helloworld'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

api=Api(app)
db.init_app(app)


@app.before_first_request
def create_table():
    db.create_all()

class UserAdd(Resource):
  def get(self):
    users=UserModel.query.all()
    return {'Users':list(x.json() for x in users)}
  def post(self):
        data=request.get_json()
        email = data["email"]
        username = data["name"]
        phone=data["phone"]
        password1 = data["password1"]
        password2 = data["password2"]

        email_exists = UserModel.query.filter_by(email=email).first()
        username_exists = UserModel.query.filter_by(name=username).first()

        if email_exists:
              response_data = {
               'Message': 'This mail exist!'
                }
              return jsonify(response_data)
        elif password1 != password2:
             response_data={'Message':'Password don\'t match!'}
             return jsonify(response_data)
        elif len(username) < 2:
            response_data={'Message':'Username is too short.'}
            return jsonify(response_data)
        elif len(password1) < 8:
            response_data={'Message':'Password is too short.'}
            return jsonify(response_data)
        elif len(email) < 4:
            response_data={'Message':'Email is invalid.'}
            return jsonify(response_data)

        else:
            new_user = UserModel(name=username,email=email, password=generate_password_hash(
                password1, method='sha256'),phone=phone)
            db.session.add(new_user)
            db.session.commit()
            db.session.flush()
            response={'Message':"Register success !"}
            return jsonify(response)
       

    
class UserLogin(Resource):
  def get(self):
    users=UserModel.query.all()
    return {'Users':list(x.json() for x in users)}
  def post(self):
      data=request.get_json()
      email = data["email"]
      password = data["password"]
      user = UserModel.query.filter_by(email=email).first()
      if user:
         if check_password_hash(user.password, password):
                token=jwt.encode({'user':user.name,'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=30)},app.secret_key)
                response={'Message':"Login success !",'token':token} 
                return  jsonify(response)
         else:
                response={'Message':"Password is incorrect.!"} 
                return  jsonify(response)
      else:
                response={'Message':"Email does not exist.!"} 
                return  jsonify(response)


api.add_resource(UserAdd,'/Users')   
api.add_resource(UserLogin,'/UsersLogin')   

app.debug=True
if __name__=='__main__':
    app.run(host='localhost',port=5000)


















