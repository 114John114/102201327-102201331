
# SkillBridge
前言：
非常感谢您能够使用该产品，这是一款能够解决在大学环境中，因找不到志同道合的合作伙伴的问题。能够解决由于课程安排和个人想法的差异，难以协调时间和目标，导致合作难度加大的问题。这是一个集中的可持续发展的平台。


该项目是一个使用 Flask 和 MySQL 数据库的 Web 应用。以下是项目的详细说明和启动指南。有任何问题麻烦联系**QQ:1780774221**
若不想下载运行环境，可以打开**只有前端**文件夹，并直接跳转至[纯前端](#section1)

## 克隆仓库

首先，你需要克隆本项目的 Git 仓库：

```bash
git clone https://github.com/114John114/102201327-102201331.git
```

## 安装 MySQL 数据库

确保你的系统已经安装了 MySQL 数据库。如果尚未安装，请根据你的操作系统进行安装。

创建指定的数据库和表：

1. 登录到 MySQL 服务器：

   ```bash
   mysql -u root -p
   ```

2. 创建数据库：

   ```sql
   CREATE DATABASE skillbridge;
   ```

3. 创建指定的表（根据你的项目需求定义 SQL 语句）：

   ```sql
   USE skillbridge;
   CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    img VARCHAR(255),
    mail VARCHAR(255),
    schedule VARCHAR(511)
    );

    CREATE TABLE projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_type ENUM('competition', 'research') NOT NULL,
    project_name VARCHAR(255) NOT NULL,
    project_leader VARCHAR(255) NOT NULL,
    description TEXT,
    project_image VARCHAR(255),
    requirements TEXT,
    maxmembers INT
    );

    CREATE TABLE members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    projectid INT,
    name VARCHAR(255) NOT NULL,
    userid INT,
    FOREIGN KEY (projectid) REFERENCES projects(id),
    FOREIGN KEY (userid) REFERENCES users(id)
    );

    CREATE TABLE applicants (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    username VARCHAR(255) NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (username) REFERENCES users(username)
    );
   ```

## 使用 VSCode 或其他编辑器

使用你选择的代码编辑器打开项目目录。

## 安装依赖

我们建议使用 Conda 虚拟环境来管理项目的依赖。以下是设置环境和安装依赖的步骤：

1. 创建一个新的 Conda 虚拟环境（Python 3.12.4）：

   ```bash
   conda create -n myenv python=3.12.4
   ```

2. 激活虚拟环境：

   ```bash
   conda activate myenv
   ```

3. 安装 Flask：

   ```bash
   conda install flask
   ```

4. 安装 Flask-MySQLdb：

   ```bash
   pip install flask-mysqldb
   ```

## 运行项目

在终端中，确保你位于项目的根目录下，然后运行：

```bash
python run.py
```

这将启动 Flask 应用，你可以通过浏览器访问应用了。

## 注意事项

- 确保你的 MySQL 服务正在运行。
- 根据你的项目配置，你可能需要设置环境变量，如数据库的用户名、密码、主机等。
- 在开发过程中，确保你的 Conda 虚拟环境一直处于激活状态。

<a id="section1"></a>
# 软件使用方法
## 登录界面
- 点击网页
> Index.html

即可进入登录界面，并可以进行登录与注册操作

## 查看项目
在登录后进入项目大厅，即可查看各个项目
> 若您使用的是 **纯前端版本**，则可以在Index.html网页内点击登录直接进入

>或是打开hall.html网页进入项目大厅，点击后可以查看项目的各项信息
![](https://img2024.cnblogs.com/blog/3512925/202410/3512925-20241011013309238-1431004072.png)


## 编辑自己的项目
可以通过左侧的菜单栏点击进入菜单管理界面，在这里可以对项目的描述、需求等进行改动，也可以在这里管理项目人员，查看新的申请加入项目的人。
任何人都可以建立一个自己的项目，除了导师，也为想创业的大学生提供了便利的服务。
> ![](https://img2024.cnblogs.com/blog/3512925/202410/3512925-20241011013756061-24980414.png)
> ![](https://img2024.cnblogs.com/blog/3512925/202410/3512925-20241011013501444-1003960196.png)
> ![](https://img2024.cnblogs.com/blog/3512925/202410/3512925-20241011013729631-1762292857.png)


## 消息
可以发消息。
## 个人主页
在这里可以查看或编写个人信息，以供他人查看，可以修改自己的名称、邮箱、密码、空余时间等。