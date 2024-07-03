from flask import Flask
from config import config_app

def create_app():
    app = Flask(__name__, static_url_path='/static')

    config_app(app)

    from .controllers.user_controllers import user
    from .controllers.author_controllers import auth
    from .controllers.main_controllers import main
    from .controllers.post_controllers import post

    app.register_blueprint(user)
    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(post)

    from config import init_mysql

    mysql = init_mysql(app)
    app.mysql = mysql

    return app