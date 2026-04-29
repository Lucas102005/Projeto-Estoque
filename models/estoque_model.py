from database import conectar

def listar_itens_completo():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute(
        "SELECT NM_ITEM, DS_ITEM, QT_ITEM FROM estoque"
    )

    dados = cursor.fetchall()
    conexao.close()

    return dados

def listar_itens_basico():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT DS_ITEM, NM_ITEM, QT_ITEM
        FROM estoque
    """)

    dados = cursor.fetchall()
    conexao.close()

    return dados