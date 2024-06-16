from flask import Flask, render_template,request,flash,redirect,url_for,session
import os
import cv2
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re



UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'xyzsdfg'

mysql=MySQL(app)

    

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processImage(filename, operation):
    print(f"the operation is {operation} and filename is {filename}")
    img = cv2.imread(f"uploads/{filename}")
    match operation:
        case "cgray":
            imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            newFilename = (f"static/{filename}")
            cv2.imwrite(newFilename, imgProcessed)
            return newFilename
        case "cwebp": 
            newFilename = f"static/{filename.split('.')[0]}.webp"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cjpg": 
            newFilename = f"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cpng": 
            newFilename = f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(newFilename, img)
            return newFilename
    pass


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/Home")
def Home():
    return render_template("home.html")

@app.route("/About")
def about():
    return render_template("about.html")

@app.route("/contact")
def contactus():
    return render_template("contact_us.html")

@app.route("/Doc")
def documentation():
    return render_template("documentation.html")

@app.route("/download")
def down():
    return render_template("down.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/edit",methods=["GET","POST"])
def edit():
    if request.method=="POST":
        operation = request.form.get("operation")
         # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "There is an error"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "No such File found"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = processImage(filename, operation)
            flash(f"Your image has been processed and is available <a href='/{new}' target='_blank'>here</a>")
            return render_template('index.html')
    return render_template('index.html')
app.run(debug=True, port=5001)