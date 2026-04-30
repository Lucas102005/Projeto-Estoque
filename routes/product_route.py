from flask import Blueprint, render_template, request, redirect, session
from models.product_model import inserir_produto, listar_produtos, buscar_produto_por_id, atualizar_produto, excluir_produto

product_bp = Blueprint('product', __name__)

@product_bp.route('/estoque')
def estoque():
    if 'nivel' not in session:
        return redirect('/login')
    produtos = listar_produtos()
    nivel = session.get('nivel', 0)
    return render_template('estoque.html', produtos=produtos, nivel=nivel)

@product_bp.route('/produtos/cadastrar', methods=['GET', 'POST'])
def cadastrar_produto():
    if session.get('nivel') not in (2, 3):
        return redirect('/estoque')
    if request.method == 'POST':
        inserir_produto(
            request.form['nome'],
            request.form['descricao'],
            float(request.form['preco']),
            int(request.form['quantidade'])
        )
        return redirect('/estoque')
    return render_template('cadastrar_produto.html')

@product_bp.route('/produtos/editar/<int:id>', methods=['GET', 'POST'])
def editar_produto(id):
    if session.get('nivel') not in (2, 3):
        return redirect('/estoque')
    produto = buscar_produto_por_id(id)
    if not produto:
        return redirect('/estoque')
    if request.method == 'POST':
        atualizar_produto(
            id,
            request.form['nome'],
            request.form['descricao'],
            float(request.form['preco']),
            int(request.form['quantidade'])
        )
        return redirect('/estoque')
    return render_template('editar_produto.html', produto=produto)

@product_bp.route('/produtos/excluir/<int:id>', methods=['POST'])
def deletar_produto(id):
    if session.get('nivel') not in (2, 3):
        return redirect('/estoque')
    excluir_produto(id)
    return redirect('/estoque')
