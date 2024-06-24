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
        document.getElementById('code-output').textContent = '';
    });

    document.getElementById('runCode').addEventListener('click', () => {
        const code = editor.getValue();
        runCode(code);
    });

    document.getElementById('debugCode').addEventListener('click', () => {
        const code = editor.getValue();
        debugCode(code);
    });

    document.getElementById('translateCode').addEventListener('click', () => {
        const code = editor.getValue();
        translateCode(code);
    });

    document.getElementById('shortcuts').addEventListener('click', () => {
        alert(`Atalhos:

        Abrir: Ctrl+O
        Novo: Ctrl+N
        Salvar: Ctrl+S
        Fechar: Ctrl+W
        Executar: Ctrl+E
        Debugar: Ctrl+D
        Traduzir: Ctrl+T
        Selecionar Coluna: Ctrl+Shift+BotãoDireitoDoMouse`);
    });

    document.getElementById('credits').addEventListener('click', () => {
        alert('Créditos:\n\nDesenvolvido por Francisco Iago Lira Passos.');
    });

    editor.on('change', () => {
        // Código comentado para evitar tradução automática
        // const code = editor.getValue();
        // translateCode(code);
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
            if (response.status === 429) {
                alert('Limite de taxa atingido. Por favor, aguarde antes de tentar novamente.');
            }
            return response.json();
        })
        .then(data => {
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
            if (response.status === 429) {
                alert('Limite de taxa atingido. Por favor, aguarde antes de tentar novamente.');
            }
            return response.json();
        })
        .then(data => {
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

    function debugCode(code) {
        fetch('https://bosonshiggs.com.br/api2/run_code', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code }),
        })
        .then(response => {
            if (response.status === 429) {
                alert('Limite de taxa atingido. Por favor, aguarde antes de tentar novamente.');
            }
            return response.json();
        })
        .then(data => {
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

    function acessarValor(objeto) {
      for (let chave in objeto) {
        return objeto[chave];
      }
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
            if (response.status === 429) {
                alert('Limite de taxa atingido. Por favor, aguarde antes de tentar novamente.');
            }
            return response.json();
        })
        .then(data => {
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

    let isMultiColumnSelecting = false;
    let startPos = null;

    editor.getWrapperElement().addEventListener('mousedown', (event) => {
        if (event.button === 0 && event.ctrlKey && event.shiftKey) {
            event.preventDefault();
            if (!isMultiColumnSelecting) {
                isMultiColumnSelecting = true;
                startPos = editor.coordsChar({ left: event.clientX, top: event.clientY });
                editor.setSelection(startPos);
            } else {
                isMultiColumnSelecting = false;
                startPos = null;
            }
        }
    });

    editor.getWrapperElement().addEventListener('mousemove', (event) => {
        if (isMultiColumnSelecting && startPos) {
            const pos = editor.coordsChar({ left: event.clientX, top: event.clientY });
            const selections = [];
            for (let line = startPos.line; line <= pos.line; line++) {
                selections.push({
                    anchor: { line, ch: startPos.ch },
                    head: { line, ch: pos.ch }
                });
            }
            editor.setSelections(selections);
        }
    });

    // Atalhos de teclado
    document.addEventListener('keydown', (event) => {
        if (event.ctrlKey && !event.shiftKey && !event.altKey) {
            switch (event.key) {
                case 'o':
                    event.preventDefault();
                    document.getElementById('openFile').click();
                    break;
                case 'n':
                    event.preventDefault();
                    document.getElementById('newFile').click();
                    break;
                case 's':
                    event.preventDefault();
                    document.getElementById('saveFile').click();
                    break;
                case 'w':
                    event.preventDefault();
                    document.getElementById('closeFile').click();
                    break;
                case 'e':
                    event.preventDefault();
                    document.getElementById('runCode').click();
                    break;
                case 'd':
                    event.preventDefault();
                    document.getElementById('debugCode').click();
                    break;
                case 't':
                    event.preventDefault();
                    document.getElementById('translateCode').click();
                    break;
                default:
                    break;
            }
        }
    });
});
