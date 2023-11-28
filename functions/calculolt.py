from flask import request


def nome_distancia(i, j):
    nomes = {
        (0, 1): "Dab",
        (0, 2): "Dac",
        (0, 3): "Daw",
        (0, 4): "Daw1",
        (1, 2): "Dbc",
        (1, 3): "Dbw",
        (1, 4): "Dbw1",
        (2, 3): "Dcw",
        (2, 4): "Dcw1",
        (3, 4): "Dww1"
    }
    return nomes.get((i, j)) or nomes.get((j, i))


def calcular_distancias():
    alturas_condutores_raw = request.form.getlist('altura_condutor[]') or []
    distancias_condutor_centro_raw = request.form.getlist(
        'condutor_centro[]') or []

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

    nome_distancia_condutores = []

    for i in range(len(alturas_condutores)):
        for j in range(i, len(alturas_condutores)):
            if i == j:
                continue
            nome = nome_distancia(i, j)
            distancia = round(((distancias_condutor_centro[j] - distancias_condutor_centro[i]) ** 2 +
                               (alturas_condutores[j] - alturas_condutores[i]) ** 2) ** 0.5, 2)
            nome_distancia_condutores.append(nome)
            distancias_entre_condutores.append(distancia)

            distancia_imagem = round(
                ((distancia ** 2) + (2 * alturas_condutores[i]) ** 2) ** 0.5, 2)
            distancias_ate_imagem.append(distancia_imagem)

   # print("Distancia img", distancias_ate_imagem)
   # print("Distancia condutor", distancias_entre_condutores)
   # print("Nome", nome_distancia_condutores)
   # print("altura_condutor", alturas_condutores)
    return distancias_ate_imagem, distancias_entre_condutores, nome_distancia_condutores
