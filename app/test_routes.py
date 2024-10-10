# app/test_routes.py
import unittest
from app import create_app, mysql
from flask import url_for

class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.db = mysql.connection
        self.cursor = self.db.cursor()

    def tearDown(self):
        self.app_context.pop()

    def test_register(self):
        response = self.client.post(url_for('main.register'), data={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)  # 检查是否重定向到登录页面

        # 检查数据库中是否存在新注册的用户
        self.cursor.execute("SELECT * FROM users WHERE username = %s", ('testuser',))
        user = self.cursor.fetchone()
        self.assertIsNotNone(user)

    def test_login(self):
        # 先注册一个用户
        self.cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", ('testuser', 'testpassword'))
        self.db.commit()

        response = self.client.post(url_for('main.login'), data={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)  # 检查是否重定向到主页

        with self.client.session_transaction() as session:
            self.assertEqual(session['username'], 'testuser')  # 检查会话中是否记录了用户名

if __name__ == '__main__':
    unittest.main()