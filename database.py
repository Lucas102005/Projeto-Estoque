import psycopg2

def conectar():
    return psycopg2.connect(
        host="db.qmpmfxpskjyiseuzuond.supabase.co",
        database="postgres",
        user="postgres",
        password="r#sg_z%uG?/69Tr",
        port="5432"
    )
