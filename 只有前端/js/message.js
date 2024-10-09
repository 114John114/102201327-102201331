// 处理选择联系人按钮点击事件
document.querySelectorAll('.contactButton').forEach(button => {
    button.addEventListener('click', function() {
        const contactName = this.getAttribute('data-name'); // 获取联系人名称
        // 跳转到聊天界面，假设聊天界面为 chat.html，并传递联系人名称
        window.location.href = `chat.html?contact=${contactName}`; 
    });
});
