from database import conectar
from datetime import date

def criar_venda(id_usuario, itens):
    conexao = conectar()
    cursor = conexao.cursor()

    vr_total = sum(i['quantidade'] * i['vr_unitario'] for i in itens)

    cursor.execute("""
        INSERT INTO vendas (ID_USUARIO, VR_VENDA, DT_VENDA, ID_CLIENTE, DS_STATUS)
        VALUES (%s, %s, %s, %s, 'pendente')
    """, (id_usuario, vr_total, date.today(), id_usuario))

    id_venda = cursor.lastrowid

    for item in itens:
        cursor.execute("""
            INSERT INTO venda_itens (ID_VENDA, ID_PRODUTO, QT_PRODUTO, VR_UNITARIO)
            VALUES (%s, %s, %s, %s)
        """, (id_venda, item['id_produto'], item['quantidade'], item['vr_unitario']))

    conexao.commit()
    cursor.close()
    conexao.close()
    return id_venda

def listar_vendas_pendentes():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("""
        SELECT v.*, u.NM_USUARIO
        FROM vendas v
        JOIN usuarios u ON v.ID_USUARIO = u.ID_USUARIO
        WHERE v.DS_STATUS = 'pendente'
        ORDER BY v.DT_VENDA DESC
    """)
    dados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return dados

def listar_itens_venda(id_venda):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("""
        SELECT vi.*, p.NM_PRODUTO
        FROM venda_itens vi
        JOIN produtos p ON vi.ID_PRODUTO = p.ID_PRODUTO
        WHERE vi.ID_VENDA = %s
    """, (id_venda,))
    dados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return dados

def aprovar_venda(id_venda):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT ID_PRODUTO, QT_PRODUTO FROM venda_itens WHERE ID_VENDA = %s
    """, (id_venda,))
    itens = cursor.fetchall()

    for item in itens:
        cursor.execute("""
            UPDATE produtos SET QT_PRODUTO = QT_PRODUTO - %s WHERE ID_PRODUTO = %s
        """, (item[1], item[0]))

    cursor.execute("""
        UPDATE vendas SET DS_STATUS = 'aprovado' WHERE ID_VENDA = %s
    """, (id_venda,))

    conexao.commit()
    cursor.close()
    conexao.close()

def rejeitar_venda(id_venda):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        UPDATE vendas SET DS_STATUS = 'rejeitado' WHERE ID_VENDA = %s
    """, (id_venda,))
    conexao.commit()
    cursor.close()
    conexao.close()

def listar_vendas_usuario(id_usuario):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM vendas WHERE ID_USUARIO = %s ORDER BY DT_VENDA DESC
    """, (id_usuario,))
    dados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return dados