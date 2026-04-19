import sqlite3

conn = sqlite3.connect('projeto.db')
cursor = conn.cursor()

print("Iniciando correção do schema...")

# 1. Fazer backup dos dados existentes em projetos (se houver)
cursor.execute("SELECT COUNT(*) FROM projetos")
count = cursor.fetchone()[0]
print(f"Projetos existentes: {count}")

# 2. Dropar a tabela antiga com schema errado
cursor.execute("DROP TABLE IF EXISTS projetos")
print("Tabela 'projetos' antiga removida.")

# 3. Criar a tabela com o schema correto (INTEGER com AUTOINCREMENT)
cursor.execute("""
CREATE TABLE projetos (
    id INTEGER NOT NULL,
    nome_projeto VARCHAR,
    elementos_json JSON,
    data_criacao DATETIME,
    data_atualizacao DATETIME,
    owner_id INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY(owner_id) REFERENCES users (id)
)
""")
print("Tabela 'projetos' recriada com schema correto (id INTEGER).")

conn.commit()

# Verificar o novo schema
cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='projetos'")
result = cursor.fetchone()
print("Novo schema:", result[0])

conn.close()
print("Concluído com sucesso!")
