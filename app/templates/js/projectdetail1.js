document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('joinProjectButton').addEventListener('click', function() {
        console.log("Button clicked");
        console.log("project_id:", project_id);
        console.log("username:", username);
        
        // 创建要发送的数据对象
        const projectData = {
            project_id: project_id, // 替换为实际的项目 ID
            username: username // 替换为实际的用户名
        };

        // 使用 fetch 发送 POST 请求
        fetch('/joinproject', { // 替换为实际的路由
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(projectData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('你已成功申请加入该项目！');
            } else {
                alert('申请提交失败');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('申请提交失败');
        });
    });
});