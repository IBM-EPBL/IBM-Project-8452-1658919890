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





@app.route('/index',methods = ['POST','GET'])
def index():



    if request.method == 'POST':
        if session.get('username') is not None:
            messages = session['username']

        else:
            messages = ""
        user = {'username': messages}
        print(messages)
        val = request.form['search']
        print(val)
        type = request.form['type']
        print(type)
        if type=='blood':


            sql = "select * from plasma_users where bg='" + val + "' and usertype='donor'"
            stmt = ibm_db.exec_immediate(conn, sql)
            rows = []
            temp_filter_user = ibm_db.fetch_both(stmt)
            print(temp_filter_user)
            index = 0
            while temp_filter_user != False:
                temp_filter_user['INDEX'] = index
                rows.append(temp_filter_user)
                index+=1
                temp_filter_user = ibm_db.fetch_both(stmt)
            print("rows----------------------------")
            print(rows)

            sql = "select * from plasma_users where usertype='donor'"
            stmt = ibm_db.exec_immediate(conn, sql)
            allusers = []
            temp_all_user = ibm_db.fetch_both(stmt)
            while temp_all_user != False:
                print(temp_all_user)
                allusers.append(temp_all_user)
                temp_all_user = ibm_db.fetch_both(stmt)
            print("allusers---------------------------------------" )
            print(allusers)
            # con = sqlite3.connect('database.db')
            # con.row_factory = sqlite3.Row

            # cur = con.cursor()
            # cur.execute("select * from plasma_users where bg=?",(val,))
            # search = cur.fetchall();
            # cur.execute("select * from plasma_users ")

            # rows = cur.fetchall();


            return render_template('index.html', title='Home', user=user,rows=allusers,search=rows)

        if type=='donorname':

            sql = "select * from plasma_users where name='" + val + "' and usertype='donor'"
            stmt = ibm_db.exec_immediate(conn, sql)
            rows = []
            temp_filter_user = ibm_db.fetch_both(stmt)
            print(temp_filter_user)
            while temp_filter_user != False:
                rows.append(temp_filter_user)
                temp_filter_user = ibm_db.fetch_both(stmt)
            print("rows----------------------------")
            print(rows)

            sql = "select * from plasma_users where usertype='donor'"
            stmt = ibm_db.exec_immediate(conn, sql)
            allusers = []
            temp_all_user = ibm_db.fetch_both(stmt)
            while temp_all_user != False:
                print(temp_all_user)
                allusers.append(temp_all_user)
                temp_all_user = ibm_db.fetch_both(stmt)
            print("allusers---------------------------------------" )
            print(allusers)

            # con = sqlite3.connect('database.db')
            # con.row_factory = sqlite3.Row

            # cur = con.cursor()
            # cur.execute("select * from plasma_users where name=?",(val,))
            # search = cur.fetchall();
            # cur.execute("select * from users ")

            # rows = cur.fetchall();


            return render_template('index.html', title='Home', user=user,rows=allusers,search=rows)



    if session.get('username') is not None:
        messages = session['username']

    else:
        messages = ""
    user = {'username': messages}
    print(messages)
    if request.method=='GET':
        # con = sqlite3.connect('database.db')
        # con.row_factory = sqlite3.Row

        # cur = con.cursor()
        # cur.execute("select * from users ")

        # rows = cur.fetchall();

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

    #messages = request.args['user']




@app.route('/list')
def list():
   con = sqlite3.connect('database.db')
   con.row_factory = sqlite3.Row

   cur = con.cursor()
   cur.execute("select * from users")

   rows = cur.fetchall();
   print(rows)
   return render_template("list.html",rows = rows)

@app.route('/drop')
def dr():
        con = sqlite3.connect('database.db')
        con.execute("DROP TABLE request")
        return "dropped successfully"

