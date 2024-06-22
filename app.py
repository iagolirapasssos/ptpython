from flask import Flask, request, jsonify
import os
from tempfile import NamedTemporaryFile
import subprocess
from ptpython.translate import translate

app = Flask(__name__)

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

    try:
        result = subprocess.run(['python3.10', temp_filename], capture_output=True, text=True, check=True)
        output = result.stdout
        error = result.stderr
    except subprocess.CalledProcessError as e:
        output = ''
        error = str(e) + '\n' + e.stderr
    finally:
        os.remove(temp_filename)

    return jsonify({'output': output, 'error': error})

if __name__ == '__main__':
    app.run(debug=True)

