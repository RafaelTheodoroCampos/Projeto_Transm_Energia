from flask import Flask, render_template, request
from functions.bitola import calcular_bitola

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/cabos')
def cabos():
    return render_template("cabos.html")


@app.route('/results', methods=['GET', 'POST'])
def results():
    corrente_nominal = float(request.form['correnteNominal'])
    metodo_instalacao = request.form['metodoInstalacao']

    # Use a função calcular_bitola para obter a bitola
    bitola = calcular_bitola(corrente_nominal, metodo_instalacao)

    if bitola is not None:
        resultado = f"A bitola recomendada para {corrente_nominal} A e método de instalação {metodo_instalacao} é {bitola} mm²."
    else:
        resultado = "Não foi encontrada uma bitola adequada na tabela para os valores fornecidos."

    return render_template("results_cabos.html", resultado=resultado)
