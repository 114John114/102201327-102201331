from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = '2004'  # 设置秘钥，保护session

    from .routes import main
    app.register_blueprint(main)

    return app
