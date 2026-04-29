import database

def inserir_produtos():
    try:
        nome = str(input("Nome do produto: "))
        descricao = str(input("Insira uma breve descrição do produto: "))
        preco = float(input("Valor do produto: "))
        quantidade = int(input("Quantidade: "))

        conexao = database.conectar()
        cursor = conexao.cursor()

        sql = """
        INSERT INTO produtos (
        NM_PRODUTO, 
        DS_PRODUTO,
        VR_PRODUTO, 
        QT_PRODUTO)
        VALUES (
        %s, 
        %s, 
        %s, 
        %s
        )
        """
        valores = (nome, descricao, preco, quantidade)

        cursor.execute(sql, valores)
        conexao.commit()

        print("Produto inserido com sucesso!")

    except ValueError:
        print("Preço e quantidade devem ser números.")

    except Exception as erro:
        print("Erro:", erro)

    finally:
        cursor.close()
        conexao.close()


inserir_produtos()