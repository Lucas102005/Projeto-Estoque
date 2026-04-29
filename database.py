import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="conexao",
        password="1234",
        database="estudos"
    )
