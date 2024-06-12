from flask import Blueprint, render_template

web_bp = Blueprint('web', __name__)

@web_bp.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@web_bp.route('/login')
def role_choose():
    return render_template('role.html')

@web_bp.route('/login/<role>')
def login_by_role(role):
    if role == 'admin':
        return render_template('adminLogin.html')
    elif role == 'superadmin':
        return render_template('superAdminLogin.html')
    
@web_bp.route('/testimoni')
def testimoni_page():
    return render_template('testimoni.html')

@web_bp.route('/faq')
def faq():
    return render_template('faq.html')