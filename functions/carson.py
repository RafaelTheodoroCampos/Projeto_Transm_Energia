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


def metodocarson():
    altura_condutor = [float(round(float(h), 2))
                       for h in request.form.getlist('altura_condutor[]')]
    raio_condutores = float(request.form['r_condutor'])
    p = float(request.form['rho'])
    f = float(request.form['freq'])
    rd = float(request.form['rd'])
    distancias_ate_imagem, distancias_entre_condutores, nome_distancia_condutores = calcular_distancias()

    # Dados Base
    pi = np.pi
    w = 2 * pi * 60
    mi0 = 4 * pi * 10 ** -7
    de = 659*(np.sqrt(p/f))
    de = round(de, 3)

    # Inicialização da matriz de impedância do solo
    num_condutores = len(altura_condutor)
    Z_solo_carson = np.zeros(
        (num_condutores, num_condutores), dtype=np.complex128)
    contador = 0
    Z_2 = np.zeros((3, 3), dtype=np.complex128)
    Z_3 = np.zeros((3, 3), dtype=np.complex128)
    # Preenchendo a matriz de impedância do solo usando um loop for
    for i in range(num_condutores):
        for j in range(num_condutores):
            if i == j:
                Z_solo_carson[i, j] = raio_condutores + rd + (1j * w * mi0) / (2 * pi) * \
                    np.log(de / altura_condutor[i])  # Impedância própria

    for i in range(num_condutores):
        for j in range(i + 1, num_condutores):
            Z_solo_carson[i, j] = rd + (1j * w * mi0) / (2 * pi) * \
                np.log(
                    de / distancias_entre_condutores[contador])
            contador += 1

    for i in range(1, num_condutores):
        for j in range(i):
            Z_solo_carson[i, j] = Z_solo_carson[j, i]

    # Trasposição
    Z_ntransposta = Z_solo_carson * 300000
    Z_1 = Z_solo_carson * 100000
    
    Z_2 = [
        [Z_1[1][1], Z_1[1][2], Z_1[1][0]],
        [Z_1[2][1], Z_1[2][2], Z_1[2][0]],
        [Z_1[0][1], Z_1[0][2], Z_1[0][0]]
    ]

    Z_3 = [
        [Z_1[2][2], Z_1[2][0], Z_1[2][1]],
        [Z_1[0][2], Z_1[0][0], Z_1[0][1]],
        [Z_1[1][2], Z_1[1][0], Z_1[1][1]]
    ]

    # Aplicando trasposição a cada 33%
    Z_2 = Z_2*100000
    Z_3 = Z_3*100000
    # Formatando

    # Verificando o tamanho de Z_1
    # Obtém o tamanho da primeira dimensão da matriz Z_1
    tamanho_Z_1 = Z_1.shape[0]

    # Ajustando as dimensões de Z_2 e Z_3 para ter o mesmo tamanho que Z_1
    if tamanho_Z_1 != Z_2.shape[0]:
        diferenca_linhas = tamanho_Z_1 - Z_2.shape[0]
        Z_2 = np.pad(Z_2, ((0, diferenca_linhas), (0, diferenca_linhas)),
                     mode='constant', constant_values=0)

    if tamanho_Z_1 != Z_3.shape[0]:
        diferenca_linhas = tamanho_Z_1 - Z_3.shape[0]
        Z_3 = np.pad(Z_3, ((0, diferenca_linhas), (0, diferenca_linhas)),
                     mode='constant', constant_values=0)

    Z_transposta = Z_1 + Z_2 + Z_3

    Z_ntransposta = formatar_matriz_complexa(Z_ntransposta)
    Z_solo_carson = formatar_matriz_complexa(Z_solo_carson)
    Z_transposta = formatar_matriz_complexa(Z_transposta)

    return Z_solo_carson, Z_transposta, Z_ntransposta
