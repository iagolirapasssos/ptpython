document.addEventListener('DOMContentLoaded', (event) => {
    const editor = CodeMirror.fromTextArea(document.getElementById('code-editor'), {
        mode: 'python',
        theme: 'monokai',
        lineNumbers: true,
        autoCloseBrackets: true
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
        document.getElementById('code-output').textContent = '';
    });

    document.getElementById('runCode').addEventListener('click', () => {
        const code = editor.getValue();
        fetch('https://bosonshiggs.com.br/api2/run_code', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code }),
        })
        .then(response => response.json())
        .then(data => {
            const output = data.output || '';
            const error = data.error || '';
            document.getElementById('code-output').textContent = output + error;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    document.getElementById('debugCode').addEventListener('click', () => {
        // Implementar funcionalidade de debug
        alert('Funcionalidade de debug ainda não implementada.');
    });

    editor.on('change', () => {
        const code = editor.getValue();
        // Função de tradução
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
        .then(response => response.json())
        .then(data => {
            const translatedCode = data.translated_code || '';
            document.getElementById('code-output').textContent = translatedCode;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});
