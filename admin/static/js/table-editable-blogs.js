var TableEditable = function () {

    return {

        //main function to initiate the module
        init: function () {
            function restoreRow(oTable, nRow) {
                var aData = oTable.fnGetData(nRow);
                var jqTds = $('>td', nRow);

                for (var i = 0, iLen = jqTds.length; i < iLen; i++) {
                    oTable.fnUpdate(aData[i], nRow, i, false);
                }

                oTable.fnDraw();
            }

            function editRow(oTable, nRow, blog_id) {

                console.log('blog_id', blog_id);

                var aData = oTable.fnGetData(nRow);
                var jqTds = $('>td', nRow);
                jqTds[0].innerHTML = '<input type="text" class="m-wrap small" value="' + aData[0] + '">';
                jqTds[1].innerHTML = '<input type="text" class="m-wrap small" value="' + aData[1] + '">';

                // jqTds[5].innerHTML = '<input type="text" class="m-wrap small" value="' + aData[5] + '">';
                jqTds[2].innerHTML = '<select id="user_select" name="users[]"' +
                    'style="width: 203.51px">' +
                    '</select>';

                jqTds[3].innerHTML = '<a class="edit" href="" url=' + blog_id + '>Save</a>';
                jqTds[4].innerHTML = '<a class="cancel" href="">Cancel</a>';

                // 通过ajzx获取 users 列表，用于构造select 下拉框选项
                $.ajax({
                    async: true,
                    url: '/api/users/',
                    type: "GET",
                    dataType: "json",
                    delay: 30,
                    success: function(result){
                        console.log(result);
                        var roles = result;
                        var objSelectNow=document.getElementById("user_select");
                        for(var i in roles){
                            var objOption = document.createElement("OPTION");
                            objOption.text = roles[i]['username'];
                            objOption.value = roles[i]['id'];
                            objSelectNow.options.add(objOption);
                        }
                    },error:function(){
                        alert('/api/users/：获取users失败!')
                    }
                });

                // 初始化下拉框
                $('#user_select').select2({
                });
            }

            function saveRow(oTable, nRow, blog_id) {
                var jqInputs = $('input', nRow);

                // 获取下拉框的值 jqInputs[4]
                var user_res = $("#user_select").select2("data");

                console.log(user_res);
                //返回数组，单选就取res[0]；好处是不仅可以获取id、text还可以获取其他属性，如res[0].name
                var author_id = user_res['id'];
                var author = user_res['text'];

                var data = {
                    'title': jqInputs[0].value,
                    'content': jqInputs[1].value,
                    'author_id': author_id,
                };

                console.log(data);

                if(blog_id == "undefined"){  // 若未获取到blog_id，则表示新增，
                     var url = "/api/blogs/";
                     var type = 'POST';
                }else {  // 若获取到用户id，表示更新已有用
                    var url = "/api/blog/" + blog_id + '/';
                    var type = 'PUT';
                    data['id'] = blog_id;
                    //console.log(blog_id);
                };
                $.ajax({
                    async: true,
                    url: url,
                    type: type,
                    data: data,
                    success: function(result){
                        // 更新本地表格
                        //console.log(result);
                        oTable.fnUpdate(jqInputs[0].value, nRow, 0, false);
                        oTable.fnUpdate(jqInputs[1].value, nRow, 1, false);

                        oTable.fnUpdate(author, nRow, 2, false);

                        oTable.fnUpdate('<a class="edit" href="">' +
                            '<span class="fa fa-pencil glyphicon icon-pencil"></span>' +
                            '</a>', nRow, 3, false);
                        oTable.fnUpdate('<a class="delete" href="">' +
                            '<span class="fa fa-trash glyphicon icon-trash"></span>' +
                            '</a>', nRow, 4, false);
                        oTable.fnDraw();
                        alert('修改成功！');
                        },
                    error:function(){
                        alert('修改失败');
                        },
                });
            }

            function cancelEditRow(oTable, nRow) {
                var jqInputs = $('input', nRow);
                oTable.fnUpdate(jqInputs[0].value, nRow, 0, false);
                oTable.fnUpdate(jqInputs[1].value, nRow, 1, false);
                oTable.fnUpdate(jqInputs[2].value, nRow, 2, false);
                oTable.fnUpdate(jqInputs[3].value, nRow, 3, false);
                oTable.fnUpdate(jqInputs[4].value, nRow, 4, false);
                oTable.fnUpdate('<a class="edit" href="">Edit</a>', nRow, 5, false);
                oTable.fnDraw();
            }

            var oTable = $('#sample_editable_1').dataTable({
                "aLengthMenu": [
                    [5, 15, 20, -1],
                    [5, 15, 20, "All"] // change per page values here
                ],
                // set the initial value
                "iDisplayLength": 5,
                "sDom": "<'row-fluid'<'span6'l><'span6'f>r>t<'row-fluid'<'span6'i><'span6'p>>",
                "sPaginationType": "bootstrap",
                "oLanguage": {
                    "sLengthMenu": "_MENU_ records per page",
                    "oPaginate": {
                        "sPrevious": "Prev",
                        "sNext": "Next"
                    }
                },
                "aoColumnDefs": [{
                        'bSortable': false,
                        'aTargets': [0]
                    }
                ]
            });

            jQuery('#sample_editable_1_wrapper .dataTables_filter input').addClass("m-wrap medium"); // modify table search input
            jQuery('#sample_editable_1_wrapper .dataTables_length select').addClass("m-wrap small"); // modify table per page dropdown
            jQuery('#sample_editable_1_wrapper .dataTables_length select').select2({
                showSearchInput : false //hide search box with special css class
            }); // initialzie select2 dropdown

            var nEditing = null;

            $('#sample_editable_1_new').click(function (e) {
                e.preventDefault();
                var aiNew = oTable.fnAddData([
                    '', '', '',
                    '<a class="edit" href="">Edit</a>',
                    '<a class="cancel" data-mode="new" href="">Cancel</a>'
                ]);
                var nRow = oTable.fnGetNodes(aiNew[0]);
                editRow(oTable, nRow);
                nEditing = nRow;
            });

            $('#sample_editable_1 a.delete').live('click', function (e) {
                e.preventDefault();

                // 点击编辑后，先获取当前行的用户id
                var blog_id = $(this).attr('url');
                var nRow = $(this).parents('tr')[0];

                if (confirm("Are you sure to delete this row ?") == true) {
                    $.ajax({
                        async: true,
                        url: '/api/blog/' + blog_id +'/',
                        type: 'DELETE',
                        success: function(result){
                            alert(result);
                            oTable.fnDeleteRow(nRow);
                        },error:function(){
                            alert('删除失败！');
                        }
                    });
                };
            });

            $('#sample_editable_1 a.cancel').live('click', function (e) {
                e.preventDefault();
                if ($(this).attr("data-mode") == "new") {
                    var nRow = $(this).parents('tr')[0];
                    oTable.fnDeleteRow(nRow);
                } else {
                    restoreRow(oTable, nEditing);
                    nEditing = null;
                }
            });

            $('#sample_editable_1 a.edit').live('click', function (e) {
                // 点击编辑后，先尝试获取当前行的用户id
                // 可以获取到表示是更新已有用户,调用save时， 传入id
                // 获取不到，表示新增用户，调用save时，传入 id=0
                var blog_id = $(this).attr('url');
                console.log('点击编辑按钮：', blog_id);

                e.preventDefault();

                /* Get the row as a parent of the link that was clicked on */
                var nRow = $(this).parents('tr')[0];

                if (nEditing !== null && nEditing != nRow) {
                    /* Currently editing - but not this row - restore the old before continuing to edit mode */
                    restoreRow(oTable, nEditing);
                    editRow(oTable, nRow, blog_id);
                    nEditing = nRow;
                } else if (nEditing == nRow && this.innerHTML == "Save") {
                    /* Editing this row and want to save it */
                    // 获取
                    saveRow(oTable, nEditing, blog_id);
                    nEditing = null;
                    //alert("Updated! Do not forget to do some ajax to sync with backend :)");
                } else {
                    /* No edit in progress - let's start one */
                    editRow(oTable, nRow, blog_id);
                    nEditing = nRow;
                }
            });

        }

    };

}();