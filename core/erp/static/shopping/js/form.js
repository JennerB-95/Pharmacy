var tblProducts;
var shoppings = {
    items: {
        laboratory: '',
        date_joined: '',
        no_bill: '',
        subtotal: 0.00,
        total: 0.00,
        products: []
    },
    calculate_invoice: function () {
        var subtotal = 0.00;
        $.each(this.items.products, function (pos, dict) {
            dict.pos = pos;
            dict.subtotal = dict.cant * parseFloat(dict.pvp_cmp);
            subtotal += dict.subtotal;
        });
        this.items.subtotal = subtotal;
        this.items.total = this.items.subtotal;

        $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2));
        $('input[name="total"]').val(this.items.total.toFixed(2));
    },
    get_products_ids: function () {
        var ids = [];
        $.each(this.items.products, function (pos, dict) {
            ids.push(dict.id);
        });
        return ids;
    },
    add: function (item) {
        this.items.products.push(item);
        this.list();
    },
    list: function () {
        this.calculate_invoice();
        tblProducts = $('#tblProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.items.products,
            ordering: false,
            lengthChange: false,
            searching: false,
            paginate: false,
            columns: [
                {"data": "id"},
                {"data": "name"},
                // {"data": "cat.name"},
                {"data": "pvp_cmp"},
                {"data": "cant"},
                {"data": "subtotal"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="job-bg btn btn-danger btn-xs btn-flat" style="color: white;"><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        // return '<input type="text" name="pvp_cmp" class="form-control text-center form-control-sm input-sm" autocomplete="off" value="' + row.pvp_cmp + '">';
                        return 'Q. ' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="cant" class="form-control text-center form-control-sm input-sm" autocomplete="off" value="' + row.cant + '">';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return 'Q. ' + parseFloat(data).toFixed(2);
                    }
                },
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {

                $(row).find('input[name="cant"]').TouchSpin({
                    min: 1,
                    max: 1000000000,
                    step: 1
                });

            },
            initComplete: function (settings, json) {

            }
        });
        // console.clear();
    },
};

function formatRepo(repo) {
    if (repo.loading) {
        return repo.text;
    }

    var option = $(
        '<div class="wrapper container">' +
        '<div class="row">' +
        '<div class="col-lg-1">' +
        '<img src="' + repo.image + '" class="img-fluid img-thumbnail d-block mx-auto rounded">' +
        '</div>' +
        '<div class="col-lg-5 text-left shadow-sm">' +
        //'<br>' +
        '<p style="margin-bottom: 0;">' +
        '<b>Nombre:</b> ' + repo.name + '<br>' +
        '<b>Categoría:</b> ' + repo.cat.name + '<br>' +
        '<b>Precio Compra:</b> <span class="badge badge-warning">Q. ' + repo.pvp_cmp + '</span>' +
        '</p>' +
        '</div>' +
        '<div class="col-lg-5 text-left shadow-sm">' +
        //'<br>' +
        '<p style="margin-bottom: 0;">' +
        '<b>Componentes:</b> ' + repo.component + '<br>' +
        '<b>Ubicacion:</b> ' + repo.lot + '<br>' +
        '</p>' +
        '</div>' +

        '</div>' +
        '</div>');

    return option;
}

