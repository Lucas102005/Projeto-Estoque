from flask import Blueprint, render_template, request, redirect, session
from models.user_model import buscar_usuario_por_email, inserir_usuario
from mysql.connector.errors import IntegrityError
import bcrypt

auth_bp = Blueprint('auth', __name__)

# ─── Emails que sempre entram como admin (nível 3) ────────────────────────────
ADMINS = {
    'lucas.sarmazo@gmail.com',
    # adicione mais emails aqui se precisar
}
# ─────────────────────────────────────────────────────────────────────────────

@auth_bp.route('/')
def home():
    return render_template('home.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha'].encode('utf-8')

        usuario = buscar_usuario_por_email(email)
        senha_hash = usuario['DS_SENHA'].encode('utf-8') if usuario else None

        if usuario and bcrypt.checkpw(senha, senha_hash):
            session['usuario_id'] = usuario['ID_USUARIO']
            session['nome']       = usuario['NM_USUARIO']
            session['funcao']     = usuario['DS_USUARIO']

            # Admin sobrescreve qualquer nível do banco
            if email.lower() in ADMINS:
                session['nivel'] = 3
            else:
                session['nivel'] = usuario['TP_PERMISSAO']

            return redirect('/estoque')
        else:
            return render_template('login.html', erro='Email ou senha inválidos.')

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@auth_bp.route('/usuarios/cadastrar', methods=['GET', 'POST'])
def cadastrar_usuario():
    if request.method == 'POST':
        nome       = request.form['nome']
        email      = request.form['email']
        senha_raw  = request.form['senha'].encode('utf-8')
        nascimento = request.form['nascimento']
        funcao     = request.form['funcao']
        genero     = request.form['genero']

        senha_hash = bcrypt.hashpw(senha_raw, bcrypt.gensalt()).decode('utf-8')
        nivel      = 2 if funcao == 'vendedor' else 1

        try:
            inserir_usuario(nome, email, senha_hash, nascimento, funcao, genero, nivel)
            return redirect('/login')
        except IntegrityError:
            return render_template('cadastrar_usuario.html', erro='Este email já está cadastrado.')

    return render_template('cadastrar_usuario.html')
