import os
from flask import Flask
from config import Config
from routes import init_routes
from flask_wtf import CSRFProtect

# CSRF protection instance (initialized in create_app)
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(Config)

    # ativa proteção CSRF para formulários
    csrf.init_app(app)

    # garante diretório de PDFs
    pdf_dir = os.path.join(app.root_path, 'static', 'pdfs')
    os.makedirs(pdf_dir, exist_ok=True)

    # registrar rotas
    init_routes(app)

    # aviso amigável em logs de startup quando variáveis críticas não estão definidas
    if not app.config.get('PIX_KEY'):
        app.logger.warning('PIX_KEY não definido. Configure PIX_KEY nas variáveis de ambiente para gerar boletos via PIX.')

    return app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', '5001'))
    debug = os.environ.get('FLASK_DEBUG', '1') == '1'
    create_app().run(debug=debug, host='0.0.0.0', port=port)