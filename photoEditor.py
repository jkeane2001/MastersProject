from flask import Flask, render_template, url_for, redirect, request, session
import sqlite3
import os
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.security import generate_password_hash, check_password_hash
from PIL import Image
import io
import base64

app = Flask(__name__)
app.config['UPLOAD_DIRECTORY'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #16MB
app.config['ALLOWED_EXTENSIONS'] = ['.jpg', '.jpeg', '.png']
app.config['SECRET_KEY'] = 'D!@dOM0r1y@mA'

def photoDatabase():
    conn = sqlite3.connect('photoEditorDB.db')
    c = conn.cursor()

    #Creates users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        userID INTEGER PRIMARY KEY AUTOINCREMENT, 
        username TEXT, 
        password TEXT, 
        name TEXT
    )''')


    #Creates userImages table
    c.execute('''CREATE TABLE IF NOT EXISTS userImages (
        imgID INTEGER PRIMARY KEY AUTOINCREMENT, 
        userID INTEGER NOT NULL,
        image BLOB,
        imgName TEXT,
        FOREIGN KEY (userID) REFERENCES users(userID)
    )''')

    conn.commit()
    conn.close

photoDatabase()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login", methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('photoEditorDB.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        #conn.commit()
        user = cursor.fetchone()
        conn.close()

        if user:
            session['username'] = username
            return redirect(url_for('userDash'))
        else:
            session['error'] = 'Invalid username or password'
            return redirect(url_for('login'))#, error='Invalid username or password')

    error = session.pop('error', None)
    return render_template('login.html', error=error)

@app.route("/signup", methods = ['GET','POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']

        if password != confirmPassword:
            return render_template('signup.html', error='Passwords do not match')

        #hashPass = generate_password_hash(password)

        conn = sqlite3.connect('photoEditorDB.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, name) VALUES (?,?,?)", (username, password, name))
        conn.commit()
        conn.close()
        redirect(url_for('login'))


    return render_template('signup.html')

@app.route("/logout", methods=['GET','POST'])
def logout():
    if request.method == 'POST':
        session.pop('username', None)
        return redirect(url_for('index'))


@app.route("/userDash", methods=['GET','POST'])
def userDash():

    return render_template('userDash.html')

@app.route("/upload", methods = ['POST'])
def uploadImage():

    try:
        username = session.get('username')
        if not username:
            return 'User is not logged in'

        image = request.files['image']
        extension = os.path.splitext(image.filename)[1].lower()

        if image:
            if extension not in app.config['ALLOWED_EXTENSIONS']:
                return 'File that was uploaded is not an image.'

            #image.save(f'uploads/{secure_filename(image.filename)}')
            #image.save(os.path.join('uploads/', secure_filename(image.filename)))
            #imagePath = os.path.join(app.config['UPLOAD_DIRECTORY'], secure_filename(image.filename))
            #image.save(imagePath)
            imgName = request.form['imageName']

            imageData = image.read()

            conn = sqlite3.connect('photoEditorDB.db')
            cursor = conn.cursor()
            cursor.execute("SELECT userID FROM users WHERE username=?", (username,))
            user = cursor.fetchone()
            if user:
                userID = user[0]
                cursor.execute("INSERT INTO userImages (userID, image, imgName) VALUES (?,?,?)", (userID, imageData, imgName))
                conn.commit()
            conn.close()

        return redirect(url_for('userDash'))
    except RequestEntityTooLarge:
        return 'File is larger than the 16MB limit. Please upload a smaller file.'

@app.route("/listImage")
def listImage():
    try:
        username = session.get('username')
        if not username:
            return 'User is not logged in'

        conn = sqlite3.connect('photoEditorDB.db')
        cursor = conn.cursor()
        cursor.execute("SELECT imgID, imgName FROM userImages WHERE userID IN (SELECT userID FROM users WHERE username=?)", (username,))
        images = cursor.fetchall()
        conn.close()

        return render_template('listImage.html', images=images)
    except Exception as e:
        return str(e)

@app.route("/viewImage/<int:imgID>")
def viewImage(imgID):
    try:
        conn = sqlite3.connect('photoEditorDB.db')
        cursor = conn.cursor()
        cursor.execute("SELECT image FROM userImages WHERE imgID=?", (imgID,))
        imageData = cursor.fetchone()[0]
        conn.close()

        if imageData:
            image = Image.open(io.BytesIO(imageData))

            imgByteArray = io.BytesIO()
            image.save(imgByteArray, format=image.format)
            imgByteArray.seek(0)

            base64Img = base64.b64encode(imgByteArray.read()).decode('utf-8')
            return render_template('viewImage.html', base64Img=base64Img, imageFormat=image.format.lower())
        else:
            return 'Image not found'
    except Exception as e:
        return str(e)




#app.run(debug=True)
app.run(debug=True, port=7567)