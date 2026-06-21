import sqlite3

conexao = sqlite3.connect("database.db")
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tarefas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descricao TEXT NOT NULL,
    data TEXT NOT NULL,
    hora TEXT NOT NULL,
    status TEXT NOT NULL,
    observacao TEXT,
    idoso_id INTEGER NOT NULL,

    FOREIGN KEY (idoso_id) REFERENCES idosos(id)
)
""")

conexao.commit()
conexao.close()

print("Tabela tarefas criada com sucesso!")