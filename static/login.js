$(document).ready(function () {
    fetch('/api/credentials')
    .then(res => res.json())
    .then(data => {
        if (data.user && data.password) {
            document.getElementById('username').value = data.user;
            document.getElementById('password').value = data.password;
            // 自动提交也可以加上这里
        }
    });
    $('#login-btn').click(function () {
        const user = $('#username').val().trim();
        const password = $('#password').val().trim();

        if (!user || !password) {
            layer.msg('请输入用户名和密码', { icon: 0 });
            return;
        }

        $.post('/api/login', { user, password }, function (res) {
            if (res.code === 200 && res.token) {
                localStorage.setItem('token', res.token);
                layer.msg('登录成功', { icon: 1, time: 1000 }, function () {
                    window.location.href = '/';
                });
            } else {
                layer.msg('登录失败: ' + (res.message || '未知错误'), { icon: 2 });
            }
        }).fail(function () {
            layer.msg('请求失败，请稍后再试', { icon: 2 });
        });
    });
});
