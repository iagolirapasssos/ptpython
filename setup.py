from setuptools import setup, find_packages

setup(
    name="ptpython",
    version='0.1.176',  # TODO: Automatizar o controle de versão.
    packages=find_packages(),
    install_requires=[
        # TODO: Listar todas as dependências necessárias aqui.
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
    url="https://github.com/iagolirapassos/ptpython",
)
