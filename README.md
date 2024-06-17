# ptpython

ptpython é uma linguagem de programação baseada no Python 3.10, mas com sintaxe e semântica em português. Esta linguagem permite que desenvolvedores escrevam código Python utilizando palavras-chave e funções embutidas em português.

## Instalação

### Instalando pelo GitHub

1. Instale diretamente do GitHub:
    ```bash
    pip install git+https://github.com/iagolirapasssos/ptpython.git
    ```

### Instalando localmente

1. Clone o repositório:
    ```bash
    git clone git+https://github.com/iagolirapasssos/ptpython.git
    cd ptpython
    ```

2. Instale o ptpython:
    ```bash
    pip install .
    ```

## Uso

Para usar o ptpython, crie um arquivo com a extensão `.ptpy` e escreva seu código em português. Em seguida, execute o arquivo com:

```bash
ptpython seu_arquivo.ptpy
```

## Palavras-chave Suportadas

[Clique aqui](tabelas_keywords.md) para ver toda a lista de palavras-chave e funções embutidas em português suportadas pelo ptpython.

## Exemplos Práticos

### Exemplo 1: Hello World

```ptpython
imprimir("Olá, Mundo!")
```

### Exemplo 2: Entrada do Usuário

```ptpython
nome = entrada("Digite seu nome: ")
imprimir(f"Olá, {nome}!")
```

### Exemplo 3: Condicional

```ptpython
idade = inteiro(entrada("Digite sua idade: "))
se idade >= 18:
    imprimir("Você é maior de idade.")
senão:
    imprimir("Você é menor de idade.")
```

### Exemplo 4: Loop For

```ptpython
para i em intervalo(5):
    imprimir(f"Iteração {i}")
```

### Exemplo 5: Loop While

```ptpython
contador = 0
enquanto contador < 5:
    imprimir(f"Contador: {contador}")
    contador += 1
```

### Exemplo 6: Função

```ptpython
função soma(a, b):
    retornar a + b

resultado = soma(5, 3)
imprimir(f"Resultado: {resultado}")
```

### Exemplo 7: Classe

```ptpython
classe Pessoa:
    def __init__(self, nome, idade):
        self.nome é nome
        self.idade é idade
    
    def cumprimentar(self):
        imprimir(f"Olá, meu nome é {self.nome} e eu tenho {self.idade} anos.")

pessoa = Pessoa("João", 30)
pessoa.cumprimentar()
```

### Exemplo 8: Tratamento de Exceções

```ptpython
tentar:
    resultado = 10 / 0
exceto ZeroDivisionError:
    imprimir("Erro: divisão por zero.")
finalmente:
    imprimir("Execução finalizada.")
```

### Exemplo 9: Compreensão de Listas

```ptpython
lista_quadrados = [x * x para x em intervalo(10)]
imprimir(f"Lista de quadrados: {lista_quadrados}")
```

### Exemplo 10: Manipulação de Dicionário

```ptpython
dicionário_exemplo = {"chave1": "valor1", "chave2": "valor2"}
para chave, valor em dicionário_exemplo.items():
    imprimir(f"{chave}: {valor}")
```

### Exemplo 11: Formatação de Texto e Números

```ptpython
# Formatação de texto
texto = "python"
imprimir(texto.maiusculo())
imprimir(texto.minusculo())
imprimir(texto.capitalizar())
imprimir(texto.título())

# Formatação de números
numero = 123.456
imprimir(arredondar(numero, 2))
imprimir(f"{numero:0.2f}")
imprimir(f"{numero:10.2f}")

# Preenchimento com zeros
numero_str = "42"
imprimir(numero_str.preencherzero(5))

# Formatação com a função formato
pi = 3.14159
imprimir("O valor de pi é aproximadamente {0:.2f}.".formatar(pi))
```

### Exemplos de Gráficos

### Exemplo 12: Gráfico de Barras

