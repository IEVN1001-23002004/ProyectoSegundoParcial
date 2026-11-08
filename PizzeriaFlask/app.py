from flask import Flask, flash, get_flashed_messages
from flask_cors import CORS
from config import config
from database import mysql
from blueprints.pedidos import pedidos

app = Flask(__name__)

app.secret_key = 'pizzeria_clave_secreta'

CORS(app)

app.config.from_object(config['development'])

mysql.init_app(app)

app.register_blueprint(pedidos, url_prefix='/api/pedidos')


@app.route('/')
def inicio():
    return 'API Pizzeria funcionando'


@app.route('/prueba_db')
def prueba_db():
    cursor = mysql.connection.cursor()

    cursor.execute('SELECT DATABASE()')

    resultado = cursor.fetchone()

    cursor.close()

    return 'Conectado a: ' + resultado[0]


@app.route('/prueba_flash')
def prueba_flash():

    flash('Pedido registrado correctamente', 'success')

    mensajes = get_flashed_messages(with_categories=True)

    return {
        'mensajes': mensajes
    }


def pagina_no_encontrada(error):
    return "<h1> Pagina no Encontrada</h1>"


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(host='0.0.0.0', port=5000, debug=True)
