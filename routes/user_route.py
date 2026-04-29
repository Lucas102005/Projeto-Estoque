from flask import Blueprint, render_template, request, redirect, session
from models.user_model import (
    inserir_usuario,
    listar_usuarios,
    buscar_usuario_por_email,
    verificar_senha
)
from models.estoque_model import (
    listar_itens_completo,
    listar_itens_basico
)
from datetime import datetime

user_bp = Blueprint("user", __name__)

@user_bp.route("/")
def home():

    if "usuario_id" not in session:
        return redirect("/login")

    if session.get("funcao") == "vendedor":
        return redirect("/painel-vendedor")
    else:
        return redirect("/painel-comprador")

@user_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        senha = request.form["senha"]

        usuario = buscar_usuario_por_email(email)

        if usuario and verificar_senha(senha, usuario["DS_SENHA"]):

            session["usuario_id"] = usuario["ID_USUARIO"]
            session["funcao"] = usuario["DS_USUARIO"]
            session["nivel"] = usuario["TP_PERMISSAO"]

            if usuario["DS_USUARIO"] == "vendedor":
                return redirect("/painel-vendedor")
            else:
                return redirect("/painel-comprador")

        return render_template("login.html", erro="Email ou senha inválidos")

    return render_template("login.html")

@user_bp.route("/logout")
def logout():

    session.clear()

    return redirect("/login")

@user_bp.route("/usuarios")
def usuarios():

    if "usuario_id" not in session:
        return redirect("/login")

    if session.get("nivel", 0) < 2:
        return "Acesso negado"

    lista = listar_usuarios()

    return render_template(
        "listar_usuarios.html",
        usuarios=lista,
        nivel=session.get("nivel", 0)
    )

@user_bp.route("/usuarios/cadastrar", methods=["GET", "POST"])
def cadastrar_usuario():

    if request.method == "POST":

        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]
        nascimento = request.form["nascimento"]
        funcao = request.form["funcao"]
        genero = request.form["genero"]

        data_formatada = datetime.strptime(
            nascimento,
            "%Y-%m-%d"
        ).date()

        inserir_usuario(
            nome,
            email,
            data_formatada,
            funcao,
            genero,
            senha
        )

        return redirect("/usuarios")

    return render_template("cadastrar_usuario.html")

@user_bp.route("/painel-vendedor")
def painel_vendedor():

    if "usuario_id" not in session:
        return redirect("/login")

    if session.get("funcao") != "vendedor":
        return "Acesso negado"

    return render_template("painel_vendedor.html")

@user_bp.route("/painel-comprador")
def painel_comprador():

    if "usuario_id" not in session:
        return redirect("/login")

    return render_template("painel_comprador.html")

@user_bp.route("/estoque")
def estoque():

    if "usuario_id" not in session:
        return redirect("/login")

    nivel = session.get("nivel", 0)

    if nivel >= 2:
        itens = listar_itens_completo()

    else:
        itens = listar_itens_basico()

    return render_template(
        "estoque.html",
        itens=itens,
        nivel=nivel
    )