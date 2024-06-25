from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from dotenv import load_dotenv
import os
from os.path import join, dirname
from pymongo import MongoClient
import jwt
from datetime import datetime, timedelta
import hashlib

web_bp = Blueprint('web', __name__)

dotenv = join(dirname(__file__), '.env')
load_dotenv(dotenv)

SECRET_KEY = os.environ.get('SECRET_KEY')
MONGO_URL = os.environ.get('MONGO_URL')
DB_NAME = os.environ.get('DB_NAME')

client = MongoClient(MONGO_URL)
db = client[DB_NAME]

@web_bp.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@web_bp.route('/admin/login')
def role_choose():
    return render_template('role.html')

@web_bp.route('/admin/login/<role>')
def login_by_role(role):
    if role == 'admin':
        return render_template('adminLogin.html')
    elif role == 'super_admin':
        return render_template('superAdminLogin.html')
    
@web_bp.route('/testimoni')
def testimoni_page():
    return render_template('testimoni.html')

@web_bp.route('/faq')
def faq():
    return render_template('faq.html')

# routes admin
@web_bp.route('/admin/dashboard',methods=['GET','POST'])
def admin_booking():
    token = request.cookies.get('token')
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_data = db.users.find_one({'fullName': payload['id']}, {'_id': False, 'pw': False})
        print(user_data)

        # ambil data jumlah order berdasarkan user yang login
        query_all_orders =  {'selectedHairStylist.hairStylistName': payload['id'].lower()}
        query_orders_done = {'selectedHairStylist.hairStylistName': payload['id'].lower(), 'status': 'Done'}
        query_orders_cancel = {'selectedHairStylist.hairStylistName': payload['id'].lower(), 'status': 'Cancel'}
        all_orders = db.orders.count_documents(query_all_orders)
        done_orders = db.orders.count_documents(query_orders_done)
        cancel_orders = db.orders.count_documents(query_orders_cancel)
        orders_data = {
            'all_orders': all_orders,
            'done_orders': done_orders,
            'cancel_orders': cancel_orders
        }
        return render_template('mainAdminBooking.html', user_data = user_data, orders_data = orders_data)
    except jwt.ExpiredSignatureError:
        return redirect(url_for('web.role_choose', msg='Login kamu udah kadaluwarsa, tolong login ulang yaa 🙏'))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('web.role_choose', msg='Maaf banget, sistem bermasalah pas kamu coba login. Tolong login ulang yaa 🙏'))

@web_bp.route('/admin/pengajuan_cuti',methods=['GET','POST'])
def admin_pengajuan_cuti():
    token = request.cookies.get('token')
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_data = db.users.find_one({'fullName': payload['id']}, {'_id': False, 'pw': False})
        print(user_data)

        # ambil data jumlah order berdasarkan user yang login
        query_all_orders =  {'selectedHairStylist.hairStylistName': payload['id'].lower()}
        query_orders_done = {'selectedHairStylist.hairStylistName': payload['id'].lower(), 'status': 'Done'}
        query_orders_cancel = {'selectedHairStylist.hairStylistName': payload['id'].lower(), 'status': 'Cancel'}
        all_orders = db.orders.count_documents(query_all_orders)
        done_orders = db.orders.count_documents(query_orders_done)
        cancel_orders = db.orders.count_documents(query_orders_cancel)
        orders_data = {
            'all_orders': all_orders,
            'done_orders': done_orders,
            'cancel_orders': cancel_orders
        }
        return render_template('mainAdminPengajuanCuti.html', user_data = user_data, orders_data = orders_data)
    except jwt.ExpiredSignatureError:
        return redirect(url_for('web.role_choose', msg='Login kamu udah kadaluwarsa, tolong login ulang yaa 🙏'))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('web.role_choose', msg='Maaf banget, sistem bermasalah pas kamu coba login. Tolong login ulang yaa 🙏'))
    return render_template('mainAdminPengajuanCuti.html')


# routes super admin
@web_bp.route('/super_admin/dashboard',methods=['GET','POST'])
def super_admin_dashboard():
    token = request.cookies.get('token')
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_data = db.users.find_one({'fullName': payload['id']}, {'_id': False, 'pw': False})

        # ambil data jumlah order berdasarkan user yang login
        query_orders_cancel = {'status': 'Cancel'}
        query_total_pegawai = {'role': 'admin'}
        all_orders = db.orders.count_documents({})
        cancel_orders = db.orders.count_documents(query_orders_cancel)
        total_pegawai = db.users.count_documents(query_total_pegawai)
        orders_data = {
            'all_orders': all_orders,
            'cancel_orders': cancel_orders,
            'total_pegawai': total_pegawai
        }

        return render_template('mainSuperAdminDashboard.html', user_data = user_data, orders_data = orders_data)
    except jwt.ExpiredSignatureError:
        return redirect(url_for('web.role_choose', msg='Login kamu udah kadaluwarsa, tolong login ulang yaa 🙏'))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('web.role_choose', msg='Maaf banget, sistem bermasalah pas kamu coba login. Tolong login ulang yaa 🙏'))


