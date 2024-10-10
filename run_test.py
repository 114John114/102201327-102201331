import unittest
from flask_testing import TestCase
from your_application import create_app, mysql  # 导入你的应用程序和数据库连接
from config import TestingConfig  # 导入测试配置

class MainRouteTests(TestCase):
    def create_app(self):
        # 创建一个使用测试配置的 Flask 应用程序
        app = create_app(TestingConfig)  # 使用 TestingConfig
        return app

    def setUp(self):
        # 设置测试数据库及其他必要的初始化
        self.app = self.create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()  # 推送应用上下文

        # 初始化测试数据库和表格
        with mysql.connection.cursor() as cursor:
            cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255), img VARCHAR(255), mail VARCHAR(255), schedule VARCHAR(255))")
            cursor.execute("CREATE TABLE IF NOT EXISTS projects (id INT AUTO_INCREMENT PRIMARY KEY, project_name VARCHAR(255), project_type VARCHAR(255), project_leader VARCHAR(255), description TEXT, project_image VARCHAR(255), requirements TEXT, maxmembers INT)")
            cursor.execute("CREATE TABLE IF NOT EXISTS members (id INT AUTO_INCREMENT PRIMARY KEY, projectid INT, name VARCHAR(255), userid INT)")
            cursor.execute("CREATE TABLE IF NOT EXISTS applicants (id INT AUTO_INCREMENT PRIMARY KEY, project_id INT, username VARCHAR(255))")

            # 插入测试用户数据
            cursor.execute("INSERT INTO users (username, password) VALUES ('testuser', 'password123')")
            mysql.connection.commit()

    def tearDown(self):
        # 清理每个测试之后的环境
        with mysql.connection.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS applicants")
            cursor.execute("DROP TABLE IF EXISTS members")
            cursor.execute("DROP TABLE IF EXISTS projects")
            cursor.execute("DROP TABLE IF EXISTS users")
        self.app_context.pop()  # 弹出应用上下文

    def test_register_user(self):
        # 测试用户注册
        response = self.client.post('/register', data={'username': 'newuser', 'password': 'newpassword'})
        self.assertEqual(response.status_code, 302)  # 检查是否重定向到登录页面
        # 检查用户是否成功插入到数据库
        with mysql.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s", ('newuser',))
            user = cursor.fetchone()
            self.assertIsNotNone(user)  # 确保用户存在

    def test_login_user(self):
        # 测试用户登录
        response = self.client.post('/login', data={'username': 'testuser', 'password': 'password123'})
        self.assertEqual(response.status_code, 302)  # 检查是否重定向到主页

    def test_show_session(self):
        # 测试显示会话中的用户名
        with self.client:
            self.client.post('/login', data={'username': 'testuser', 'password': 'password123'})
            response = self.client.get('/show_session')
            self.assertIn(b'Username: testuser', response.data)  # 检查是否包含用户名

    def test_create_project(self):
        # 测试创建项目
        with self.client:
            self.client.post('/login', data={'username': 'testuser', 'password': 'password123'})
            response = self.client.post('/createproject', data={
                'manager': 'testuser',
                'project-name': 'Test Project',
                'category': 'competition',
                'description': 'Test project description',
                'participants': '2',
                'participants-number': '5',
                'image': ''
            })
            self.assertEqual(response.status_code, 302)  # 检查是否重定向到主页

    def test_logout_user(self):
        # 测试用户注销
        with self.client:
            self.client.post('/login', data={'username': 'testuser', 'password': 'password123'})
            response = self.client.get('/logout')
            self.assertEqual(response.status_code, 302)  # 检查是否重定向到登录页面
            response = self.client.get('/show_session')
            self.assertIn(b'Username: 未登录', response.data)  # 确保显示为未登录

    def test_my_projects(self):
        # 测试查看用户项目
        with self.client:
            self.client.post('/login', data={'username': 'testuser', 'password': 'password123'})
            self.client.post('/createproject', data={
                'manager': 'testuser',
                'project-name': 'Test Project',
                'category': 'Development',
                'description': 'Test project description',
                'participants': '2',
                'participants-number': '5',
                'image': ''
            })
            response = self.client.get('/myprojects')
            self.assertIn(b'Test Project', response.data)  # 检查项目是否在页面中

    def test_update_profile(self):
        # 测试更新用户信息
        with self.client:
            self.client.post('/login', data={'username': 'testuser', 'password': 'password123'})
            response = self.client.post('/update_profile', data={
                'username': 'testuser',
                'email': 'testuser@example.com',
                'password': '',
                'monday': '9-11',
                'tuesday': '',
                'wednesday': '',
                'thursday': '',
                'friday': '',
                'saturday': '',
                'sunday': '',
            })
            self.assertEqual(response.status_code, 302)  # 检查是否重定向到我的主页

    def test_delete_project(self):
        # 测试删除项目
        with self.client:
            self.client.post('/login', data={'username': 'testuser', 'password': 'password123'})
            self.client.post('/createproject', data={
                'manager': 'testuser',
                'project-name': 'Test Project to Delete',
                'category': 'Development',
                'description': 'This will be deleted',
                'participants': '2',
                'participants-number': '5',
                'image': ''
            })
            with mysql.connection.cursor() as cursor:
                cursor.execute("SELECT id FROM projects WHERE project_name = %s", ('Test Project to Delete',))
                project = cursor.fetchone()
                project_id = project['id']  # 获取项目ID
            response = self.client.get(f'/deleteproject/{project_id}')
            self.assertEqual(response.status_code, 302)  # 检查是否重定向到主页

    def test_project_details(self):
        # 测试查看项目详细信息
        with self.client:
            self.client.post('/login', data={'username': 'testuser', 'password': 'password123'})
            self.client.post('/createproject', data={
                'manager': 'testuser',
                'project-name': 'Project for Details',
                'category': 'Development',
                'description': 'Test project for details view',
                'participants': '2',
                'participants-number': '5',
                'image': ''
            })
            with mysql.connection.cursor() as cursor:
                cursor.execute("SELECT id FROM projects WHERE project_name = %s", ('Project for Details',))
                project = cursor.fetchone()
                project_id = project['id']  # 获取项目ID
            response = self.client.get(f'/project/{project_id}')
            self.assertIn(b'Project for Details', response.data)  # 检查项目名称是否在页面中

if __name__ == '__main__':
    unittest.main()  # 运行测试
