import sqlite3

conexao = sqlite3.connect("database.db")
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS medicamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_medicamento TEXT NOT NULL,
    dosagem TEXT NOT NULL,
    horario TEXT NOT NULL,
    observacoes TEXT,
    idoso_id INTEGER NOT NULL,

    FOREIGN KEY (idoso_id) REFERENCES idosos(id)
)
""")

conexao.commit()
conexao.close()

print("Tabela medicamentos criada com sucesso!")