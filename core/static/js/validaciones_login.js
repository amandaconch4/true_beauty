const form = document.getElementById('loginForm');
const username = document.getElementById('username');
const password = document.getElementById('password');
const usernameError = document.getElementById('username-error');
const passwordError = document.getElementById('password-error');

// Limpiar mensajes de error globales
function limpiarMensajesError() {
    if (usernameError) {
        usernameError.textContent = '';
        usernameError.style.display = 'none';
    }
    if (passwordError) {
        passwordError.textContent = '';
        passwordError.style.display = 'none';
    }
}

username.addEventListener('input', function() {
    if (username.value.trim() !== '') {
        usernameError.textContent = '';
        usernameError.classList.remove('mostrar');
    }
});

password.addEventListener('input', function() {
    if (password.value.trim() !== '') {
        passwordError.textContent = '';
        passwordError.classList.remove('mostrar');
    }
});

// Validación visual en tiempo real de la contraseña en login
const reqLength = document.getElementById('req-length');
const reqUpper = document.getElementById('req-uppercase');
const reqNumber = document.getElementById('req-number');
const reqSpecial = document.getElementById('req-special');

password.addEventListener('input', function() {
    const value = password.value;

    // Longitud
    if (value.length >= 6 && value.length <= 18) {
        reqLength.classList.remove('invalid');
        reqLength.classList.add('valid');
    } else {
        reqLength.classList.remove('valid');
        reqLength.classList.add('invalid');
    }
    // Mayúscula
    if (/[A-Z]/.test(value)) {
        reqUpper.classList.remove('invalid');
        reqUpper.classList.add('valid');
    } else {
        reqUpper.classList.remove('valid');
        reqUpper.classList.add('invalid');
    }
    // Número
    if (/\d/.test(value)) {
        reqNumber.classList.remove('invalid');
        reqNumber.classList.add('valid');
    } else {
        reqNumber.classList.remove('valid');
        reqNumber.classList.add('invalid');
    }
    // Especial
    if (/[.,!@#$%^&*]/.test(value)) {
        reqSpecial.classList.remove('invalid');
        reqSpecial.classList.add('valid');
    } else {
        reqSpecial.classList.remove('valid');
        reqSpecial.classList.add('invalid');
    }
});

// Validación al enviar el formulario
form.addEventListener('submit', function(e) {
    let esValido = true;

    if (username.value.trim() === '') {
        usernameError.textContent = 'Por favor, ingrese su nombre de usuario';
        usernameError.classList.add('mostrar');
        esValido = false;
    } else {
        usernameError.textContent = '';
        usernameError.classList.remove('mostrar');
    }

    if (password.value.trim() === '') {
        passwordError.textContent = 'Por favor, ingrese su contraseña';
        passwordError.classList.add('mostrar');
        esValido = false;
    } else {
        passwordError.textContent = '';
        passwordError.classList.remove('mostrar');

        if (
            !(password.value.length >= 6 && password.value.length <= 18) ||
            !(/[A-Z]/.test(password.value)) ||
            !(/\d/.test(password.value)) ||
            !(/[.,!@#$%^&*]/.test(password.value))
        ) {
            passwordError.textContent = 'La contraseña no cumple con los requisitos';
            passwordError.classList.add('mostrar');
            esValido = false;
        }
    }

    if (!esValido) {
        e.preventDefault();
    }
});

// Mostrar/ocultar contraseña
function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    const icon = document.getElementById(`toggleIcon-${inputId}`);
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