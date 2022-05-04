var tblProducts;
var cli = {};
var product;
var fvSale;
var fvClient;
var input_datejoined;
var input_endate;
var input_birthdate;
var formGroupCredit;
var defaultDate;
var tblSearchProd;

var vents = {
    details: {
        cli: '',
        date_joined: '',
        end_date: '',
        subtotal: 0.00,
        iva: 0.00,
        dscto: 0.00,
        total: 0.00,
        payment: 0,
        prods: [],
    },
    calculate_invoice: function () {
        var subtotal = 0.00;
        $.each(this.details.prods, function (i, item) {
            item.pos = i;
            item.cant = parseInt(item.cant);
            item.subtotal = item.cant * parseFloat(item.pvp);
            subtotal += item.subtotal;
        });
        vents.details.subtotal = subtotal;
        vents.details.iva = subtotal * iva;
        vents.details.total = subtotal + vents.details.iva;
        $('input[name="subtotal"]').val(vents.details.subtotal.toFixed(2));
        $('input[name="iva"]').val(vents.details.iva.toFixed(2));
        $('input[name="total"]').val(vents.details.total.toFixed(2));
    },
    list_products: function () {
        this.calculate_invoice();
        tblProducts = $('#tblProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.details.prods,
            ordering: false,
            lengthChange: false,
            searching: false,
            paginate: false,
            columns: [
                {data: "id"},
                {data: "name"},
                {data: "categ.name"},
                {data: "stock"},
                {data: "cant"},
                {data: "pvp"},
                {data: "subtotal"},
            ],
            columnDefs: [
                {
                    targets: [-4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<span class="badge badge-secondary">' + data + '</span>';
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.stock === 0) {
                            return '---';
                        }
                        return '<input type="text" class="form-control input-sm" autocomplete="off" name="cant" value="' + row.cant + '">';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.stock === 0) {
                            return '---';
                        }
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.stock === 0) {
                            return '---';
                        }
                        return '<input type="text" class="form-control input-sm" autocomplete="off" name="pvp" value="' + row.pvp + '">';
                    }
                },
                {
                    targets: [0],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-flat btn-xs"><i class="fa fa-trash fa-1x"></i></a>';
                    }
                },
            ],
            rowCallback: function (row, data, index) {
                var frm = $(row).closest('tr');

                frm.find('input[name="cant"]')
                    .TouchSpin({
                        min: 1,
                        max: data.stock,
                    })
                    .keypress(function (e) {
                        return validate_form_text('numbers', e, null);
                    });

                frm.find('input[name="pvp"]')
                    .TouchSpin({
                        min: 0.00,
                        max: 1000000,
                        step: 0.01,
                        decimals: 2,
                        boostat: 5,
                        maxboostedstep: 10,
                    })
                    .keypress(function (e) {
                        return validate_decimals($(this), e);
                    });

            },
            initComplete: function (settings, json) {

            },
        });
    },
    get_products_ids: function () {
        var ids = [];
        $.each(this.details.prods, function (i, item) {
            ids.push(item.id);
        });
        return ids;
    },
    add_product: function (item) {
        this.details.prods.push(item);
        this.list_products();
    },
};


