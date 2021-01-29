var mensaje = function ( ms) {
    $.blockUI({
        message : '<h3>'+ms+'<i class="fa fa-spinner fa-spin fa-fw"></i></h3>',
        css: {
            border: 'none',
            padding: '15px',
            backgroundColor: '#000',
            '-webkit-border-radius': '10px',
            '-moz-border-radius': '10px',
            opacity: .5,
            color: '#fff'
        }
    });
};

$.ajaxSetup({    
    beforeSend: function () {
        mensaje('Solicitando');
    },
    complete: function (jqXHR, textStatus) {
      //$.unblockUI();
      setTimeout($.unblockUI, 1000);
    },
    error: function (jqXHR, textStatus,error) {
      mensaje('Error: ' +  error);
      //$.unblockUI();
      setTimeout($.unblockUI, 1000);
    }
});

