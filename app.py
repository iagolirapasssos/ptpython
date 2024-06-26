from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
from tempfile import NamedTemporaryFile
import subprocess
from ptpython.translate import translate
import redis

app = Flask(__name__)
CORS(app, resources={r"/api2/*": {"origins": "*"}})

# Configuração do Redis para Flask-Limiter
redis_client = redis.Redis(host='localhost', port=6379, db=0)
limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri="redis://localhost:6379"
)

@app.before_request
def handle_options_requests():
    if request.method == 'OPTIONS':
        return Response(status=200)

@app.route('/')
def index():
    return 'PtPython IDE API'

@app.route('/translate_code', methods=['POST'])
@limiter.limit("5 per minute")  # Exemplo de limite de taxa
def translate_code():
    data = request.json
    code = data.get('code', '')
    translated_code = translate(code)
    return jsonify({'translated_code': translated_code})

@app.route('/run_code', methods=['POST'])
@limiter.limit("5 per minute")  # Exemplo de limite de taxa
def run_code():
    data = request.json
    code = data.get('code', '')
    user_inputs = data.get('inputs', {})

    translated_code = translate(code)
    
    if contains_dangerous_commands(translated_code):
        return jsonify({'error': 'Código contém comandos potencialmente perigosos.'}), 400
    
    input_prompts = extract_input_prompts(translated_code)

    with NamedTemporaryFile(mode='w+', suffix='.py', delete=False) as temp_file:
        temp_file.write(translated_code)
        temp_file.flush()
        temp_filename = temp_file.name

    output, error = execute_code(temp_filename, user_inputs)
    os.remove(temp_filename)

    result_output = output.strip() + '\n' + error.strip()
    
    return jsonify({'output': result_output, 'prompts': input_prompts})

def inputs_only(user_inputs):
    out = ''
    cont = 0
    for a in user_inputs.values():
        out += a + '\n'
        cont += 1
    return out, cont

def extract_input_prompts(code):
    import re
    pattern = r'input\("([^"]+)"\)'
    return re.findall(pattern, code)

def contains_dangerous_commands(code):
    dangerous_commands = ['import os', 'import subprocess', 'open(', 'eval(', 'exec(']
    return any(cmd in code for cmd in dangerous_commands)

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

    # Coleta os prompts de entrada do código
    input_prompts = extract_input_prompts(open(temp_filename).read())
    input_data = ''.join([get_input(prompt) for prompt in input_prompts])

    output, error = process.communicate(input=input_data)

    # Remove os prompts de entrada da saída
    filtered_output = filter_output(output, input_prompts)

    return filtered_output, error

def filter_output(output, prompts):
    for prompt in prompts:
        output = output.replace(prompt, '')
    return output

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6000)