document.addEventListener('DOMContentLoaded', function (e) {
    const frmSale = document.getElementById('frmSale');
    fvSale = FormValidation.formValidation(frmSale, {
            locale: 'es_ES',
            localization: FormValidation.locales.es_ES,
            plugins: {
                trigger: new FormValidation.plugins.Trigger(),
                submitButton: new FormValidation.plugins.SubmitButton(),
                bootstrap: new FormValidation.plugins.Bootstrap(),
                excluded: new FormValidation.plugins.Excluded(),
                icon: new FormValidation.plugins.Icon({
                    valid: 'fa fa-check',
                    invalid: 'fa fa-times',
                    validating: 'fa fa-refresh',
                }),
            },
            fields: {
                payment: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione una forma de pago'
                        },
                    }
                },
                date_joined: {
                    validators: {
                        notEmpty: {
                            message: 'La fecha es obligatoria'
                        },
                        date: {
                            format: 'YYYY-MM-DD',
                            message: 'La fecha no es vÃ¡lida'
                        }
                    }
                },
                end_date: {
                    validators: {
                        notEmpty: {
                            message: 'La fecha es obligatoria'
                        },
                        date: {
                            format: 'YYYY-MM-DD',
                            message: 'La fecha no es vÃ¡lida'
                        }
                    }
                },
            },
        }
    )
        .on('core.element.validated', function (e) {
            if (e.valid) {
                const groupEle = FormValidation.utils.closest(e.element, '.form-group');
                if (groupEle) {
                    FormValidation.utils.classSet(groupEle, {
                        'has-success': false,
                    });
                }
                FormValidation.utils.classSet(e.element, {
                    'is-valid': false,
                });
            }
            const iconPlugin = fvSale.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            if (!e.result.valid) {
                const messages = [].slice.call(frmSale.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
            }
        })
        .on('core.form.valid', function () {
            var url_refresh = frmSale.getAttribute('data-url');

            if ($.isEmptyObject(cli)) {
                message_error('Debe tener un cliente seleccionado');
                $('input[name="search_cli"]').focus().select();
                return false;
            }

            vents.details.cli = cli.id;
            vents.details.date_joined = $('input[name="date_joined"]').val();
            vents.details.end_date = $('input[name="end_date"]').val();
            vents.details.payment = $('select[name="payment"]').val();

            if (vents.details.prods.length === 0) {
                message_error('Debe tener al menos un item en el detalle de la venta');
                return false;
            }

            submit_with_ajax('NotificaciÃ³n',
                'Â¿Estas seguro de guardar la siguiente compra?',
                pathname,
                {
                    'action': $('input[name="action"]').val(),
                    'id': $('input[name="id"]').val(),
                    'items': JSON.stringify(vents.details)
                },
                function (request) {
                    printInvoice(request.id);
                    location.href = '/erp/crm/sale/add/';
                },
            );
        });
});

document.addEventListener('DOMContentLoaded', function (e) {
    const frmClient = document.getElementById('frmClient');
    fvClient = FormValidation.formValidation(frmClient, {
            locale: 'es_ES',
            localization: FormValidation.locales.es_ES,
            plugins: {
                trigger: new FormValidation.plugins.Trigger(),
                submitButton: new FormValidation.plugins.SubmitButton(),
                bootstrap: new FormValidation.plugins.Bootstrap(),
                icon: new FormValidation.plugins.Icon({
                    valid: 'fa fa-check',
                    invalid: 'fa fa-times',
                    validating: 'fa fa-refresh',
                }),
            },
            fields: {
                names: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                    }
                },
                dni: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 10
                        },
                        digits: {},
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    obj: frmCli.querySelector('[name="dni"]').value,
                                    type: 'dni',
                                    action: 'validate_cli'
                                };
                            },
                            message: 'El nÃºmero de cedula ya se encuentra registrado',
                            method: 'POST'
                        }
                    }
                },
                mobile: {
                    validators: {
                        digits: {}
                    }
                },
                email: {
                    validators: {
                        regexp: {
                            regexp: /^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$/i,
                            message: 'El email no es correcto'
                        }
                    }
                },
                address: {
                    validators: {

                    }
                },
                birthdate: {
                    validators: {
                        notEmpty: {
                            message: 'La fecha es obligatoria'
                        },
                        date: {
                            format: 'YYYY-MM-DD',
                            message: 'La fecha no es vÃ¡lida'
                        }
                    }
                },
            },
        }
    )
        .on('core.element.validated', function (e) {
            if (e.valid) {
                const groupEle = FormValidation.utils.closest(e.element, '.form-group');
                if (groupEle) {
                    FormValidation.utils.classSet(groupEle, {
                        'has-success': false,
                    });
                }
                FormValidation.utils.classSet(e.element, {
                    'is-valid': false,
                });
            }
            const iconPlugin = fvClient.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            if (!e.result.valid) {
                const messages = [].slice.call(frmClient.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
            }
        })
        .on('core.form.valid', function () {
            submit_with_ajax('NotificaciÃ³n', 'Â¿Estas seguro de guardar el siguiente cliente?', pathname,
                {
                    names: $('#id_names').val(),
                    mobile: $('#id_mobile').val(),
                    address: $('#id_address').val(),
                    email: $('#id_email').val(),
                    dni: $('#id_dni').val(),
                    action: 'create_client'
                },
                function () {
                    $('#myModalAddClient').modal('hide');
                }
            );
        });
});


