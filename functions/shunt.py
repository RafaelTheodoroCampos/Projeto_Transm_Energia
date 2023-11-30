from flask import Flask, Response, redirect, render_template, request
from functions.calculolt import calcular_distancias
from functions.carson import formatar_matriz_complexa
import numpy as np
import io
import base64
import matplotlib.pyplot as plt




def format_matrix(matrix):
    rows, cols = matrix.shape
    formatted_matrix = np.empty((rows, cols), dtype=object)

    for i in range(rows):
        for j in range(cols):
            real_part = matrix[i, j]
            

            # Format real part
            if abs(real_part) >= 1e4 or abs(real_part) < 1e-4:
                real_str = "{:.1e}".format(real_part)
            else:
                real_str = "{:.4f}".format(real_part)

            
            formatted_matrix[i, j] = f"{real_str}"

    return formatted_matrix

def capacitancia():
    altura_condutor = [float(round(float(h), 2))
                       for h in request.form.getlist('altura_condutor[]')]
    raio_condutores = float(request.form['r_condutor'])
   
    distancias_ate_imagem, distancias_entre_condutores, nome_distancia_condutores = calcular_distancias()

    # Dados Base
    pi = np.pi
    e0 = 8.854 * 10 ** -12

    # Inicialização da matriz de impedância do solo
    num_condutores = len(altura_condutor)
    P_shunt = np.zeros(
        (num_condutores, num_condutores), dtype=float)
    contador = 0
    # Preenchendo a matriz de impedância do solo usando um loop for
    for i in range(num_condutores):
        for j in range(num_condutores):
            if i == j:
                P_shunt[i, j] =  (1) / (2 * pi * e0) * \
                    np.log(2* altura_condutor[i] / raio_condutores )  # Impedância própria

    for i in range(num_condutores):
        for j in range(i + 1, num_condutores):
            P_shunt[i, j] = (1) / (2 * pi * e0) * \
                np.log(
                    distancias_ate_imagem [contador] / distancias_entre_condutores[contador])
            contador += 1

    for i in range(1, num_condutores):
        for j in range(i):
            P_shunt[i, j] = P_shunt[j, i]


   
    C_shunt = np.linalg.inv(P_shunt)
    capacitancias = []
    rows, cols = C_shunt.shape
    aux_shunt = np.copy(C_shunt)
    contador = 0
    
    for i in range(rows):
        contador = 0
        for j in range(cols):
            contador += aux_shunt[i, j]
        contador_formatado = "{:.1e}".format(contador)
        capacitancias.append(contador_formatado)
    
  
        
    C_shunt = format_matrix(C_shunt)
    P_shunt = format_matrix(P_shunt)
    return P_shunt, C_shunt, capacitancias