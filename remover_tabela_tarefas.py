import sqlite3

conexao = sqlite3.connect("database.db")
cursor = conexao.cursor()

cursor.execute("DROP TABLE tarefas")

conexao.commit()
conexao.close()

print("Tabela tarefas removida!")