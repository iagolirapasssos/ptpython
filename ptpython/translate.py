import re
from ptpython.keywords.python_keywords import KEYWORDS as PYTHON_KEYWORDS
from ptpython.keywords.python_builtins import BUILTINS as PYTHON_BUILTINS
from ptpython.keywords.matplotlib_keywords import KEYWORDS as MATPLOTLIB_KEYWORDS
from ptpython.keywords.matplotlib_builtins import BUILTINS as MATPLOTLIB_BUILTINS
from ptpython.keywords.discord_keywords import KEYWORDS as DISCORD_KEYWORDS
from ptpython.keywords.discord_builtins import BUILTINS as DISCORD_BUILTINS

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

    # Encontre todas as definições de classes e funções definidos pelo usuário
    #user_defined_classes = re.findall(r'class\s+(\w+)', code)
    # Encontre todas as definições de classes e funções definidos pelo usuário
    user_defined_classes_1 = re.findall(r'classe\s+(\w+)\s*:', code)
    user_defined_classes_2 = re.findall(r'classe\s+(\w+)\s*\(', code)
    user_defined_functions = re.findall(r'função\s+(\w+)\s*\(', code)
    user_defined_names = set(user_defined_classes_1 + user_defined_classes_2 + user_defined_functions)

    # Crie um dicionário para armazenar os nomes definidos pelo usuário
    user_defined_dict = {name: f'__USER_DEF_{i}__' for i, name in enumerate(user_defined_names)}
   
   # Substitua temporariamente os nomes definidos pelo usuário por marcadores
    for name, placeholder in user_defined_dict.items():
        code = re.sub(rf'\b{name}\b', placeholder, code)

    # Substituição das palavras-chave
    all_keywords = {**PYTHON_KEYWORDS, **MATPLOTLIB_KEYWORDS, **DISCORD_KEYWORDS}
    for pt, en in sorted(all_keywords.items(), key=lambda item: -len(item[0])):
        if pt not in user_defined_dict:
            code = re.sub(rf'\b{pt}\b', en, code)

    # Substituição das funções embutidas
    all_builtins = {**PYTHON_BUILTINS, **MATPLOTLIB_BUILTINS, **DISCORD_BUILTINS}
    for pt, en in all_builtins.items():
        # Pule a tradução se o nome estiver no dicionário de nomes definidos pelo usuário
        if pt not in user_defined_dict:
            code = re.sub(rf'\b{pt}\b', en, code)

    # Restaure os nomes definidos pelo usuário
    for name, placeholder in user_defined_dict.items():
        code = code.replace(placeholder, name)

    # Recoloque as strings originais no código
    for i, string in enumerate(strings):
        code = code.replace(f'__STRING_{i}__', string)

    return code
