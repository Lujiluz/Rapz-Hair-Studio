from flask import Flask,redirect,url_for,render_template,request

app=Flask(__name__)
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

if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)