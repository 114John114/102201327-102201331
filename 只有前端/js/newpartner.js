// 处理申请人按钮点击事件
document.querySelectorAll('.applicantButton').forEach(button => {
    button.addEventListener('click', function() {
        const applicantName = this.getAttribute('data-name'); // 获取申请人姓名
        // 跳转到个人主页，假设个人主页为 personalpage.html，并传递申请人姓名
        window.location.href = `personalpage.html?applicant=${applicantName}`;
    });
});
