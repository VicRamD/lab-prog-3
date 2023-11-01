var hoy = new Date();
var dd = hoy.getDate();
var mm = hoy.getMonth() + 1; //Enero es 0!
var yyyy = hoy.getFullYear();

if (dd < 10) {
   dd = '0' + dd;
}

if (mm < 10) {
   mm = '0' + mm;
}

hoy = yyyy + '-' + mm + '-' + dd;
if(document.getElementById("id_fecha_presentacion") !== null){
    document.getElementById("id_fecha_presentacion").setAttribute("max", hoy);
}
if(document.getElementById("id_tribunal-fecha_disposicion") !== null){
    document.getElementById("id_tribunal-fecha_disposicion").setAttribute("max", hoy);
}
