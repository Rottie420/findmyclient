from flask import Flask
from routes.main import main_bp
from config import APP_SECRET_KEY


app = Flask(__name__, static_folder='static',
        template_folder='templates'
    )
app.secret_key = APP_SECRET_KEY
app.register_blueprint(main_bp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
