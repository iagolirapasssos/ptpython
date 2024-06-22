from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os
from tempfile import NamedTemporaryFile
import subprocess
from ptpython.translate import translate
import asyncio
import threading

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

@socketio.on('run_code')
def handle_run_code(json):
    code = json.get('code', '')
    translated_code = translate(code)
    
    with NamedTemporaryFile(mode='w+', suffix='.py', delete=False) as temp_file:
        temp_file.write(translated_code)
        temp_file.flush()
        temp_filename = temp_file.name

    thread = threading.Thread(target=execute_code, args=(temp_filename,))
    thread.start()

def execute_code(temp_filename):
    asyncio.run(async_run_code(temp_filename))

async def async_run_code(temp_filename):
    import pty
    import select

    master_fd, slave_fd = pty.openpty()
    process = subprocess.Popen(['python3.10', '-u', temp_filename], stdin=slave_fd, stdout=slave_fd, stderr=slave_fd, text=True)

    socketio.start_background_task(target=read_output, master_fd=master_fd)

    while process.poll() is None:
        await asyncio.sleep(1)

    os.remove(temp_filename)

def read_output(master_fd):
    while True:
        ready, _, _ = select.select([master_fd], [], [])
        if master_fd in ready:
            output = os.read(master_fd, 1024).decode()
            socketio.emit('output', {'output': output})

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=6000)
