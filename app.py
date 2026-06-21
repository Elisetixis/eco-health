from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        conexao = sqlite3.connect("database.db")
        cursor = conexao.cursor()

        cursor.execute("""
        SELECT * FROM usuarios
        WHERE email = ?
        AND senha = ?
        """, (email, senha))

        usuario = cursor.fetchone()
        conexao.close()

        if usuario:
            return redirect("/dashboard")

        return "Email ou senha inválidos!"

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    conexao = sqlite3.connect("database.db")
    cursor = conexao.cursor()

    cursor.execute("SELECT COUNT(*) FROM idosos")
    total_idosos = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM medicamentos")
    total_medicamentos = cursor.fetchone()[0]

    cursor.execute("SELECT * FROM idosos")
    idosos = cursor.fetchall()

    cursor.execute("""
    SELECT 
    medicamentos.id,
    idosos.nome,
    medicamentos.nome_medicamento,
    medicamentos.dosagem,
    medicamentos.horario,
    medicamentos.observacoes
    FROM medicamentos
    INNER JOIN idosos
    ON medicamentos.idoso_id = idosos.id
    """)

    medicamentos = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM tarefas")
    total_tarefas = cursor.fetchone()[0]

    cursor.execute("""
SELECT
    tarefas.id,
    idosos.nome,
    tarefas.descricao,
    tarefas.data,
    tarefas.hora,
    tarefas.status,
    tarefas.observacao
    FROM tarefas
    INNER JOIN idosos
    ON tarefas.idoso_id = idosos.id
    """)

    tarefas = cursor.fetchall()

    conexao.close()

    return render_template(
    "dashboard.html",
    total_idosos=total_idosos,
    total_medicamentos=total_medicamentos,
    total_tarefas=total_tarefas,
    idosos=idosos,
    medicamentos=medicamentos,
    tarefas=tarefas
)


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]
        confirmar_senha = request.form["confirmar_senha"]
        telefone = request.form["telefone"]
        tipo_usuario = request.form["tipo_usuario"]

        if senha != confirmar_senha:
            return "As senhas não coincidem!"

        conexao = sqlite3.connect("database.db")
        cursor = conexao.cursor()

        cursor.execute("""
        INSERT INTO usuarios (nome, email, senha, telefone, tipo_usuario)
        VALUES (?, ?, ?, ?, ?)
        """, (nome, email, senha, telefone, tipo_usuario))

        conexao.commit()
        conexao.close()

        return redirect("/")

    return render_template("cadastro.html")

@app.route("/cadastrar_idoso", methods=["GET", "POST"])
def cadastrar_idoso():
    if request.method == "POST":
        nome = request.form["nome"]
        idade = request.form["idade"]
        sexo = request.form["sexo"]
        telefone_responsavel = request.form["telefone_responsavel"]
        observacoes = request.form["observacoes"]

        usuario_id = 1

        conexao = sqlite3.connect("database.db")
        cursor = conexao.cursor()

        cursor.execute("""
        INSERT INTO idosos (nome, idade, sexo, telefone_responsavel, observacoes, usuario_id)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (nome, idade, sexo, telefone_responsavel, observacoes, usuario_id))

        conexao.commit()
        conexao.close()

        return redirect("/dashboard")

    return render_template("cadastrar_idoso.html")

@app.route("/excluir_idoso/<int:id>")
def excluir_idoso(id):

    conexao = sqlite3.connect("database.db")
    cursor = conexao.cursor()

    cursor.execute(
        "DELETE FROM idosos WHERE id = ?",
        (id,)
    )

    conexao.commit()
    conexao.close()

    return redirect("/dashboard")

@app.route("/editar_idoso/<int:id>", methods=["GET", "POST"])
def editar_idoso(id):

    conexao = sqlite3.connect("database.db")
    cursor = conexao.cursor()

    if request.method == "POST":
        nome = request.form["nome"]
        idade = request.form["idade"]
        sexo = request.form["sexo"]
        telefone_responsavel = request.form["telefone_responsavel"]
        observacoes = request.form["observacoes"]

        cursor.execute("""
        UPDATE idosos
        SET nome = ?, idade = ?, sexo = ?, telefone_responsavel = ?, observacoes = ?
        WHERE id = ?
        """, (nome, idade, sexo, telefone_responsavel, observacoes, id))

        conexao.commit()
        conexao.close()

        return redirect("/dashboard")

    cursor.execute("SELECT * FROM idosos WHERE id = ?", (id,))
    idoso = cursor.fetchone()

    conexao.close()

    return render_template("editar_idoso.html", idoso=idoso)


@app.route("/cadastrar_medicamento", methods=["GET", "POST"])
def cadastrar_medicamento():

    conexao = sqlite3.connect("database.db")
    cursor = conexao.cursor()

    if request.method == "POST":

        nome_medicamento = request.form["nome_medicamento"]
        dosagem = request.form["dosagem"]
        horario = request.form["horario"]
        observacoes = request.form["observacoes"]
        idoso_id = request.form["idoso_id"]

        cursor.execute("""
        INSERT INTO medicamentos
        (
            nome_medicamento,
            dosagem,
            horario,
            observacoes,
            idoso_id
        )
        VALUES (?, ?, ?, ?, ?)
        """, (
            nome_medicamento,
            dosagem,
            horario,
            observacoes,
            idoso_id
        ))

        conexao.commit()
        conexao.close()

        return redirect("/dashboard")

    cursor.execute("SELECT * FROM idosos")
    idosos = cursor.fetchall()

    conexao.close()

    return render_template(
        "cadastrar_medicamento.html",
        idosos=idosos
    )

@app.route("/cadastrar_tarefa", methods=["GET", "POST"])
def cadastrar_tarefa():

    conexao = sqlite3.connect("database.db")
    cursor = conexao.cursor()

    if request.method == "POST":
        descricao = request.form["descricao"]
        data = request.form["data"]
        hora = request.form["hora"]
        status = request.form["status"]
        observacao = request.form["observacao"]
        idoso_id = request.form["idoso_id"]

        cursor.execute("""
        INSERT INTO tarefas (
            descricao,
            data,
            hora,
            status,
            observacao,
            idoso_id
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            descricao,
            data,
            hora,
            status,
            observacao,
            idoso_id
        ))

        conexao.commit()
        conexao.close()

        return redirect("/dashboard")

    cursor.execute("SELECT * FROM idosos")
    idosos = cursor.fetchall()

    conexao.close()

    return render_template(
        "cadastrar_tarefa.html",
        idosos=idosos
    )

