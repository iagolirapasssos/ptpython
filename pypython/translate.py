import re
from pypython.keywords import KEYWORDS
from pypython.builtins import BUILTINS

def translate(code):
    # Tradução das palavras-chave
    for pt, en in KEYWORDS.items():
        code = re.sub(rf'\b{pt}\b', en, code)
    # Tradução das funções embutidas
    for pt, en in BUILTINS.items():
        code = re.sub(rf'\b{pt}\b', en, code)
    return code