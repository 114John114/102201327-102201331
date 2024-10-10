from flask import Blueprint, render_template, request, redirect, url_for, session, Flask, g, jsonify
import MySQLdb.cursors
from . import mysql


main = Blueprint('main', __name__)

@main.route('/show_session')
def show_session():
    username = session.get('username', '未登录')
    return f'Username: {username}'

@main.before_request
def load_user_avatar():
    if 'username' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE username = %s", (session['username'],))
        user = cursor.fetchone()
        g.userid = user['id']
        if user and user['img']:
            g.avatar_url = user['img']
        else:
            g.avatar_url = url_for('static', filename='images/avatar.png')
    else:
        '''g.avatar_url = url_for('static', filename='images/avatar.png')'''

@main.route('/')
def home():
    if 'username' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""
            SELECT p.id, p.project_name,p.project_leader, p.description, p.project_type, p.requirements, GROUP_CONCAT(m.name SEPARATOR ', ') AS members
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
    print('Session in myhome:', session)  # 调试信息
    if 'username' in session:
        print('---------------------myhome---------------------')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT username, mail, schedule FROM users WHERE username = %s", (session['username'],))
        user = cursor.fetchone()
        print('success get user:', user)
        if user and user['schedule']:
            schedule = user['schedule'].split(',')  # 假设schedule是一个逗号分隔的字符串
        else:
            schedule = []
        
        return render_template('myhome.html', username=session['username'], user=user, schedule=schedule)
    return redirect(url_for('main.login'))

@main.route('/update_profile', methods=['POST'])
def update_profile():
    print('---------------------update_profile---------------------')
    if 'username' in session:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        schedule = ','.join([
            request.form.get('monday', ''),
            request.form.get('tuesday', ''),
            request.form.get('wednesday', ''),
            request.form.get('thursday', ''),
            request.form.get('friday', ''),
            request.form.get('saturday', ''),
            request.form.get('sunday', ''),
        ])
        print('success get email:', email)
        print('success get schedule:', schedule)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if password:
            cursor.execute("""
                UPDATE users SET mail = %s, password = %s, schedule = %s WHERE username = %s
            """, (email, password, schedule, session['username']))
        else:
            cursor.execute("""
                UPDATE users SET mail = %s, schedule = %s WHERE username = %s
            """, (email, schedule, session['username']))
        mysql.connection.commit()
        return redirect(url_for('main.myhome'))
    return redirect(url_for('main.login'))

@main.route('/createproject', methods=['GET', 'POST'])
def createproject():
    if request.method == 'POST':
        project_leader = request.form['manager']
        project_name = request.form['project-name']
        project_type = request.form.get('category')
        description = request.form['description']
        requirements = request.form['participants']
        maxmembers = request.form['participants-number']
        image = request.form['image']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO projects (project_name, project_type, project_leader, description, project_image, requirements, maxmembers) VALUES (%s, %s, %s, %s, %s, %s, %s)", (project_name, project_type, project_leader, description, image, requirements, maxmembers))
        mysql.connection.commit()
        projectid = cursor.lastrowid
        cursor.execute("INSERT INTO members (projectid, name, userid) VALUES (%s, %s, %s)", (projectid, project_leader, g.userid))
        mysql.connection.commit()
        return redirect(url_for('main.home'))
    return render_template('create-project.html', username=session['username'],)

@main.route('/project/<int:project_id>')
def project(project_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM projects WHERE id = %s", (project_id,))
    project = cursor.fetchone()
    cursor.execute("SELECT * FROM members WHERE projectid = %s", (project_id,))
    members = cursor.fetchall()
    return render_template('project-details1.html', username=session['username'], project=project, members=members)

@main.route('/joinproject', methods=['POST'])
def joinproject():
    data = request.get_json()
    project_id = data.get('project_id')
    username = data.get('username')
    '''# 检查项目和用户是否存在
    if project_id not in projects:
        return jsonify({'success': False, 'message': '项目不存在'})
    if username not in users:
        return jsonify({'success': False, 'message': '用户不存在'})'''
    
    # 将用户加入数据库的applicants表中
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("INSERT INTO applicants (project_id, username) VALUES (%s, %s)", (project_id, username))
    mysql.connection.commit()
    return jsonify({'success': True, 'message': '申请已提交'})
    

@main.route('/editproject/<int:project_id>', methods=['GET', 'POST'])
def editproject(project_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM projects WHERE id = %s", (project_id,))
    project = cursor.fetchone()
    cursor.execute("SELECT * FROM members WHERE projectid = %s", (project_id,))
    members = cursor.fetchall()
    return render_template('project-edit1.html', username=session['username'], project=project, members=members)

@main.route('/updateproject/<int:project_id>', methods=['POST'])
def updateproject(project_id):
    try:
        print('---------------------updateproject---------------------')
        # 从请求中获取 JSON 数据
        data = request.get_json()

        # 检查是否接收到数据
        if not data:
            return jsonify({'success': False, 'message': '未收到有效的数据'})

        project_leader = data.get('project_leader')
        project_type = data.get('project_type')
        description = data.get('description')
        #maxmembers = data.get('maxmembers')

        # 更新数据库中的项目数据
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""
            UPDATE projects 
            SET project_type = %s, project_leader = %s, description = %s 
            WHERE id = %s
        """, (project_type, project_leader, description, project_id))
        
        mysql.connection.commit()

        # 返回成功响应
        return jsonify({"success": True, "message": "项目已保存"})  # 返回 JSON 格式的数据
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})  # 返回错误信息
    
@main.route('/newpartner/<int:project_id>')
def newpartner(project_id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT username FROM applicants WHERE project_id = %s", (project_id,))
    applicants = cur.fetchall()

    user_info = []
    for applicant in applicants:
        cur.execute("SELECT * FROM users WHERE username = %s", (applicant['username'],))
        user = cur.fetchone()
        user_info.append(user)

    return render_template('newpartner.html', username=session['username'], project_id=project_id, applicants=user_info)

@main.route('/newpartner/<int:project_id>/<string:username>')
def applicant_detail(project_id, username):
    # 根据 project_id 和 username 获取详细信息
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    applicant = cur.fetchone()
    if not applicant:
        return "Applicant not found", 404
    if applicant and applicant['schedule']:
            schedule = applicant['schedule'].split(',')  # 假设schedule是一个逗号分隔的字符串
    else:
        schedule = []
    # 渲染模板并显示用户详情
    return render_template('personalpage.html', project_id=project_id, applicant=applicant, schedule=schedule)

@main.route('/accept_application', methods=['POST'])
def acceptapplicant():
    data = request.get_json()
    project_id = data.get('project_id')
    username = data.get('username')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("DELETE FROM applicants WHERE project_id = %s AND username = %s", (project_id, username))
    mysql.connection.commit()
    cursor.execute("INSERT INTO members (projectid, name, userid) VALUES (%s, %s)", (project_id, username))
    mysql.connection.commit()
    return redirect(url_for('main.newpartner', project_id=project_id))

@main.route('/deleteproject/<int:project_id>')
def deleteproject(project_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("DELETE FROM projects WHERE id = %s", (project_id,))
    mysql.connection.commit()
    cursor.execute("DELETE FROM members WHERE projectid = %s", (project_id,))
    mysql.connection.commit()
    return redirect(url_for('main.home'))

