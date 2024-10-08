from flask import Blueprint, render_template, request, redirect, url_for, session, Flask
import MySQLdb.cursors
from . import mysql


main = Blueprint('main', __name__)

@main.route('/')
def home():
    if 'username' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""
            SELECT p.id, p.project_name,p.project_leader, p.description,  GROUP_CONCAT(m.name SEPARATOR ', ') AS members
            FROM projects p
            LEFT JOIN members m ON p.id = m.projectid
            GROUP BY p.id, p.project_name
        """)
        projects = cursor.fetchall()
        return render_template('home.html', username=session['username'], projects=projects)
    return redirect(url_for('main.login'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 注册逻辑：存储用户信息到 MySQL 数据库
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        account = cursor.fetchone()
        if account:
            return '用户名已存在，请重新注册！'
        else:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            mysql.connection.commit()
            return redirect(url_for('main.login'))  # 注册成功后重定向到登录页面

    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

         # 验证用户信息
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        account = cursor.fetchone()
        if account:
            session['username'] = username  # 记录登录状态
            return redirect(url_for('main.home'))  # 登录成功后重定向到主页
        else:
            return '用户名或密码错误！'

    return render_template('login.html')

@main.route('/logout')
def logout():
    session.pop('username', None)  # 注销用户
    return redirect(url_for('main.login'))
