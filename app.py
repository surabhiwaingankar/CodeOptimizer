from flask import Flask, request, jsonify, send_file, after_this_request
import os
from main import optimize 
from autogen_logs import calculate_costs

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
        
        logging_session_id = optimize(file_content)
        (total_tokens, total_cost), (session_tokens, session_cost) = calculate_costs(logging_session_id)
        
        new_file_path = "code/optimized.py"
        
        if os.path.exists(new_file_path):
            @after_this_request
            def add_headers(response):
                response.headers['logging_session_id'] = logging_session_id
                response.headers['total_tokens'] = str(total_tokens)
                response.headers['total_cost'] = str(total_cost)
                response.headers['session_tokens'] = str(session_tokens)
                response.headers['session_cost'] = str(session_cost)
                return response
            
            response = send_file(new_file_path, as_attachment=True)
            response.status_code = 200
            return response
        else:
            return jsonify({"error": "Failed to optimize file"}), 500
    else:
        return jsonify({"error": "Invalid file type. Only .py files are allowed."}), 400

if __name__ == '__main__':
    app.run(debug=False)
