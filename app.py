from flask import Flask
from routes.user_route import user_bp

app = Flask(__name__)
app.secret_key = "estoque_2026_lucas_projeto"

app.register_blueprint(user_bp)

if __name__ == "__main__":
    app.run(debug = True, port = 8000)
