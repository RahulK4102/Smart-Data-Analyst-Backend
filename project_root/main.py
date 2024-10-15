import os
from flask import Flask, request, redirect, url_for, render_template, flash, jsonify

app = Flask(__name__)

# Configure the upload folder path to 'project_root/data'
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))  # This gives the project_root directory
UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, 'data')         # Create the path for 'data' directory
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions (optional)
ALLOWED_EXTENSIONS = {'csv', 'xls', 'xlsx'}

# Check if the file has a valid extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for the home page with file upload form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle file upload from form submission
@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the request contains a file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']

    # If no file is selected
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    # If the file is valid and has the correct extension
    if file and allowed_file(file.filename):
        filename = file.filename
        # Save the file to the 'data' directory inside project_root
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        flash('File successfully uploaded to data folder')
        return redirect(url_for('index'))
    else:
        flash('Invalid file type')
        return redirect(request.url)

# API endpoint to handle file upload programmatically (e.g., via Postman or another app)
@app.route('/api/upload', methods=['POST'])
def api_upload_file():
    # Check if the request contains a file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']

    # If no file is selected
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # If the file is valid and has the correct extension
    if file and allowed_file(file.filename):
        filename = file.filename
        # Save the file to the 'data' directory inside project_root
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return jsonify({'message': f'File {filename} successfully uploaded to data folder'}), 200
    else:
        return jsonify({'error': 'Invalid file type'}), 400

# Main entry point
if __name__ == "__main__":
    # Ensure the 'data' folder exists, create it if not
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.secret_key = 'supersecretkey'
    # Remove app.run() for production deployment to Vercel
    app.run() 
