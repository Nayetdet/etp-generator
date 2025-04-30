from config import Config
from routes.etp_route import etp_bp
from flask import Flask

class AppFacade:
    
    def __init__(self):
        self.app = Flask(__name__)
    
    def configure_app(self):
        self.app.config['OPENAPI_KEY'] = Config.OPENAI_KEY

    def register_blueprints(self):
        self.app.register_blueprint(etp_bp)

    def create_app(self):
        self.configure_app()
        self.register_blueprints()
        return self.app
