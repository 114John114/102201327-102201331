from flask import Blueprint, render_template, request, redirect, url_for, session

main = Blueprint('main', __name__)

# 临时存储用户信息(实际上应存储在数据库中）
users = {}

@main.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('main.login'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 注册逻辑：简单存储用户信息
        if username in users:
            return '用户名已存在，请重新注册！'
        users[username] = password
        return redirect(url_for('main.login'))  # 注册成功后重定向到登录页面

    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 验证用户信息
        if username in users and users[username] == password:
            session['username'] = username  # 记录登录状态
            return redirect(url_for('main.home'))  # 登录成功后重定向到主页
        return '用户名或密码错误！'

    return render_template('login.html')

@main.route('/logout')
def logout():
    session.pop('username', None)  # 注销用户
    return redirect(url_for('main.login'))
