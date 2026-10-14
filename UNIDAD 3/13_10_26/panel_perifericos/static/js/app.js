async function cargarConfiguracion() {
    const respuesta = await fetch("/api/config");

    if (!respuesta.ok) {
        throw new Error("Error al cargar la configuración");
    }

    const configuracion = await respuesta.json();
    document.querySelector("Titulo")
        .textContent = configuracion.titulo;
}

cargarConfiguracion();