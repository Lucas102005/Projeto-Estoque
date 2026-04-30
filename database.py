import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="Lsarmazo",
        password="1996567",
        database="estudos"
    )
