from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import os
from tempfile import NamedTemporaryFile
import subprocess
from ptpython.translate import translate

app = Flask(__name__)
CORS(app, resources={r"/api2/*": {"origins": "*"}})

user_inputs = []  # Lista para armazenar as entradas do usuário
input_index = 0  # Índice para controlar qual entrada solicitar

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
    global user_inputs, input_index
    data = request.json
    code = data.get('code', '')
    translated_code = translate(code)

    with NamedTemporaryFile(mode='w+', suffix='.py', delete=False) as temp_file:
        temp_file.write(translated_code)
        temp_file.flush()
        temp_filename = temp_file.name

    output, prompts = execute_code(temp_filename)
    os.remove(temp_filename)

    # Se houver prompts, envie-os para o cliente
    if prompts:
        input_index = 0
        user_inputs = []
        return jsonify({'output': output, 'prompts': prompts})
    
    return jsonify({'output': output})

def execute_code(temp_filename):
    global input_index
    prompts = []

    def mock_input(prompt):
        nonlocal prompts
        prompts.append(prompt)
        if input_index < len(user_inputs):
            user_input = user_inputs[input_index]
            input_index += 1
            return user_input
        return ''  # Retornar string vazia se não houver mais entradas

    # Redefinir a função input para coletar prompts
    original_input = __builtins__.input
    __builtins__.input = mock_input

    process = subprocess.Popen(
        ['python3.10', '-u', temp_filename],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    output, error = process.communicate()
    output += error

    # Restaurar a função input original
    __builtins__.input = original_input

    return output, prompts

@app.route('/submit_input', methods=['POST'])
def submit_input():
    global input_index
    data = request.json
    user_input = data.get('input', '')
    user_inputs.append(user_input)
    input_index += 1
    return jsonify({'status': 'input received'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6000)
