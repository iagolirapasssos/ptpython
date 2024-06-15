import sys
import logging
import subprocess
from tempfile import NamedTemporaryFile
from pypython.translate import translate

# Configuração do logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    if len(sys.argv) != 2:
        logging.error("Uso: ptpython <arquivo>")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        # TODO: Adicionar verificação de permissão ao abrir o arquivo.
        with open(filename, 'r', encoding='utf-8') as file:
            code = file.read()
        #logging.debug(f"Código original lido do arquivo:\n{code}")
    except FileNotFoundError:
        logging.error(f"Erro: Arquivo '{filename}' não encontrado.")
        sys.exit(1)

    translated_code = translate(code)
    #logging.debug(f"Código traduzido:\n{translated_code}")

    # TODO: Verificar se a criação de arquivo temporário é a melhor abordagem para execução do código.
    # Cria um arquivo temporário para o código traduzido
    with NamedTemporaryFile(mode='w+', suffix='.py', delete=False) as temp_file:
        temp_file.write(translated_code)
        temp_file.flush()
        temp_filename = temp_file.name

    try:
        # Executa o código traduzido usando python3.10
        result = subprocess.run(['python3.10', temp_filename], check=True)
        #logging.info("Código executado com sucesso.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Erro na execução: {e}")
    finally:
        # Remove o arquivo temporário
        import os
        os.remove(temp_filename)

if __name__ == '__main__':
    main()
