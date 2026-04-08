from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Função para verificar as credenciais no banco de dados
def verificar_login(email, senha):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    
    # Busca o usuário com o e-mail e senha fornecidos
    cursor.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
    usuario = cursor.fetchone()
    
    conn.close()
    return usuario

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    senha = request.form.get('password')
    
    usuario = verificar_login(email, senha)
    
    if usuario:
        return f"Bem-vindo, {usuario[1]}! Login realizado com sucesso."
    else:
        return "Erro: E-mail ou senha incorretos!", 401

if __name__ == '__main__':
    app.run(debug=True)
    import sqlite3

conn = sqlite3.connect('usuarios.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL
    )
''')
# Inserindo um usuário de exemplo
cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES ('Admin', 'teste@email.com', '123456')")
conn.commit()
conn.close()
print("Banco de dados criado com sucesso!")
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'chave_secreta_super_segura_123' # Necess