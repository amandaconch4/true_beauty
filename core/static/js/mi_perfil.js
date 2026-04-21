// Selección de elementos
const form = document.getElementById('perfilForm');
const nombreInput = document.getElementById('nombre_completo');
const emailInput = document.getElementById('email');
const celularInput = document.getElementById('celular');
const passwordNueva = document.getElementById('password_nueva');
const passwordConfirmar = document.getElementById('password_confirmar');

// Requisitos visuales
const reqNombreLongitud = document.getElementById('req-nombre-length');
const reqEmailFormato = document.getElementById('req-email-formato');
const reqEmailEspacios = document.getElementById('req-email-espacios');
const reqCelularDigits = document.getElementById('req-celular-digits');
const reqLength = document.getElementById('req-length');
const reqUpper = document.getElementById('req-uppercase');
const reqNumber = document.getElementById('req-number');
const reqSpecial = document.getElementById('req-special');

// VALIDACIÓN DE NOMBRE COMPLETO
function validarNombre(nombre) {
    nombre = (nombre || '').trim();
    const longitud = nombre.length >= 8;
    if (reqNombreLongitud) {
        reqNombreLongitud.className = longitud ? 'valido' : 'invalid';
    }
    return longitud;
}

// VALIDACIÓN DE EMAIL
function validarEmail(email) {
    email = (email || '').trim();
    const formatoValido = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    const sinEspacios = email.indexOf(' ') === -1;
    
    if (reqEmailFormato) reqEmailFormato.className = formatoValido ? 'valido' : 'invalid';
    if (reqEmailEspacios) reqEmailEspacios.className = sinEspacios ? 'valido' : 'invalid';
    
    return formatoValido && sinEspacios;
}

// VALIDACIÓN DE CELULAR
function validarCelular(celular) {
    celular = (celular || '').trim();
    const formatoValido = /^\d{9}$/.test(celular);
    if (reqCelularDigits) {
        reqCelularDigits.className = formatoValido ? 'valido' : 'invalid';
    }
    return formatoValido;
}

// VALIDACIÓN DE CONTRASEÑA NUEVA
function validarPasswordNueva(password) {
    password = password || '';
    const longitud = password.length >= 6 && password.length <= 18;
    const mayuscula = /[A-Z]/.test(password);
    const numero = /\d/.test(password);
    const especial = /[.,!@#$%^&*]/.test(password);
    
    if (reqLength) reqLength.className = longitud ? 'valido' : 'invalid';
    if (reqUpper) reqUpper.className = mayuscula ? 'valido' : 'invalid';
    if (reqNumber) reqNumber.className = numero ? 'valido' : 'invalid';
    if (reqSpecial) reqSpecial.className = especial ? 'valido' : 'invalid';
    
    return longitud && mayuscula && numero && especial;
}

// Eventos en tiempo real
nombreInput?.addEventListener('input', () => {
    validarNombre(nombreInput.value);
    document.getElementById('nombre-error').textContent = '';
});

emailInput?.addEventListener('input', () => {
    validarEmail(emailInput.value);
    document.getElementById('email-error').textContent = '';
});

celularInput?.addEventListener('input', () => {
    // Solo permitir números
    celularInput.value = celularInput.value.replace(/\D/g, '').slice(0, 9);
    validarCelular(celularInput.value);
    document.getElementById('celular-error').textContent = '';
});

passwordNueva?.addEventListener('input', () => {
    validarPasswordNueva(passwordNueva.value);
    document.getElementById('password-error').textContent = '';
});

passwordConfirmar?.addEventListener('input', () => {
    document.getElementById('password-confirmar-error').textContent = '';
});

// Toggle password visibility
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

// Funciones para el modal de eliminar cuenta
function confirmarEliminarCuenta() {
    const modal = document.getElementById('modal-eliminar');
    if (modal) {
        modal.classList.add('show');
        document.body.style.overflow = 'hidden';
    }
}

function cerrarModal() {
    const modal = document.getElementById('modal-eliminar');
    if (modal) {
        modal.classList.remove('show');
        document.body.style.overflow = '';
    }
}

// Cerrar modal al hacer clic fuera de él
document.getElementById('modal-eliminar')?.addEventListener('click', (e) => {
    if (e.target.id === 'modal-eliminar') {
        cerrarModal();
    }
});

// Cerrar modal con tecla Escape
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        cerrarModal();
    }
});

// Validación al enviar
form?.addEventListener('submit', (e) => {
    let valido = true;
    
    // Validar nombre
    if (!validarNombre(nombreInput?.value)) {
        document.getElementById('nombre-error').textContent = 'El nombre completo debe tener al menos 8 caracteres.';
        valido = false;
    }
    
    // Validar email
    if (!validarEmail(emailInput?.value)) {
        document.getElementById('email-error').textContent = 'Ingrese un correo electrónico válido.';
        valido = false;
    }
    
    // Validar celular
    if (!validarCelular(celularInput?.value)) {
        document.getElementById('celular-error').textContent = 'El celular debe tener exactamente 9 dígitos.';
        valido = false;
    }
    
    // Validar contraseña solo si se está intentando cambiar
    const passwordActual = document.getElementById('password_actual')?.value;
    const passwordNuevaVal = passwordNueva?.value;
    const passwordConfirmarVal = passwordConfirmar?.value;
    
    if (passwordNuevaVal || passwordConfirmarVal || passwordActual) {
        if (!passwordActual) {
            alert('Debe ingresar su contraseña actual para cambiar la contraseña.');
            valido = false;
        } else if (passwordNuevaVal && !validarPasswordNueva(passwordNuevaVal)) {
            document.getElementById('password-error').textContent = 'La nueva contraseña no cumple con los requisitos.';
            valido = false;
        } else if (passwordNuevaVal !== passwordConfirmarVal) {
            document.getElementById('password-confirmar-error').textContent = 'Las contraseñas no coinciden.';
            valido = false;
        }
    }
    
    if (!valido) {
        e.preventDefault();
    }
});

// Inicializar validaciones al cargar
document.addEventListener('DOMContentLoaded', () => {
    validarNombre(nombreInput?.value || '');
    validarEmail(emailInput?.value || '');
    validarCelular(celularInput?.value || '');
    validarPasswordNueva('');
});
