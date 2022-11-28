from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from database import db
from encrypt import bcrypt
from flask_migrate import Migrate
from config import BaseConfig
from routes.imges.images import imageUser
from routes.user.user import appuser

app = Flask(__name__)
app.register_blueprint(appuser)
app.register_blueprint(imageUser)
app.config.from_object(BaseConfig)

CORS(app)

bcrypt.init_app(app)
db.init_app(app)
# configurar flask-migrate
migrate = Migrate()
migrate.init_app(app, db)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)






