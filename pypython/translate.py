import re
from pypython.keywords import KEYWORDS
from pypython.builtins import BUILTINS

def translate(code):
    # TODO: Verificar se há formas mais eficientes de identificar e substituir strings no código.
    # Expressão regular para identificar strings
    string_pattern = r'(\'[^\']*\'|"[^"]*")'

    # Encontre todas as strings no código
    strings = re.findall(string_pattern, code)

    # TODO: Avaliar se a substituição de strings por marcadores é a melhor abordagem.
    # Substitua temporariamente as strings por marcadores
    for i, string in enumerate(strings):
        code = code.replace(string, f'__STRING_{i}__')

    # TODO: Otimizar a substituição das palavras-chave.
    # Substituição das palavras-chave
    for pt, en in sorted(KEYWORDS.items(), key=lambda item: -len(item[0])):
        code = re.sub(rf'\b{pt}\b', en, code)

    # Substituição das funções embutidas
    for pt, en in BUILTINS.items():
        code = re.sub(rf'\b{pt}\b', en, code)

    # Recoloque as strings originais no código
    for i, string in enumerate(strings):
        code = code.replace(f'__STRING_{i}__', string)

    return code
