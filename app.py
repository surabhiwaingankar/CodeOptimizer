from flask import Flask, request, jsonify, send_file
import os
from main import optimize  # Assuming optimize function is defined in main module
import time

app = Flask(__name__)

UPLOAD_FOLDER = 'code'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['CODE_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and file.filename.endswith('.py'):
        file_path = os.path.join(app.config['CODE_FOLDER'], file.filename)
        file.save(file_path)
        
        # Read file content
        with open(file_path, 'r') as f:
            file_content = f.read()
        
        # Call optimize function asynchronously
        optimize(file_content)
        
        # Wait for optimized.py to be created
        wait_time = 0
        max_wait_time = 10  # Maximum time to wait in seconds
        new_file_path = "code/optimized.py"
        
        while not os.path.exists(new_file_path) and wait_time < max_wait_time:
            time.sleep(1)
            wait_time += 1
        
        if os.path.exists(new_file_path):
            # Send file as attachment
            return send_file(new_file_path, as_attachment=True), 200
        else:
            return jsonify({"error": "Failed to optimize file"}), 500
        
    else:
        return jsonify({"error": "Invalid file type. Only .py files are allowed."}), 400

if __name__ == '__main__':
    app.run(debug=False)