@app.route('/login',methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('/login.html')
    if request.method == 'POST':

        email = request.form['email']
        password = request.form['pass']
        usertype = request.form['usertype']
        # if email == 'admin@bloodbank.com' and password == 'admin':
        #     a = 'yes'
        #     session['username'] = email
        #     #session['logged_in'] = True
        #     session['admin'] = True
        #     return redirect(url_for('index'))

        sql="select name,email,pass,usertype from plasma_users where email='" + email + "'"
        stmt = ibm_db.exec_immediate(conn, sql)
        row = ibm_db.fetch_both(stmt)
        print(row)
        if not row:
            print("User Not Exists")
            return render_template('/login.html')
        # rows = cur.fetchall();
        print(row['EMAIL'],row['PASS'],row["USERTYPE"])
        a = row['EMAIL']
        print(a)
        u = {'username': a}
        p = row['PASS']
        utype = row['USERTYPE']
        print(p)

        if email == a and password == p and usertype == utype:
            session['username'] = a
            session['name'] = row["NAME"]
            session['usertype'] = row["USERTYPE"]
            session['level'] = 0
            session['logged_in'] = True
            # return redirect(url_for('index'))
            if(row["USERTYPE"] == 'recipients'):
                return redirect('dashboard')
            else:
                session['level'] = 0
                sql="select * from plasma_request where toemail='" + email + "'"
                stmt = ibm_db.exec_immediate(conn, sql)
                data = ibm_db.fetch_both(stmt)
                points = 0
                while(data != False):
                    if(data['STATUS'] == 'Accepted'):
                        points+=3
                    else:
                        points-=2
                    data = ibm_db.fetch_both(stmt)
                session['level'] = points 
                return render_template('/index.html')
        else:
            return render_template('/login.html')
        # return render_template('/login.html')
    else:
        return render_template('/')


@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   session.pop('logged_in',None)
   session.pop('usertype',None)
   session.pop('name',None)
   try:
       session.pop('admin',None)
   except KeyError as e:
       print("I got a KeyError - reason " +str(e))


   return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
   totalblood=0
   con = sqlite3.connect('database.db')
   con.row_factory = sqlite3.Row

   cur = con.cursor()
   cur.execute("select * from blood")

   rows = cur.fetchall();
   for row in rows:
       totalblood  += int(row['qty'])
   
   cur.execute("select * from users")
   users = cur.fetchall();

   Apositive=0
   Opositive=0
   Bpositive=0
   Anegative=0
   Onegative=0
   Bnegative=0
   ABpositive=0
   ABnegative = 0

   print(rows)
   cur.execute("select * from blood where type=?",('A+',))
   type = cur.fetchall();
   for a in type:
       Apositive += int(a['qty'])

   cur.execute("select * from blood where type=?",('A-',))
   type = cur.fetchall();
   for a in type:
       Anegative += int(a['qty'])


   cur.execute("select * from blood where type=?",('O+',))
   type = cur.fetchall();
   for a in type:
       Opositive += int(a['qty'])

   cur.execute("select * from blood where type=?",('O-',))
   type = cur.fetchall();
   for a in type:
       Onegative += int(a['qty'])

   cur.execute("select * from blood where type=?",('B+',))
   type = cur.fetchall();
   for a in type:
       Bpositive += int(a['qty'])


   cur.execute("select * from blood where type=?",('B-',))
   type = cur.fetchall();
   for a in type:
       Bnegative += int(a['qty'])



   cur.execute("select * from blood where type=?",('AB+',))
   type = cur.fetchall();
   for a in type:
       ABpositive += int(a['qty'])


   cur.execute("select * from blood where type=?",('AB-',))
   type = cur.fetchall();
   for a in type:
       ABnegative += int(a['qty'])


   bloodtypestotal = {'apos': Apositive,'aneg':Anegative,'opos':Opositive,'oneg':Onegative,'bpos':Bpositive,'bneg':Bnegative,'abpos':ABpositive,'abneg':ABnegative}






   return render_template("requestdonors.html",rows = rows,totalblood = totalblood,users=users,bloodtypestotal=bloodtypestotal)


@app.route('/bloodbank')
def bl():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")
    conn.execute('CREATE TABLE IF NOT EXISTS blood (id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT, donorname TEXT, donorsex TEXT, qty TEXT, dweight TEXT, donoremail TEXT, phone TEXT)')
    print( "Table created successfully")
    conn.close()
    return render_template('/adddonor.html')


@app.route('/addb',methods =['POST','GET'])
def addb():
    msg = ""
    if request.method == 'POST':
        try:
           type = request.form['blood_group']
           donorname = request.form['donorname']
           donorsex = request.form['gender']
           qty = request.form['qty']
           dweight = request.form['dweight']
           email = request.form['email']
           phone = request.form['phone']



           with sqlite3.connect("database.db") as con:
              cur = con.cursor()
              cur.execute("INSERT INTO blood (type,donorname,donorsex,qty,dweight,donoremail,phone) VALUES (?,?,?,?,?,?,?)",(type,donorname,donorsex,qty,dweight,email,phone) )
              con.commit()
              msg = "Record successfully added"
        except:
           con.rollback()
           msg = "error in insert operation"

        finally:
            flash("added new entry!")
            return redirect(url_for('dashboard'))
            con.close()

    else:
        return render_template("rest.html",msg=msg)

@app.route("/editdonor/<id>", methods=('GET', 'POST'))
def editdonor(id):
    msg =""
    if request.method == 'GET':
        con = sqlite3.connect('database.db')
        con.row_factory = sqlite3.Row

        cur = con.cursor()
        cur.execute("select * from blood where id=?",(id,))
        rows = cur.fetchall();
        return render_template("editdonor.html",rows = rows)
    if request.method == 'POST':
        try:
           type = request.form['blood_group']
           donorname = request.form['donorname']
           donorsex = request.form['gender']
           qty = request.form['qty']
           dweight = request.form['dweight']
           email = request.form['email']
           phone = request.form['phone']



           with sqlite3.connect("database.db") as con:
              cur = con.cursor()
              cur.execute("UPDATE blood SET type = ?, donorname = ?, donorsex = ?, qty = ?,dweight = ?, donoremail = ?,phone = ? WHERE id = ?",(type,donorname,donorsex,qty,dweight,email,phone,id) )
              con.commit()
              msg = "Record successfully updated"
        except:
           con.rollback()
           msg = "error in insert operation"

        finally:
            flash('saved successfully')
            return redirect(url_for('dashboard'))
            con.close()

@app.route("/myprofile/<email>", methods=('GET', 'POST'))
def myprofile(email):
    msg =""
    if request.method == 'GET':

        print(email)
        # con = sqlite3.connect('database.db')
        # con.row_factory = sqlite3.Row

        # cur = con.cursor()
        # cur.execute("select * from users where email=?",(email,))
        # rows = cur.fetchall();

        # sql = "select * from plasma_users where email='" + email + "'"
        sql="select * from plasma_users where email='" + email + "'"
        stmt = ibm_db.exec_immediate(conn, sql)
        rows = [ibm_db.fetch_both(stmt)]
        print(rows)
        return render_template("myprofile.html",rows = rows)

    if request.method == 'POST':
        try:
           name = request.form['name']
           addr = request.form['addr']
           city = request.form['city']
           pin = request.form['pin']
           bg = request.form['bg']
           email = request.form['email']
           avail=request.form['Aval']
           print(name,addr,avail)
           
           sql = "UPDATE plasma_users SET name='" + name + "',addr='" + addr + "',city='" + city + "',pin='" + pin + "',bg='" + bg + "',available='" + avail +"' where email='" + email + "'"
           print(sql)
           stmt = ibm_db.exec_immediate(conn, sql)          
           if(ibm_db.num_rows(stmt)==1):
                print("Updated")
                msg = "Successfully Updated"
           else:
                print("Not Updated")
                msg = "Not Successfully Inserted"


        #    with sqlite3.connect("database.db") as con:
        #       cur = con.cursor()
        #       cur.execute("UPDATE users SET name = ?, addr = ?, city = ?, pin = ?,bg = ?, email = ? WHERE email = ?",(name,addr,city,pin,bg,emailid,email) )
        #       con.commit()
        #       msg = "Record successfully updated"
        except Exception as e:
            print("Error",e)
            msg = "error in insert operation"

        finally:
           flash('profile saved')
           return redirect(url_for('index'))
           con.close()



@app.route('/contactforblood/<emailid>', methods=('GET', 'POST'))
def contactforblood(emailid):
    if request.method == 'GET':
        # sql = "CREATE TABLE IF NOT EXISTS plasma_request (id INTEGER PRIMARY KEY AUTOINCREMENT, toemail VARCHAR(32), fromemail VARCHAR(32), toname VARCHAR(32), toaddr VARCHAR(100))"
        # stmt = ibm_db.exec_immediate(conn, sql)
        # rows = ibm_db.fetch_both(stmt)
        # print(rows)

        fromemail = session['username']
        name = request.form['nm']
        addr = request.form['add']

        print(fromemail,emailid)

        # To get number of rows----------------------
        sql = "select * from plasma_request"
        stmt = ibm_db.exec_immediate(conn,sql)
        rows = 0
        dictionary = ibm_db.fetch_row(stmt)
        while dictionary != False:
            print(dictionary)
            dictionary = ibm_db.fetch_row(stmt)
            rows+=1
        # To get number of rows end----------------------
        # get new row index-------------------------
        rows+=1
        print(rows)
        # get new row index-------------------------
        sql = "INSERT INTO plasma_request (id,toemail,fromemail,toname,toaddr,status) VALUES (" + str(rows) + " , '"+ emailid + "' , '" + fromemail + "' , '" + name + "' , '" + addr + "' , 'PENDING')"
        print(sql)
        # get new row index end-------------------------
        stmt = ibm_db.exec_immediate(conn, sql)
        if(ibm_db.num_rows(stmt)==1):
            msg = "Successfully Inserted"
        else:
            msg = "Not Successfully Inserted"
        print(msg)
        flash('request sent')
        return redirect(url_for('index'))
    if request.method == 'POST':
        fromemail = session['username']
        name = request.form['nm']
        addr = request.form['add']

        print(fromemail,emailid)
        sql = "select * from plasma_request"
        stmt = ibm_db.exec_immediate(conn,sql)
        rows = 0
        dictionary = ibm_db.fetch_row(stmt)
        while dictionary != False:
            print(dictionary)
            dictionary = ibm_db.fetch_row(stmt)
            rows+=1
        rows+=1
        print(rows)
        sql = "INSERT INTO plasma_request (id,toemail,fromemail,toname,toaddr,status) VALUES (" + str(rows) + " , '"+ emailid + "' , '" + fromemail + "' , '" + name + "' , '" + addr + "' , 'PENDING')"
        print(sql)
        stmt = ibm_db.exec_immediate(conn, sql)
        if(ibm_db.num_rows(stmt)==1):
            msg = "Successfully Inserted"
        else:
            msg = "Not Successfully Inserted"
        print(msg)
        # conn.execute("INSERT INTO request (toemail,formemail,toname,toaddr) VALUES (?,?,?,?)",(emailid,fromemail,name,addr) )
        # conn.commit()
        # conn.close()
        flash('request sent')
        return redirect(url_for('index'))



@app.route('/notifications',methods=('GET','POST'))
def notifications():
    if request.method == 'GET':
            sql = "select * from plasma_request where toemail='" + session['username'] +"'"
            stmt = ibm_db.exec_immediate(conn , sql)
            row = ibm_db.fetch_both(stmt)
            notify = []
            while(row != False):
                notify.append(row)
                row = ibm_db.fetch_both(stmt)
            print(notify)
            notify = notify[::-1]
            # conn = sqlite3.connect('database.db')
            # print("Opened database successfully")
            # conn.row_factory = sqlite3.Row

            # cur = conn.cursor()
            # cor = conn.cursor()
            
            # cur.execute('select * from plasma_request where toemail=?',(session['username'],))
            # cor.execute('select * from plasma_request where toemail=?',(session['username'],))
            # row = cor.fetchone();
            # rows = cur.fetchall();
            if row:
                return render_template('notifications.html')
            else:
                return render_template('notifications.html',rows=notify)


@app.route('/notifyusers',methods=('GET','POST'))
def notifyusers():
    if request.method == 'GET':
            sql = "select * from plasma_request where fromemail='" + session['username'] +"'"
            stmt = ibm_db.exec_immediate(conn , sql)
            row = ibm_db.fetch_both(stmt)
            notify = []
            while(row != False):
                notify.append(row)
                row = ibm_db.fetch_both(stmt)
            notify = notify[::-1]
            # conn = sqlite3.connect('database.db')
            # print("Opened database successfully")
            # conn.row_factory = sqlite3.Row

            # cur = conn.cursor()
            # cor = conn.cursor()
            
            # cur.execute('select * from plasma_request where toemail=?',(session['username'],))
            # cor.execute('select * from plasma_request where toemail=?',(session['username'],))
            # row = cor.fetchone();
            # rows = cur.fetchall();
            if row:
                return render_template('notifications.html')
            else:
                return render_template('notifications.html',rows=notify)



@app.route('/changestatus/<emailID>')
def changestatus(emailID):
    id=emailID[:-1]
    status=emailID[-1]
    print(id,status)
    # sql = "select * from plasma_request where fromemail='" + email +"' and toemail='" + session['username'] + "'"
    sql = "select * from plasma_request where id=" + str(id)
    print(sql)
    stmt = ibm_db.exec_immediate(conn,sql)
    row = ibm_db.fetch_both(stmt)
    print(row)
    try:
        if(row['STATUS'] == None or row['STATUS'] == 'PENDING'):
            if(status == 'A'):
                print('A')
                # sql = "update plasma_request set status='Accepted' where fromemail='" + email +"' and toemail='" + session['username'] + "'"
                sql = "update plasma_request set status='Accepted' where id=" + str(id)
                print(sql)
                stmt = ibm_db.exec_immediate(conn,sql)
            else:
                print('R')
                # sql = "update plasma_request set status='Rejected' where fromemail='" + email +"' and toemail='" + session['username'] + "'"
                sql = "update plasma_request set status='Rejected' where id=" + str(id)
                print(sql)
                stmt = ibm_db.exec_immediate(conn,sql)
    except Exception as e:
        print(e)
        return render_template("notifications.html")
    return redirect(url_for('notifications'))






@app.route('/deleteuser/<useremail>',methods=('GET', 'POST'))
def deleteuser(useremail):
    if request.method == 'GET':
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute('delete from users Where email=?',(useremail,))
        flash('deleted user:'+useremail)
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))


@app.route('/deletebloodentry/<id>',methods=('GET', 'POST'))
def deletebloodentry(id):
    if request.method == 'GET':
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute('delete from blood Where id=?',(id,))
        flash('deleted entry:'+id)
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))

@app.route('/deleteme/<useremail>',methods=('GET', 'POST'))
def deleteme(useremail):
    if request.method == 'GET':
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute('delete from users Where email=?',(useremail,))
        flash('deleted user:'+useremail)
        conn.commit()
        conn.close()
        session.pop('username', None)
        session.pop('logged_in',None)
        return redirect(url_for('index'))

@app.route('/deletenoti/<id>',methods=('GET', 'POST'))
def deletenoti(id):
    if request.method == 'GET':
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute('delete from request Where id=?',(id,))
        flash('deleted notification:'+id)
        conn.commit()
        conn.close()
        return redirect(url_for('notifications'))



if __name__ == '__main__':
    app.run(debug=True)
