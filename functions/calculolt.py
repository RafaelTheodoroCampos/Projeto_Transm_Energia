from flask import request, jsonify


def calcular_distancias():
    alturas_condutores_raw = request.form.getlist('altura_condutor[]')
    distancias_condutor_centro_raw = request.form.getlist('condutor_centro[]')

    # Verifique se há valores vazios ou ausentes
    if '' in alturas_condutores_raw or '' in distancias_condutor_centro_raw:
        # Lida com valores ausentes
        return None, None

    # Converta para floats
    alturas_condutores = list(map(float, alturas_condutores_raw))
    distancias_condutor_centro = list(
        map(float, distancias_condutor_centro_raw))

    # Resto do seu código de cálculo de distâncias...

    distancias_entre_condutores = []
    distancias_ate_imagem = []

    for i in range(len(alturas_condutores)):
        for j in range(i + 1, len(alturas_condutores)):
            distancia = ((distancias_condutor_centro[j] - distancias_condutor_centro[i]) ** 2 +
                         (alturas_condutores[j] - alturas_condutores[i]) ** 2) ** 0.5
            distancias_entre_condutores.append(distancia)

    for i in range(len(alturas_condutores)):
        distancia_imagem = (
            (distancias_entre_condutores[i] ** 2) + (2 * alturas_condutores[i]) ** 2) ** 0.5
        distancias_ate_imagem.append(distancia_imagem)
    print("AAAAA", distancias_ate_imagem, distancias_entre_condutores)
    return distancias_entre_condutores, distancias_ate_imagem
