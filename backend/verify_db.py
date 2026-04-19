import sqlite3

conn = sqlite3.connect('projeto.db')
cursor = conn.cursor()
cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='projetos'")
res = cursor.fetchone()
print("SCHEMA", res)

cursor.execute("SELECT count(*) FROM projetos")
print("COUNT", cursor.fetchone())
