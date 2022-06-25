# Nama Kelompok 
# Rizky Nafianto 19090098
# Aida Nur Syabani 19090011

from distutils.log import debug
from flask import Flask, render_template, request, redirect, url_for, session, request, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

import jwt
import os
import datetime

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pythonlogin'

# Intialize MySQL
mysql = MySQL(app)


# http://localhost:5000/pythonlogin/ - the following will be our login page, which will use both GET and POST requests
@app.route('/loginadmin', methods=['GET', 'POST'])
def loginadmin():
    # Output message if something goes wrong...
    msg = ''
        # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
                # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
                # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            token =jwt.encode(
                {
                    "username":username,
                    "exp":datetime.datetime.now() + datetime.timedelta(minutes=120)
                }, app.config['SECRET_KEY'], algorithm="HS256"
            )
            print(token)
            # Redirect to home page
            return redirect(url_for('tambah'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('login copy.html', msg=msg)

@app.route("/api/v1/Api", methods=["POST"])
def tambah():
  encoded = request.json['token']
  print(encoded)
  json = jwt.decode(encoded, app.secret_key, algorithms="HS256")
  username = json['username']
  return jsonify({'username': username}), 200

if __name__ == '__main__':
   app.run(debug = True, port=5000)

# http://localhost:5000/python/logout - this will be the logout page
@app.route('/logoutuser')
def logoutuser():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('loginuser'))

@app.route('/logoutadmin')
def logoutadmin():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('loginadmin'))

# http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
                # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO user VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


@app.route('/')
# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
@app.route('/loginuser', methods=['GET', 'POST'])
def loginuser():
    # Output message if something goes wrong...
    msg = ''
        # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
                # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
                # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('index'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg)


@app.route('/index')
def index():
    # Check if user is loggedin
    if 'loggedin' in session:
#         # User is loggedin show them the home page
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute("SELECT * FROM tamu ORDER BY id desc")
#         datatamu = cursor.fetchall()
#         hari_ini = tamuhari()
#         minggu_ini = tamuminggu()
#         bulan_ini = tamubulan()
#         total_tamu = totaltamu()
        return render_template('index.html')
    # User is not loggedin redirect to login page
    return redirect(url_for('loginuser'))

@app.route('/admin')
def dashboard():
    # Check if user is loggedin
    if 'loggedin' in session:
#         # User is loggedin show them the home page
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute("SELECT * FROM tamu ORDER BY id desc")
#         datatamu = cursor.fetchall()
#         hari_ini = tamuhari()
#         minggu_ini = tamuminggu()
#         bulan_ini = tamubulan()
#         total_tamu = totaltamu()
        return render_template('dashboard.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('loginadmin'))


if __name__ == '__main__' :
    app.run(debug=True)

