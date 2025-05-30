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
        const visibleCheckboxes = $('#device-list .form-check:visible input[type=checkbox]');
        const allChecked = visibleCheckboxes.length > 0 && visibleCheckboxes.filter(':checked').length === visibleCheckboxes.length;
        visibleCheckboxes.prop('checked', !allChecked);
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
// 监听 IP 搜索框输入
   $('#ipSearch').on('input', function () {
       console.log(1)
        const keyword = $(this).val().toLowerCase();
       console.log(keyword)
        $('#device-list .device-item').each(function () {
            const ip = $(this).data('ip')?.toLowerCase() || '';
            if (ip.includes(keyword)) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });
function fetchDevices() {
    $.get('/api/device/list', function (response) {
        if (response.code === 200 && response.data) {
            const deviceList = $('#device-list');
            deviceList.empty();
            for (const [ip, deviceCode] of Object.entries(response.data)) {
                const checkboxId = 'device-' + deviceCode;
                const checkbox = `
                    <div class="device-item" data-ip="${ip}">
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" value="${ip}" id="${checkboxId}">
                            <label class="form-check-label" for="${checkboxId}">
                                ${ip}
                            </label>
                        </div>
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
