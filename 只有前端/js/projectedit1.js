// 获取元素
const editButton = document.getElementById('editButton');
const saveButton = document.getElementById('saveButton');
const projectName = document.getElementById('projectName');
const projectCategory = document.getElementById('projectCategory');
const projectDescription = document.getElementById('projectDescription');
const formElements = [projectName, projectCategory, projectDescription]; // 将项目字段打包进数组

// 点击“编辑项目”按钮，启用编辑模式
editButton.addEventListener('click', function() {
    formElements.forEach(element => {
        const input = document.createElement('input'); // 创建输入框
        input.type = 'text';
        input.value = element.textContent; // 将元素当前的文本作为输入框的初始值
        input.setAttribute('data-original-text', element.textContent); // 存储原始文本以便取消时恢复
        element.replaceWith(input); // 将元素替换为输入框
    });
    editButton.style.display = 'none'; // 隐藏“编辑项目”按钮
    saveButton.style.display = 'inline'; // 显示“保存项目”按钮
});

// 点击“保存项目”按钮，保存数据并禁用编辑模式
saveButton.addEventListener('click', function() {
    const inputs = document.querySelectorAll('input[type="text"]'); // 获取所有输入框
    inputs.forEach(input => {
        const span = document.createElement('span');
        span.textContent = input.value; // 将输入框中的值作为新的文本
        input.replaceWith(span); // 将输入框替换为文本
    });
    
    editButton.style.display = 'inline'; // 显示“编辑项目”按钮
    saveButton.style.display = 'none'; // 隐藏“保存项目”按钮

    // 模拟保存数据到服务器
    alert('项目已保存');
});
