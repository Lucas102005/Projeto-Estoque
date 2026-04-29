from database import conectar
import bcrypt


def inserir_usuario(nome, email, data_nascimento, funcao, genero, senha):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO usuarios
        (NM_USUARIO, DS_EMAIL, DT_NASCIMENTO, DS_USUARIO, DS_GENERO, DS_SENHA)
        VALUES (%s, %s, %s, %s, %s, %s)'
    """

    senha_hash = bcrypt.hashpw(
        senha.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    cursor.execute(
        sql, (
            nome, 
            email,
            data_nascimento, 
            funcao, 
            genero, 
            senha_hash
        )
    )

    conexao.commit()
    conexao.close()


def listar_usuarios():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios")
    dados = cursor.fetchall()

    cursor.close()
    conexao.close()

    return dados


def buscar_usuario_por_email(email):

    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM usuarios WHERE DS_EMAIL = %s",
        (email,)
    )

    usuario = cursor.fetchone()

    conexao.close()

    return usuario


def verificar_senha(senha_digitada, senha_hash):
    return bcrypt.checkpw(
        senha_digitada.encode("utf-8"),
        senha_hash.encode("utf-8")
    )