function printInvoice(id) {
    var printWindow = window.open("/erp/crm/sale/print/invoice/" + id + "/", 'Print', 'left=200, top=200, width=950, height=500, toolbar=0, resizable=0');
    printWindow.addEventListener('load', function () {
        printWindow.print();
    }, true);
}


$(function () {

    formGroupCredit = $('#formGroupCredit');
    defaultDate = new moment().format("YYYY-MM-DD");
    input_datejoined = $('input[name="date_joined"]');
    input_endate = $('input[name="end_date"]');
    input_search_cli = $('input[name="search_cli"]');
    input_cli_dni = $('input[name="pdni"]');
    input_birthdate = $('input[name="birthdate"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es",
    });

    $('select[name="payment"]')
        .on('change.select2', function () {
            fvSale.revalidateField('payment');
            var id = $(this).val();
            var start_date = input_datejoined.val();
            input_endate.datetimepicker('minDate', start_date);
            input_endate.datetimepicker('date', start_date);
            formGroupCredit.hide();
            if (id === 'credito') {
                formGroupCredit.show();
            }
        });

    $('.btnRemoveAll').on('click', function () {
        if (vents.details.prods.length === 0) return false;
        dialog_action('NotificaciÃ³n', 'Â¿Estas seguro de eliminar todos los items de tu detalle?', function () {
            var removeValFromIndex = [];
            $.each(vents.details.prods, function (k, v) {
                if (!v.hasOwnProperty('state')) {
                    removeValFromIndex.push(v.pos);
                }
            });
            for (var i = removeValFromIndex.length - 1; i >= 0; i--) {
                vents.details.prods.splice(removeValFromIndex[i], 1);
            }
            vents.list_products();
        });
    });

    $('input[name="search"]').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: pathname,
                data: {
                    'action': 'search_products',
                    'term': request.term,
                    'ids': JSON.stringify(vents.get_products_ids()),
                },
                dataType: "json",
                type: "POST",
                beforeSend: function () {

                },
                success: function (data) {
                    response(data);
                }
            });
        },
        min_length: 3,
        delay: 300,
        select: function (event, ui) {
            event.preventDefault();
            $(this).blur();
            if (ui.item.stock === 0) {
                message_error('El stock de este producto esta en 0');
                return false;
            }
            ui.item.cant = 1;
            vents.add_product(ui.item);
            $(this).val('').focus();
        }
    });

    $('.btnClear').on('click', function () {
        $('input[name="search"]').val('').focus();
    });

    $('#tblProducts tbody')
        .on('change', 'input[name="cant"]', function () {
            var td = tblProducts.cell($(this).closest('td, li')).index();
            var row = tblProducts.row(td.row).data();
            vents.details.prods[row.pos].cant = parseInt($(this).val());
            vents.calculate_invoice();
            var tr = $(this).parents('tr')[0];
            var subtotal = vents.details.prods[row.pos].subtotal.toFixed(2);
            $('td:eq(6)', tr).html('$' + subtotal);
        })
        .on('change', 'input[name="pvp"]', function () {
            var td = tblProducts.cell($(this).closest('td, li')).index();
            var row = tblProducts.row(td.row).data();
            vents.details.prods[row.pos].pvp = parseFloat($(this).val());
            vents.calculate_invoice();
            var tr = $(this).parents('tr')[0];
            var subtotal = vents.details.prods[row.pos].subtotal.toFixed(2);
            $('td:eq(6)', tr).html('$' + subtotal);
        })
        .on('click', 'a[rel="remove"]', function () {
            var td = tblProducts.cell($(this).closest('td, li')).index();
            var row = tblProducts.row(td.row).data();
            vents.details.prods.splice(row.pos, 1);
            vents.list_products();
        });

    input_search_cli.autocomplete({
        source: function (request, response) {
            $.ajax({
                url: pathname,
                data: {
                    action: 'search_cli',
                    term: request.term,
                },
                dataType: "json",
                type: "POST",
                beforeSend: function () {

                },
                success: function (data) {
                    response(data);
                }
            });
        },
        min_length: 3,
        delay: 300,
        select: function (event, ui) {
            event.preventDefault();
            $(this).val(ui.item.names);
            $(this).blur();
            cli = ui.item;
            input_cli_dni.val(ui.item.dni);
        }
    });

    $('.btnClearClient').on('click', function () {
        cli = null;
        $('#pdni').val('');
        $('input[name="search_cli"]').val('').focus();
    });

    $('.btnAddClient').on('click', function () {
        $('#myModalAddClient').modal('show');
    });

    $('#myModalAddClient').on('hidden.bs.modal', function () {
        fvClient.resetForm(true);
    });

    input_birthdate.datetimepicker({
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
        defaultDate: new moment().format("YYYY-MM-DD")
    });

    input_birthdate.datetimepicker('date', input_birthdate.val());

    input_birthdate.on('change.datetimepicker', function (e) {
        fvClient.revalidateField('birthdate');
    });

    $('input[name="dni"]').keypress(function (e) {
        return validate_form_text('numbers', e, null);
    });

    $('input[name="mobile"]').keypress(function (e) {
        return validate_form_text('numbers', e, null);
    });

    input_datejoined.datetimepicker({
        format: 'YYYY-MM-DD',
        useCurrent: false,
        locale: 'es',
        orientation: 'bottom',
        keepOpen: false
    });

    input_datejoined.datetimepicker('date', input_datejoined.val());

    input_datejoined.on('change.datetimepicker', function (e) {
        fvSale.revalidateField('date_joined');
        input_endate.datetimepicker('minDate', e.date);
        input_endate.datetimepicker('date', e.date);
    });

    input_endate.datetimepicker({
        useCurrent: false,
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
        minDate: defaultDate
    });

    input_endate.datetimepicker('date', input_endate.val());

    input_endate.on('change.datetimepicker', function (e) {
        fvSale.revalidateField('end_date');
    });

    formGroupCredit.hide();

    $('.btnSearch').on('click', function () {
        tblSearchProd = $('#tblSearchProd').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {
                    'action': 'search_products',
                    'term': $('input[name="search"]').val(),
                    'ids': JSON.stringify(vents.get_products_ids()),
                },
                dataSrc: ""
            },
            //paging: false,
            //ordering: false,
            //info: false,
            columns: [
                {data: "name"},
                {data: "categ.name"},
                {data: "pvp"},
                {data: "stock"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
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
                        if (row.stock > 0) {
                            return '<a rel="add" class="btn btn-secondary btn-flat btn-xs"><i class="fas fa-plus"></i></a>'
                        }
                        return 'No se puede agregar'
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
        vents.add_product(row);
        tblSearchProd.row($(this).parents('tr')).remove().draw();
    });

    if (!$.isEmptyObject(cli)) {
        input_cli_dni.val(cli.dni);
        input_search_cli.val(cli.names);
    }
});