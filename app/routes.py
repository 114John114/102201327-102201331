from flask import Blueprint, render_template, request, redirect, url_for, session, Flask
import MySQLdb.cursors
from . import mysql


main = Blueprint('main', __name__)

@main.route('/show_session')
def show_session():
    return str(session)

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
        return render_template('hall.html', username=session['username'], projects=projects)
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

    return render_template('index.html')

@main.route('/logout')
def logout():
    session.pop('username', None)  # 注销用户
    return redirect(url_for('main.login'))

@main.route('/myprojects')
def myprojects():
    if 'username' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""
            SELECT p.id, p.project_name,p.project_type, p.project_leader, p.description,  GROUP_CONCAT(m.name SEPARATOR ', ') AS members
            FROM projects p
            LEFT JOIN members m ON p.id = m.projectid
            WHERE p.project_leader = %s
            GROUP BY p.id, p.project_name
        """, (session['username'],))
        projects = cursor.fetchall()
        return render_template('yourproject.html', username=session['username'], projects=projects)
    return redirect(url_for('main.login'))

@main.route('/message')
def message():
    return render_template('message.html')

@main.route('/myhome')
def myhome():
    return render_template('myhome.html')

@main.route('/createproject', methods=['GET', 'POST'])
def createproject():
    if request.method == 'POST':
        project_name = request.form['project-name']
        project_type = request.form['create_category']
        description = request.form['description']
        requirements = request.form['participants']
        maxmembers = request.form['participants-number']
        image = request.form['image']
        members = request.form['members']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO projects (project_name, project_type, project_leader, description, project_image, requirements, maxmembers) VALUES (%s, %s, %s, %s)", (project_name, project_type, session['username'], description, image, requirements, maxmembers))
        mysql.connection.commit()
        projectid = cursor.lastrowid
        members = members.split(',')
        for member in members:
            cursor.execute("INSERT INTO members (projectid, name) VALUES (%s, %s)", (projectid, member))
            mysql.connection.commit()
        return redirect(url_for('main.home'))
    return render_template('create-project.html')

@main.route('/project/<int:project_id>')
def project(project_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM projects WHERE id = %s", (project_id,))
    project = cursor.fetchone()
    cursor.execute("SELECT * FROM members WHERE projectid = %s", (project_id,))
    members = cursor.fetchall()
    return render_template('project.html', project=project, members=members)

@main.route('/editproject/<int:project_id>', methods=['GET', 'POST'])
def editproject(project_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM projects WHERE id = %s", (project_id,))
    project = cursor.fetchone()
    cursor.execute("SELECT * FROM members WHERE projectid = %s", (project_id,))
    members = cursor.fetchall()
    if request.method == 'POST':
        project_name = request.form['project-name']
        project_type = request.form['create_category']
        description = request.form['description']
        requirements = request.form['participants']
        maxmembers = request.form['participants-number']
        image = request.form['image']
        members = request.form['members']
        cursor.execute("UPDATE projects SET project_name=%s, project_type=%s, description=%s, project_image=%s, requirements=%s, maxmembers=%s WHERE id=%s", (project_name, project_type, description, image, requirements, maxmembers, project_id))
        mysql.connection.commit()
        cursor.execute("DELETE FROM members WHERE projectid = %s", (project_id,))
        members = members.split(',')
        for member in members:
            cursor.execute("INSERT INTO members (projectid, name) VALUES (%s, %s)", (project_id, member))
            mysql.connection.commit()
        return redirect(url_for('main.home'))
    return render_template('edit-project.html', project=project, members=members)

@main.route('/deleteproject/<int:project_id>')
def deleteproject(project_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("DELETE FROM projects WHERE id = %s", (project_id,))
    mysql.connection.commit()
    cursor.execute("DELETE FROM members WHERE projectid = %s", (project_id,))
    mysql.connection.commit()
    return redirect(url_for('main.home'))

