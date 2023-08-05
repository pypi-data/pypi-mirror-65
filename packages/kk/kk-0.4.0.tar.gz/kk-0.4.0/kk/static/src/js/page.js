var user = null;

function changeUserState(user) {
  $('.logout').removeClass('layui-hide');
  $('.login').addClass('layui-hide');
  $('.username').text(user.username || user.nickName);
  if(user.admin) {
    $('.user-admin').removeClass('layui-hide');
  }
}

function checkUser() {
  user = localStorage.getItem('user');
  if(user){
    user = JSON.parse(user);
    changeUserState(user);
  }else{
    $.get('/user', function (ret) {
      if (!ret.err) {
        localStorage.setItem('user', JSON.stringify(ret));
        changeUserState(ret);
        user = ret;
      } else {
        $('.login').removeClass('layui-hide');
      }
    })
  }
}

function logout(){
  localStorage.removeItem('user');
  removeCookie('token');
  removeCookie('endpoints');
  $.get('/logout', function () {
    location.href = '/';
  })
}

function copyData(data){
  var copyFrom = $('<textarea id="copyFrom">');
  copyFrom.css({
    position: "absolute",
    left: "-1000px",
    top: "-1000px",
  });
  copyFrom.text(data);
  $('body').append(copyFrom);
  copyFrom.select();
  document.execCommand('copy');
  copyFrom.remove();
  layer.msg('复制成功');
}

function copyBtn(selector){
  var btnCopy = new ClipboardJS(selector, {
    target: function (trigger) {
      return $(trigger).parents('tr').find('input')[0];
    }
  })
  btnCopy.on('success', function (e) {
    layer.msg('已复制到剪贴板', {
      time: 2000
    });
    e.clearSelection();
  })
  btnCopy.on('error', function (e) {
    layer.msg('复制出错，请手动复制', {
      time: 2000
    });
  })
}

function guid(){
  function S4(){
    return (((1+Math.random())*0x10000)|0).toString(16).substring(1)
  }
  return (S4()+S4()+"-"+S4()+"-"+S4()+"-"+S4()+"-"+S4()+S4()+S4());
}

