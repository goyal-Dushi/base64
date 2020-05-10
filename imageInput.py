import base64

from flask import Flask, url_for, redirect, request, flash, render_template
import os
from werkzeug.utils import secure_filename
from pdf2image import convert_from_path

app = Flask(__name__)

# UPLOADS_PATH = join(dirname(realpath(__file__)), 'static/uploads/')
# UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = './static/uploads/'


# checking for the file extension name
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# the content to be displayed
@app.route('/')
def formDisplay():
    return render_template('get_image.html')


def checkFile(file_to_check):
    encoded_string = " "
    imageFile = ['.jpg', '.jpeg', '.png']
    if file_to_check.endswith(".pdf"):
        with open('static/uploads/'+file_to_check, "rb") as pdf_file:
            encoded_string = base64.b64encode(pdf_file.read())
    elif file_to_check.endswith(tuple(imageFile)):
        with open('static/uploads/'+file_to_check, "rb") as img_file:
            encoded_string = base64.b64encode(img_file.read()).decode('utf-8')
    return encoded_string


# to check whether the file is uploaded by the user or not
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        # if correct filename is speicifed by the user
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # basedir = os.path.abspath(os.path.dirname(__file__))
            # else:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            base64_string = checkFile(filename)
            if filename.endswith(".pdf"):
                images = convert_from_path(filename.getpage[0])
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], images))
                # os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                filename = images
            return render_template('output.html', filename=filename, string=base64_string)


# sending the image filename to the src of the image
@app.route('/output/<filename>')
def uploaded_file(filename):
    return redirect(url_for('static', filename='uploads/' + filename))


if __name__ == "__main__":
    app.run(debug=True)
