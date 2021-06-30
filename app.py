from flask import Flask, render_template, request
from webscraping import run_webscraping
from dtm import run_dtm
from ldawithgridsearch import run_lda
from configparser import ConfigParser

config_object = ConfigParser()
config_object.read("config.ini")
LDA_params = config_object["LDA"]

no_of_top_words = int(LDA_params['no_of_top_words'])
base_html = LDA_params['base']


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST', 'GET'])
def submit():
    if request.method == 'POST' or request.method == 'GET':
        product = request.form['product']
        if product == '':
            return render_template('index.html', message='Please enter required fields')
        else:
            file = run_webscraping(products_to_review=product)
            dtm, links = run_dtm(file)
            df = run_lda(dtm, links, no_of_top_words)
            return render_template('results.html', tables=[base_html % df.to_html(classes='data')], header="true")


if __name__ == '__main__':
    app.debug = True
    app.run()
