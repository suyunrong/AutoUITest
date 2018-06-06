/* 动态改变模块信息 */
function show_module(module_info, id) {
    module_info = module_info.split('replaceFlag');
    var a = $(id);
    a.empty();
    for (var i = 0; i < module_info.length; i++) {
        if (module_info[i] !== "") {
            var value = module_info[i].split('^=');
            a.prepend("<option value='" + value[0] + "' >" + value[1] + "</option>")
        }
    }
    a.prepend("<option value='' selected >请选择</option>");
}

/* 动态改变用例信息 */
function show_case(case_info, id) {
    case_info = case_info.split('replaceFlag');
    var a = $(id);
    a.empty();
    for (var i = 0; i < case_info.length; i++) {
        if (case_info[i] !== "") {
            var value = case_info[i].split('^=');
            a.prepend("<option value='" + value[0] + "' >" + value[1] + "</option>")
        }
    }
    a.prepend("<option value='' selected >单用例测试，无需依赖</option>");

}

/* 动态改变环境信息 */
function show_env(case_info, id) {
    case_info = case_info.split('replaceFlag');
    var a = $(id);
    a.empty();
    for (var i = 0; i < case_info.length; i++) {
        if (case_info[i] !== "") {
            var value = case_info[i].split('^=');
            a.prepend("<option value='" + value[0] + "' >" + value[1] + "</option>")
        }
    }
    a.prepend("<option value='' selected >单用例测试，无需依赖</option>");

}

/*表单信息异步传输*/
function info_ajax(id, url) {
    var data = $(id).serializeJSON();
    if (id === '#add_task') {
        var include = [];
        var i = 0;
        $("ul#pre_case li a").each(function () {
            include[i++] = [$(this).attr('id'), $(this).text()];
        });
        data['module'] = include;
    }

    $.ajax({
        type: 'post',
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function (data) {
            if (data !== 'ok') {
                if (data.indexOf('/api/') !== -1) {
                    window.location.href = data;
                } else {
                    myAlert(data);
                }
            }
            else {
                window.location.reload();
            }
        }
        ,
        error: function () {
            myAlert('Sorry，服务器可能开小差啦, 请重试!');
        }
    });

}

/* 动态获取值 */
function auto_load(id, url, target, type) {
    var data = $(id).serializeJSON();
    if (id === '#form_case_message') {
        data = {
            "testcase": {
                "name": data,
                "type": type
            }
        }
    } else if (id === '#form_config') {
        data = {
            "config": {
                "name": data,
                "type": type
            }
        }
    } else {
        data = {
            "task": {
                "name": data,
            }
        }
    }
    $.ajax({
        type: 'post',
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function (data) {
            if (type === 'module') {
                show_module(data['content'], target);
            } else {
                show_case(data['content'], target.split(',')[0]);
                show_case(data['content'], target.split(',')[1]);
            }
        }
        ,
        error: function () {
            myAlert('Sorry，服务器可能开小差啦, 请重试!');
        }
    });

}

/*新增内容ajax*/
function add_data_ajax(id, url) {
    var data = $(id).serializeJSON();
    console.log(data);
    $.ajax({
        type: 'post',
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function (data) {
            if (data['msg'] === 'ok') {
                myAlert(data['content']);
                if (id.indexOf('project') !== -1) {
                    window.location.href = '/data/project_list/1'
                } else if (id.indexOf('module') !== -1) {
                    window.location.href = '/data/module_list/1'
                } else if (id.indexOf('case') !== -1) {
                    window.location.href = '/data/case_list/1'
                } else if (id.indexOf('env') !== -1) {
                    window.location.href = '/data/env_list/1'
                }
            } else {
                myAlert(data['content'])
            }
        },
        error: function () {
            myAlert('Sorry，服务器可能开小差啦, 请重试!');
        }
    });
}

/*更新内容ajax*/
function update_data_ajax(id, url) {
    var data = $(id).serializeJSON();
    $.ajax({
        type: 'post',
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function (data) {
            if (data['msg'] === 'ok') {
                myAlert(data['content']);
                window.location.reload();
            } else {
                myAlert(data['content'])
            }
        },
        error: function () {
            myAlert('Sorry，服务器可能开小差啦, 请重试!');
        }
    });
}

// 删除内容ajax
function del_data_ajax(id, url) {
    var data = {
        "id": id,
        'mode': 'del'
    };
    console.log(data);
    $.ajax({
        type: 'post',
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function (data) {
            if (data['msg'] === 'ok') {
                myAlert(data['content']);
                window.location.reload();
            } else {
                myAlert(data['content'])
            }
        },
        error: function () {
            myAlert('Sorry，服务器可能开小差啦, 请重试!');
        }
    });
}

// 添加用例
function add_case_ajax(type) {

    var caseInfo = $("#form_case_message").serializeJSON();
    var scriptInfo = $("#form_script_message").serializeJSON();

    if ($('#prepos_case_id option:selected').val() === ''
            && $('#postpos_case_id option:selected').val() === '') {
            caseInfo['prepos_case'] = [];
            caseInfo['postpos_case'] = [];
        } else if ($('#prepos_case_id option:selected').val() !== ''
            && $('#postpos_case_id option:selected').val() === '') {
            caseInfo['prepos_case'] = [$('#prepos_case_id').val()];
            caseInfo['postpos_case'] = [];
        } else if ($('#prepos_case_id option:selected').val() === ''
            && $('#postpos_case_id option:selected').val() !== '') {
            caseInfo['prepos_case'] = [];
            caseInfo['postpos_case'] = [$('#postpos_case_id').val()];
        } else {
            caseInfo['prepos_case'] = [$('#prepos_case_id').val()];
            caseInfo['postpos_case'] = [$('#postpos_case_id').val()];
        }

    var testcase = {
        "case": caseInfo,
        "scripts": scriptInfo
    }

    if (type === 'edit') {
        url = '/data/edit_case/';
    } else {
        url = '/data/add_case/';
    }

    $.ajax({
        type: 'post',
        url: url,
        data: JSON.stringify(testcase),
        contentType: "application/json",
        success: function (data) {
            if (data['msg'] === 'ok') {
                myAlert(data['content']);
                window.location.href = '/data/case_list/1'
            } else {
                myAlert(data['content'])
            }
        },
        error: function () {
            myAlert('Sorry，服务器可能开小差啦, 请重试!');
        }
    });
}


