import json


def importar_tabela_valores():
    with open('../tabelas/Tabela36_PVC.json', 'r') as arquivo:
        tabela_valores = json.load(arquivo)
    return tabela_valores


def calcular_bitola(corrente_nominal, metodo_instalacao):
    tabela_valores = importar_tabela_valores()

    for bitola, corrente in tabela_valores.get(metodo_instalacao, []):
        if corrente_nominal <= corrente:
            return bitola
    return None  # Retorna None se nenhum valor for encontrado na tabela


# Exemplo de uso:
corrente_nominal = 25  # Altere para o valor desejado
metodo_instalacao = "A1_2"  # Altere para o método de instalação desejado
bitola = calcular_bitola(corrente_nominal, metodo_instalacao)

if bitola is not None:
    print(
        f"A bitola recomendada para {corrente_nominal} A e método de instalação {metodo_instalacao} é {bitola} mm².")
else:
    print("Não foi encontrada uma bitola adequada na tabela para os valores fornecidos.")
