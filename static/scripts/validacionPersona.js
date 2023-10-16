function validacionDeTeclasNumericas(event){
    return (event.charCode >= 48 && event.charCode <= 57)
}

function validacionDeTeclasLetras(evt){
    return ((evt.charCode >= 65 && evt.charCode <= 90)||(evt.charCode >= 97 && evt.charCode <= 122)||evt.charCode == 32);
}

let cuilInput = document.getElementById("id_cuil");

/*cuilInput.addEventListener("keydown", (evt) => {
    let valorCuil = cuilInput.value;
    if(valorCuil.length <= 11){
        return true;
    }else{
        return false;
    }
})*/

function cuil11Digitos(){
    let valorCuil = cuilInput.value;
    //alert("Valor: " + valorCuil)
    if(valorCuil.length < 11){
        return true;
    }else{
        return false;
    }
}

function controlCuil(evt){
    let esTeclaNum = validacionDeTeclasNumericas(evt);
    let longitud11 = cuil11Digitos();

    if(esTeclaNum && longitud11){
        return true;
    }else{
    return false;
    }
}