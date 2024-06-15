from setuptools import setup, find_packages

setup(
    name="ptpython",
    version='0.1.37',
    packages=find_packages(),
    install_requires=[
        # Dependências aqui (por exemplo: 'ply==3.11' se precisar de um lexer/parser)
    ],
    entry_points={
        'console_scripts': [
            'ptpython=pypython.main:main',
        ],
    },
    author="Francisco Iago Lira Passos",
    author_email="iagolirapassos@gmail.com",
    description="Uma linguagem de programação baseada em Python 3.10 com sintaxe e semântica em português.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/iagolirapasssos/ptpython",
)
