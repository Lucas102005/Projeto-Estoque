from database import conectar

def inserir_usuario(nome, email, senha, nascimento, funcao, genero, nivel):
    conexao = conectar()
    cursor = conexao.cursor()
    sql = """
        INSERT INTO usuarios (NM_USUARIO, DS_EMAIL, DS_SENHA, DT_NASCIMENTO, DS_USUARIO, DS_GENERO, TP_PERMISSAO)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (nome, email, senha, nascimento, funcao, genero, nivel))
    conexao.commit()
    cursor.close()
    conexao.close()

def buscar_usuario_por_email(email):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE DS_EMAIL = %s", (email,))
    usuario = cursor.fetchone()
    cursor.close()
    conexao.close()
    return usuario

def listar_usuarios():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios")
    dados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return dados

def excluir_usuario(id_usuario):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM usuarios WHERE ID_USUARIO = %s", (id_usuario,))
    conexao.commit()
    cursor.close()
    conexao.close()
