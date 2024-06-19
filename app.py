from flask import Flask, render_template, request, session, flash
from werkzeug.utils import secure_filename
import cv2 
import os
import math, random

app = Flask(__name__)

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="vtpip09_2022"
)

app.secret_key = 'your secret key'

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/ad')
def ad():
    return render_template('ad.html')

@app.route('/doctor')
def doctor():
    return render_template('doctor.html')

@app.route('/user')
def user():
    return render_template('user.html')

@app.route('/adoc')
def adoc():
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM doctor')
    account = cursor.fetchall()
    return render_template('adoc.html', result = account)

@app.route('/auser')
def auser():
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM user')
    account = cursor.fetchall()
    return render_template('auser.html', result = account)

@app.route('/asymp')
def asymp():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM userdet WHERE status= 'pending'")
    account = cursor.fetchall()
    return render_template('asymp.html', result = account)

@app.route('/docreq')
def docreq():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM sreport WHERE dreq= 'pending'")
    account = cursor.fetchall()
    return render_template('docreq.html', result = account)

@app.route('/ureq')
def ureq():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM sreport WHERE ureq= 'pending'")
    account = cursor.fetchall()
    return render_template('ureq.html', result = account)

@app.route('/adsend/<string:id>')
def adsend(id):
    cursor = mydb.cursor()
    cursor.execute("update sreport set dreq ='completed' WHERE Id = "+ id)
    mydb.commit()
    return render_template('adhome.html')

@app.route('/ausend/<string:id>')
def ausend(id):
    cursor = mydb.cursor()
    cursor.execute("update sreport set ureq ='completed' WHERE Id = "+ id)
    mydb.commit()
    return render_template('adhome.html')

@app.route('/abed/<string:id>')
def abed(id):
    cursor = mydb.cursor()
    cursor.execute("update dpre set bstatus ='Done' WHERE Id = "+ id)
    mydb.commit()
    return render_template('adhome.html')

@app.route('/dpre')
def dpre():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM dpre WHERE bed= 'yes' and bstatus ='pending'")
    account = cursor.fetchall()
    cursor.execute("SELECT * FROM dpre WHERE bstatus ='Done'")
    account1 = cursor.fetchall()
    return render_template('dpre.html', result = account, result1 = account1)

@app.route('/alogin', methods = ['POST', 'GET'])
def alogin():
    if request.method == 'POST':
        uid = request.form['uid']
        pwd = request.form['pwd']
        if uid == 'lab' and pwd == 'lab':
            return render_template('ahome.html')
        else:
            return render_template('admin.html')

@app.route('/adlogin', methods = ['POST', 'GET'])
def adlogin():
    if request.method == 'POST':
        uid = request.form['uid']
        pwd = request.form['pwd']
        if uid == 'admin' and pwd == 'admin':
            return render_template('adhome.html')
        else:
            return render_template('ad.html')

@app.route('/ulogin', methods = ['POST', 'GET'])
def ulogin():
    if request.method == 'POST':
        uid = request.form['uid']
        pwd = request.form['pwd']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM user WHERE email = %s AND password = %s', (uid, pwd))
        account = cursor.fetchone()
        if account:
            session['uid'] = request.form['uid']
            session['name'] = account[0]
            return render_template('uhome.html', result = account[0])
        else:
            flash("Please Enter Valid Details...")
            return render_template('user.html')

@app.route('/dlogin', methods = ['POST', 'GET'])
def dlogin():
    if request.method == 'POST':
        uid = request.form['uid']
        pwd = request.form['pwd']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM doctor WHERE email = %s AND password = %s', (uid, pwd))
        account = cursor.fetchone()
        if account:
            session['uid'] = request.form['uid']
            session['name'] = account[0]
            session['man'] = account[4]
            return render_template('dhome.html', result = account[0])
        else:
            return render_template('doctor.html')

@app.route('/ahome')
def ahome():
    return render_template('ahome.html')

@app.route('/adhome')
def adhome():
    return render_template('ahome.html')

@app.route('/uregister')
def uregister():
    return render_template('ureg.html')

@app.route('/dregister')
def dregister():
    return render_template('dreg.html')

@app.route('/dreg', methods = ['POST', 'GET'])
def dreg():
    if request.method == 'POST':
        name = request.form['name']
        uid = request.form['uid']
        pwd = request.form['pwd']
        mob = request.form['mob']
        dep = request.form['dep']
        var = (name, uid, pwd, mob, dep)
        cursor = mydb.cursor()
        cursor.execute('insert into doctor values (%s, %s, %s, %s, %s)', var)
        mydb.commit()
        if cursor.rowcount == 1:
            flash("Doctor Registered Successfuly") 
            return render_template('adhome.html')
        else:
            flash("Invalid Details, Doctor not Registered")
            return render_template('dreg.html')

