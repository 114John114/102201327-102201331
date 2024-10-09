//修改密码
	// script.js
	const editButton = document.getElementById('editButton');
	const saveButton = document.getElementById('saveButton');
	const cancelButton = document.getElementById('cancelButton');
	const formElements = document.querySelectorAll('#profileForm input');
	const passwordInput = document.getElementById('password');
	const passwordLabel = document.getElementById('passwordword');
	// 点击“修改信息”按钮时，启用表单编辑
	editButton.addEventListener('click', function() {
		formElements.forEach(element => {
			element.disabled = false; // 启用所有表单输入框
		});
        passwordLabel.style.display = 'block'; // 显示
        passwordInput.style.display = 'block'; // 显示密码输入框
        passwordInput.disabled = false; // 启用密码输入框
		editButton.style.display = 'none'; // 隐藏“修改信息”按钮
		saveButton.style.display = 'inline'; // 显示“保存修改”按钮
		cancelButton.style.display = 'inline'; // 显示“取消”按钮
	});
	
	// 点击“保存修改”按钮时，禁用表单编辑并保存数据
	document.getElementById('profileForm').addEventListener('submit', function(event) {
		event.preventDefault(); // 防止表单默认提交行为
		formElements.forEach(element => {
			element.disabled = true; // 禁用所有表单输入框
		});
        passwordLabel.style.display = 'none'; // 隐藏
		editButton.style.display = 'inline'; // 显示“修改信息”按钮
		saveButton.style.display = 'none'; // 隐藏“保存修改”按钮
		cancelButton.style.display = 'none'; // 隐藏“取消”按钮
        passwordInput.style.display = 'none'; // 隐藏密码输入框
		// 模拟保存数据到服务器
		alert('信息已保存');
	});
	
	// 点击“取消”按钮时，恢复原始状态并禁用表单
	cancelButton.addEventListener('click', function() {
		formElements.forEach(element => {
			element.disabled = true; // 禁用所有表单输入框
			element.value = element.defaultValue; // 恢复默认值
		});
        passwordInput.style.display = 'none'; // 隐藏密码输入框
        passwordLabel.style.display = 'none'; // 隐藏
		editButton.style.display = 'inline'; // 显示“修改信息”按钮
		saveButton.style.display = 'none'; // 隐藏“保存修改”按钮
		cancelButton.style.display = 'none'; // 隐藏“取消”按钮
	});