function webUpload(selector){
  var demoListView = $('#upload-list');
  var uploader = WebUploader.create({
    swf: '/static/bower_components/fex-webuploader/dist/Uploader.swf',
    server: location.pathname,
    dnd: document.body,
    disableGlobalDnd: true,
    paste: document.body,
    pick: {
      id: selector,
      innerHTML: '<i class="layui-icon layui-icon-upload"></i><p>点击上传或将文件拖拽到此处（截图可粘贴）</p>',
      multiple: true,
    },
    auto: true,
    prepareNextFile: true,
    chunked: true,
    chunkSize: 5 * 1024 * 1024,
    chunkRetry: 3,
    threads: 5,
    formData: {
      token: (function(){ return getCookie('token') || ''; })(),
      guid: (function(){ return guid(); })(),
    },
    fileNumLimit: 100,
    duplicate: true,
  });

  uploader.on('fileQueued', function(file) {
    demoListView.parents('table').removeClass('layui-hide');
    var html = $(['<tr id="'+ file.id +'">'
      ,'<td style="text-align:left !important">'+ file.name +'</td>'
      ,'<td style="width:80px">'+ (file.size/1014).toFixed(1) +'kb</td>'
      ,'<td style="width:80px">准备上传</td>'
      ,'<td style="width:100px">'
      ,'<button class="layui-btn layui-btn-xs file-reload">重传</button>'
      ,'<button class="layui-btn layui-btn-xs layui-btn-danger file-remove">删除</button>'
      ,'</td>'
      ,'<td style="width:300px">'
      ,'<div class="layui-progress" lay-filter="' + file.id + '" lay-showPercent="true"><div class="layui-progress-bar" lay-percent="0%"></div></div>'
      ,'</td>'
      ,'</tr>'].join(''));
    demoListView.append(html);

    $(document).on('click', 'tr .file-reload', function(){
      uploader.upload(uploader.getFile($(this).parents('tr').attr("id"), true));
    })
    $(document).on('click', 'tr .file-remove', function(){
      var tr = $(this).parents('tr');
      uploader.removeFile(uploader.getFile(tr.attr("id"), true));
      tr.remove();
    })
    uploader.md5File(file)
      .progress(function(percent){
        element.progress(file.id, (percent * 100).toFixed(1) + '%');
      })
      .then(function(md5){
        file.md5 = md5;
      });
  });

  uploader.on('uploadProgress', function(file, percent){
    var tr = demoListView.find('tr#'+ file.id)
      ,tds = tr.children();
    tds.eq(2).html('<span style="color: #5FB878;">正在上传</span>');
    element.progress(file.id, (percent * 100).toFixed(1) + '%');
  });
  uploader.on('uploadSuccess', function(file, ret){
    console.log('upload succeed' + file.id)
    var tr = demoListView.find('tr#'+ file.id)
      ,tds = tr.children();
    if(file.size > uploader.options.chunkSize){
      var data = {
        action: 'merge',
        id: file.id,
        size: file.size,
        name: file.name,
        md5: file.md5,
      };
      for(var i in uploader.options.formData){
        data[i] = uploader.options.formData[i];
      }
      $.post(location.pathname, data, function(ret){
        if(ret.err == 0){
          tds.eq(2).html('<span style="color: #5FB878;">上传成功</span>');
        }else{
          tds.eq(2).html('<span style="color: #FF5722;">上传失败</span>');
        }
      })
    }else{
      if(ret.err == 0){
        tds.eq(2).html('<span style="color: #5FB878;">上传成功</span>');
      }else{
        tds.eq(2).html('<span style="color: #FF5722;">上传失败</span>');
      }
    }
  });

  uploader.on('uploadError', function(file){
    var tr = demoListView.find('tr#'+ file.id)
      ,tds = tr.children();
    tds.eq(2).html('<span style="color: #FF5722;">上传失败</span>');
  })

  $(document).on('change', 'input[type=file]', function(){
    console.log('upload ' + this.files.length + ' files');
    if(this.files.length > 100){
      layer.msg('每次最多上传100个文件');
    }else{
      uploader.addFiles(this.files);
    }
  })
}

