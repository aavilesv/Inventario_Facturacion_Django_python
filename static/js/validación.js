$('.chosen-select').chosen();
$('#websendeos').stacktable();

function sololetras(e) {
    tecla = (document.all) ? e.keyCode : e.which; // 2
    if (tecla == 8)
        return true; // 3
    patron = /[A-Za-z\s]/; // 4
    te = String.fromCharCode(tecla); // 5
    return patron.test(te); // 6
}
function soloNumeros(e) {
    var key = window.Event ? e.which : e.keyCode;
    return (key >= 48 && key <= 57)
}
function valida() {
    var nombre = document.getElementById('Celular').value;
    if (nombre == null || nombre.length < 7 || nombre.length > 11 || /^\s+$/.test(nombre)) {
        swal('Info!', 'Debe ingresar su celular o Telefono fijo, ingresar los digitos necesarios!');
        return false;
    }
}
function validaa() {
    var nombre = document.getElementById('Celularr').value;
    if (nombre == null || nombre.length < 7 || nombre.length > 11 || /^\s+$/.test(nombre)) {
        swal('Info!', 'Debe ingresar su celular o Telefono fijo, ingresar los digitos necesarios!');
        return false;
    }
}
function todo()
{
    if (valCedula()==false||valida()==false) {
        return false;
    }else {
        return true;
    }
}
function valCedula() {
    var cedula = document.getElementById("Cedula").value;
    if(cedula.length == 10){
        //Obtenemos el digito de la region que sonlos dos primeros digitos
        var digito_region = cedula.substring(0,2);
        //Pregunto si la region existe ecuador se divide en 24 regiones
        if( digito_region >= 1 && digito_region <=24 ){
            var dig;
            var suma_total=0;
            for (var i=0;i<9;i++){
                dig = parseInt(cedula.substring(i,i+1));
                if (i%2==0){
                    dig = dig*2 ;
                    if ( dig > 9)
                        dig = dig - 9;
                }
                suma_total = suma_total + dig;
            }
            // Extraigo el ultimo digito
            var ultimo_digito   = parseInt(cedula.substring(9,10));
            //Obtenemos la decena inmediata
            var z = 0;
            while (suma_total % 10 != 0) {
                suma_total++;
                z++;
            }
            //Validamos que el digito validador sea igual al de la cedula
            if(z == ultimo_digito){
                // alert('la cedula:' + cedula + ' es correcta');
                return true;
            }else{
                swal('Info!', 'La cedula:' + cedula + ' es incorrecta');
                return false;
            }
        }else{
            // imprimimos en consola si la region no pertenece
            swal('Info!', 'Esta cedula no pertenece a ninguna region');
            return false;
        }
    }
    swal('Info!', 'Ingrese sus digitos de cédula ');
    return false;
}

function validaron()
{
    if (ruc()==false||validaa()==false) {
        return false;
    }else {
        return true;
    }
}
function ruc() {
    var cedula = document.getElementById("Cedulaa").value;
    var ruc=cedula.substring(10,13);
    cedula=cedula.substring(0,10);
    if(cedula.length >= 10 && cedula.length <= 13 ){
        //Obtenemos el digito de la region que sonlos dos primeros digitos
        var digito_region = cedula.substring(0,2);
        //Pregunto si la region existe ecuador se divide en 24 regiones
        if( digito_region >= 1 && digito_region <=24 ){
            var dig;
            var suma_total=0;
            for (var i=0;i<9;i++){
                dig = parseInt(cedula.substring(i,i+1));
                if (i%2==0){
                    dig = dig*2 ;
                    if ( dig > 9)
                        dig = dig - 9;
                }
                suma_total = suma_total + dig;
            }
            // Extraigo el ultimo digito
            var ultimo_digito   = parseInt(cedula.substring(9,10));
            //Obtenemos la decena inmediata
            var z = 0;
            while (suma_total % 10 != 0) {
                suma_total++;
                z++;
            }
            //Validamos que el digito validador sea igual al de la cedula
            if(z == ultimo_digito){
                // alert('la cedula:' + cedula + ' es correcta');
                return true;
            }else{
                swal('Info!', 'Ruc o Cédula:' + cedula +ruc +' es incorrecta');
                return false;
            }
        }else{
            // imprimimos en consola si la region no pertenece
            swal('Info!', 'Esta cedula no pertenece a ninguna region');
            return false;
        }
    }
    swal('Info!', 'Ingrese sus digitos correctos de cédula o ruc ');
    return false;
}
/*
function validaCmbTipCli() {
  var indice = document.getElementById('cboTipCli').selectedIndex;
  if (indice == null || indice == 0) {
    //alertify.error("Debe seleccionar Tipo de cliente");
    alertify.alert("Debe seleccionar Tipo de cliente", function(){
      alertify.message('OK');
    });

    return false;
  }
}*/
/* JSON.stingify
  <input type="checkbox" id="idinss{{ cuentasporpagar.id }}"
 idnn="{{ cuentasporpagar.id }}" class="enviaotrocliente" >
 lista_clientescuentas = [];
$(".enviaotrocliente").each(function(){
  var idn =parseInt($(this).attr("idnn"));
  if ($('#idinss'+idn).attr('checked')){
	    var item = { id: idn};
            lista_clientescuentas .push(item);
  }
  
  if( $('.enviaotrocliente').is(':checked') ) {
  }
});*/