// 复制
function copy_data_ajax(id, url) {
    var data = {
        "data": $(id).serializeJSON(),
        'mode': 'copy'
    };
    $.ajax({
        type: 'post',
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function (data) {
            if (data['msg'] === 'ok') {
                myAlert(data['content']);
                window.location.href = '/data/case_list/1'
            } else {
                myAlert(data['content'])
            }
        },
        error: function () {
            myAlert('Sorry，服务器可能开小差啦, 请重试!');
        }
    });
}

function config_ajax(type) {
    var dataType = $("#config_data_type").serializeJSON();
    var caseInfo = $("#form_config").serializeJSON();
    var variables = $("#config_variables").serializeJSON();
    var parameters = $('#config_params').serializeJSON();
    var hooks = $('#config_hooks').serializeJSON();
    var request_data = null;
    if (dataType.DataType === 'json') {
        try {
            request_data = eval('(' + $('#json-input').val() + ')');
        }
        catch (err) {
            myAlert('Json格式输入有误！')
            return
        }
    } else {
        request_data = $("#config_request_data").serializeJSON();
    }
    var headers = $("#config_request_headers").serializeJSON();

    const config = {
        "config": {
            "name": caseInfo,
            "variables": variables,
            "parameters": parameters,
            "request": {
                "headers": headers,
                "type": dataType.DataType,
                "request_data": request_data
            },
            "hooks": hooks,

        }
    };
    if (type === 'edit') {
        url = '/api/edit_config/';
    } else {
        url = '/api/add_config/';
    }
    $.ajax({
        type: 'post',
        url: url,
        data: JSON.stringify(config),
        contentType: "application/json",
        success: function (data) {
            if (data === 'session invalid') {
                window.location.href = "/api/login/";
            } else {
                if (data.indexOf('/api/') != -1) {
                    window.location.href = data;
                } else {
                    myAlert(data);
                }
            }
        },
        error: function () {
            myAlert('Sorry，服务器可能开小差啦, 请重试!');
        }
    });
}

/*提示 弹出*/
function myAlert(data) {
    $('#my-alert_print').text(data);
    $('#my-alert').modal({
        relatedTarget: this
    });
}

function post(url, params) {
    var temp = document.createElement("form");
    temp.action = url;
    temp.method = "post";
    temp.style.display = "none";
    for (var x in params) {
        var opt = document.createElement("input");
        opt.name = x;
        opt.value = params[x];
        temp.appendChild(opt);
    }
    document.body.appendChild(temp);
    temp.submit();
    return temp;
}

function del_row(id) {
    var attribute = id;
    var chkObj = document.getElementsByName(attribute);
    var tabObj = document.getElementById(id);
    for (var k = 0; k < chkObj.length; k++) {
        if (chkObj[k].checked) {
            tabObj.deleteRow(k + 1);
            k = -1;
        }
    }
}


function add_row(id) {
    var tabObj = document.getElementById(id);//获取添加数据的表格
    var rowsNum = tabObj.rows.length;  //获取当前行数
    var style = 'width:100%; border: none';
    var cell_check = "<input type='checkbox' name='" + id + "' style='width:55px' />";
    var cell_step_desc = "<input type='text' name='scripts[][step_desc]' value='' style='" + style + "' />";
    var cell_ele_pos = "<input type='text' name='scripts[][ele_pos]' value='' style='" + style + "' />";
    var cell_page_oper = "<input type='text' name='scripts[][page_oper]' value='' style='" + style + "' />";
    var cell_page_oper_val = "<input type='text' name='scripts[][page_oper_val]' value='' style='" + style + "' />";
    var cell_page_exp = "<input type='text' name='scripts[][page_exp]' value='' style='" + style + "' />";
    var cell_slepp_time = "<input type='text' name='scripts[][slepp_time]' value='' style='" + style + "' />";

    var myNewRow = tabObj.insertRow(rowsNum);
    var newTdObj0 = myNewRow.insertCell(0);
    var newTdObj1 = myNewRow.insertCell(1);
    var newTdObj2 = myNewRow.insertCell(2);
    var newTdObj3 = myNewRow.insertCell(3);
    var newTdObj4 = myNewRow.insertCell(4);
    var newTdObj5 = myNewRow.insertCell(5);
    var newTdObj6 = myNewRow.insertCell(6);

    newTdObj0.innerHTML = cell_check
    newTdObj1.innerHTML = cell_step_desc;
    newTdObj2.innerHTML = cell_ele_pos;
    newTdObj3.innerHTML = cell_page_oper;
    newTdObj4.innerHTML = cell_page_oper_val;
    newTdObj5.innerHTML = cell_page_exp;
    newTdObj6.innerHTML = cell_slepp_time;
}




