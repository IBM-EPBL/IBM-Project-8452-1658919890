from flask import render_template
import sqlite3
# import requests
from flask import Flask
from flask import request,redirect,url_for,session,flash
from flask_wtf import Form
from wtforms import TextField

import ibm_db


conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=9938aec0-8105-433e-8bf9-0fbb7e483086.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32459;PROTOCOL=TCPIP;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=vqf74844;PWD=D5iOiJ8ilcEj5VL2;", "", "")
print("Opened database successfully")

app = Flask(__name__)
app.secret_key = "super secret key"

@app.route('/')
def hel():
    if session.get('username')==True:
        messages = session['username']

    else:
        messages = ""
    user = {'username': messages}
    return redirect(url_for('index',user=user))


@app.route('/reg')
def add():
    return render_template('register.html')


@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
    msg = ""
   #con = None
    if request.method == 'POST':
        try:
            nm = request.form['nm']
            addr = request.form['add']
            city = request.form['city']
            pin = request.form['pin']
            bg = request.form['bg']
            email = request.form['email']
            passs = request.form['pass']
            usertype = request.form['usertype']
            avail='F'
            if(usertype=="recipients"):
                avail='T'
        
            sql = "INSERT INTO plasma_users (name,addr,city,pin,bg,email,pass,usertype,available) VALUES ('"+nm+"','"+addr+"','" +city+"','"+ pin+"','"+ bg+"','"+email+"','"+passs+"','"+usertype+"','"+avail+"')"
            stmt = ibm_db.exec_immediate(conn, sql)
            print(sql)
            if(ibm_db.num_rows(stmt)==1):
                print("inserted")
                msg = "Successfully Inserted"
            else:
                print("Not inserted")
                msg = "Not Successfully Inserted"
        except Exception as e:
            print(e)
            msg = "error in insert operation"
        finally:
            return redirect(url_for('index'))





@app.route('/index',methods = ['GET'])
def index():
    
    if session.get('username') is not None:
        messages = session['username']

    else:
        messages = ""
    user = {'username': messages}

    if request.method=='GET':

        sql = "select * from plasma_users"
        stmt = ibm_db.exec_immediate(conn, sql)
        row = ibm_db.fetch_both(stmt)
        rows = []
        index = 0
        while(row != False):
            row["INDEX"] = index
            rows.append(row)
            index+=1
            row = ibm_db.fetch_both(stmt)
        return render_template('index.html', title='Home', user=user, rows=rows)

   




if __name__ == '__main__':
    app.run(debug=True)
