from blueprints.pedidos import pedidos

def registrar_blueprints(app):
    app.register_blueprint(pedidos, url_prefix='/api/pedidos')

