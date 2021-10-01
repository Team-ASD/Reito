function muestraModal(url,tipo,usuario){
    document.getElementById('formEliminar').action = url;
    document.getElementById('contenido-modal').innerHTML = `¿Deseas eliminar a ${tipo} ${usuario}?`;
}

function muestraModalUsuarios(url,usuario){
    document.getElementById('formEliminarUsuario').action = url;
    document.getElementById('contenido-modal').innerHTML = `¿Deseas eliminar al usuario ${usuario}?`
}

<script>
     $(document).ready(function(){
        $('.dropdown-toggle').dropdown()
    });
</script>