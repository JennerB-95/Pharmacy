(function($) {
  showAlert = function(type, objAlert) {
    'use strict';
    if (type === 'basic') {
      swal({
        text: objAlert.text,
        button: objAlert.button
      })

    } else if (type === 'title-and-text') {
      swal({
        title: objAlert.title,
        text: objAlert.text,
        button: objAlert.button
      })

    } else if (type === 'success-message') {
      swal({
        title: objAlert.title,
        text: objAlert.text,
        icon: 'success',
        button: {
          text: 'Continuar',
          value: true,
          visible: true,
          className: "btn btn-primary btn-success-confirm"
        }
      })

    } else if (type === 'error-message') {
      swal({
        title: objAlert.title,
        text: objAlert.text,
        icon: 'error',
        button: {
          text: 'Continuar',
          value: true,
          visible: true,
          className: "btn btn-primary btn-error-continue"
        }
      })

    } else if (type === 'auto-close') {
      swal({
        title: objAlert.title,
        text: objAlert.text,
        timer: objAlert.timer,
        button: false
      }).then(
        function() {},
        // handling the promise rejection
        function(dismiss) {
          if (dismiss === 'timer') {
            // console.log('I was closed by the timer')
          }
        }
      )
    } else if (type === 'warning-message-and-cancel') {
      swal({
        title: objAlert.title,
        text: objAlert.text,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3f51b5',
        cancelButtonColor: '#ff4081',
        confirmButtonText: 'Great ',
        buttons: {
          cancel: {
            text: 'Cancelar',
            value: null,
            visible: true,
            className: "btn btn-danger",
            closeModal: true,
          },
          confirm: {
            text: 'Confirmar',
            value: true,
            visible: true,
            className: "btn btn-primary",
            closeModal: true
          }
        }
      })

    } else if (type === 'custom-html') {
      swal({
        content: {
          element: "input",
          attributes: {
            placeholder: "Type your password",
            type: "password",
            class: 'form-control'
          },
        },
        button: {
          text: "OK",
          value: true,
          visible: true,
          className: "btn btn-primary"
        }
      })
    } else if (type === 'payment') {
      swal({
        content: '<h3>Test</h3>',
        button: {
          text: "OK",
          value: true,
          visible: true,
          className: "btn btn-primary"
        }
      })
    }
  }

})(jQuery);