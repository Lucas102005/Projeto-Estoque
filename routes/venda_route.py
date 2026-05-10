from flask import Blueprint, render_template, request, redirect, session
from models.venda_model import (criar_venda, listar_vendas_pendentes,
                                listar_itens_venda, aprovar_venda,
                                rejeitar_venda, listar_vendas_usuario)
from models.product_model import listar_produtos

venda_bp = Blueprint('venda', __name__)

@venda_bp.route('/comprar')
def comprar():
    if 'nivel' not in session:
        return redirect('/login')
    if session.get('nivel') != 1:
        return redirect('/estoque')
    produtos = listar_produtos()
    return render_template('comprar.html', produtos=produtos)

@venda_bp.route('/comprar/finalizar', methods=['POST'])
def finalizar_compra():
    if session.get('nivel') != 1:
        return redirect('/login')

    itens = []
    for key, value in request.form.items():
        if key.startswith('quantidade_') and int(value) > 0:
            id_produto = int(key.replace('quantidade_', ''))
            preco      = float(request.form.get(f'preco_{id_produto}', 0))
            itens.append({
                'id_produto':  id_produto,
                'quantidade':  int(value),
                'vr_unitario': preco
            })

    if not itens:
        return redirect('/comprar')

    criar_venda(session['usuario_id'], itens)
    return redirect('/minhas-compras')

@venda_bp.route('/minhas-compras')
def minhas_compras():
    if session.get('nivel') != 1:
        return redirect('/login')
    vendas = listar_vendas_usuario(session['usuario_id'])
    return render_template('minhas_compras.html', vendas=vendas)

@venda_bp.route('/pedidos')
def pedidos():
    if session.get('nivel') not in (2, 3):
        return redirect('/estoque')
    pendentes = listar_vendas_pendentes()
    for v in pendentes:
        v['itens'] = listar_itens_venda(v['ID_VENDA'])
    return render_template('pedidos.html', pendentes=pendentes)

@venda_bp.route('/pedidos/aprovar/<int:id>', methods=['POST'])
def aprovar(id):
    if session.get('nivel') not in (2, 3):
        return redirect('/pedidos')
    aprovar_venda(id)
    return redirect('/pedidos')

@venda_bp.route('/pedidos/rejeitar/<int:id>', methods=['POST'])
def rejeitar(id):
    if session.get('nivel') not in (2, 3):
        return redirect('/pedidos')
    rejeitar_venda(id)
    return redirect('/pedidos')