// Selección de elementos
const form = document.getElementById('registroForm');
const nombreInput = document.getElementById('id_nombre_completo');
const usernameInput = document.getElementById('id_username');
const emailInput = document.getElementById('id_email');
const passwordInput = document.getElementById('id_password1');
const fechaNacimiento = document.getElementById('id_fecha_nacimiento');
const direccionInput = document.getElementById('id_direccion');
const celularInput = document.getElementById('id_celular');
// Errores
const nombreError = document.getElementById('nombre_completo-error');
const usernameError = document.getElementById('nombre_usuario-error');
const emailError = document.getElementById('correo-error');
const passwordError = document.getElementById('password1-error');
const fechaError = document.getElementById('fecha_nacimiento-error');
const direccionError = document.getElementById('direccion-error');
const celularError = document.getElementById('celular-error');
// Requisitos visuales
const reqLength = document.getElementById('req-length');
const reqNumber = document.getElementById('req-number');
const reqSpecial = document.getElementById('req-special');
const reqFormato = document.getElementById('req-email-formato');
const reqSinEspacios = document.getElementById('req-email-sin-espacios');
const reqDominio = document.getElementById('req-email-dominio');
const reqUpper = document.getElementById('req-uppercase');
const reqNombreLongitud = document.getElementById('req-nombre-length');
const reqUsernameLongitud = document.getElementById('req-username-length');
const reqUsernameSinEspacios = document.getElementById('req-username-sin-espacios');
const reqCelularDigits = document.getElementById('req-celular-digits');
// VALIDACIÓN VISUAL DE NOMBRE COMPLETO
function validarNombreCompleto(nombre) {
    nombre = (nombre || '').trim();
    const longitud = nombre.length >= 8;
    reqNombreLongitud.className = longitud ? 'valido' : 'invalid';
    return longitud;
}
// VALIDACIÓN VISUAL DE USERNAME
function validarUsername(username) {
    username = (username || '').trim();
    const longitud = username.length >= 5 && username.length <= 18;
    const sinEspacios = username.indexOf(' ') === -1;
    reqUsernameLongitud.className = longitud ? 'valido' : 'invalid';
    reqUsernameSinEspacios.className = sinEspacios ? 'valido' : 'invalid';
    return longitud && sinEspacios;
}
// VALIDACIÓN VISUAL DE CONTRASEÑA
function validarContrasena(contrasena) {
    contrasena = contrasena || '';
    const longitud = contrasena.length >= 8 && contrasena.length <= 18;
    const mayuscula = /[A-Z]/.test(contrasena);
    const numero = /\d/.test(contrasena);
    const especial = /[.,!@#$%^&*]/.test(contrasena);
    reqLength.className = longitud ? 'valido' : 'invalid';
    reqUpper.className = mayuscula ? 'valido' : 'invalid';
    reqNumber.className = numero ? 'valido' : 'invalid';
    reqSpecial.className = especial ? 'valido' : 'invalid';
    return longitud && mayuscula && numero && especial;
}
// VALIDACIÓN VISUAL DE EMAIL
function validarEmail(email) {
    email = (email || '').trim();
    const formatoValido = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    const sinEspacios = email.indexOf(' ') === -1;
    const dominioValido = email.includes('@') &&
        /^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(email.split('@')[1] || '');
    reqFormato.className = formatoValido ? 'valido' : 'invalid';
    reqSinEspacios.className = sinEspacios ? 'valido' : 'invalid';
    reqDominio.className = dominioValido ? 'valido' : 'invalid';
    return formatoValido && sinEspacios && dominioValido;
}
// VALIDACIÓN VISUAL DE CELULAR
function validarCelular(celular) {
    celular = (celular || '').trim();
    const formatoValido = /^\d{9}$/.test(celular);
    reqCelularDigits.className = formatoValido ? 'valido' : 'invalid';
    return formatoValido;
}
function validarEdad(fecha) {
    if (!fecha) return false;
    const hoy = new Date();
    const cumple = new Date(fecha);
    let edad = hoy.getFullYear() - cumple.getFullYear();
    const m = hoy.getMonth() - cumple.getMonth();
    if (m < 0 || (m === 0 && hoy.getDate() < cumple.getDate())) edad--;
    return edad >= 13;
}
// Eventos en tiempo real
nombreInput?.addEventListener('input', () => {
    validarNombreCompleto(nombreInput.value);
    nombreError.textContent = '';
});
usernameInput?.addEventListener('input', () => {
    validarUsername(usernameInput.value);
    usernameError.textContent = '';
});
passwordInput?.addEventListener('input', () => {
    validarContrasena(passwordInput.value);
    passwordError.textContent = '';
});
emailInput?.addEventListener('input', () => {
    validarEmail(emailInput.value);
    emailError.textContent = '';
});
celularInput?.addEventListener('input', () => {
    validarCelular(celularInput.value);
    celularError.textContent = '';
});
[nombreInput, usernameInput, fechaNacimiento, direccionInput, celularInput].forEach(input => {
    input?.addEventListener('input', () => {
        const span = document.getElementById(input.id.replace('id_', '') + '-error');
        if (span) span.style.display = 'none';
    });
});
// Validación al enviar
form?.addEventListener('submit', (e) => {
    let valido = true;
    if (!validarNombreCompleto(nombreInput?.value)) {
        nombreError.textContent = 'Ingrese un nombre completo válido';
        nombreError.style.display = 'block';
        valido = false;
    }
    if (!validarUsername(usernameInput?.value)) {
        usernameError.textContent = 'Ingrese un nombre de usuario válido';
        usernameError.style.display = 'block';
        valido = false;
    }
    if (!validarEmail(emailInput?.value)) {
        emailError.textContent = 'Revise los requisitos del correo electrónico';
        emailError.style.display = 'block';
        valido = false;
    }
    if (!validarContrasena(passwordInput?.value)) {
        passwordError.textContent = 'Revise los requisitos de la contraseña';
        passwordError.style.display = 'block';
        valido = false;
    }
    if (!validarEdad(fechaNacimiento?.value)) {
        fechaError.textContent = 'Debe tener al menos 13 años';
        fechaError.style.display = 'block';
        valido = false;
    }
    if (!validarCelular(celularInput?.value)) {
        celularError.textContent = 'Ingrese un número de celular válido (9 dígitos)';
        celularError.style.display = 'block';
        valido = false;
    }
    if (!valido) e.preventDefault();
});
// Inicializar requisitos al cargar (todos parten en rojo)
document.addEventListener('DOMContentLoaded', () => {
    validarNombreCompleto(nombreInput?.value || '');
    validarUsername(usernameInput?.value || '');
    validarEmail(emailInput?.value || '');
    validarContrasena(passwordInput?.value || '');
    validarCelular(celularInput?.value || '');
});
function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    const icon = document.getElementById(`toggleIcon-${inputId}`);
    if (!input || !icon) return;
    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}
