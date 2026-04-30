from flask import Blueprint, render_template, session, redirect
from models.user_model import listar_usuarios, excluir_usuario

user_bp = Blueprint('user', __name__)

@user_bp.route('/usuarios')
def listar():
    if 'nivel' not in session:
        return redirect('/login')
    usuarios = listar_usuarios()
    return render_template('listar_usuarios.html', usuarios=usuarios, nivel=session.get('nivel'))

@user_bp.route('/usuarios/excluir/<int:id>', methods=['POST'])
def deletar_usuario(id):
    if session.get('nivel') != 3:          # só admin pode excluir
        return redirect('/usuarios')
    if id == session.get('usuario_id'):    # não se exclui
        return redirect('/usuarios')
    excluir_usuario(id)
    return redirect('/usuarios')
