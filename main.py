# QuickPage Project GPL-3.0 LICENSE
# login.py creator: Edward Hsing
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, current_user, login_required, UserMixin, login_user, logout_user
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import os
import subprocess
import socket

# for sqlite
import sqlite3
conn = sqlite3.connect('quickpage.db')
cs = conn.cursor()
try:
    cs.execute('''CREATE TABLE user
        (name varchar(20),
            password varchar(20),
            pagenumber varchar(20) PRIMARY KEY
            );''')
except:
    pass
cs.close()
conn.close()

def filelist(username):
    path = f'./users/{username}'
    files = str(os.listdir(path))
    listfiles = files.replace('[', '').replace(']', '').replace("'", '')
    return listfiles

def userfiles(username):
    path = f'./users/{username}'
    files = os.listdir(path)
    num_png = len(files)
    return num_png

def checkuser(username, password):
        conn = sqlite3.connect('quickpage.db')
        cs = conn.cursor()
        cursor = cs.execute(f"select * from user where name='{username}';")
        
        for row in cursor:
            getusername = row[0]
            getpassword = row[1]
        cs.close()
        conn.close()
        try:
            if getusername == username:
                if check_password_hash(getpassword, password):
                    return True
            else:
               return None
        except:
            return None
class User(UserMixin):
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return "1"

# end flyos user init
app = Flask(__name__)

app.secret_key = os.urandom(24) # protect flyos
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    user = User()
    return user
@app.route('/')
@login_required
def redirectmain():
    redirect(url_for('panelmain'))
@app.route('/dashboard/index')
@login_required
def panelmain():
    return render_template('./main.html',username=user_name,pagelist=filelist(user_name))
@app.route('/login', methods=['GET', 'POST'])
def login():
    global user_name
    if request.method == 'POST':
        user_name = request.form.get('username')
        password = request.form.get('password')
        user = User()
        if user_name == '':
            return render_template('./info.html',info='Incorrect username or password')
        if password == '':
            return render_template('./info.html',info='Incorrect username or password')
        if checkuser(user_name, password):
            login_user(user)
            return redirect(url_for('panelmain'))
        return render_template('./info.html',info='Incorrect username or password')
        

    return render_template('./login.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User()
        if username == '':
            return render_template('./info.html',info='Please enter a username')
        if password == '':
            return render_template('./info.html',info='Please enter a password')
        passwordhash = generate_password_hash(password)
        try:
            os.mkdir(f'./users/{username}')
        except:
            return render_template('./info.html',info='User Already exits')
        conn = sqlite3.connect('quickpage.db')
        cs = conn.cursor()
        cs.execute(f"INSERT INTO user (name, password, pagenumber) VALUES ('{username}', '{passwordhash}', 10)")
        conn.commit()
        cs.close()
        return 'registration success'
    if request.method == 'GET':
        return render_template('./register.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
@app.route("/dashboard/create", methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        try:
            os.mkdir('./users/' + user_name)
        except:
            pass
        getfilename = request.form['filename']
        getcode = request.form['code']
        with open(f'./users/{user_name}/{getfilename}','w') as f:
            f.write(getcode)
        return f'''

<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="/static/css/bootstrap.min.css" rel="stylesheet">
    <meta charset="utf-8">
      <nav class="navbar navbar-light bg-light">
        <div class="container-fluid">
          <span class="navbar-brand mb-0 h1">Created successfully!</span>
        </div>
      </nav>
Your URL: http://quickpage.digitalplat.org/pages/{user_name}/?filename={getfilename}<br>
Remove footer URL:http://quickpage.digitalplat.org/pages/{user_name}/?filename={getfilename}&option=removefooter<br>
Diable Template URL(Including disabling bootstrap): http://quickpage.digitalplat.org/pages/{user_name}/?filename={getfilename}&option=disabletemplate
</body>
</html>
'''
    if request.method == 'GET':
        conn = sqlite3.connect('quickpage.db')
        cs = conn.cursor()
        cursor = cs.execute(f"select * from user where name='{user_name}';")
        for row in cursor:
            getusername = row[0]
            getpassword = row[1]
            getpagenumber = row[2]
            
        if getpagenumber <= str(userfiles(user_name)):
            conn.commit()
            cs.close()
            conn.close()
            return render_template('./info.html',info='Sorry, you can only create up to five pages, please delete some pages in "Delete Page"')
        return render_template('./create.html',username=user_name)
@app.route('/dashboard/edit/', methods=['GET', 'POST'])
@login_required
def editpage():
    if request.method == 'GET':
        global getcodefilename
        getcodefilename = request.args.get('filename')
        f = open(f'./users/{user_name}/{getcodefilename}')
        readcodecontent = f.read()
        return render_template('./edit.html', codecontent=readcodecontent)
    if request.method == 'POST':
        getcode = request.form['code']
        f = open(f'./users/{user_name}/{getcodefilename}',"w")
        f.write(getcode)
        return render_template('./info.html',info='Successfully saved')
        

@app.route('/dashboard/deletepage', methods=['GET', 'POST'])
@login_required
def deletepage():
    if request.method == 'GET':
        return render_template('./delete.html', pagelist=filelist(user_name))
    if request.method == 'POST':
        getfilename = request.form['filename']
        os.remove(f'./users/{user_name}/{getfilename}')
        return render_template('./info.html',info='Success!')

quickpagehead = """

<!doctype html>
<html>
<head>
<body>
    <meta charset="utf-8">
    
    <style>
        body {
            padding-bottom: 50px;
        }
 
        .footer {
            position: fixed;
            left: 0px;
            bottom: 0px;
            width: 100%;
            height: 50px;
            background-color: #eee;
            z-index: 9999;
        }
    </style>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="/static/css/bootstrap.min.css" rel="stylesheet">

        <meta charset="utf-8">
        <title>QuickPage</title>
    </head>
<div id="page-container">
   <div id="content-wrap">
"""
poweredby = """
<footer class="bg-light text-center text-lg-start">
  <div class="footer text-center text-dark" style="background-color: rgba(0, 0, 0, 0.2);">

    <a class="footer text-dark" href="https://www.digitalplat.org/">Powered By: DigitalPlat QuickPage</a>
  </div>
</footer>
"""
quickpagefoot = """
</div>
<script src="/static/js/bootstrap.bundle.js"></script>
</body>
</html>
"""
@app.route("/pages/<username>/")
def viewpages(username):
    getfilename = request.args.get('filename')
    getoptions = request.args.get('option')
    f = open(f'./users/{username}/{getfilename}')
    content = f.read()
    if getoptions == 'removefooter':
        return quickpagehead + content + quickpagefoot
    elif getoptions == 'disabletemplate':
        return content
    return quickpagehead + content + quickpagefoot + poweredby
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
