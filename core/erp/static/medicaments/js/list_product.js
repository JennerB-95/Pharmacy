
$(function () {

        tblProduct = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            // {"data": "id"},
            {"data": "barcode"},
            {"data": "name"},
            // {"data": "cat.name"},
            {"data": "stock"},
            {"data": "due_date"},
            {"data": "lot"},
            {"data": "image"},
            {"data": "pvp"},
            {"data": "pvp"},
        ],
        columnDefs: [
            {
                targets: [0],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {    
                    return '<svg id="code" name="code"></svg>' 
                }
            },
            {
                targets: [-6],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {    
                    if (row.stock >= 0 & row.stock < 10){
                        return '<div class="badge badge-danger badge-pill">'+ row.stock+ '</div>'
                    }
                    if (row.stock > 10 & row.stock < 50){
                        return '<div class="badge badge-warning badge-pill">' +row.stock + '</div>'
                    }
                    else{
                        return '<div class="badge badge-success badge-pill">' +row.stock + '</div>'                                  
                    }
                }
            },
            {
                targets: [-5],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {    
                    if (row.status_med > 30){
                        return '<div class="badge badge-success badge-pill">'+ row.status_med+ ' - ' + row.due_date +'</div>'
                    }
                    if (row.status_med <= 30 & row.status_med > 0){
                        return '<div class="badge badge-warning badge-pill">' +row.status_med + ' - ' +row.due_date+ '</div>'
                    }
                    else{
                        return '<div class="badge badge-danger badge-pill">' +row.status_med + ' - ' + row.due_date + '</div>'                                  
                    }
                }
            },
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<a rel="see"> <img src="'+data+'" class="img-fluid d-block mx-auto" style="width: 50px; height: 50px;"></a>';
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return 'Q.'+parseFloat(data).toFixed(2);
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/erp/product/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a>';
                    buttons += '<a href="/erp/product/delete/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        rowCallback(row, data, displayNum, displayIndex, dataIndex) {            
            $(row).find('svg[name="code"]').JsBarcode(data.barcode,{displayValue:true, width:0.5, height:30, fontSize:10});
        },
        initComplete: function (settings, json) {
        }
    });


    $('#data tbody').on('click', 'a[rel="see"]', function(){
        var tr = tblProduct.cell($(this).closest('td, li')).index();
        var data = tblProduct.row(tr.row).data();
        $('#image').attr("src", data.image);
        $("label[for='name']").text(data.name);
        $('#barcode').JsBarcode(data.barcode,{displayValue:true,fontSize:10, width:1, height:50 });
        $("label[for='lab']").text(data.lab.description);
        $("label[for='cat']").text(data.cat.name);
        $("label[for='price_vnt']").text('Q. '+ data.pvp);
        $("label[for='component']").text(data.component);
        $("label[for='indication']").text(data.indication);

        $('#myModalProduct').modal('show');
        console.log(data);
    }); 

});
