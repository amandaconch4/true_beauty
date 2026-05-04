// Valida fecha y hora usando la fecha local del navegador.
document.addEventListener('DOMContentLoaded', function () {
    const fechaInput = document.getElementById('fecha');
    const horaInput = document.getElementById('hora');

    if (!fechaInput || !horaInput) return;

    const hoy = new Date();
    const horaActual = hoy.getHours();
    const minutosActuales = hoy.getMinutes();

    function fechaLocalISO(fecha) {
        const year = fecha.getFullYear();
        const month = String(fecha.getMonth() + 1).padStart(2, '0');
        const day = String(fecha.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }

    const fechaHoyStr = fechaLocalISO(hoy);

    function validarHoras() {
        const fechaSeleccionada = fechaInput.value;
        const esHoy = fechaSeleccionada === fechaHoyStr;

        horaInput.querySelectorAll('option').forEach(function (option) {
            if (option.value === '') return;

            if (!esHoy) {
                option.disabled = false;
                option.style.color = '';
                return;
            }

            const partesHora = option.value.split(':').map(Number);
            const hora = partesHora[0];
            const minutos = partesHora[1];
            const esPasada = hora < horaActual || (hora === horaActual && minutos < minutosActuales);

            option.disabled = esPasada;
            option.style.color = esPasada ? '#ccc' : '';
        });
    }

    let fechaMinima = fechaHoyStr;

    if (horaActual >= 17) {
        const manana = new Date();
        manana.setDate(manana.getDate() + 1);
        fechaMinima = fechaLocalISO(manana);
    }

    fechaInput.min = fechaMinima;

    if (!fechaInput.value || fechaInput.value < fechaMinima) {
        fechaInput.value = fechaMinima;
    }

    validarHoras();
    fechaInput.addEventListener('change', validarHoras);
});