$(function () {
 
    $('.select2').select2({
        // theme: "bootstrap4",
        language: 'es'
    });

    $('#date_joined').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        // minDate: moment().format("YYYY-MM-DD")
    });

    // $("input[name='iva']").TouchSpin({
    //     min: 0,
    //     max: 100,
    //     step: 0.01,
    //     decimals: 2,
    //     boostat: 5,
    //     maxboostedstep: 10,
    //     postfix: '%'
    // }).on('change', function () {
    //     shoppings.calculate_invoice();
    // })
    //     .val(0.12);

    // search products

    /*$('input[name="search"]').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_products',
                    'term': request.term
                },
                dataType: 'json',
            }).done(function (data) {
                response(data);
            }).fail(function (jqXHR, textStatus, errorThrown) {
                //alert(textStatus + ': ' + errorThrown);
            }).always(function (data) {

            });
        },
        delay: 500,
        minLength: 1,
        select: function (event, ui) {
            event.preventDefault();
            console.clear();
            ui.item.cant = 1;
            ui.item.subtotal = 0.00;
            console.log(shoppings.items);
            shoppings.add(ui.item);
            $(this).val('');
        }
    });*/

    $('.btnRemoveAll').on('click', function () {
        if (shoppings.items.products.length === 0) return false;
        alert_action('Notificación', '¿Estas seguro de eliminar todos los items de tu detalle?', function () {
            shoppings.items.products = [];
            shoppings.list();
        }, function () {

        });
    });

    // event cant
    $('#tblProducts tbody')
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            alert_action('Notificación', '¿Estas seguro de eliminar el producto de tu detalle?',
                function () {
                    shoppings.items.products.splice(tr.row, 1);
                    shoppings.list();
                }, function () {

                });
        })
        .on('change', 'input[name="cant"]', function () {
            console.clear();
            var cant = parseInt($(this).val());
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            shoppings.items.products[tr.row].cant = cant;
            shoppings.calculate_invoice();
            $('td:eq(5)', tblProducts.row(tr.row).node()).html('Q' + shoppings.items.products[tr.row].subtotal.toFixed(2));
        })
        // .on('change', 'input[name="pvp_cmp"]', function () {
        //     console.clear();
        //     var pvp_cmp = parseInt($(this).val());
        //     var tr = tblProducts.cell($(this).closest('td, li')).index();
        //     shoppings.items.products[tr.row].pvp_cmp = pvp_cmp;
        //     shoppings.calculate_invoice();
        //     $('td:eq(5)', tblProducts.row(tr.row).node()).html('Q' + shoppings.items.products[tr.row].subtotal.toFixed(2));
        // })

    $('.btnClearSearch').on('click', function () {
        $('input[name="search"]').val('').focus();
    });

    // event submit
    $('form').on('submit', function (e) {
        e.preventDefault();

        if (shoppings.items.products.length === 0) {
            message_error('Debe al menos tener un item en su detalle de compra');
            return false;
        }

        shoppings.items.date_joined = $('input[name="date_joined"]').val();
        shoppings.items.laboratory = $('select[name="laboratory"]').val();
        shoppings.items.no_bill = $('input[name="no_bill"]').val();
        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('shoppings', JSON.stringify(shoppings.items));
        submit_with_ajax(window.location.pathname, 'Notificación',
            '¿Estas seguro de realizar la siguiente acción?', parameters, function (response) {
                    location.href = '/erp/shopping/list/';                
            });
    });





    $('.btnSearch').on('click', function () {
        tblSearchProd = $('#tblSearchProd').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_products',
                    'term': $('select[name="search"]').val(),
                    'ids': JSON.stringify(shoppings.get_products_ids()),
                },
                dataSrc: ""
            },
            //paging: false,
            //ordering: false,
            //info: false,
            columns: [
                {data: "name"},
                {data: "cat.name"},
                {data: "pvp_cmp"},
                {data: "pvp"},
                {data: "stock"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-3, -4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return 'Q' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.stock > 0) {
                            return '<span class="badge badge-success">' + data + '</span>'
                        }
                        return '<span class="badge badge-warning">' + data + '</span>'
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a rel="add" class="job-bg btn btn-success btn-flat btn-xs"><i class="fas fa-plus"></i></a>'
                    }
                }
            ],
            rowCallback: function (row, data, index) {
                var tr = $(row).closest('tr');
                if (data.stock === 0) {
                    $(tr).css({'background': '#dc3345', 'color': 'white'});
                }
            },
        });
        $('#myModalSearchProd').modal('show');
    });

    $('#tblSearchProd tbody').on('click', 'a[rel="add"]', function () {
        var row = tblSearchProd.row($(this).parents('tr')).data();
        row.cant = 1;
        shoppings.add(row);
        tblSearchProd.row($(this).parents('tr')).remove().draw();
    });








    $('select[name="search"]').select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: window.location.pathname,
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                    action: 'search_products'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese codigo de barra',
        minimumInputLength: 1,
        templateResult: formatRepo,
    }).on('select2:select', function (e) {
        var data = e.params.data;
        data.cant = 1;
        data.subtotal = 0.00;
        shoppings.add(data);
        $(this).val('').trigger('change.select2');
    });

    shoppings.list();
});