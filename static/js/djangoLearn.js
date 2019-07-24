$(function () {
    $('#dl').click(dl);
    $('#zc').click(zc);
    $('#ryxxb').click(ryxxb);
    $('#lpr').click(lpr);

    $(window).keyup(function (event) {
        if (event.keyCode == 13) {
            ss();
        }
    });

    $("#ss").click(ss);
});

// 登录
function dl() {
    var url = '/loginData';
    var data = {
        'name':$('#name').val(),
        'password':$('#password').val()
    }
    $.post(url, data, function (result) {
        console.log(result);
        if(result.state == '1'){
            alert('登录成功!');
            location.href = '/index';
        }else{
            alert(result.msg);
        }
    });
}

// 注册
function zc() {
    var url = '/registerData';
    var data = {
        'name':$('#username').val(),
        'password':$('#pwd').val()
    }
    $.post(url, data, function (result) {
        alert(result);
        location.href = '/login';
    });
}


var num = 0;
// 获取人员信息详情
function ryxxb() {
    num++;
    console.log(num);
    if(num % 2 == 0){
        $("#xq").hide();
    }else{
        $("#xq").show();
    }
    $.getJSON('/ryxxb', function (result) {
        $("#xq").empty();
        console.log(typeof result);
        for(var i = 0;i < result.length;i++){
            var rytable = result[i];
            // var tem = template.replace('[id]',rytable.fields.user);
            var tem = template.replace('[name]',rytable.fields.user);
            tem = tem.replace('[pwd]',rytable.fields.pwd);
            $("#xq").append(tem);
        }
    });
}

var template = '<tr>' +
                    // '<td>' + '[id]' + '</td>' +
                    '<td>' + '[name]' + '</td>' +
                    '<td>' + '[pwd]' + '</td>' +
                '</tr>';


function ss() {
    // window.location.href = "/news?word=" + news;
    var url = '/news';
    var data = {"word":$("#news").val()}
    if($("#news").val() == null || $("#news").val() == "") {
        alert("输入框不能为空哟!");
    }else {
        $.post(url,data,function (result) {
            $("#xw").empty();
            var res = JSON.parse(result);
            for(var i = 0;i < res.length;i++){
                var rytable = res[i];
                var tem = templatexw.replace('[hre]',rytable.fields.hre);
                tem = tem.replace('[tit]',rytable.fields.tit);
                $("#xw").append(tem);
            }
            $("#news").val("");
        });
    }

}

var templatexw = '<tr>' +
                    '<td>' +
                        '<a href="' + '[hre]' +'" target="_blank">' +
                            '[tit]' +
                        '</a>' +
                    '</td>' +
                '</tr>'

console.log(templatexw);


function lpr() {
    var formData = new FormData();
    formData.append("img", document.getElementById("file1").files[0]);
    $.ajax({
        url: "/lpr",
        type: "POST",
        data: formData,
        /**
        *必须false才会自动加上正确的Content-Type
        */
        contentType: false,
        /**
        * 必须false才会避开jQuery对 formdata 的默认处理
        * XMLHttpRequest会对 formdata 进行正确的处理
        */
        processData: false,
        success: function (data) {
            alert(data);
        },
        error: function () {

        }
    });
}