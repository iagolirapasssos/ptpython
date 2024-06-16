import importlib.util
import os

def load_keywords_or_builtins(file_path):
    """
    Carrega palavras-chave ou funções embutidas de um arquivo Python.

    Args:
        file_path (str): O caminho para o arquivo Python.

    Returns:
        dict: Um dicionário de palavras-chave ou funções embutidas.
    """
    spec = importlib.util.spec_from_file_location("module", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if hasattr(module, 'KEYWORDS'):
        return module.KEYWORDS
    elif hasattr(module, 'BUILTINS'):
        return module.BUILTINS
    else:
        raise AttributeError(f"O arquivo {file_path} não possui 'KEYWORDS' ou 'BUILTINS'.")

def generate_table(data, title):
    """
    Gera uma tabela Markdown a partir de um dicionário.

    Args:
        data (dict): O dicionário contendo os dados para a tabela.
        title (str): O título da tabela.

    Returns:
        str: A tabela em formato Markdown.
    """
    table = f"## {title}\n"
    table += "| Português        | Inglês       |\n"
    table += "| ---------------- | ------------ |\n"
    for pt, en in data.items():
        table += f"| {pt:<16} | {en:<12} |\n"
    return table

def main():
    """
    Função principal que carrega os arquivos de palavras-chave e funções embutidas,
    gera tabelas Markdown e salva no arquivo 'tabelas.md'.
    """
    keywords_dir = 'pypython/keywords'
    tables = []

    # Ordenar os arquivos pelo nome
    filenames = sorted([f for f in os.listdir(keywords_dir) if f.endswith('.py') and f != '__init__.py'])

    for filename in filenames:
        file_path = os.path.join(keywords_dir, filename)
        try:
            data = load_keywords_or_builtins(file_path)
            title = filename.replace('_', ' ').replace('.py', '').title()
            tables.append(generate_table(data, title))
        except AttributeError as e:
            print(f"Erro ao carregar {file_path}: {e}")

    with open('tabelas_keywords.md', 'w') as f:
        for table in tables:
            f.write(table)
            f.write("\n")

if __name__ == "__main__":
    main()
