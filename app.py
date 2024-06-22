from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os
import subprocess
from tempfile import NamedTemporaryFile
from ptpython.translate import translate

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

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

@socketio.on('run_code')
def handle_run_code(json):
    code = json.get('code', '')
    translated_code = translate(code)
    with NamedTemporaryFile(mode='w+', suffix='.py', delete=False) as temp_file:
        temp_file.write(translated_code)
        temp_file.flush()
        temp_filename = temp_file.name

    try:
        process = subprocess.Popen(
            ['python3.10', temp_filename],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                socketio.emit('output', {'output': output.strip()})

        return_code = process.poll()
        if return_code != 0:
            error = process.stderr.read()
            socketio.emit('output', {'output': error.strip()})
    except Exception as e:
        socketio.emit('output', {'output': str(e)})
    finally:
        os.remove(temp_filename)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=6000)
