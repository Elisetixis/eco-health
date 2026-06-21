import sqlite3

conexao = sqlite3.connect("database.db")
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS idosos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    idade INTEGER NOT NULL,
    sexo TEXT NOT NULL,
    telefone_responsavel TEXT NOT NULL,
    observacoes TEXT,
    usuario_id INTEGER NOT NULL,

    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
)
""")

conexao.commit()
conexao.close()

print("Tabela idosos criada com sucesso!")