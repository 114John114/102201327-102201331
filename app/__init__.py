from flask import Flask
from flask_mysqldb import MySQL
from .config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB

mysql = MySQL()

def create_app():
    app = Flask(__name__)
    
    app.config['MYSQL_HOST'] = MYSQL_HOST
    app.config['MYSQL_USER'] = MYSQL_USER
    app.config['MYSQL_PASSWORD'] = MYSQL_PASSWORD
    app.config['MYSQL_DB'] = MYSQL_DB
    app.secret_key = '2004'

    mysql.init_app(app)
    from .routes import main
    app.register_blueprint(main)

    return app
