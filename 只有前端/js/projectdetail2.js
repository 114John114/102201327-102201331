document.getElementById('joinProjectButton').addEventListener('click', function() {
    // 在这里添加加入项目的逻辑，比如发送请求到服务器
    alert('你已成功申请加入该项目！');
});

document.addEventListener('DOMContentLoaded', function() {
    // 示例项目数据
    const projectData = {
        name: '大数据分析',
        category: '科研项目',
        manager: 'Alice John',
        description: '这是一个大数据分析项目',
        image: 'images/placeholder2.png', // 确保有这个图片文件
        requirements: '数据分析师',
        recruitment: '5/15'
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