layui.use(['layer', 'element', 'tree', 'form'], function () {
  layer = layui.layer;
  element = layui.element;
  form = layui.form;
  $ = layui.$;

  copyBtn('.btn-copy');
  webUpload('#upload-box');

  $(function () {
    checkUser();

    var masonryNode = $('#masonry');
    if(masonryNode.length >= 1){
      masonryNode.imagesLoaded(function(){
        masonryNode.masonry({
          itemSelector: '.layui-col-md2',
          columnWidth: '.layui-col-md2',
          isAnimated: true,
        });
      });
    }

    $.get(location.pathname + '?f=tree', function(ret){
      layui.tree.render({
        elem: '#tree',
        accordion: true,
        isJump: true,
        data: ret.nodes,
      });
    })

    $(document).on('click', '.user-logout', function () {
      logout();
    })

    $(document).on("mouseover", '.layui-tips', function(){
      var that = this;
      layer.tips($(that).attr('tips'), that, {tips: 1});
    })

    $(document).on("mouseleave", '.layui-tips', function(){
      layer.closeAll('tips');
    })

    $(document).on("click", ".tree-toggle", function(){
      if(getCookie("tree")){
        removeCookie("tree")
        $('.tree-toggle i').removeClass("layui-icon-shrink-right").addClass("layui-icon-spread-left")
        $("#tree").addClass("layui-hide")
        $(".tree-table").addClass("layui-col-md12").removeClass("layui-col-md10")
      }else{
        setCookie("tree", "on")
        $('.tree-toggle i').removeClass("layui-icon-spread-left").addClass("layui-icon-shrink-right")
        $("#tree").removeClass("layui-hide")
        $(".tree-table").addClass("layui-col-md10").removeClass("layui-col-md12")
      }
    })

    $(document).on("click", ".batch-preview", function(){
      if(getCookie("preview")){
        removeCookie("preview")
      }else{
        setCookie("preview", "on")
      }
      layer.msg("切换中...")
      location.reload()
    })

    $(document).on('click', '.batch-display', function(){
      if(getCookie("display")){
        removeCookie("display")
      }else{
        setCookie("display", "on")
      }
      layer.msg("切换中...")
      location.reload()
    })

    $(document).on('click', '.batch-select', function(){
      $('.filelist tbody tr').each(function(){
        $(this).find('input[type=checkbox]').prop('checked', true);
      })
    })

    $(document).on('click', '.batch-unselect', function(){
      $('.filelist tbody tr').each(function(){
        var checkbox = $(this).find("input[type=checkbox]")
        checkbox.prop('checked', !checkbox.prop('checked'))
      })
    })

    $(document).on("click", ".batch-delete", function(){
      layer.confirm('确定删除？', {icon: 2, title: '提示'}, function(index){
        $("input:checkbox:checked").each(function(){
          var tr = $(this).parents("tr");
          var url = $(tr.find("td")[1]).find("a").attr("href");
          var name = $(tr.find("td")[1]).find("a").text();
          $.post(url, {'action': 'delete'}, function(ret){
            if(ret.err) layer.msg(ret.msg)
            else{
              tr.slideUp();
              layer.msg('删除' + name + '成功');
            }
          })
        })
      })
    })

    $(document).on("click", ".batch-unshare", function(){
      layer.confirm('确定取消？', {icon: 2, title: '提示'}, function(index){
        $("input:checkbox:checked").each(function(){
          var tr = $(this).parents("tr");
          var url = $(tr.find("td")[1]).find("a").attr("href");
          var name = $(tr.find("td")[1]).find("a").text();
          $.post(url, {'action': 'unshare'}, function(ret){
            if(ret.err) layer.msg(ret.msg)
            else layer.msg('取消分享' + name + '成功');
          })
        })
      })
    })

    $(document).on("click", ".btn-preview", function(){
      var tr = $(this).parents("tr");
      var url = $(tr.find("td")[1]).find("a").attr("href") + '?f=preview';
      var title = $(tr.find("td")[1]).find("a").text();
      layer.open({
        type: 2,
        title: title,
        content: url,
        shadeClose: true,
        area: ['1000px', '700px'],
        success: function(layero, index){
          var css = {"display": "block", "max-width": "100%"};
          $($("iframe").contents().find("body")).children("img:first").css(css);
        }
      })
    })
    
    $(document).on("click", ".btn-link", function(){
      var tr = $(this).parents("tr");
      var url = $(tr.find("td")[1]).find("a").attr("href");
      copyData(location.protocol + '//' + location.hostname + url);
    })

    $(document).on("click", ".btn-folder", function(){
      var tr = $(this).parents("tr");
      var url = $(tr.find("td")[1]).find("a").attr("href");
      layer.prompt({
        formType: 2,
        value: '',
        title: '请输入文件夹名',
        area: ['200px', '50px'],
      }, function(value, index, elem){
        location.href = location.pathname + '/' + $.trim(value);
      })
    })

    $(document).on("click", ".btn-rename", function(){
      var tr = $(this).parents("tr");
      var url = $(tr.find("td")[1]).find("a").attr("href");
      var name = $(tr.find("td")[1]).find("a").text();
      layer.prompt({
        formType: 2,
        value: name,
        title: '请输入新文件名',
        area: ['200px', '50px'],
      }, function(value, index, elem){
        var data = {'action': 'rename', 'filename': $.trim(value)}
        $.post(url, data, function(ret){
          layer.close(index);
          if(ret.err)  layer.msg(ret.msg)
          else{
            layer.msg('重命名成功');
            location.reload();
          }
        })
      })
    })

    $(document).on("click", ".btn-move", function(){
      var tr = $(this).parents("tr");
      var url = $(tr.find("td")[1]).find("a").attr("href");
      layer.prompt({
        formType: 2,
        value: '',
        title: '请输入完整的文件夹路径',
        area: ['200px', '50px'],
      }, function(value, index, elem){
        var data = {'action': 'move', 'dirname': $.trim(value)}
        $.post(url, data, function(ret){
          layer.close(index);
          if(ret.err)  layer.msg(ret.msg)
          else{
            layer.msg('移动文件成功');
            location.reload();
          }
        })
      })
    })

    $(document).on("click", ".btn-action", function(){
      var tr = $(this).parents("tr");
      var url = $(tr.find("td")[1]).find("a").attr("href");
      var action = $(this).attr("action");
      var text = $(this).attr("text");
      if(text) layer.msg(text, {time: 30000});
      $.post(url, {'action': action}, function(ret){
        if(ret.msg) layer.msg(ret.msg)
        if(ret.url){
          var url = location.protocol + '//' + ret.url;
          copyData(url);
        }
      })
    })

    $(document).on("click", ".btn-delete", function(){
      var tr = $(this).parents("tr");
      var url = $(tr.find("td")[1]).find("a").attr("href");
      layer.confirm('确定删除？', {icon: 2, title: '提示'}, function(index){
        var data = {'action': 'delete'};
        $.post(url, data, function(ret){
          layer.close(index);
          if(ret.err)  layer.msg(ret.msg);
          else{
            layer.msg('删除成功');
            location.reload();
          }
        })
      })
    })

    $(document).on('click', '.btn-manage', function () {
      var id = $(this).parents('tr').data('id');
      var action = $(this).attr('action')
      $.post(location.pathname, {
        id: id,
        action: action
      }, function (ret) {
        if (ret.err) layer.msg(ret.msg);
        else location.reload();
      })
    })

    $(document).on('click', '.btn-email', function(){
      var email = $(this).parents('.layui-form-item').find('input').val();
      layer.msg('发送中，请稍后', {time:  60000});
      $.post('/email/check', {'email': email}, function(ret){
        if(ret.err) layer.msg(ret.msg)
        else layer.msg('发送验证码成功')
      })
    })

    $(document).on('click', '.weixin-login', function(){
      var id = $(this).data('id');
      var url = 'https://wx.ishield.cn/qrcode?site_id=' + id;
      $.get(url, function(ret){
        if(ret.err){
          layer.msg(ret.msg);
        }else{
          var counter = 0;
          var timer = setInterval(function () {
            counter += 1;
            $.get('/check', {
              scene: ret.data.check
            }, function(res){
              if(res.err == 0){
                clearInterval(timer);
                var next = parseUrl().params.next;
                if(next){
                  location.href = decodeURIComponent(next);
                }else{
                  location.href = '/admin';
                }
              }else if(res.err == 2){
                clearInterval(timer);
                layui.layer.alert(res.msg);
              }
              if( counter >= 1800 ){
                clearInterval(timer);
              }
            })
          }, 2000)
          layer.open({
            type: 1,
            title: false,
            area: ['340px', '340px'],
            offset: '200px',
            shadeClose: true,
            closeBtn: true,
            shade: 0.5,
            id: 'LAY_layuipro',
            moveType: 1,
            content: '<img src="' + ret.data.code + '">',
            cancel: function(index, layero){
              clearInterval(timer);
            }
          });
        }
      })
    })

    form.on('submit(default)', function (data) {
      var text = $(this).text();
      var btn = $(this);
      $(this).text('正在提交').addClass('layui-btn-disabled');
      $.ajax({
        type: data.form.getAttribute('method'),
        url: data.form.getAttribute('action'),
        data: data.field,
        success: function (ret) {
          var next = parseUrl().params.next;
          if (ret.err) layer.msg(ret.msg);
          else if (next || data.form.getAttribute('href')) {
            layer.msg('提交成功，重定向页面中');
            setTimeout(function(){
              if(next) {
                location.href = decodeURIComponent(next);
              }else{
                location.href = data.form.getAttribute('href');
              }
            }, 1000);
          }
          else if(data.form.getAttribute("reload")){
            layer.msg('提交成功, 刷新页面中');
            setTimeout(function(){
              location.reload();
            }, 1000)
          }else {
            layer.msg('提交成功');
          }
        },
        error: function () {
          layer.msg('提交失败');
        },
        complete: function () {
          btn.text(text).removeClass('layui-btn-disabled');
        }
      })
      return false;
    })

  })
})
