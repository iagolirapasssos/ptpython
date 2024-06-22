from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import os
from tempfile import NamedTemporaryFile
import subprocess
from ptpython.translate import translate

app = Flask(__name__)
CORS(app, resources={r"/api2/*": {"origins": "*"}})

@app.before_request
def handle_options_requests():
    if request.method == 'OPTIONS':
        return Response(status=200)

@app.route('/')
def index():
    return 'PtPython IDE API'

@app.route('/translate_code', methods=['POST'])
def translate_code():
    data = request.json
    code = data.get('code', '')
    translated_code = translate(code)
    return jsonify({'translated_code': translated_code})

@app.route('/run_code', methods=['POST'])
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
    
    # Simule a entrada do usuário aqui
    user_input = 'simulated input\n'
    output, error = process.communicate(input=user_input)
    return output + error

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6000)
