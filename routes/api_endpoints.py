from datetime import datetime, timedelta
import hashlib
from flask import Flask, Blueprint,redirect,url_for,render_template,request, jsonify
from dotenv import load_dotenv
import os
from os.path import join, dirname
from pymongo import MongoClient
import jwt


api_bp = Blueprint('api', __name__)

dotenv = join(dirname(__file__), '.env')
load_dotenv(dotenv)

SECRET_KEY = os.environ.get('SECRET_KEY')
MONGO_URL = os.environ.get('MONGO_URL')
DB_NAME = os.environ.get('DB_NAME')

client = MongoClient(MONGO_URL)
db = client[DB_NAME]


UPLOAD_FOLDER = 'static/assets/img/profiles'


@api_bp.route('/api/v1/admin_login', methods=['POST'])
def admin_login():
  """endpoint untuk handle login
  """
  data = request.get_json()
  role = data.get('role')
  if role == 'admin':
    username = data.get('username')
    print(username)
    password = data.get('password')
    print(password)
    hashed_pw = hashlib.sha256(password.encode('utf-8')).hexdigest()

    isUser = db.users.find_one({
      'fullName': username,
      'password': hashed_pw,
      'role': role
    })
    # print(isUser)
    if isUser:
      payload = {
        'id': username,
        'exp': datetime.now() + timedelta(seconds=60 * 60 * 24)
      }
      token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
      return jsonify({
        'code': 200,
        'result': 'success',
        'token': token,
        'role': 'admin'
      })
    else:
      return jsonify({
        'code': 401,
        'result': 'failed',
        'msg': "Username/password-nya salah, aa.."
      })
  elif role == 'super_admin':
    username = data.get('username')
    password = data.get('password')
    hashed_pw = hashlib.sha256(password.encode('utf-8')).hexdigest()

    isUser = db.users.find_one({
      'fullName': username,
      'password': hashed_pw,
      'role': role
    })
    print(isUser)
    if isUser:
      payload = {
        'id': username,
        'exp': datetime.now() + timedelta(seconds=60 * 60 * 24)
      }
      token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
      return jsonify({
        'code': 200,
        'result': 'success',
        'token': token,
        'role': 'super_admin'
      })
    else:
      return jsonify({
        'code': 401,
        'result': 'failed',
        'msg': "Username/password-nya salah, aa.."
      })


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

@api_bp.route('/api/v1/add_user', methods=['GET', 'POST'])
def add_user():
    """endpoint untuk menambahkan user (admin) baru
    """
    
    if request.method == 'POST':
      
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
    return render_template('newUser.html')

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

@api_bp.route('/api/v1/get_services')
def get_services():
  data = [
    {
    'service_id': 'S001',
    'service_name': 'Down Perm',
    'price': '100K',
    'desc': 'Treatment melemahkan volumen rambut yang terlalu kaku'
    },
    {
    'service_id': 'S002',
    'service_name': 'Basic Color',
    'price': '75K',
    'desc': 'Coloring warna basic (hitam, biru, dark brown)'
    },
    {
    'service_id': 'S003',
    'service_name': 'Hair Perm',
    'price': '300K',
    'desc': 'Mengeritingkan rambut'
    },
    {
    'service_id': 'S004',
    'service_name': 'Fashion Color (Highlight)',
    'price': '350K',
    'desc': 'Abu-abu, silver, dan lain-lain'
    },
    {
    'service_id': 'S005',
    'service_name': 'Creambath',
    'price': '75K',
    'desc': 'Perawatan rambut'
    },
    {
    'service_id': 'S006',
    'service_name': 'Fashion Color Full',
    'price': '400K',
    'desc': 'Warna-warna terang (abu-abu, merah, putih, dll)'
    },
    {
    'service_id': 'S007',
    'service_name': 'Hair Cut',
    'price': 'start from 55K',
    'desc': 'Cukur + keramas + handuk panas + tonic + pomade'
    },
    {
    'service_id': 'S008',
    'service_name': 'Full Service',
    'price': 'start from 125K',
    'desc': 'Hair cut + creambath + blackmask + handuk panas + pijit kepala'
    },
    
  ]
  return jsonify({
      'code': 200,
      'result': 'success',
      'services': data
    })

