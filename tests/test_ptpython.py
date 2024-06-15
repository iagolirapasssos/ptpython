import unittest
from pypython.translate import translate

class TestPtPython(unittest.TestCase):
    def test_keywords(self):
        self.assertEqual(translate("se verdadeiro:\n    imprimir('Olá')"), "if True:\n    print('Olá')")

    def test_builtins(self):
        self.assertEqual(translate("imprimir(entrada('Digite algo: '))"), "print(input('Digite algo: '))")

if __name__ == '__main__':
    unittest.main()
