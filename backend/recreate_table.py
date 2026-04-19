import sqlite3

conn = sqlite3.connect('projeto.db')
cursor = conn.cursor()

print("Recriando tabela projetos para corrigir o problema do ID...")

cursor.execute("DROP TABLE IF EXISTS projetos")

cursor.execute("""
CREATE TABLE projetos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_projeto VARCHAR,
    elementos_json JSON,
    data_criacao DATETIME,
    data_atualizacao DATETIME,
    owner_id INTEGER,
    FOREIGN KEY(owner_id) REFERENCES users (id)
)
""")

conn.commit()
print("Tabela recriada com sucesso!")

conn.close()
