from flask import Flask, Response, redirect, render_template, request
from functions.calculolt import calcular_distancias

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

    distancias_ate_imagem, distancias_entre_condutores, nome_distancia_condutores = calcular_distancias()
    return render_template('r_lt.html', dist_imagens=distancias_ate_imagem, dist_entre_condutores=distancias_entre_condutores, condutores=nome_distancia_condutores)


if __name__ == '__main__':
    app.run(host='192.168.1.64', port='5000', debug=True)
