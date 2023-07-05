     function buttons () {
        return {
          btnAdd: {
            text: 'Add new row',
            icon: 'bi bi-trash',
            event: function () {
              alert('Do some stuff to e.g. add a new row')
            },
            attributes: {
              class: 'Add a new row to the table'
            }
          }
        }
    }


 // Formatter for "name" column
    function nameFormatter(value, row, index) {
        return '<input id="nameinput" type="text" class="form-control " value="' + value + '">';
    }

       // Define options for select input
    const typeOptions_db = [
        {value: "PostgreSQL", text: "PostgreSQL"},
        {value: "AliCloud", text: "AliCloud"},
        {value: "Oracle", text: "Oracle"},
        {value: "DB2", text: "DB2"},
        {value: "GCP", text: "GCP"},
        {value: "API", text: "API"},
        {value: "Fileserver", text: "Fileserver"},
    ];

    // Formatter for "type" column
    function typeFormatter_db(value, row, index) {
        let optionsHtml = '';
        typeOptions_db.forEach(option => {
            optionsHtml += '<option value="' + option.value + '"';
            if (option.value === value) {
                optionsHtml += ' selected';
            }
            optionsHtml += '>' + option.text + '</option>';
        });
        return '<select id="typedbinput" class="form-select ">' + optionsHtml + '</select>';
    }


           // Define options for select input
    const typeOptions = [
        {value: "My connection", text: "My connection"},
        {value: "External connection", text: "External connection"}
    ];

    // Formatter for "type" column
    function typeFormatter(value, row, index) {
        let optionsHtml = '';
        typeOptions.forEach(option => {
            optionsHtml += '<option value="' + option.value + '"';
            if (option.value === value) {
                optionsHtml += ' selected';
            }
            optionsHtml += '>' + option.text + '</option>';
        });
        return '<select id="typeinput" class="form-select">' + optionsHtml + '</select>';
    }


    function hostFormatter(value, row, index) {
        return '<input id="hostinput"  type="text" class="form-control" value="' + value + '">';
    }


    function libraryFormatter(value, row, index) {
        return '<input id="libraryinput"  type="text" class="form-control" value="' + value + '">';
    }

    function userFormatter(value, row, index) {
        return '<input id="userinput"  type="text" class="form-control" value="' + value + '">';
    }


    function pwdFormatter(value, row, index) {
        return '<input type="password" id="pwdinput"  type="text" class="form-control" value="' + value + '">';
    }

       // Formatter for "action" column
    function actionFormatter(value, row, index) {
        return ' <div class="btn-group" role="group" aria-label="...">'+
        '<button  class="btn btn-sm btn-primary edit-row" > <i class="bi bi-pencil-square"></i> </button>'+
        '<button  class="btn btn-sm btn-danger delete-row" style="margin-left: 10px;"><i class="bi bi-trash"></i></button>'+
      '</div>'
    }

    const $table = $('#table');

    /////delete function
    function deleteRow($tr) {
        const id = $tr.find('td:eq(0)').text();
        console.log({id: id})
        $.ajax({
            url: '/delete-data',
            type: 'POST',
            data: JSON.stringify({id: id}),
            contentType: 'application/json',
            success: function () {
                toastr.success('Delete successfully!');
                $tr.remove();
                $('#table').bootstrapTable('refresh');
            },
            error: function (error) {
                console.log(error);
                toastr.success('Failed to delete the data. Please try again.');
            }
        });
    }


    $table.on('click', '.delete-row', function () {
        const $tr = $(this).closest('tr');

        bootbox.confirm({
            message: 'Please confirm if you want to delete?',
            buttons: {
                confirm: {
                    label: 'Yes',
                    className: 'btn-success'
                },
                cancel: {
                    label: 'No',
                    className: 'btn-danger'
                }
            },
            callback: function (result) {
                if (result) {
                    deleteRow($tr)
                }
            }
        });

    });



    /////edit function

    function saveRow($tr) {
        const connect_id = $tr.find('td:eq(0)').text();
        const connect_name = $tr.find('input[id="nameinput"]').val();
        const dbtype = $tr.find('select[id="typedbinput"]').val();
        const connect_type = $tr.find('select[id="typeinput"]').val();
        const username = $tr.find('select[id="userinput"]').val();
        const pwd = $tr.find('input[id="pwdinput"]').val();
        const library = $tr.find('select[id="libraryinput"]').val();
        const host = $tr.find('input[id="hostinput"]').val();

        console.log($tr.data('unique-id'));
        console.log($tr.find('.editable:eq(0)').val());

        const data = {
            'connect_id': connect_id,
            'connect_name': connect_name,
            'dbtype': dbtype,
            'connect_type': connect_type,
            'host': host,
            'dblibrary': library,
            'username': username,
            'pwd': pwd,
        };

        console.log(data)

        $.ajax({
            url: '/update-data',
            type: 'POST',
            data: JSON.stringify(data),
            contentType: 'application/json',
            success: function () {
                $('#table').bootstrapTable('refresh');
                toastr.success('update successfully!');

            },
            error: function (error) {
                console.log(error);
                alert('Failed to save the data. Please try again.');
            }
        });
    }

    $table.on('click', '.edit-row', function () {
        const $tr = $(this).closest('tr');
        const $editBtn = $(this);
        const $saveBtn = $('<button class="btn btn-sm btn-success save-row">Save</button>');
        $editBtn.replaceWith($saveBtn);
        $tr.find('input, select').prop('disabled', false);
        $tr.find('input, select').addClass('editable');
        $tr.addClass('editing');
    });

    $table.on('click', '.save-row', function () {
        const $tr = $(this).closest('tr');
        const $saveBtn = $(this);
        const $editBtn = $('<button class="btn btn-sm btn-primary edit-row">Edit</button>');
        $saveBtn.replaceWith($editBtn);
        $tr.find('input, select').prop('disabled', true);
        $tr.find('input, select').removeClass('editable');
        $tr.removeClass('editing');
        // 调用 saveRow 保存编辑状态
        console.log($tr)
        saveRow($tr);
    });

