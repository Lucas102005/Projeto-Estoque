import database
import bcrypt


conectar = database.conectar()


def inserir_usuario(nome, email, data_nascimento, funcao, genero, senha):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO usuarios
        (NM_USUARIO, DS_EMAIL, DT_NASCIMENTO, DS_USUARIO, DS_GENERO, DS_SENHA)
        VALUES (%s, %s, %s, %s, %s, %s)'
    """

    senha_bytes = senha.encode("utf-8")
    salt = bcrypt.gensalt()
    senha_hash = bcrypt.hashpw(senha_bytes, salt)

    cursor.execute(
        sql, (
            nome, 
            email,
            data_nascimento, 
            funcao, 
            genero, 
            senha_hash.decode("utf-8")
        )
    )

    conexao.commit()
    conexao.close()


def verificar_senha(senha_digitada, senha_hash_banco):

    senha_digitada_bytes = senha_digitada.encode("utf-8")
    senha_hash_bytes = senha_hash_banco.encode("utf-8")

    return bcrypt.checkpw(senha_digitada_bytes, senha_hash_bytes)


def listar_usuarios():
    conexao = database.conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()

    cursor.close()
    conexao.close()

    return usuarios


def buscar_usuario_por_email(email):

    conexao = conectar
    cursor = conexao.cursor(dictionary=True)

    sql = "SELECT * FROM usuarios WHERE DS_EMAIL = %s"
    cursor.execute(sql, (email,))

    usuario = cursor.fetchone()

    cursor.close()
    conexao.close()

    return usuario


def buscar_usuario_por_email(email):

    conexao = conectar()  
    cursor = conexao.cursor(dictionary=True)

    sql = "SELECT * FROM usuarios WHERE DS_EMAIL = %s"
    cursor.execute(sql, (email,))

    usuario = cursor.fetchone()

    cursor.close()
    conexao.close()

    return usuario