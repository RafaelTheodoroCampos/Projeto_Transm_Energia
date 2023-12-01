from flask import Flask, Response, jsonify, redirect, render_template, request
from functions.calculolt import calcular_distancias
from functions.metodo_img import metododasimagens
from functions.carson import metodocarson, calcular_impedancia, grafico
from functions.shunt import capacitancia
import datetime
# Importe a função do arquivo pdf_generator


app = Flask(__name__, static_url_path='/static',
            template_folder='templates', static_folder='static')


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/cabos')
def cabos():
    return render_template("dimensionamento_Cabos/cabos.html")


@app.route('/longituginais')
def longituginais():
    return render_template("linhas_transmissao/longituginais.html")

@app.route('/transversais')
def transversais():
    return render_template("linhas_transmissao/transversais.html")

@app.route('/resultadolt_long', methods=['GET', 'POST'])
def resultadolt_long():
    data_atual = datetime.datetime.now()
    dia = data_atual.day
    mes = data_atual.month
    ano = data_atual.year

    # Formato desejado para a data (dia/mês/ano)
    data_formatada = f"{dia}/{mes}/{ano}"
    nome_projeto = request.form['nome_projeto']
    tensao_linha = request.form['tensao']
    distancia = request.form['tipo_distancia']
    freq = request.form['freq']
    Z_solo_carson, Z_transposta, Z_ntransposta, Z_solo_carson_complex, Z_solo_transposta_complex = metodocarson()
    impedancias1, impedancias2, impedancias3 = calcular_impedancia(Z_solo_carson_complex, Z_solo_transposta_complex)
    plot_encoded = grafico(impedancias1, impedancias2, impedancias3)
   
    Z_solo = metododasimagens()
    dados = {
        'nome_projeto': nome_projeto,
        'Z_solo': Z_solo,
        'Z_solo_carson': Z_solo_carson,
        'Z_transposta': Z_transposta,
        'Z_ntransposta': Z_ntransposta,
        'tensao_linha': tensao_linha,
        'plot_encoded': plot_encoded,
        'freq': freq,
        'distancia': distancia,
        'data': data_formatada}

    distancias_ate_imagem, distancias_entre_condutores, nome_distancia_condutores = calcular_distancias()
    return render_template('linhas_transmissao/r_lt_long.html', dist_imagens=distancias_ate_imagem, dist_entre_condutores=distancias_entre_condutores, condutores=nome_distancia_condutores,
                           dados=dados)

@app.route('/escolhametodo')
def escolhametodo():
    return render_template("linhas_transmissao/escolhametodo.html")


@app.route('/resultadolt_tran', methods=['GET', 'POST'])
def resultadolt_tran():
    data_atual = datetime.datetime.now()
    dia = data_atual.day
    mes = data_atual.month
    ano = data_atual.year

    # Formato desejado para a data (dia/mês/ano)
    data_formatada = f"{dia}/{mes}/{ano}"
    nome_projeto = request.form['nome_projeto']
    tensao_linha = request.form['tensao']
    distancia = request.form['tipo_distancia']
    freq = request.form['freq']
    
    P_shunt, C_shunt, capacitancias = capacitancia()
    dados = {
        'nome_projeto': nome_projeto,
        'coeficiente_potecial_proprio': P_shunt,
        'coeficiente_potecial_mutuo': C_shunt,
        'capacitancias' : capacitancias,
        'freq': freq,
        'distancia': distancia,
        'data': data_formatada}

    distancias_ate_imagem, distancias_entre_condutores, nome_distancia_condutores = calcular_distancias()
    return render_template('linhas_transmissao/r_lt_tran.html', dist_imagens=distancias_ate_imagem, dist_entre_condutores=distancias_entre_condutores, condutores=nome_distancia_condutores,
                           dados=dados)



if __name__ == '__main__':
    app.run(host='172.16.231.103', port='5000', debug=True)
