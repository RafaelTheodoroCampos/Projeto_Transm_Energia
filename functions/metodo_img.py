from flask import Flask, Response, redirect, render_template, request
from functions.calculolt import calcular_distancias
import numpy as np

# Função para formatar números complexos para strings legíveis


def formatar_numero_complexo(num):
    real_part = '{:.5f}'.format(num.real)
    imag_part = '{:.5f}'.format(num.imag)
    return f'{real_part}+{imag_part}j' if num.imag >= 0 else f'{real_part}{imag_part}j'


def formatar_matriz_complexa(matriz):
    matriz_formatada = np.vectorize(formatar_numero_complexo)(matriz)
    return matriz_formatada.tolist()


def metododasimagens():
    altura_condutor = [float(round(float(h), 2))
                       for h in request.form.getlist('altura_condutor[]')]
    raio_condutores = float(request.form['r_condutor'])
    rmg = float(request.form['rmg'])
    distancias_ate_imagem, distancias_entre_condutores, nome_distancia_condutores = calcular_distancias()

    # Dados Base
    pi = np.pi
    w = 2 * pi * 60
    mi0 = 4 * pi * 10 ** -7

    # Inicialização da matriz de impedância do solo
    num_condutores = len(altura_condutor)
    Z_solo = np.zeros((num_condutores, num_condutores), dtype=np.complex128)
    contador = 0
    # Preenchendo a matriz de impedância do solo usando um loop for
    for i in range(num_condutores):
        for j in range(num_condutores):
            if i == j:
                Z_solo[i, j] = raio_condutores + (1j * w * mi0) / (2 * pi) * \
                    np.log(2 * altura_condutor[i] / rmg)  # Impedância própria

    for i in range(num_condutores):
        for j in range(i + 1, num_condutores):
            Z_solo[i, j] = (1j * w * mi0) / (2 * pi) * \
                np.log(
                distancias_ate_imagem[contador] / distancias_entre_condutores[contador])
            contador += 1

    for i in range(1, num_condutores):
        for j in range(i):
            Z_solo[i, j] = Z_solo[j, i]

    Z_solo = formatar_matriz_complexa(Z_solo)
    return Z_solo
