from distutils.log import debug
from email import message
from flask import Flask,render_template,request,redirect,url_for
import ibm_db
conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=98538591-7217-4024-b027-8baa776ffad1.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=30875;PROTOCOL=TCPIP;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=qwt20119;PWD=K1QvT2KCZy9syqan;", "", "")
app=Flask(__name__)

@app.route("/")
def homepage():
    return render_template("index.html")
@app.route("/register", methods =["GET", "POST"])
def register():
    if request.method == "POST":
        sql="select * from user where email='"+request.form.get("email")+"' or username='"+request.form.get("username")+"'";
        stmt = ibm_db.exec_immediate(conn, sql)
        result = ibm_db.fetch_both(stmt)
        if result:
            print("User Already Exists")
            return render_template("index.html",message="User Already Exists")
        email = request.form.get("email")
        username = request.form.get("username")
        rollno = request.form.get("rollno")
        passw=request.form.get("psw")
        sql="insert into user values('"+email+"','"+username+"',"+rollno+",'"+passw+"')";
        stmt = ibm_db.exec_immediate(conn, sql)
        if(ibm_db.num_rows(stmt)==1):
            return render_template("created.html")
        else:
            return render_template("index.html",message="Error While Creating User")
    return render_template("index.html");

@app.route("/login", methods =["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        passw=request.form.get("psw")
        sql="select * from user where username='"+request.form.get("username")+"'";
        stmt = ibm_db.exec_immediate(conn, sql)
        result = ibm_db.fetch_both(stmt)
        if not result:
            print("User Not Exists")
            return render_template("login.html",message="Username Not Found")
        sql="select * from users where username='"+request.form.get("username")+"' and password='"+passw+"'";
        stmt = ibm_db.exec_immediate(conn, sql)
        result = ibm_db.fetch_both(stmt)
        if not result:
            print("Wrong Password")
            return render_template("login.html",message="Wrong Password")
        # return render_template("login.html",message="Logging in")
        return redirect(url_for('dashboard',name = username))
    return render_template("login.html")
@app.route('/dashboard/<name>')
def dashboard(name):
    return render_template("dashboard.html",name=name)
if __name__=="__main__":
    if conn:
        print("Database Connected Successfully")
        app.run(debug=True)