@app.route('/ureg', methods = ['POST', 'GET'])
def ureg():
    if request.method == 'POST':
        name = request.form['name']
        uid = request.form['uid']
        pwd = request.form['pwd']
        mob = request.form['mob']
        loc = request.form['loc']
        var = (name, uid, pwd, mob, loc)
        cursor = mydb.cursor()
        cursor.execute('insert into user values (%s, %s, %s, %s, %s)', var)
        mydb.commit()
        if cursor.rowcount == 1:
            flash("User Registered Successfuly") 
            return render_template('user.html')
        else:
            flash("Invalid Details, User not Registered")
            return render_template('ureg.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('index.html')

@app.route('/duser')
def duser():
    uid = session['uid']
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM userdet WHERE DocId = '"+uid+"' and status= 'approved'")
    account = cursor.fetchall()
    return render_template('duser.html', result = account)

@app.route('/dreport')
def dreport():
    uid = session['uid']
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM userdet WHERE DocId = '"+uid+"' and status= 'completed'")
    account = cursor.fetchall()
    return render_template("dreport.html", result = account)

@app.route('/usymp')
def usymp():
    return render_template("udoc.html")

@app.route('/ureport')
def ureport():
    uid = session['uid']
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM userdet WHERE email = '"+uid+"' and status= 'completed'")
    account = cursor.fetchall()
    return render_template("ureport.html", result = account)

@app.route('/asend', methods = ['POST', 'GET'])
def asend():
    if request.method == 'POST':
        sid = request.form['id']
        did = request.form['did']
        cursor = mydb.cursor()
        var = (did, 'approved' ,sid)
        cursor.execute('update userdet set docid = %s, status = %s where id=%s', var)
        mydb.commit()
        if cursor.rowcount == 1:
            flash("Sent Successfuly") 
            return render_template('adhome.html')
        else:
            cursor = mydb.cursor()
            cursor.execute("SELECT * FROM userdet WHERE status= 'pending'")
            account = cursor.fetchall()
            return render_template('asymp.html', result = account)

@app.route('/usend', methods = ['POST', 'GET'])
def usend():
    if request.method == 'POST':
        name = session['name']
        uid = session['uid']
        sym = request.form['sym']
        var = (name, uid, sym)
        cursor = mydb.cursor()
        cursor.execute('insert into userdet (id, name, email, symptoms, status) values (0, %s, %s, %s, "pending")', var)
        mydb.commit()
        if cursor.rowcount == 1:
            flash("Symptoms sent Successfuly") 
            return render_template('uhome.html', result = name)
        else:
            flash("Invalid Details, User not Registered")
            cursor.execute('SELECT * FROM doctor')
            account = cursor.fetchall()
            return render_template("udoc.html", result = account)

@app.route('/dsend/<string:id>')
def dsend(id):
    cursor = mydb.cursor()
    cursor.execute("update userdet set status ='process' WHERE Id = "+ id)
    mydb.commit()
    if cursor.rowcount == 1:
        return render_template('dhome.html', result = session['name'])
    else:
        uid = session['uid']
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM userdet WHERE DocId = '"+uid+"' and status= 'pending'")
        account = cursor.fetchall()
        return render_template('duser.html', result = account)
    
@app.route('/sreport')
def sreport():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM userdet WHERE status= 'process'")
    account = cursor.fetchall()
    return render_template('sreport.html', result = account)

@app.route('/ssend/<string:id>')
def ssend(id):
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM userdet WHERE id="+id)
    account = cursor.fetchone()
    return render_template('ssend.html', result = account)
    
@app.route('/send', methods = ['POST', 'GET'])
def send():
    if request.method == 'POST':
        cid = request.form['id']
        name = request.form['name']
        uid = request.form['uid']
        did = request.form['did']
        f = request.files['file']
        fname = "C:/MiniProject/MPCS12/CODE/MPCS12_2023/static/"+f.filename
        f.save(secure_filename(f.filename))
        img = cv2.imread(f.filename)
        cv2.imwrite(fname, img) 
        key = token()
        var = (cid, name, uid, did, f.filename, key)
        cursor = mydb.cursor()
        cursor.execute('insert into sreport (id, name, email, docid, filename, key1) values (%s, %s, %s, %s, %s, %s)', var)
        mydb.commit()
        os.remove(f.filename)
        if cursor.rowcount == 1:
            cursor.execute("update userdet set status ='completed' WHERE Id = "+ cid)
            mydb.commit()
            return render_template('ahome.html')
        else:
            cursor.execute("SELECT * FROM userdet WHERE status= 'process'")
            account = cursor.fetchall()
            return render_template('sreport.html', result = account)

@app.route('/drep/<string:id>')
def drep(id):
    cursor = mydb.cursor()
    cursor.execute("SELECT filename FROM sreport WHERE id= "+id)
    account = cursor.fetchone()
    session['id'] = id
    session['fname'] = account[0]
    return render_template('drep.html')

@app.route('/drequest')
def drequest():
    return render_template('drequest.html')

@app.route('/drq')
def drq():
    cid = session['id']
    cursor = mydb.cursor()
    cursor.execute("update sreport set dreq ='pending' WHERE Id = "+ cid)
    mydb.commit()
    if cursor.rowcount == 1:
        flash("Key Requested Successfully...")
        return render_template('dhome.html', result = session['name'])
    else:
        flash("Key Request not Done")
        return render_template('dhome.html', result = session['name'])
    
@app.route('/dkey')
def dkey():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM sreport WHERE dreq='completed' and docid='" + session['uid'] + "'")
    account = cursor.fetchall()
    return render_template('dkey.html', result = account)

@app.route('/dpres')
def dpres():
    return render_template('dpres.html')

@app.route('/dpc', methods = ['POST', 'GET'])
def dpc():
    if request.method == 'POST':
        cid = session['id']
        med = request.form['med']
        bed = request.form['bed']
        food = request.form['food']
        cursor = mydb.cursor()
        cursor.execute("SELECT email FROM sreport WHERE id = " +cid)
        eid = cursor.fetchone()
        print(eid)
        bst = 'Done'
        if bed == 'yes':
            bst = 'pending'
        var = (cid, eid[0], med, bed, food, bst)
        cursor.execute('insert into dpre values (%s, %s, %s, %s, %s, %s)', var)
        mydb.commit()
        if cursor.rowcount == 1:
            flash("Prescription sent Successfully...")
            return render_template('dhome.html', result = session['name'])
        else:
            flash("Prescription not sent")
            return render_template('dhome.html', result = session['name'])

@app.route('/display')
def display():
    cid = session['id']
    cursor = mydb.cursor()
    cursor.execute("SELECT filename FROM sreport WHERE id= "+cid)
    account = cursor.fetchone()
    return render_template('display.html', result = account)

@app.route('/urep/<string:id>')
def urep(id):
    cursor = mydb.cursor()
    cursor.execute("SELECT filename FROM sreport WHERE id= "+id)
    account = cursor.fetchone()
    session['id'] = id
    session['fname'] = account[0]
    return render_template('urep.html')

@app.route('/urequest')
def urequest():
    cid = session['id']
    cursor = mydb.cursor()
    cursor.execute("SELECT key1 FROM sreport WHERE id= "+cid)
    account = cursor.fetchone()
    return render_template('urequest.html', result = account)

@app.route('/urq')
def urq():
    cid = session['id']
    cursor = mydb.cursor()
    cursor.execute("update sreport set ureq ='pending' WHERE Id = "+ cid)
    mydb.commit()
    if cursor.rowcount == 1:
        flash("Key Requested Successfully...")
        return render_template('uhome.html', result = session['name'])
    else:
        flash("Key Request not Done")
        return render_template('uhome.html', result = session['name'])
    
@app.route('/ukey')
def ukey():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM sreport WHERE ureq='completed' and email='" + session['uid'] + "'")
    account = cursor.fetchall()
    return render_template('ukey.html', result = account)

@app.route('/uprec')
def uprec():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM dpre WHERE email='" + session['uid'] + "'")
    account = cursor.fetchall()
    return render_template('uprec.html', result = account)

@app.route('/udisplay')
def udisplay():
    cid = session['id']
    cursor = mydb.cursor()
    cursor.execute("SELECT filename FROM sreport WHERE id= "+cid)
    account = cursor.fetchone()
    return render_template('udisplay.html', result = account)

def token():
    st = "abcdefijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    length = len(st)
    OTP = ""
    for i in range(10) :
        OTP += st[math.floor(random.random() * length)]
    return OTP

if __name__ == '__main__':
   app.run()