document.addEventListener('DOMContentLoaded', (event) => {
    const editor = CodeMirror.fromTextArea(document.getElementById('code-editor'), {
        mode: 'python',
        theme: 'monokai',
        lineNumbers: true,
        autoCloseBrackets: true
    });

    const translatedEditor = CodeMirror.fromTextArea(document.getElementById('translated-code-editor'), {
        mode: 'python',
        theme: 'monokai',
        lineNumbers: true,
        readOnly: true
    });

    document.getElementById('openFile').addEventListener('click', () => {
        document.getElementById('fileInput').click();
    });

    document.getElementById('fileInput').addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                editor.setValue(e.target.result);
            };
            reader.readAsText(file);
        }
    });

    document.getElementById('newFile').addEventListener('click', () => {
        editor.setValue('');
    });

    document.getElementById('saveFile').addEventListener('click', () => {
        const blob = new Blob([editor.getValue()], { type: 'text/plain;charset=utf-8' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'code.ptpy';
        link.click();
    });

    document.getElementById('closeFile').addEventListener('click', () => {
        editor.setValue('');
        translatedEditor.setValue('');
    });

    document.getElementById('runCode').addEventListener('click', () => {
        const code = editor.getValue();
        runCode(code);
    });

    document.getElementById('debugCode').addEventListener('click', () => {
        alert('Funcionalidade de debug ainda não implementada.');
    });

    editor.on('change', () => {
        const code = editor.getValue();
        translateCode(code);
    });

    function translateCode(code) {
        fetch('https://bosonshiggs.com.br/api2/translate_code', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code }),
        })
        .then(response => {
            console.log(`Translate response status: ${response.status}`);
            return response.json();
        })
        .then(data => {
            console.log('Translated data received:', data);
            const translatedCode = data.translated_code || '';
            translatedEditor.setValue(translatedCode);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    function runCode(code) {
        fetch('https://bosonshiggs.com.br/api2/run_code', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code }),
        })
        .then(response => {
            console.log(`Run response status: ${response.status}`);
            console.log(`Run response: ${response}`);
            return response.json();
        })
        .then(data => {
            console.log('Run output received:', data);
            if (data.prompts && data.prompts.length > 0) {
                handlePrompts(data.prompts, code);
            } else {
                displayOutput(data.output);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    function handlePrompts(prompts, code) {
        const inputs = {};
        let promises = prompts.map(prompt => {
            return new Promise((resolve) => {
                let userInput = promptUserInput(prompt);
                inputs[prompt] = userInput;
                resolve();
            });
        });

        Promise.all(promises).then(() => {
            runCodeWithInputs(code, inputs);
        });
    }

    function runCodeWithInputs(code, inputs) {
        fetch('https://bosonshiggs.com.br/api2/run_code', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code, inputs }),
        })
        .then(response => {
            console.log(`Run response with inputs status: ${response.status}`);
            return response.json();
        })
        .then(data => {
            console.log('Run output with inputs received:', data);
            displayOutput(data.output);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    function promptUserInput(prompt) {
        return window.prompt(prompt);
    }

    function displayOutput(output) {
        const terminalOutput = document.getElementById('terminal-output');
        terminalOutput.textContent += output + '\n';
        terminalOutput.scrollTop = terminalOutput.scrollHeight;
    }

    const terminalInput = document.getElementById('terminal-input');
    const terminalOutput = document.getElementById('terminal-output');

    terminalInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            const userInput = terminalInput.value;
            terminalInput.value = '';
            terminalOutput.textContent += `> ${userInput}\n`;

            runCode(userInput);
        }
    });
});
