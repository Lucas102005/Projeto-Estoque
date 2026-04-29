from database import conectar

def listar_itens_completo():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM estoque")

    dados = cursor.fetchall()
    conn.close()
    return dados

def listar_itens_basico():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT DS_ITEM, NM_ITEM, QT_ITEM
        FROM estoque
    """)

    dados = cursor.fetchall()
    conn.close()
    return dados
