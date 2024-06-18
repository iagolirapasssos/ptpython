from pygments.lexers import PythonLexer
from pygments.token import Keyword, Name
from ptpython.keywords.python_keywords import KEYWORDS as PYTHON_KEYWORDS
from ptpython.keywords.python_builtins import BUILTINS as PYTHON_BUILTINS
from ptpython.keywords.matplotlib_keywords import KEYWORDS as MATPLOTLIB_KEYWORDS
from ptpython.keywords.matplotlib_builtins import BUILTINS as MATPLOTLIB_BUILTINS
from ptpython.keywords.discord_keywords import KEYWORDS as DISCORD_KEYWORDS
from ptpython.keywords.discord_builtins import BUILTINS as DISCORD_BUILTINS

# Combine all keywords and builtins
ALL_KEYWORDS = {**PYTHON_KEYWORDS, **MATPLOTLIB_KEYWORDS, **DISCORD_KEYWORDS}
ALL_BUILTINS = {**PYTHON_BUILTINS, **MATPLOTLIB_BUILTINS, **DISCORD_BUILTINS}

class CombinedLexer(PythonLexer):
    EXTRA_KEYWORDS = set(ALL_KEYWORDS.keys())
    EXTRA_BUILTINS = set(ALL_BUILTINS.keys())

    def get_tokens_unprocessed(self, text):
        for index, token, value in super().get_tokens_unprocessed(text):
            if token is Name and value in self.EXTRA_KEYWORDS:
                yield index, Keyword, value
            elif token is Name and value in self.EXTRA_BUILTINS:
                yield index, Name.Builtin, value
            else:
                yield index, token, value
