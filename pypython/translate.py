import re
from pypython.keywords.python_keywords import KEYWORDS as PYTHON_KEYWORDS
from pypython.keywords.python_builtins import BUILTINS as PYTHON_BUILTINS
from pypython.keywords.matplotlib_keywords import KEYWORDS as MATPLOTLIB_KEYWORDS
from pypython.keywords.matplotlib_builtins import BUILTINS as MATPLOTLIB_BUILTINS
from pypython.keywords.discord_keywords import KEYWORDS as DISCORD_KEYWORDS
from pypython.keywords.discord_builtins import BUILTINS as DISCORD_BUILTINS

def translate(code):
    """
    Traduza o código ptpython para Python padrão.

    Este método identifica e substitui palavras-chave e funções embutidas do ptpython para suas
    equivalentes em Python. Ele também cuida de preservar as strings e funções definidas pelo usuário durante o processo de tradução.

    Args:
        code (str): O código ptpython a ser traduzido.

    Returns:
        str: O código traduzido para Python padrão.
    """
    # Expressão regular para identificar strings
    string_pattern = r'(\'[^\']*\'|"[^"]*")'

    # Encontre todas as strings no código
    strings = re.findall(string_pattern, code)

    # Substitua temporariamente as strings por marcadores
    for i, string in enumerate(strings):
        code = code.replace(string, f'__STRING_{i}__')

    # Encontre todas as definições de funções e métodos definidos pelo usuário
    user_defined_functions = re.findall(r'def\s+(\w+)\s*\(', code)
    user_defined_methods = re.findall(r'class\s+\w+\s*:\s*def\s+(\w+)\s*\(', code)
    user_defined_names = set(user_defined_functions + user_defined_methods)

    # Substituição das palavras-chave
    all_keywords = {**PYTHON_KEYWORDS, **MATPLOTLIB_KEYWORDS, **DISCORD_KEYWORDS}
    for pt, en in sorted(all_keywords.items(), key=lambda item: -len(item[0])):
        code = re.sub(rf'\b{pt}\b', en, code)

    # Substituição das funções embutidas
    all_builtins = {**PYTHON_BUILTINS, **MATPLOTLIB_BUILTINS, **DISCORD_BUILTINS}
    for pt, en in all_builtins.items():
        if pt not in user_defined_names:
            code = re.sub(rf'\b{pt}\b', en, code)

    # Recoloque as strings originais no código
    for i, string in enumerate(strings):
        code = code.replace(f'__STRING_{i}__', string)

    return code
