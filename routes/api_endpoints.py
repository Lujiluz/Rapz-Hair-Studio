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
    'price': '55K',
    'desc': 'Cukur + keramas + handuk panas + tonic + pomade'
    },
    {
    'service_id': 'S008',
    'service_name': 'Full Service',
    'price': '125K',
    'desc': 'Hair cut + creambath + blackmask + handuk panas + pijit kepala'
    },
    
  ]
  return jsonify({
      'code': 200,
      'result': 'success',
      'services': data
    })
  
@api_bp.route('/api/v1/addOrder', methods=['POST'])
def add_order():
  """API endpoint untuk memasukkan data order ke database
  """
  booking_data = request.get_json()
  db.orders.insert_one(booking_data)
  return jsonify({'result': 'success', 'msg': 'Booking kamu berhasil dibuat. Jangan lupa dateng~👌'})

@api_bp.route('/api/v1/get_orders/<hashedUserId>')
def get_orders(hashedUserId):
  """API endpoint untuk mendapatkan data orders"""
  
  order_data = db.orders.find_one({'userId': hashedUserId}, {'_id': False})
  order_price = 0
  barber_price = 0 
  for order in order_data['selectedServices']:
    order_price = order_price + int(order['price'][:-1])
  for barber in order_data['selectedHairStylist']:
    barber_price = barber_price + int(barber['hairStylistPrice'][:-1])
  
  total_pay = order_price + barber_price
  data = {
    'email': order_data['email'],
    'name': order_data['name'],
    'services_order': order_data['selectedServices'],
    'barber_order': order_data['selectedHairStylist'],
    'tanggalBooking': order_data['tanggalBooking'],
    'waNum': order_data['waNum'],
    'total_pay': total_pay,
    'status': 'pending'
  }
  
  db.orders.update_one({'userId': hashedUserId}, {'$set': {'total_pay(K)': total_pay}})
  return jsonify({'result': 'still testing', 'order_data': data} )

@api_bp.route('/api/v1/cancel_order/<hashedUserId>', methods=['POST'])
def cancel_order(hashedUserId):
  """API endpoint untuk handle cancel order
  """
  db.orders.update_one({'userId': hashedUserId}, {'$set': {'is_cancel': True}})
  return jsonify({'result': 'success..', 'msg': 'Pesananmu berhasil dibatalkan! 👌'})

# api endpoint untuk dashboard admin
@api_bp.route('/api/v1/get_order_by_admin', methods=['GET'])
def get_order_by_admin():
  hair_stylist_name = request.args.get('hairStylistName')
  if not hair_stylist_name:
    return jsonify({'result': 'error', 'msg': 'hairStylistName parameter is required.'}), 400
  
  query =  {'selectedHairStylist.hairStylistName': hair_stylist_name}
  orders = list(db.orders.find(query, {'_id': False}))
  return jsonify({'result': 'success', 'msg': 'testing', 'orders': orders})

@api_bp.route('/api/v1/order_done', methods=['POST'])
def confirm_oder():
  """"API endpoint for confirming order"""
  hashedUserId = request.form['userId']
  db.orders.update_one({'userId': hashedUserId}, {'$set': {'status': 'Done'}})
  return jsonify({'result': 'success', 'msg': 'Orderan yang ini kelar a, alhamdulillah~🙏'})

@api_bp.route('/api/v1/order_cancel', methods=['POST'])
def cancel_oder():
  """"API endpoint for confirming order"""
  hashedUserId = request.form['userId']
  db.orders.update_one({'userId': hashedUserId}, {'$set': {'status': 'Cancel'}})
  return jsonify({'result': 'success', 'msg': 'Orderan yang ini dibatalkan a, aman ajaa~👌'})

@api_bp.route('/api/v1/pengajuan_cuti', methods=['POST'])
def pengajuan_cuti():
  nama = request.form['nama']
  print(nama)
  tglAwal = request.form['tglAwal']
  tglAkhir = request.form['tglAkhir']
  alasanCuti = request.form['alasanCuti']

  data = {
    'nama': nama,
    'tglAwal': tglAwal,
    'tglAkhir': tglAkhir,
    'alasanCuti': alasanCuti,
    'status': 'pending'
  }
  
  db.pengajuan_cuti.insert_one(data)
  return jsonify({'result': 'success', 'msg': 'permohonan cutimu berhasil diajukan, a~👌', 'statusCuti': 'pending'}), 200

@api_bp.route('/api/v1/data_pengajuan_cuti', methods=['GET'])
def data_pengajuan_cuti():
  nama = request.args.get('nama')
  data_pengajuan = list(db.pengajuan_cuti.find({'nama': nama}, {'_id': False}))
  return jsonify({'result': 'success', 'dataPengajuan': data_pengajuan}), 200

# akhir api endpoint untuk dashboard admin
# @api_bp.route('/api/v1/pengajuan_cuti')
# def pengajuan_cuti():
#   """api endpoint untuk memasukkan mock data pengajuan cuti. Next akan diubah menjadi api 
#   endpoint handle pengajuan cuti
#   """
#   data = [
#     {
#         "hairStylist_id": "HS001",
#         "tgl_cuti": "2024-07-01",
#         "tgl_masuk": "2024-07-10",
#         "is_approved": None
#     },
#     {
#         "hairStylist_id": "HS002",
#         "tgl_cuti": "2024-07-05",
#         "tgl_masuk": "2024-07-15",
#         "is_approved": None
#     },
#     {
#         "hairStylist_id": "HS003",
#         "tgl_cuti": "2024-07-08",
#         "tgl_masuk": "2024-07-18",
#         "is_approved": None
#     },
#     {
#         "hairStylist_id": "HS004",
#         "tgl_cuti": "2024-07-12",
#         "tgl_masuk": "2024-07-20",
#         "is_approved": None
#     },
#     {
#         "hairStylist_id": "HS005",
#         "tgl_cuti": "2024-07-15",
#         "tgl_masuk": "2024-07-25",
#         "is_approved": None
#     }
#   ]
#   return jsonify({'result': 'success', 'data': data})