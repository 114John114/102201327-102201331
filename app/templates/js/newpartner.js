document.addEventListener('DOMContentLoaded', function() {
     // 获取项目 ID（假设项目 ID 存储在某个元素的 data-project-id 属性中）
     const project_id = document.getElementById('projectInfo').getAttribute('data-project-id');

     // 处理申请人按钮点击事件
     document.querySelectorAll('.applicantButton').forEach(button => {
         button.addEventListener('click', function() {
             const applicantName = this.getAttribute('data-name'); // 获取申请人姓名
             
             // 构建跳转 URL
             const url = `/newpartner/${project_id}/${applicantName}`;
             
             // 跳转到路由
             window.location.href = url;
        });
    });
});
