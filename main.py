
from flask import Flask, request, jsonify, flash, redirect, send_from_directory
from page_rotate import rotate_pages, MEDIA_ROOT
import os

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input_files')
ALLOWED_EXTENSIONS = {'pdf', }

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/rotate', methods=['POST'])
def rotate():
    data = request.form
    if 'file' not in request.files:
        flash('No file part')
        return jsonify({'error': 'No file part'}), 400
    angle = data['angle']
    pages = data['pages'].split(',')
    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        file_out_name = rotate_pages(os.path.join(UPLOAD_FOLDER, file.filename), angle, pages)

        return jsonify({'filename': file_out_name})

    return jsonify({'error': 'Something went wrong'}), 400

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(MEDIA_ROOT, filename)


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.debug = True
    app.run()