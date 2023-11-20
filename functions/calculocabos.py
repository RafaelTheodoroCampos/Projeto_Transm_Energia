import json
from flask import render_template, request
# Define uma função para importar os valores do arquivo JSON


def importar_tabela_valores():
    with open('C:\\Users\\rafae\\Desktop\\Eng_Ele\\projetoie\\Projeto_inst.E\\data\\tabela36_pvc.json', 'r') as arquivo:
        tabela_valores = json.load(arquivo)
    return tabela_valores

# Função para calcular a bitola


def calcular_bitola():

    return None
