from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from tempfile import NamedTemporaryFile
import subprocess
from ptpython.translate import translate

app = Flask(__name__)
CORS(app, resources={r"/api2/*": {"origins": "*"}}, supports_credentials=True)

@app.route('/')
def index():
    return 'PtPython IDE API'

@app.route('/api2/translate_code', methods=['POST'])
def translate_code():
    data = request.json
    code = data.get('code', '')
    translated_code = translate(code)
    return jsonify({'translated_code': translated_code})

@app.route('/api2/run_code', methods=['OPTIONS', 'POST'])
def run_code():
    if request.method == 'OPTIONS':
        return build_cors_preflight_response()
    elif request.method == 'POST':
        data = request.json
        code = data.get('code', '')
        translated_code = translate(code)

        with NamedTemporaryFile(mode='w+', suffix='.py', delete=False) as temp_file:
            temp_file.write(translated_code)
            temp_file.flush()
            temp_filename = temp_file.name

        output = execute_code(temp_filename)
        os.remove(temp_filename)
        return jsonify({'output': output})

def build_cors_preflight_response():
    response = jsonify({'status': 'success'})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
    return response

def execute_code(temp_filename):
    process = subprocess.Popen(
        ['python3.10', '-u', temp_filename],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    output, error = process.communicate()
    return output + error

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6000)
