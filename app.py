from flask import Flask, Response, redirect, render_template, request
from functions.calculolt import calcular_distancias
from functions.metodo_img import metododasimagens
from functions.carson import metodocarson
import datetime
# Importe a função do arquivo pdf_generator


app = Flask(__name__, static_url_path='/static',
            template_folder='templates', static_folder='static')


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/cabos')
def cabos():
    return render_template("cabos.html")


@app.route('/transmissao')
def transmissao():
    return render_template("transmissao.html")


@app.route('/resultadolt', methods=['GET', 'POST'])
def resultadolt():
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
    Z_solo_carson, Z_transposta, Z_ntransposta = metodocarson()
    Z_solo = metododasimagens()
    dados = {
        'nome_projeto': nome_projeto,
        'Z_solo': Z_solo,
        'Z_solo_carson': Z_solo_carson,
        'Z_transposta': Z_transposta,
        'Z_ntransposta': Z_ntransposta,
        'tensao_linha': tensao_linha,
        'freq': freq,
        'distancia': distancia,
        'data': data_formatada}

    distancias_ate_imagem, distancias_entre_condutores, nome_distancia_condutores = calcular_distancias()
    return render_template('r_lt.html', dist_imagens=distancias_ate_imagem, dist_entre_condutores=distancias_entre_condutores, condutores=nome_distancia_condutores, dados=dados)


if __name__ == '__main__':
    app.run(host='192.168.1.64', port='5000', debug=True)
