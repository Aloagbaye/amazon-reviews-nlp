from flask import Flask, render_template, request
from webscraping import run_webscraping
from dtm import run_dtm
from ldawithgridsearch import run_lda


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        product = request.form['product']
        if product == '':
            return render_template('index.html', message='Please enter required fields')
        else:
            file = run_webscraping(products_to_review=product)
            dtm = run_dtm(file)
            df = run_lda(dtm, 5)
            return render_template('results.html', tables=[df.to_html(classes='data')], header="true")


if __name__ == '__main__':
    app.debug = True
    app.run()
