from flask import Flask
from flask_cors import CORS
from view import main_views

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(main_views)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)