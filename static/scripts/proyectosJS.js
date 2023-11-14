/*function agregarEstudiante(){
    let bodyTabla = document.getElementById("tablaAlumnos");
    let nombreInput = document.getElementById("nombreAlumno");
    let nombreValor = nombreInput.value;
    let apellidoInput = document.getElementById("apellidoAlumno");
    let apellidoValor = apellidoInput.value;
    let dniInput = document.getElementById("dniAlumno");
    let dniValor = dniInput.value;
    let matriculaInput = document.getElementById("matriculaAlumno");
    let matriculaValor = matriculaInput.value;

    let fila = document.createElement("tr");
    let colDNI = document.createElement("td");
    colDNI.appendChild(document.createTextNode(dniValor));
    let colApellido = document.createElement("td");
    colApellido.appendChild(document.createTextNode(apellidoValor));
    let colNombre = document.createElement("td");
    colNombre.appendChild(document.createTextNode(nombreValor));
    let colMatricula = document.createElement("td");
    colMatricula.appendChild(document.createTextNode(matriculaValor));

    let comparacion = evitarEstudiantesRepetidos(dniValor);
    if(comparacion){
        alert(`Ya se ha ingresado un estudiante con DNI ${dniValor}`);
    }else{
        fila.appendChild(colDNI);
        fila.appendChild(colApellido);
        fila.appendChild(colNombre);
        fila.appendChild(colMatricula);
        bodyTabla.appendChild(fila);
        
        nombreInput.value = "";
        apellidoInput.value = "";
        dniInput.value = "";
        matriculaInput.value = "";
    }
} */

/*function evitarEstudiantesRepetidos(dni){
    let celdasDatosEstudiantes = document.getElementsByTagName("td");
    let comparacion = false;
    let hijoCelda;
    for(let i = 0; i < celdasDatosEstudiantes.length; i+=4){
        hijoCelda = celdasDatosEstudiantes[i].firstChild;
        if(hijoCelda.data === dni){
            comparacion = true;
        }
    }
    return comparacion;
}*/

function validacionDeTeclasNumericas(event){
    return (event.charCode >= 48 && event.charCode <= 57)
}

function validacionDeTeclasLetras(evt){
    return ((evt.charCode >= 65 && evt.charCode <= 90)||(evt.charCode >= 97 && evt.charCode <= 122)||evt.charCode == 32);
}

let nombreInput = document.getElementById("id_nombre");

function ocultarOpciones(){
    const list_e = document.getElementById('integrantesSelecionados');
    const cadena = document.getElementById('buscarEstudiante').value.toUpperCase();
    const options = list_e.childNodes;

    if(cadena === ''){
        for(i=1; i<options.length; i=i+2){
            console.log(options[i]);
            options[i].style.display = 'block';
        }
    }
    else{
        for(i=1; i<options.length; i=i+2){
            if(options[i].innerHTML.toUpperCase().includes(cadena)){
                options[i].style.display = 'block';
            }else{
                options[i].style.display = 'none';
            }
        }
    }
}

function mostrarTodasLasOpciones(){
    const list_e = document.getElementById('integrantesSelecionados');
    const options = list_e.childNodes;

    for(i=1; i<options.length; i=i+2){
        options[i].style.display = 'block';
    }
}