@app.route("/excluir_tarefa/<int:id>")
def excluir_tarefa(id):
    conexao = sqlite3.connect("database.db")
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM tarefas WHERE id = ?", (id,))

    conexao.commit()
    conexao.close()

    return redirect("/dashboard")

@app.route("/concluir_tarefa/<int:id>")
def concluir_tarefa(id):

    conexao = sqlite3.connect("database.db")
    cursor = conexao.cursor()

    cursor.execute("""
    UPDATE tarefas
    SET status = 'Concluída'
    WHERE id = ?
    """, (id,))

    conexao.commit()
    conexao.close()

    return redirect("/dashboard")


@app.route("/reabrir_tarefa/<int:id>")
def reabrir_tarefa(id):

    conexao = sqlite3.connect("database.db")
    cursor = conexao.cursor()

    cursor.execute("""
    UPDATE tarefas
    SET status = 'Pendente'
    WHERE id = ?
    """, (id,))

    conexao.commit()
    conexao.close()

    return redirect("/dashboard")

@app.route("/editar_medicamento/<int:id>", methods=["GET", "POST"])
def editar_medicamento(id):

    conexao = sqlite3.connect("database.db")
    cursor = conexao.cursor()

    if request.method == "POST":

        nome = request.form["nome"]
        dosagem = request.form["dosagem"]
        horario = request.form["horario"]
        observacoes = request.form["observacoes"]

        cursor.execute("""
        UPDATE medicamentos
        SET nome_medicamento = ?,
            dosagem = ?,
            horario = ?,
            observacoes = ?
        WHERE id = ?
        """, (nome, dosagem, horario, observacoes, id))

        conexao.commit()
        conexao.close()

        return redirect("/dashboard")

    cursor.execute("""
    SELECT * FROM medicamentos
    WHERE id = ?
    """, (id,))

    medicamento = cursor.fetchone()

    conexao.close()

    return render_template(
        "editar_medicamento.html",
        medicamento=medicamento
    )

@app.route("/excluir_medicamento/<int:id>")
def excluir_medicamento(id):

    conexao = sqlite3.connect("database.db")
    cursor = conexao.cursor()

    cursor.execute("""
    DELETE FROM medicamentos
    WHERE id = ?
    """, (id,))

    conexao.commit()
    conexao.close()

    return redirect("/dashboard")

@app.route("/editar_tarefa/<int:id>", methods=["GET", "POST"])
def editar_tarefa(id):

    conexao = sqlite3.connect("database.db")
    cursor = conexao.cursor()

    if request.method == "POST":

        descricao = request.form["descricao"]
        data = request.form["data"]
        hora = request.form["hora"]
        status = request.form["status"]
        observacao = request.form["observacao"]

        cursor.execute("""
        UPDATE tarefas
        SET descricao=?,
            data=?,
            hora=?,
            status=?,
            observacao=?
        WHERE id=?
        """, (descricao, data, hora, status, observacao, id))

        conexao.commit()
        conexao.close()

        return redirect("/dashboard")

    cursor.execute("""
    SELECT * FROM tarefas
    WHERE id=?
    """, (id,))

    tarefa = cursor.fetchone()

    print(tarefa)

    conexao.close()

    return render_template(
        "editar_tarefa.html",
        tarefa=tarefa
    )


  


if __name__ == "__main__":
    app.run(debug=True)