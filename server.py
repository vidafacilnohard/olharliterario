#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask backend para Olhar Literário (serve frontend estático e fornece API simples)

Endpoints:
 - POST /api/register
 - POST /api/login
 - GET/POST /api/profile
 - POST /api/upload-photo
 - POST /api/comments
 - GET  /api/comments

Banco de dados: SQLite (database.db)
"""
from pathlib import Path
import sqlite3
import uuid
import os
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, send_from_directory, abort
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / 'database.db'
IMAGES_DIR = BASE_DIR / 'images'
IMAGES_DIR.mkdir(exist_ok=True)

app = Flask(__name__, static_folder=str(BASE_DIR), static_url_path='')


def get_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            email TEXT UNIQUE,
            password_hash TEXT,
            dataNascimento TEXT,
            telefone TEXT,
            bio TEXT,
            foto TEXT
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tokens (
            token TEXT PRIMARY KEY,
            user_id INTEGER,
            expires_at TEXT
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            book_title TEXT,
            comment TEXT,
            rating INTEGER,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()


def create_token(user_id):
    token = uuid.uuid4().hex
    expires = (datetime.utcnow() + timedelta(days=7)).isoformat()
    conn = get_db()
    conn.execute('INSERT INTO tokens (token, user_id, expires_at) VALUES (?,?,?)', (token, user_id, expires))
    conn.commit()
    conn.close()
    return token


def get_user_by_token(token):
    if not token:
        return None
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT user_id, expires_at FROM tokens WHERE token=?', (token,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return None
    if datetime.fromisoformat(row['expires_at']) < datetime.utcnow():
        # expired
        conn.close()
        return None
    user_id = row['user_id']
    cur.execute('SELECT id,nome,email,dataNascimento,telefone,bio,foto FROM users WHERE id=?', (user_id,))
    user = cur.fetchone()
    conn.close()
    return user


def auth_required(fn):
    def wrapper(*args, **kwargs):
        auth = request.headers.get('Authorization', '')
        token = ''
        if auth.startswith('Bearer '):
            token = auth.split(' ', 1)[1]
        user = get_user_by_token(token)
        if not user:
            return jsonify({'error': 'Unauthorized'}), 401
        request.user = user
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper


@app.route('/')
def index():
    return send_from_directory(str(BASE_DIR), 'index.html')


@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json() or {}
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')
    dataNascimento = data.get('dataNascimento')
    if not email or not senha or not nome:
        return jsonify({'error': 'Missing fields'}), 400
    pwd_hash = generate_password_hash(senha)
    conn = get_db()
    try:
        cur = conn.cursor()
        cur.execute('INSERT INTO users (nome,email,password_hash,dataNascimento) VALUES (?,?,?,?)', (nome, email, pwd_hash, dataNascimento))
        conn.commit()
        user_id = cur.lastrowid
    except Exception as e:
        conn.close()
        return jsonify({'error': 'Email already registered'}), 400
    conn.close()
    token = create_token(user_id)
    return jsonify({'user': {'id': user_id, 'nome': nome, 'email': email}, 'token': token})


@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json() or {}
    email = data.get('email')
    senha = data.get('senha')
    if not email or not senha:
        return jsonify({'error': 'Missing fields'}), 400
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT id,password_hash,nome FROM users WHERE email=?', (email,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return jsonify({'error': 'Invalid credentials'}), 400
    user_id = row['id']
    if not check_password_hash(row['password_hash'], senha):
        return jsonify({'error': 'Invalid credentials'}), 400
    token = create_token(user_id)
    return jsonify({'user': {'id': user_id, 'nome': row['nome'], 'email': email}, 'token': token})


@app.route('/api/profile', methods=['GET', 'POST'])
@auth_required
def api_profile():
    user = request.user
    if request.method == 'GET':
        return jsonify(dict(user))
    data = request.get_json() or {}
    nome = data.get('nome')
    telefone = data.get('telefone')
    bio = data.get('bio')
    dataNascimento = data.get('dataNascimento')
    conn = get_db()
    conn.execute('UPDATE users SET nome=?, telefone=?, bio=?, dataNascimento=? WHERE id=?', (nome, telefone, bio, dataNascimento, user['id']))
    conn.commit()
    conn.close()
    return jsonify({'success': True})


@app.route('/api/upload-photo', methods=['POST'])
@auth_required
def api_upload_photo():
    if 'file' not in request.files:
        return jsonify({'error': 'No file'}), 400
    f = request.files['file']
    if f.filename == '':
        return jsonify({'error': 'No filename'}), 400
    ext = os.path.splitext(f.filename)[1].lower()
    filename = f'user_{request.user["id"]}_' + uuid.uuid4().hex + ext
    dest = IMAGES_DIR / filename
    f.save(str(dest))
    conn = get_db()
    conn.execute('UPDATE users SET foto=? WHERE id=?', (str(dest.name), request.user['id']))
    conn.commit()
    conn.close()
    return jsonify({'foto': 'images/' + dest.name})


@app.route('/api/comments', methods=['POST', 'GET'])
def api_comments():
    if request.method == 'POST':
        auth = request.headers.get('Authorization', '')
        token = ''
        if auth.startswith('Bearer '):
            token = auth.split(' ', 1)[1]
        user = get_user_by_token(token)
        if not user:
            return jsonify({'error': 'Unauthorized'}), 401
        data = request.get_json() or {}
        book_title = data.get('book_title')
        comment = data.get('comment')
        rating = int(data.get('rating') or 0)
        conn = get_db()
        conn.execute('INSERT INTO comments (user_id,book_title,comment,rating,created_at) VALUES (?,?,?,?,?)', (user['id'], book_title, comment, rating, datetime.utcnow().isoformat()))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    else:
        book = request.args.get('book')
        conn = get_db()
        cur = conn.cursor()
        if book:
            cur.execute('SELECT c.*, u.nome as user_nome FROM comments c LEFT JOIN users u ON u.id=c.user_id WHERE book_title=? ORDER BY created_at DESC', (book,))
        else:
            cur.execute('SELECT c.*, u.nome as user_nome FROM comments c LEFT JOIN users u ON u.id=c.user_id ORDER BY created_at DESC')
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return jsonify(rows)


if __name__ == '__main__':
    init_db()
    port = 8000
    print('Starting Flask server on http://localhost:%d' % port)
    app.run(host='0.0.0.0', port=port)
