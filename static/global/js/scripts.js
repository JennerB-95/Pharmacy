const initDataTable = id => {
  $('#' + id).DataTable({
    "aLengthMenu": [
      [10, 20, 50, -1],
      [10, 20, 50, "All"]
    ],
    "iDisplayLength": 10,
    "language": {
      search: ""
    }
  });
  $('#' + id).each(function () {
    var datatable = $(this);
    // SEARCH - Add the placeholder for Search and Turn this into in-line form control
    var search_input = datatable.closest('.dataTables_wrapper').find('div[id$=_filter] input');
    search_input.attr('placeholder', 'Filter results');
    search_input.removeClass('form-control-sm');
    // LENGTH - Inline-Form control
    var length_sel = datatable.closest('.dataTables_wrapper').find('div[id$=_length] select');
    length_sel.removeClass('form-control-sm');
  });
}

const destroyDataTable = id => $('#' + id).DataTable().destroy()

const clearInputs = className => {
  const fields = document.getElementsByClassName(className)
  for (const field of fields) {
    field.value = ''
  }
}

const initSelect2ModalFields = () => {
  $(".select-2-modal").select2({
    theme: "bootstrap",
    width: 'auto',
    dropdownAutoWidth: true,
    dropdownParent: $('#modal')
  })
}

const initSelect2Fields = () => $(".select-2").select2()

const ShowModal = (title, body, footer, size) => {
  $(`#modal-title`).html(title)
  $(`#modal-body`).html(body)
  $(`#modal-footer`).html(footer)
  if (size) $('.modal-dialog').addClass(size)
  $('#modal').modal('toggle')
}

const getCurrentPage = page => {
  const currentURL = location.href.split('/')
  return currentURL[currentURL.length - 2] === page
}