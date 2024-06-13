from flask import Blueprint, render_template

web_bp = Blueprint('web', __name__)

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


    """
    
@app.route('/',methods=['GET','POST'])
def home():
    return render_template('mainSuperAdminDashboard.html')

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

@app.route('/addUser',methods=['GET','POST'])
def addUser():
    return render_template('mainSuperAdminAddUser.html')

@app.route('/add_user')
def admin_login():
    return render_template('newUser.html')
    """