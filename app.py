import os
import csv
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

os.environ['FLASK_DEBUG'] = 'True'

app.debug = os.environ.get('FLASK_DEBUG') == 'True'


@app.route('/')
def ola():
    return render_template('index.html')


@app.route('/glossario')
def glossario():

    glossario_de_termo = []

    with open('bd_glossario.csv', newline='', encoding='utf-8') as arquivo:
        reader = csv.reader(arquivo, delimiter=';')
        for i in reader:
            glossario_de_termo.append(i)

    return render_template('glossario.html', glossario=glossario_de_termo)


@app.route('/novo_termo')
def novo_termo():
    return render_template('adicionar_termo.html')


@app.route('/criar_termo', methods=['POST', ])
def criar_termo():
    termo = request.form['termo']
    definicao = request.form['definicao']

    with open('bd_glossario.csv', 'a', newline='', encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo, delimiter=';')
        writer.writerow([termo, definicao])

    return redirect(url_for('glossario'))


@app.route('/excluir_termo/<int:termo_id>', methods=['POST'])
def excluir_termo(termo_id):

    with open('bd_glossario.csv', 'r',  newline='') as file:
        reader = csv.reader(file)
        linhas = list(reader)

    for i, linha in enumerate(linhas):
        if i == termo_id:
            del linhas[i]
            break

    with open('bd_glossario.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(linhas)

    return redirect(url_for('glossario'))


@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


if __name__ == "__main__":
    app.run()