```ptpython
# Importar a biblioteca matplotlib e nomeá-la como plt
importar matplotlib.pyplot como plt

# Dados para o gráfico de barras
categorias = ['A', 'B', 'C', 'D', 'E']
valores = [5, 7, 3, 8, 6]

# Criar o gráfico de barras
plt.bar(categorias, valores, cor='c', label='Valores')

# Adicionar título e rótulos aos eixos
plt.xlabel('Categorias')
plt.ylabel('Valores')
plt.suptitle('Gráfico de Barras')

# Adicionar uma legenda
plt.legenda()

# Exibir o gráfico
plt.exibir()

# Salvar o gráfico como imagem
plt.salvarfigura('grafico_barras.png')
```

### Exemplo 13: Histograma

```ptpython
# Importar a biblioteca matplotlib e nomeá-la como plt
importar matplotlib.pyplot como plt

# Dados para o histograma
importar numpy como np
dados = np.random.randn(1000)

# Criar o histograma
plt.hist(dados, bins=30, cor='m', alpha=0.7, label='Frequência')

# Adicionar título e rótulos aos eixos
plt.xlabel('Valor')
plt.ylabel('Frequência')
plt.suptitle('Histograma')

# Adicionar uma legenda
plt.legenda()

# Exibir o gráfico
plt.exibir()

# Salvar o gráfico como imagem
plt.salvarfigura('histograma.png')
```

### Exemplo 14: Gráfico de Dispersão

```ptpython
# Importar a biblioteca matplotlib e nomeá-la como plt
importar matplotlib.pyplot como plt

# Dados para o gráfico de dispersão
importar numpy como np

x = np.random.rand(100)
y = np.random.rand(100)
cores = np.random.rand(100)
tamanho = 100 * np.random.rand(100)

# Criar o gráfico de dispersão
plt.scatter(x, y, c=cores, s=tamanho, alpha=0.5, cmap='viridis', label='Pontos')

# Ad

icionar título e rótulos aos eixos
plt.xlabel('Eixo X')
plt.ylabel('Eixo Y')
plt.suptitle('Gráfico de Dispersão')

# Adicionar uma legenda
plt.legenda()

# Exibir o gráfico
plt.exibir()

# Salvar o gráfico como imagem
plt.salvarfigura('grafico_dispersao.png')
```

### Exemplo 15: Gráfico de Setores (Pizza)

```ptpython
# Importar a biblioteca matplotlib e nomeá-la como plt
importar matplotlib.pyplot como plt

# Dados para o gráfico de pizza
fatias = [15, 30, 45, 10]
rotulos = ['Primeiro', 'Segundo', 'Terceiro', 'Quarto']
cores = ['c', 'm', 'r', 'b']
explosao = (0, 0.1, 0, 0)  # destaca a segunda fatia

# Criar o gráfico de pizza
plt.pie(fatias, labels=rotulos, colors=cores, explode=explosao, autopct='%1.1f%%', shadow=True, startangle=140)

# Adicionar título
plt.suptitle('Gráfico de Pizza')

# Exibir o gráfico
plt.exibir()

# Salvar o gráfico como imagem
plt.salvarfigura('grafico_pizza.png')
```

### Adicionando Novas Palavras-chave

Para adicionar novas palavras-chave para bibliotecas adicionais, siga estes passos:

1. Abra o arquivo `builtins.py` no diretório `pypython`.
2. Adicione as novas palavras-chave no dicionário `BUILTINS`. Por exemplo, para adicionar suporte a uma nova função `nova_funcao` em uma biblioteca `nova_biblioteca`, você pode fazer assim:

```python
BUILTINS = {
    # ... outras traduções ...
    "nova_funcao": "nova_funcao",
    # ... outras traduções ...
}
```

3. Salve o arquivo e instale novamente o `ptpython` localmente para aplicar as mudanças:

```bash
pip install .
```

## Créditos

ptpython foi desenvolvido por Prof. Francisco Iago Lira Passos (iagolirapassos@gmail.com). Agradecemos por utilizar esta ferramenta e esperamos que ela facilite seu aprendizado e uso do Python em português.