from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from tempfile import NamedTemporaryFile
import subprocess
from ptpython.translate import translate
import asyncio

app = Flask(__name__)
CORS(app, resources={r"/api2/*": {"origins": "*"}})

@app.route('/')
def index():
    return 'PtPython IDE API'

@app.route('/api2/translate_code', methods=['POST'])
def translate_code():
    data = request.json
    code = data.get('code', '')
    translated_code = translate(code)
    return jsonify({'translated_code': translated_code})

@app.route('/api2/run_code', methods=['POST'])
def run_code():
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
