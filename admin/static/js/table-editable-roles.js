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

            function editRow(oTable, nRow, role_id) {

                console.log('role_id', role_id);

                var aData = oTable.fnGetData(nRow);
                var jqTds = $('>td', nRow);
                jqTds[0].innerHTML = '<input type="text" class="m-wrap small" value="' + aData[0] + '">';
                jqTds[1].innerHTML = '<input type="text" class="m-wrap small" value="' + aData[1] + '">';

                // jqTds[5].innerHTML = '<input type="text" class="m-wrap small" value="' + aData[5] + '">';
                jqTds[2].innerHTML = '<select id="user_select" name="users[]" multiple="multiple"' +
                    'style="width: 203.51px">' +
                    '</select>';

                jqTds[3].innerHTML = '<select id="operation_select" name="operations[]" multiple="multiple"' +
                    'style="width: 203.51px">' +
                    '</select>';

                jqTds[4].innerHTML = '<a class="edit" href="" url=' + role_id + '>Save</a>';
                jqTds[5].innerHTML = '<a class="cancel" href="">Cancel</a>';

                // 通过ajax获取 用户 列表，用于构造select 下拉框选项
                $.ajax({
                    async: true,
                    url: '/api/users/',
                    type: "GET",
                    dataType: "json",
                    delay: 30,
                    success: function(result){
                        console.log(result);
                        var users = result;
                        var objSelectNow=document.getElementById("user_select");
                        for(var i in users){
                            var objOption = document.createElement("OPTION");
                            objOption.text = users[i]['username'];
                            objOption.value = users[i]['id'];
                            objSelectNow.options.add(objOption);
                        }
                    },error:function(){
                        alert('/api/users/：获取users失败!')
                    }
                });

                // 通过ajax获取 operations 列表，用于构造select 下拉框选项
                $.ajax({
                    async: true,
                    url: '/api/operations/',
                    type: "GET",
                    dataType: "json",
                    delay: 30,
                    success: function(result){
                        console.log(result);
                        var operations = result;
                        var objSelectNow=document.getElementById("operation_select");
                        for(var i in operations){
                            var objOption = document.createElement("OPTION");
                            objOption.text = operations[i]['name'];
                            objOption.value = operations[i]['id'];
                            objSelectNow.options.add(objOption);
                        }
                    },error:function(){
                        alert('/api/operations/：获取operations失败!')
                    }
                });

                // 初始化下拉框
                $('#user_select').select2({
                });
                $('#operation_select').select2({
                });
            }

            function saveRow(oTable, nRow, role_id) {
                var jqInputs = $('input', nRow);

                // 获取下拉框的值 jqInputs[2]
                var user_res = $("#user_select").select2("data");
                // console.log(user_res);
                //返回数组，单选就取res[0]；好处是不仅可以获取id、text还可以获取其他属性，如res[0].name
                var user_ids = [];
                var user_texts= [];
                for(var i in user_res){
                    user_ids.push(user_res[i].id);
                    user_texts.push(user_res[i].text);
                }

                // 获取下拉框的值 jqInputs[2]
                var operation_res = $("#operation_select").select2("data");
                // console.log(user_res);
                //返回数组，单选就取res[0]；好处是不仅可以获取id、text还可以获取其他属性，如res[0].name
                var operation_ids = [];
                var operation_texts= [];
                for(var i in operation_res){
                    operation_ids.push(operation_res[i].id);
                    operation_texts.push(operation_res[i].text);
                }

                var data = {
                    'name': jqInputs[0].value,
                    'status': jqInputs[1].value,
                    'users': user_ids.toString(),
                    'operations': operation_ids.toString(),
                };

                console.log(data);

                // 通过传入参数 role_id 判断时新增还是修改
                if(role_id == "undefined"){  // 若未获取到role_id，则表示新增，
                     var url = "/api/roles/";
                     var type = 'POST';
                }else{  // 若获取到用户id，表示更新已有用
                    var url = "/api/role/" + role_id + '/';
                    var type = 'PUT';
                    data['id'] = role_id;
                    //console.log(role_id);
                };

                $.ajax({
                    async: true,
                    url: url,
                    type: type,
                    data: data,
                    success: function(result){
                        // 更新本地表格
                        console.log(result);
                        oTable.fnUpdate(jqInputs[0].value, nRow, 0, false);
                        oTable.fnUpdate(jqInputs[1].value, nRow, 1, false);

                        oTable.fnUpdate('[' + user_texts.toString() + ']', nRow, 2, false);
                        oTable.fnUpdate('[' + operation_texts.toString() + ']', nRow, 3, false);

                        oTable.fnUpdate('<a class="edit" href="">' +
                            '<span class="fa fa-pencil glyphicon icon-pencil"></span>' +
                            '</a>', nRow, 4, false);
                        oTable.fnUpdate('<a class="delete" href="">' +
                            '<span class="fa fa-trash glyphicon icon-trash"></span>' +
                            '</a>', nRow, 5, false);
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
                    '', '1', '', '',
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
                var role_id = $(this).attr('url');
                var nRow = $(this).parents('tr')[0];

                if (confirm("Are you sure to delete this row ?") == true) {
                    $.ajax({
                        async: true,
                        url: '/api/role/' + role_id +'/',
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
                var role_id = $(this).attr('url');
                console.log('点击编辑按钮：', role_id);

                e.preventDefault();

                /* Get the row as a parent of the link that was clicked on */
                var nRow = $(this).parents('tr')[0];

                if (nEditing !== null && nEditing != nRow) {
                    /* Currently editing - but not this row - restore the old before continuing to edit mode */
                    restoreRow(oTable, nEditing);
                    editRow(oTable, nRow, role_id);
                    nEditing = nRow;
                } else if (nEditing == nRow && this.innerHTML == "Save") {
                    /* Editing this row and want to save it */
                    // 获取
                    saveRow(oTable, nEditing, role_id);
                    nEditing = null;
                    //alert("Updated! Do not forget to do some ajax to sync with backend :)");
                } else {
                    /* No edit in progress - let's start one */
                    editRow(oTable, nRow, role_id);
                    nEditing = nRow;
                }
            });

        }

    };

}();