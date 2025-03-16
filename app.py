import os
from datetime import datetime
from flask import Flask, request, redirect, url_for, render_template, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'supersecretkey'
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

# Tạo thư mục upload nếu chưa tồn tại
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/')
def index():
    # Lấy danh sách các tệp đã tải lên
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    message = request.args.get('message')
    return render_template('index.html', files=files, message=message)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('index'))
    if file:
        # Lấy tên file an toàn
        filename = secure_filename(file.filename)

        # Kiểm tra phần mở rộng của tệp
        ext = os.path.splitext(filename)[1].lower()
        timestamp = datetime.now().strftime("%Y-%m-%d_%Hh%Mp%Ss")

        # Đặt tên file mới dựa trên loại tệp
        if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
            new_filename = f"Image_{timestamp}{ext}"
        elif ext in ['.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx', '.csv', '.ppt', '.pptx']:
            new_filename = f"{ext[1:].capitalize()}_{timestamp}{ext}"
        else:
            new_filename = f"Unknown_File_{timestamp}{ext}"

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)

        # Lưu tệp với tên mới
        file.save(file_path)
        return redirect(url_for('index', message='File uploaded successfully'))


@app.route('/delete', methods=['POST'])
def delete_file():
    filename = request.form['filename']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    return redirect(url_for('index', message='File deleted successfully'))


@app.errorhandler(413)
def request_entity_too_large(error):
    return redirect(url_for('index', message='File is too large.'))


if __name__ == '__main__':
    app.run(debug=True)
