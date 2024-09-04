from flask import Flask
from extensions import db, migrate
from config import Config

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)

from routes import routes_bp

app.register_blueprint(routes_bp)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()
