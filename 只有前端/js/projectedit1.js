document.addEventListener('DOMContentLoaded', function() {
    // 示例项目数据
    const projectData = {
        name: '数学建模',
        category: '比赛',
        manager: 'John Doe',
        description: '这是一个数学建模项目',
        image: 'images/placeholder1.png', // 确保有这个图片文件
        requirements: '代码手, 建模手',
        recruitment: '10/20'
    };

    // 填充页面信息
    document.getElementById('projectName').textContent = projectData.name;
    document.getElementById('projectCategory').textContent = projectData.category;
    document.getElementById('projectManager').textContent = projectData.manager;
    document.getElementById('projectDescription').textContent = projectData.description;
    document.getElementById('projectImage').src = projectData.image;
    document.getElementById('projectRequirements').textContent = projectData.requirements;
    document.getElementById('projectRecruitment').textContent = projectData.recruitment;
});


// 处理成员按钮点击事件
document.querySelectorAll('.messageButton').forEach(button => {
    button.addEventListener('click', function() {
        const memberName = this.previousElementSibling.textContent;
        alert(`向 ${memberName} 发送信息...`); // 这里可以扩展为实际发送信息的逻辑
    });
});

// 删除项目按钮事件
document.getElementById('deleteButton').addEventListener('click', function() {
    const confirmation = confirm("你确定要删除这个项目吗？");
    if (confirmation) {
        alert("项目已删除！"); // 这里可以扩展为实际删除项目的逻辑
        // 可以重定向到其他页面或刷新页面
        window.location.href = 'index.html'; // 返回到项目列表页面
    }
});

// 编辑项目按钮事件
document.getElementById('editButton').addEventListener('click', function() {
    const projectName = document.getElementById('projectName');
    const projectCategory = document.getElementById('projectCategory');
    const projectDescription = document.getElementById('projectDescription');

    // 允许编辑
    const newName = prompt("输入新的项目名称:", projectName.textContent);
    if (newName) {
        projectName.textContent = newName;
    }

    const newCategory = prompt("输入新的项目分类:", projectCategory.textContent);
    if (newCategory) {
        projectCategory.textContent = newCategory;
    }

    const newDescription = prompt("输入新的项目描述:", projectDescription.textContent);
    if (newDescription) {
        projectDescription.textContent = newDescription;
    }

    alert("项目已更新！"); // 提示用户项目更新
});
