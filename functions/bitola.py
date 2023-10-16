import json
from flask import render_template, request
# Define uma função para importar os valores do arquivo JSON


def importar_tabela_valores():
    with open('../tabelas/Tabela36_PVC.json', 'r') as arquivo:
        tabela_valores = json.load(arquivo)
    return tabela_valores

# Função para calcular a bitola


def calcular_bitola(corrente_nominal, metodo_instalacao):
    tabela_valores = importar_tabela_valores()
    if metodo_instalacao in tabela_valores:
        valores = tabela_valores[metodo_instalacao]
        for bitola, corrente in valores:
            if corrente_nominal <= corrente:
                return bitola
    return None
