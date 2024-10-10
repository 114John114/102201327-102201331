// 点击“编辑项目”按钮，启用编辑模式
document.addEventListener('DOMContentLoaded', function() {
    // 获取元素
    const editButton = document.getElementById('editButton');
    const saveButton = document.getElementById('saveButton');
    const projectCategory = document.getElementById('projectCategory');
    const projectManager = document.getElementById('projectManager');
    const projectDescription = document.getElementById('projectDescription');

    // 检查是否找到元素
    if (!editButton || !saveButton) {
        console.error('编辑按钮或保存按钮未找到，请检查 ID 是否正确。');
        return; // 终止执行
    }
    // 直接使用 project_id
    console.log("project_id:", project_id);

0
    // 点击“编辑项目”按钮，启用编辑模式
    editButton.addEventListener('click', function() {
        // 将项目内容替换为可编辑的输入框
        const categoryInput = document.createElement('input');
        categoryInput.type = 'text';
        categoryInput.value = projectCategory.textContent;
        categoryInput.name = 'category';
        projectCategory.replaceWith(categoryInput);

        const managerInput = document.createElement('input');
        managerInput.type = 'text';
        managerInput.value = projectManager.textContent;
        managerInput.name = 'manager';
        projectManager.replaceWith(managerInput);

        const descriptionInput = document.createElement('textarea');
        descriptionInput.value = projectDescription.textContent;
        descriptionInput.name = 'description';
        projectDescription.replaceWith(descriptionInput);

        // 显示保存按钮，隐藏编辑按钮
        editButton.style.display = 'none';
        saveButton.style.display = 'inline';

        // 点击“保存项目”按钮，保存编辑后的内容
        saveButton.addEventListener('click', function() {
            projectCategory.textContent = categoryInput.value;
            categoryInput.replaceWith(projectCategory);

            projectManager.textContent = managerInput.value;
            managerInput.replaceWith(projectManager);

            projectDescription.textContent = descriptionInput.value;
            descriptionInput.replaceWith(projectDescription);

            saveButton.style.display = 'none';
            editButton.style.display = 'inline';

            // 发送数据到后端
            const projectData = {
                project_type: projectCategory.textContent,
                project_leader: projectManager.textContent,
                description: projectDescription.textContent
            };

            fetch('/updateproject/'+ project_id, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(projectData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('项目已保存！');
                } else {
                    console.error('Error message from server:', data.message);
                    alert('项目保存失败: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error occurred during project saving:', error);
                alert('项目保存失败，发生错误: ' + error);
            });
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    console.log("newPartnerURL:", newPartnerURL);
    console.log("Button clicked");
    addMemberButton.addEventListener('click', function() {
        window.location.href = newPartnerURL;
    })
});
