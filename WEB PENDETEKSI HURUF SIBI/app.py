from flask import Flask, render_template, request, redirect, url_for, session, Response, jsonify
# from flask_mysqldb import MySQL
# import MySQLdb.cursors
import re
# from flask_login import current_user
from detection import Video
# from flask_cors import CORS


app = Flask(__name__)

# # Change this to your secret key (can be anything, it's for extra protection)
# app.secret_key = 'your secret key'

# # Enter your database connection details below
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'pendeteksi_tamu'

# # Intialize MySQL
# mysql = MySQL(app)

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")
def gen(detection):
    while True:
        frame=detection.get_frame()
        yield(b'--frame\r\n'
       b'Content-Type:  image/jpeg\r\n\r\n' + frame +
         b'\r\n\r\n')

@app.route('/video')
def video():
    return Response(gen(Video()),
    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/deteksi')
def deteksi():
    return render_template('deteksi.html')



# @app.post("/predict")
# def predict():
#     text = request.get_json().get("message")
#     TODO: check if text is valid
#     response = get_response(text)
#     message = {"answer": response}
#     return jsonify(message)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     # Output message if something goes wrong...
#     msg = ''
#     # Check if "username" and "password" POST requests exist (user submitted form)
#     if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
#         # Create variables for easy access
#         username = request.form['username']
#         password = request.form['password']
#         # Check if account exists using MySQL
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (username, password,))
#         # Fetch one record and return result
#         user = cursor.fetchone()
#         # If account exists in accounts table in out database
#         if user:
#             # Create session data, we can access this data in other routes
#             session['loggedin'] = True
#             session['id'] = user['id']
#             session['username'] = user['username']
#             # Redirect to home page
#             return redirect(url_for('dashboard'))
#         else:
#             # Account doesnt exist or username/password incorrect
#             msg = 'Incorrect username/password!'
#     # Show the login form with message (if any)
#     return render_template('login.html', msg=msg)

# @app.route('/logout')
# def logout():
#     # Remove session data, this will log the user out
#    session.pop('loggedin', None)
#    session.pop('id', None)
#    session.pop('username', None)
#    # Redirect to login page
#    return redirect(url_for('login'))

# @app.route('/admin')
# def dashboard():
#     # Check if user is loggedin
#     if 'loggedin' in session:
#         # User is loggedin show them the home page
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute("SELECT * FROM tamu ORDER BY id desc")
#         datatamu = cursor.fetchall()
#         hari_ini = tamuhari()
#         minggu_ini = tamuminggu()
#         bulan_ini = tamubulan()
#         total_tamu = totaltamu()
#         return render_template('dashboard.html', username=session['username'], datatamu=datatamu, hari_ini=hari_ini, minggu_ini=minggu_ini, bulan_ini=bulan_ini, total_tamu=total_tamu)
#     # User is not loggedin redirect to login page
#     return redirect(url_for('login'))

