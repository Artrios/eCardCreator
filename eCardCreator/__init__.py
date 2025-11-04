import os

from flask import Flask
from flask.helpers import send_file

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    @app.route('/data/<lang>/<file_name>')
    def get_data(lang,file_name):
        return send_file(f"data/{lang}/{file_name}")
    
    @app.route('/data/images/<file_name>')
    def get_image(file_name):
        return send_file(f"data/images/{file_name}")

    @app.route('/data/images/trainers/<file_name>')
    def get_trainer(file_name):
        return send_file(f"data/images/trainers/{file_name}")
    
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import ecard
    app.register_blueprint(ecard.bp)

    return app
