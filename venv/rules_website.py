from flask import Flask, url_for


app = Flask(__name__)


@app.route('/rules')
def rules():
    return '''<img src="{}" alt="здесь должна была быть картинка, но не нашлась">
            <h1>Правила игры в "сундучки"</h1>'''.format(url_for('static', filename='img/rules.png'))


if __name__ == '__main__':
    app.run(port=5000)