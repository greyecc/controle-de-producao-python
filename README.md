# Sistema de Controle de Qualidade de Peças

Projeto desenvolvido em Python para a disciplina de **Algoritmos e Lógica de
Programação**. O sistema simula a inspeção de peças em uma linha de montagem,
classificando-as como aprovadas ou reprovadas e organizando as peças aprovadas
em caixas.

## Objetivo

Automatizar a avaliação de peças produzidas por uma empresa industrial. Cada
peça é inspecionada com ID, peso, cor e comprimento. O programa compara esses
dados com os critérios de qualidade. Somente peças aprovadas são cadastradas;
as reprovações ficam em um histórico separado e não bloqueiam o ID.

## Critérios de qualidade

Uma peça é aprovada somente quando atende a todos os critérios abaixo:

- Peso entre **95 g e 105 g**, incluindo os valores limites.
- Cor **azul** ou **verde**.
- Comprimento entre **10 cm e 20 cm**, incluindo os valores limites.

Quando uma peça não atende a um ou mais critérios, todos os motivos da
reprovação são registrados no histórico de inspeções, sem cadastrar a peça.

## Funcionalidades

O menu principal oferece as seguintes opções:

1. Cadastrar uma nova peça.
2. Listar peças cadastradas e o histórico de reprovações.
3. Remover uma peça cadastrada mediante confirmação.
4. Listar as caixas finalizadas.
5. Gerar um relatório final completo.
0. Encerrar o programa.

### Armazenamento em caixas

- Somente peças aprovadas são armazenadas.
- Cada caixa comporta no máximo 10 peças.
- Ao receber a décima peça, a caixa é finalizada automaticamente.
- A próxima peça aprovada inicia uma nova caixa.
- Se uma peça estiver em uma caixa aberta e for removida, ela também será
  retirada dessa caixa.
- Uma caixa finalizada permanece como registro histórico.

### Histórico de reprovações

- Uma peça reprovada não entra na lista de peças cadastradas.
- Seu ID fica imediatamente disponível para uma nova tentativa.
- O resultado reprovado e seus motivos permanecem apenas no histórico de
  inspeções para consulta e para o relatório final.

## Tecnologias utilizadas

- Python 3.
- Biblioteca padrão `unittest` para testes automáticos.
- VS Code como ambiente de desenvolvimento.

O projeto não depende de bibliotecas externas.

## Estrutura do projeto

```text
TB 3 - Controle de Produção
├── main.py
├── README.md
├── documentos/
├── entrega/
└── testes/
    └── test_main.py
```

- `main.py`: código-fonte da aplicação.
- `testes/test_main.py`: testes automáticos.
- `documentos/`: materiais teóricos do trabalho.
- `entrega/`: arquivos finais que serão enviados à faculdade.

## Como executar

1. Abra a pasta do projeto no VS Code.
2. Abra o terminal integrado pelo menu **Terminal > New Terminal**.
3. Execute:

```powershell
python main.py
```

4. Digite o número da opção desejada e pressione `Enter`.

## Exemplo de peça aprovada

```text
ID da peça: 1
Peso em gramas: 100
Cor da peça: azul
Comprimento em centímetros: 15

Peça 1 cadastrada e APROVADA.
Peça armazenada na caixa 1 (1/10).
```

## Exemplo de peça reprovada

```text
ID da peça: 2
Peso em gramas: 110
Cor da peça: vermelha
Comprimento em centímetros: 8

Peça 2 REPROVADA. O cadastro não foi realizado.
Motivos da reprovação:
- Peso fora do padrão (permitido: 95 g a 105 g)
- Cor inválida (permitidas: azul ou verde)
- Comprimento fora do padrão (permitido: 10 cm a 20 cm)
```

## Como executar os testes

No terminal, a partir da pasta principal do projeto, execute:

```powershell
python -m unittest discover -s testes -v
```

O resultado esperado termina com:

```text
Ran 8 tests
OK
```

## Conceitos de programação aplicados

O projeto utiliza:

- Variáveis e constantes.
- Entrada e saída de dados.
- Condições com `if`, `elif` e `else`.
- Repetições com `while` e `for`.
- Funções.
- Listas, conjuntos e dicionários.
- Validação e conversão de valores.
- Testes automatizados.

## Possíveis expansões

Em um ambiente industrial real, o protótipo poderia receber automaticamente
as medidas por sensores, enviar resultados para um banco de dados ou sistema
de gestão e utilizar visão computacional para verificar outras características
das peças. Essas possibilidades não fazem parte da versão teste atual.
