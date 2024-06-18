### Instalação das dependências

Antes de começar, instale as dependências necessárias:

```bash
pip install pygments tk ttkthemes
```


```

### Funcionalidades implementadas:
1. **Novo arquivo**: Limpa o editor para criar um novo arquivo.
2. **Abrir arquivo**: Permite abrir arquivos `.ptpy` existentes.
3. **Salvar**: Salva o arquivo atual.
4. **Salvar como**: Salva o arquivo atual com um novo nome.
5. **Executar**: Traduza e execute o código ptpython.
6. **Coloração da sintaxe**: Realça a sintaxe do código utilizando `Pygments`.

### Execução

Para executar a IDE, salve o código acima em um arquivo, por exemplo, `ptpython_ide.py`, e execute o script:

```bash
python ptpython_ide.py
```

### Observações
- A coloração da sintaxe está configurada para o estilo "monokai". Você pode alterar para outro estilo disponível no Pygments.
- Este exemplo é básico e serve como ponto de partida. Para uma IDE mais robusta, considere adicionar funcionalidades adicionais como auto-complete, debug, etc.