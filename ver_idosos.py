import sqlite3

conexao = sqlite3.connect("database.db")
cursor = conexao.cursor()

cursor.execute("SELECT * FROM idosos")

idosos = cursor.fetchall()

for idoso in idosos:
    print(idoso)

conexao.close()