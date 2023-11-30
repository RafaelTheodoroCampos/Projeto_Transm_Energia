from flask import Flask, Response, redirect, render_template, request
from functions.calculolt import calcular_distancias
import numpy as np
import io
import base64
import matplotlib.pyplot as plt

# Função para formatar números complexos para strings legíveis


def calcular_impedancia(matriz, matriz1):

    impedancia_inicial3 = matriz1[1][2] / 300000
    impedancia_final3 = matriz1[1][2]

    impedancia_inicial2 = matriz[1][2]
    impedancia_final2 = impedancia_inicial2 * 300000

    impedancia_inicial = matriz[0][2]
    impedancia_final = impedancia_inicial * 300000

    # Divisão da distância em 20 intervalos para 300 km
    intervalos = 20
    delta_distancia = 300000 / intervalos

    # Cálculo da impedância em cada ponto ao longo da linha

    impedancias3 = []
    for i in range(intervalos + 1):
        # Interpolação linear para calcular a impedância em cada ponto
        distancia_atual = i * delta_distancia
        parte_imaginaria = impedancia_inicial3.imag + \
            (distancia_atual / 300000) * \
            (impedancia_final3.imag - impedancia_inicial3.imag)
        impedancia_ponto = parte_imaginaria
        impedancias3.append((distancia_atual, impedancia_ponto))

    impedancias2 = []
    for i in range(intervalos + 1):
        # Interpolação linear para calcular a impedância em cada ponto
        distancia_atual = i * delta_distancia
        parte_imaginaria = impedancia_inicial2.imag + \
            (distancia_atual / 300000) * \
            (impedancia_final2.imag - impedancia_inicial2.imag)
        impedancia_ponto = parte_imaginaria
        impedancias2.append((distancia_atual, impedancia_ponto))

    impedancias1 = []
    for i in range(intervalos + 1):
        # Interpolação linear para calcular a impedância em cada ponto
        distancia_atual = i * delta_distancia
        parte_imaginaria = impedancia_inicial.imag + \
            (distancia_atual / 300000) * \
            (impedancia_final.imag - impedancia_inicial.imag)
        impedancia_ponto = parte_imaginaria
        impedancias1.append((distancia_atual, impedancia_ponto))

    return impedancias1, impedancias2, impedancias3


def grafico(impedancia1, impedancia2, impedancia3):

    # Extrair os dados de distância e impedância para cada conjunto
    distancias_1 = [x[0] for x in impedancia1]
    impedancias_valores_1 = [x[1] for x in impedancia1]

    distancias_2 = [x[0] for x in impedancia2]
    impedancias_valores_2 = [x[1] for x in impedancia2]

    distancias_3 = [x[0] for x in impedancia3]
    impedancias_valores_3 = [x[1] for x in impedancia3]

    # Plotar o gráfico com marcadores para os pontos finais
    plt.figure(figsize=(10, 6))  # Ajuste do tamanho do gráfico
    plt.plot(distancias_3, impedancias_valores_3,
             linestyle='-', color='g', label='[Z] Transposta')
    plt.plot(distancias_1, impedancias_valores_1,
             linestyle='-', color='b', label='[Z] Mútua 1')
    plt.plot(distancias_2, impedancias_valores_2,
             linestyle='-', color='r', label='[Z] Mútua 2')

    # Adicionar marcadores para os últimos pontos de Mútua 1 e Mútua 2
    plt.scatter(distancias_1[-1], impedancias_valores_1[-1],
                color='blue', marker='o', s=100, )
    plt.scatter(distancias_2[-1], impedancias_valores_2[-1],
                color='red', marker='o', s=100, )

    # Calcular e mostrar a diferença entre os últimos valores das impedâncias
    diferenca = impedancias_valores_2[-1] - impedancias_valores_1[-1]
    texto_diferenca = f'Δ: {diferenca:.2f}'
    plt.text(1.05 * distancias_2[-1], 1.03 * impedancias_valores_2[-1], texto_diferenca,
             fontsize=13, fontweight='bold', ha='right', va='top', rotation='vertical')

    # Adicionar uma linha entre os últimos pontos de Mútua 1 e Mútua 2
    plt.plot([distancias_1[-1], distancias_2[-1]], [impedancias_valores_1[-1],
             impedancias_valores_2[-1]], linestyle='--', color='black')

    plt.xlabel('Distância')
    plt.ylabel('Impedância')
    plt.title('')
    plt.grid(True)
    plt.legend()

    # Salvar a figura em memória
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Converter a figura para base64
    plot_encoded = base64.b64encode(img.getvalue()).decode('utf-8')
    img.close()

    return plot_encoded


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

    Z_1 = np.copy(Z_solo_carson)
    tz2 = [1, 2, 0]
    tz3 = [2, 0, 1]
    for i in range(3):
        for j in range(3):
            Z_2[i, j] = Z_1[tz2[i], tz2[j]]

    for i in range(3):
        for j in range(3):
            Z_3[i, j] = Z_1[tz3[i], tz3[j]]

    
    # Aplicando trasposição a cada 33% no caso de uma linha de 300km
    Z_2 *= 100000
    Z_3 *= 100000
    Z_1 *= 300000
    submatriz_3x3 = Z_1[:3, :3]
    submatriz_3x3 /= 3
    Z_1[:3, :3] = submatriz_3x3
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
    Z_solo_transposta_complex = Z_transposta
    Z_solo_carson_complex = Z_solo_carson
    Z_ntransposta = Z_solo_carson * 300000  # Para o exemplo
    Z_ntransposta = formatar_matriz_complexa(Z_ntransposta)
    Z_solo_carson = formatar_matriz_complexa(Z_solo_carson)
    Z_transposta = formatar_matriz_complexa(Z_transposta)

    return Z_solo_carson, Z_transposta, Z_ntransposta, Z_solo_carson_complex, Z_solo_transposta_complex