@web_bp.route('/super_admin/persetujuan_cuti')
def super_admin_persetujuan_cuti():
    token = request.cookies.get('token')
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_data = db.users.find_one({'fullName': payload['id']}, {'_id': False, 'pw': False})

        # ambil data jumlah order berdasarkan user yang login
        query_orders_cancel = {'status': 'Cancel'}
        query_total_pegawai = {'role': 'admin'}
        all_orders = db.orders.count_documents({})
        cancel_orders = db.orders.count_documents(query_orders_cancel)
        total_pegawai = db.users.count_documents(query_total_pegawai)
        orders_data = {
            'all_orders': all_orders,
            'cancel_orders': cancel_orders,
            'total_pegawai': total_pegawai
        }

        return render_template('mainSuperAdminPersetujuanCuti.html', user_data = user_data, orders_data = orders_data)
    except jwt.ExpiredSignatureError:
        return redirect(url_for('web.role_choose', msg='Login kamu udah kadaluwarsa, tolong login ulang yaa 🙏'))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('web.role_choose', msg='Maaf banget, sistem bermasalah pas kamu coba login. Tolong login ulang yaa 🙏'))


@web_bp.route('/super_admin/users')
def super_admin_users():
    token = request.cookies.get('token')
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_data = db.users.find_one({'fullName': payload['id']}, {'_id': False, 'pw': False})

        # ambil data jumlah order berdasarkan user yang login
        query_orders_cancel = {'status': 'Cancel'}
        query_total_pegawai = {'role': 'admin'}
        all_orders = db.orders.count_documents({})
        cancel_orders = db.orders.count_documents(query_orders_cancel)
        total_pegawai = db.users.count_documents(query_total_pegawai)
        orders_data = {
            'all_orders': all_orders,
            'cancel_orders': cancel_orders,
            'total_pegawai': total_pegawai
        }

        return render_template('mainSuperAdminUsers.html', user_data = user_data, orders_data = orders_data)
    except jwt.ExpiredSignatureError:
        return redirect(url_for('web.role_choose', msg='Login kamu udah kadaluwarsa, tolong login ulang yaa 🙏'))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('web.role_choose', msg='Maaf banget, sistem bermasalah pas kamu coba login. Tolong login ulang yaa 🙏'))


@web_bp.route('/super_admin/add_users')
def super_admin_add_users():
    token = request.cookies.get('token')
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_data = db.users.find_one({'fullName': payload['id']}, {'_id': False, 'pw': False})

        # ambil data jumlah order berdasarkan user yang login
        query_orders_cancel = {'status': 'Cancel'}
        query_total_pegawai = {'role': 'admin'}
        all_orders = db.orders.count_documents({})
        cancel_orders = db.orders.count_documents(query_orders_cancel)
        total_pegawai = db.users.count_documents(query_total_pegawai)
        orders_data = {
            'all_orders': all_orders,
            'cancel_orders': cancel_orders,
            'total_pegawai': total_pegawai
        }

        return render_template('mainSuperAdminAddUser.html', user_data = user_data, orders_data = orders_data)
    except jwt.ExpiredSignatureError:
        return redirect(url_for('web.role_choose', msg='Login kamu udah kadaluwarsa, tolong login ulang yaa 🙏'))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('web.role_choose', msg='Maaf banget, sistem bermasalah pas kamu coba login. Tolong login ulang yaa 🙏'))


@web_bp.route('/super_admin/testimoni')
def super_admin_testimoni():
    token = request.cookies.get('token')
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_data = db.users.find_one({'fullName': payload['id']}, {'_id': False, 'pw': False})

        # ambil data jumlah order berdasarkan user yang login
        query_orders_cancel = {'status': 'Cancel'}
        query_total_pegawai = {'role': 'admin'}
        all_orders = db.orders.count_documents({})
        cancel_orders = db.orders.count_documents(query_orders_cancel)
        total_pegawai = db.users.count_documents(query_total_pegawai)
        orders_data = {
            'all_orders': all_orders,
            'cancel_orders': cancel_orders,
            'total_pegawai': total_pegawai
        }

        return render_template('mainSuperAdminTestimoni.html', user_data = user_data, orders_data = orders_data)
    except jwt.ExpiredSignatureError:
        return redirect(url_for('web.role_choose', msg='Login kamu udah kadaluwarsa, tolong login ulang yaa 🙏'))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('web.role_choose', msg='Maaf banget, sistem bermasalah pas kamu coba login. Tolong login ulang yaa 🙏'))


@web_bp.route('/booking')
def booking_page():
    return render_template('main_booking_page.html')

@web_bp.route('/booking/<pagenum>')
def booking_form_page(pagenum):
    return render_template(f'booking_page_{pagenum}.html')
        
# page routing admin dashboard
@web_bp.route('/admin/pengajuan_cuti')
def pengajuan_cuti_page():
    return render_template('mainAdminPengajuanCuti.html')
# page routing super admin dashboard

"""
@app.route('/Persetujuan_cuti',methods=['GET','POST'])
def persetujuan():
    return render_template('mainSuperAdminPersetujuanCuti.html')


@app.route('/Users',methods=['GET','POST'])
def users():
    return render_template('mainSuperAdminUsers.html')

@app.route('/testimoni',methods=['GET','POST'])
def testimoni():
    return render_template('mainSuperAdminTestimoni.html')

@app.route('/admin',methods=['GET','POST'])
def admin():
    return render_template('mainAdminBooking.html')

"""

# @web_bp.route('/addUser',methods=['GET','POST'])
# def addUser():
#     return render_template('mainSuperAdminAddUser.html')

@web_bp.route('/add_user')
def admin_login():
    return render_template('newUser.html')