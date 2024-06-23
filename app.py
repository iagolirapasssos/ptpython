from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
from tempfile import NamedTemporaryFile
import subprocess
from ptpython.translate import translate

app = Flask(__name__)
CORS(app, resources={r"/api2/*": {"origins": "*"}})

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

@app.before_request
def handle_options_requests():
    if request.method == 'OPTIONS':
        return Response(status=200)

@app.route('/')
@limiter.exempt
def index():
    return 'PtPython IDE API'

@app.route('/translate_code', methods=['POST'])
@limiter.limit("10 per minute")
def translate_code():
    data = request.json
    code = data.get('code', '')
    translated_code = translate(code)
    return jsonify({'translated_code': translated_code})

@app.route('/run_code', methods=['POST'])
@limiter.limit("10 per minute")
def run_code():
    data = request.json
    code = data.get('code', '')
    user_inputs = data.get('inputs', {})

    translated_code = translate(code)
    input_prompts = extract_input_prompts(translated_code)

    with NamedTemporaryFile(mode='w+', suffix='.py', delete=False) as temp_file:
        temp_file.write(translated_code)
        temp_file.flush()
        temp_filename = temp_file.name

    output = execute_code(temp_filename, user_inputs)
    os.remove(temp_filename)
    return jsonify({'output': output, 'prompts': input_prompts})

def extract_input_prompts(code):
    import re
    pattern = r'input\("([^"]+)"\)'
    return re.findall(pattern, code)

def execute_code(temp_filename, user_inputs):
    process = subprocess.Popen(
        ['python3.10', '-u', temp_filename],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    def get_input(prompt):
        return user_inputs.get(prompt, '') + '\n'

    inputs = [get_input(prompt) for prompt in extract_input_prompts(open(temp_filename).read())]
    input_data = ''.join(inputs)

    output, error = process.communicate(input=input_data)
    return (output + error).strip()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6000)
