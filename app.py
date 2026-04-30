from flask import Flask
from routes.user_route import user_bp
from routes.product_route import product_bp
from routes.auth_route import auth_bp

app = Flask(__name__)
app.secret_key = "estoque_2026_lucas_projeto"

app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(product_bp)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
