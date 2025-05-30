$(document).ready(function () {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '/login';
        return;
    }

    fetchDevices();
    $('#refresh-devices-btn').click(function() {
        fetchDevices();
    });
    $('#select-all-btn').click(function () {
        const checkboxes = $('#device-list input[type=checkbox]');
        const allChecked = checkboxes.length === checkboxes.filter(':checked').length;
        checkboxes.prop('checked', !allChecked);
    });

    $('#start-btn').click(function() {
        const btn = $(this);
        const selectedDevices = $('#device-list input[type=checkbox]:checked').map(function() {
        return this.value;
    }).get();

    if (selectedDevices.length === 0) {
        layer.msg('请选择至少一个设备', {icon: 0});
        return;
    }

    btn.prop('disabled', true);  // 禁用按钮防止重复点击
        console.log(token)
    $.post('/start_task', { devices: selectedDevices , token: token}, function(response) {
        if (response.code === 200) {
            layer.msg('任务已开始', {icon: 1});
            // 这里任务已经开始，可以保持按钮禁用
        } else {
            layer.msg('启动失败: ' + response.message, {icon: 2});
            btn.prop('disabled', false);  // 失败解禁按钮
        }
    }).fail(function() {
        layer.msg('请求失败', {icon: 2});
        btn.prop('disabled', false);  // 请求失败解禁按钮
    });
});

    setInterval(fetchLogs, 1000);
});

function fetchDevices() {
    $.get('/api/device/list', function (response) {
        if (response.code === 200 && response.data) {
            const deviceList = $('#device-list');
            deviceList.empty();
            for (const [ip, deviceCode] of Object.entries(response.data)) {
                const checkboxId = 'device-' + deviceCode;
                const checkbox = `
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" value="${ip}" id="${checkboxId}">
                        <label class="form-check-label" for="${checkboxId}">
                            ${ip}
                        </label>
                    </div>
                `;
                deviceList.append(checkbox);
            }
        } else {
            layer.msg('获取设备列表失败: ' + response.message, { icon: 2 });
        }
    }).fail(function () {
        layer.msg('请求设备列表接口失败', { icon: 2 });
    });
}

function fetchLogs() {
    $.get('/get_logs', function (data) {
        const logContainer = $('#log-container');
        logContainer.empty();
        data.forEach(log => {
            logContainer.append(`<div>${log}</div>`);
        });
        logContainer.scrollTop(logContainer[0].scrollHeight);
    });
}
