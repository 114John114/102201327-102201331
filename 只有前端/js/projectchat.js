// 获取联系人名称
const urlParams = new URLSearchParams(window.location.search);
const contact = urlParams.get('contact');
document.getElementById('contactName').textContent = contact;

// 发送消息按钮点击事件
document.getElementById('sendButton').addEventListener('click', function() {
    const message = document.getElementById('messageInput').value;
    const chatArea = document.getElementById('chatArea');

    if (message) {
        chatArea.innerHTML += `<p><strong>${contact}:</strong> ${message}</p>`;
        document.getElementById('messageInput').value = ''; // 清空输入框
        chatArea.scrollTop = chatArea.scrollHeight; // 滚动到聊天记录底部
    }
});
