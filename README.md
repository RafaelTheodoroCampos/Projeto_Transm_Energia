# Cálculos de Linhas de Transmissão com Diferentes Métodos - CEFET-RJ

O projeto consiste em um website educativo que permite o cálculo de parâmetros longitudinais e transversais de linhas de transmissão, comparando os resultados obtidos por diferentes métodos. Este programa realiza cálculos utilizando a matriz de impedância, incluindo a consideração de para-raios. 

## 🚀 Começando

Estas instruções permitirão que você obtenha uma cópia do projeto em funcionamento na sua máquina local.

### 📋 Pré-requisitos

- [Python 3+](https://www.python.org/)
- Biblioteca Flask

Para instalar Flask, execute o comando:

```bash
pip install Flask
```
### 🔧 Instalação
Após instalar as ferramentas necessárias, siga os passos abaixo:
* Baixe os arquivos do projeto da página do projeto.
* Inicie o programa através do comando:
 ```bash
python app.py
```
📖 Descrição dos Métodos
O programa inclui diversos métodos para calcular os parâmetros de linhas de transmissão. Abaixo, uma breve descrição de cada método utilizado:

Cálculo da Matriz de Impedância:

Este método calcula a matriz de impedância da linha de transmissão, considerando todos os componentes e suas interações eletromagnéticas.
Incorporação de Para-raios:

Adiciona a influência dos para-raios no cálculo da impedância, permitindo uma análise mais precisa e realista das condições de operação da linha.
Parâmetros Longitudinais:

Calcula os parâmetros longitudinais (resistência, indutância) ao longo da extensão da linha de transmissão, utilizando a matriz de impedância ajustada.
Parâmetros Transversais:

Determina os parâmetros transversais (capacitância, condutância), considerando a configuração física e elétrica da linha.
Cada método é implementado de maneira modular, permitindo que os usuários visualizem e compreendam o impacto de cada componente individualmente, bem como em conjunto. O website fornece uma interface intuitiva para entrada de dados e visualização dos resultados, facilitando o aprendizado e a comparação dos diferentes métodos de cálculo.
