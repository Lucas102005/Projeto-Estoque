from database import conectar

def inserir_produto(nome, descricao, preco, quantidade):
    conexao = conectar()
    cursor = conexao.cursor()
    sql = """
        INSERT INTO produtos (NM_PRODUTO, DS_PRODUTO, VR_PRODUTO, QT_PRODUTO)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(sql, (nome, descricao, preco, quantidade))
    conexao.commit()
    cursor.close()
    conexao.close()

def listar_produtos():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM produtos")
    dados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return dados

def buscar_produto_por_id(id_produto):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM produtos WHERE ID_PRODUTO = %s", (id_produto,))
    produto = cursor.fetchone()
    cursor.close()
    conexao.close()
    return produto

def atualizar_produto(id_produto, nome, descricao, preco, quantidade):
    conexao = conectar()
    cursor = conexao.cursor()
    sql = """
        UPDATE produtos
        SET NM_PRODUTO = %s, DS_PRODUTO = %s, VR_PRODUTO = %s, QT_PRODUTO = %s
        WHERE ID_PRODUTO = %s
    """
    cursor.execute(sql, (nome, descricao, preco, quantidade, id_produto))
    conexao.commit()
    cursor.close()
    conexao.close()

def excluir_produto(id_produto):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM produtos WHERE ID_PRODUTO = %s", (id_produto,))
    conexao.commit()
    cursor.close()
    conexao.close()
