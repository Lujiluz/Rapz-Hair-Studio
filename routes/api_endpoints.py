from datetime import datetime
import hashlib
from flask import Flask, Blueprint,redirect,url_for,render_template,request, jsonify
from dotenv import load_dotenv
import os
from os.path import join, dirname
from pymongo import MongoClient

api_bp = Blueprint('api', __name__)

dotenv = join(dirname(__file__), '.env')
load_dotenv(dotenv)

SECRET_KEY = os.environ.get('SECRET_KEY')
MONGO_URL = os.environ.get('MONGO_URL')
DB_NAME = os.environ.get('DB_NAME')

client = MongoClient(MONGO_URL)
db = client[DB_NAME]


UPLOAD_FOLDER = 'static/assets/img/profiles'


@api_bp.route('/api/v1/get_user')
def get_user():
  """endpoint untuk mendapatkan data seluruh user
  menerima argument role: /api/v1/get_user?role=<role>
  
  returns:
  (tanpa argument)
    object: result dan data seluruh users
  (dengan argument)
    object: result message dan data users berdasarkan role
  """
  
  role = request.args.get('role')

  if role:
    data = list(db.users.find({'role': role}, {"_id": False}))
    return jsonify({'result': 'success', 'users': data})
  
  data = list(db.users.find({}, {'_id': False}))
  return jsonify({'result': 'success', 'users': data})

@api_bp.route('/api/v1/add_user', methods=['POST'])
def add_user():
    """endpoint untuk menambahkan user (admin) baru
    """
    
    fullName = request.form['fullName']
    email = request.form['email']
    password = request.form['password']
    hashed_pw = hashlib.sha256(password.encode('utf-8')).hexdigest()
    waNum = request.form['waNum']
    role = request.form['role']
    pricePerService = request.form['pricePerService']
    profile_img = request.files['profile_img']
    curr_date = datetime.now().strftime('%d%m%Y-%H%M%S')
    
    if profile_img:
        img_name = profile_img.filename
        img_path = os.path.join(UPLOAD_FOLDER, f'{curr_date}_{img_name}')
        profile_img.save(img_path)
    else:
        img_name = None
    data = {
            'fullName': fullName,
            'email': email,
            'profile_img': img_path,
            'password': hashed_pw,
            'wa_num': waNum,
            'price_per_service': pricePerService,
            'role': role,
            'is_cuti': False,
        }
    
    db.users.insert_one(data)
    return jsonify({
        'result': 'success'
        })

@api_bp.route('/api/v1/get_testimoni', methods=['GET'])
def get_testimoni():
  """endpoint untuk mendapatkan data testimoni
  """
  
  data = list(db.testimoni.find({}, {'_id': False}))
  
  return jsonify({
    'result': 'success',
    'testimoni': data
  })

@api_bp.route('/api/v1/add_testimoni', methods=['POST'])
def add_testimoni():
  """endpoint untuk menambahkan data testimoni
  """
  
  name = request.form['name']
  rating = request.form['rating']
  review = request.form['review']
  
  data = {
    'name': name,
    'rating': rating,
    'review': review
  }
  
  db.testimoni.insert_one(data)
  
  return jsonify({'result': 'success'})


