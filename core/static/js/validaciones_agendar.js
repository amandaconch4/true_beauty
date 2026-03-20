// Validar fecha y hora para agendar citas (hoy solo hasta las 17:00)
document.addEventListener('DOMContentLoaded', function() {
    const fechaInput = document.getElementById('fecha');
    const horaInput = document.getElementById('hora');
    const hoy = new Date();
    const horaActual = hoy.getHours();
    const minutosActuales = hoy.getMinutes();
    const fechaHoyStr = hoy.toISOString().split('T')[0];

    // Función para validar y actualizar horas disponibles
    function validarHoras() {
        const fechaSeleccionada = fechaInput.value;
        const esHoy = fechaSeleccionada === fechaHoyStr;

        if (esHoy) {
            // Si es hoy, deshabilitar horas que ya pasaron
            const horasDisponibles = horaInput.querySelectorAll('option');
            horasDisponibles.forEach(option => {
                if (option.value === '') return; // Skip placeholder

                const [hora, minutos] = option.value.split(':').map(Number);
                const esPasada = hora < horaActual || (hora === horaActual && minutos < minutosActuales);

                if (esPasada) {
                    option.disabled = true;
                    option.style.color = '#ccc';
                } else {
                    option.disabled = false;
                    option.style.color = '';
                }
            });
        } else {
            // Si es una fecha futura, habilitar todas las horas
            const horasDisponibles = horaInput.querySelectorAll('option');
            horasDisponibles.forEach(option => {
                option.disabled = false;
                option.style.color = '';
            });
        }
    }

    // Si son las 17:00 o después, deshabilitar fecha de hoy
    if (horaActual >= 17) {
        // Establecer la fecha mínima a mañana
        const mañana = new Date();
        mañana.setDate(mañana.getDate() + 1);
        const fechaMañana = mañana.toISOString().split('T')[0];
        fechaInput.min = fechaMañana;
        fechaInput.value = fechaMañana; // Preseleccionar mañana
    } else {
        // Si es antes de las 17:00, se puede elegir hoy
        fechaInput.min = fechaHoyStr;
        fechaInput.value = fechaHoyStr; // Preseleccionar hoy (permitido antes de las 17:00)
    }

    // Validar horas al cargar la página
    validarHoras();

    // Validar horas cuando cambie la fecha
    fechaInput.addEventListener('change', validarHoras);
});

