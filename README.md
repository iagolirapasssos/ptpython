# ptpython

ptpython é uma linguagem de programação baseada no Python 3.10, mas com sintaxe e semântica em português. Esta linguagem permite que desenvolvedores escrevam código Python utilizando palavras-chave e funções embutidas em português.

## Instalação

### Instalando pelo GitHub

1. Instale diretamente do GitHub:
    ```bash
    pip install git+https://github.com/seuusuario/ptpython.git
    ```

### Instalando localmente

1. Clone o repositório:
    ```bash
    git clone https://github.com/seuusuario/ptpython.git
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

Aqui estão as palavras-chave em português suportadas pelo ptpython:

| Português      | Inglês      |
| -------------- | ----------- |
| se             | if          |
| senão          | else        |
| para           | for         |
| enquanto       | while       |
| função         | def         |
| retornar       | return      |
| classe         | class       |
| importar       | import      |
| de             | from        |
| como           | as          |
| tentar         | try         |
| exceto         | except      |
| finalmente     | finally     |
| com            | with        |
| passar         | pass        |
| continuar      | continue    |
| interromper    | break       |
| verdadeiro     | True        |
| falso          | False       |
| nulo           | None        |
| global         | global      |
| não local      | nonlocal    |
| é              | is          |
| não é          | is not      |
| em             | in          |
| não em         | not in      |
| e              | and         |
| ou             | or          |
| não            | not         |
| levantar       | raise       |
| afirmar        | assert      |
| eliminar       | del         |

## Funções Embutidas Suportadas

Aqui estão algumas das funções embutidas em português suportadas pelo ptpython:

| Português        | Inglês       |
| ---------------- | ------------ |
| imprimir         | print        |
| entrada          | input        |
| inteiro          | int          |
| flutuante        | float        |
| cadeia           | str          |
| lista            | list         |
| dicionário       | dict         |
| conjunto         | set          |
| tupla            | tuple        |
| soma             | sum          |
| mapear           | map          |
| filtro           | filter       |
| lambda           | lambda       |
| abrir            | open         |
| comprimento      | len          |
| intervalo        | range        |
| enumerar         | enumerate    |
| tudo             | all          |
| qualquer         | any          |
| tipo             | type         |
| éinstância       | isinstance   |
| tematributo      | hasattr      |
| obteratributo    | getattr      |
| definiratributo  | setattr      |
| eliminaratributo | delattr      |

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
        self.nome = nome
        self.idade = idade
    
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

## Créditos

ptpython foi desenvolvido por [Seu Nome]. Agradecemos por utilizar esta ferramenta e esperamos que ela facilite seu aprendizado e uso do Python em português.

Este arquivo `README.md` fornece instruções claras sobre como instalar e usar o `ptpython`, detalha as palavras-chave e funções embutidas suportadas, e oferece exemplos práticos para ajudar os usuários a começar. Além disso, inclui créditos ao autor.