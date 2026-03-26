// Seleccion de elementos
const form = document.getElementById("registroForm");

const nombreInput = document.getElementById("id_nombre_completo");
const usernameInput = document.getElementById("id_username");
const emailInput = document.getElementById("id_email");
const passwordInput = document.getElementById("id_password1");
const password2Input = document.getElementById("id_password2");
const fechaNacimiento = document.getElementById("id_fecha_nacimiento");
const direccionInput = document.getElementById("id_direccion");
const celularInput = document.getElementById("id_celular");

// Errores
const nombreError = document.getElementById("nombre_completo-error");
const usernameError = document.getElementById("nombre_usuario-error");
const emailError = document.getElementById("correo-error");
const passwordError = document.getElementById("password1-error");
const password2Error = document.getElementById("password2-error");
const fechaError = document.getElementById("fecha_nacimiento-error");
const direccionError = document.getElementById("direccion-error");
const celularError = document.getElementById("celular-error");

// Requisitos visuales
const reqLength = document.getElementById("req-length");
const reqNumber = document.getElementById("req-number");
const reqSpecial = document.getElementById("req-special");
const reqFormato = document.getElementById("req-email-formato");
const reqSinEspacios = document.getElementById("req-email-sin-espacios");
const reqDominio = document.getElementById("req-email-dominio");
const reqUpper = document.getElementById("req-uppercase");
const reqNombreLongitud = document.getElementById("req-nombre-length");
const reqUsernameLongitud = document.getElementById("req-username-length");
const reqUsernameSinEspacios = document.getElementById("req-username-sin-espacios");

function validarNombreCompleto(nombre) {
    nombre = nombre.trim();
    const longitud = nombre.length >= 8;
    reqNombreLongitud.className = nombre ? (longitud ? "valido" : "invalid") : "";
    return nombre && longitud;
}

function validarUsername(username) {
    username = username.trim();
    const longitud = username.length >= 5 && username.length <= 18;
    const sinEspacios = username.indexOf(" ") === -1;
    reqUsernameLongitud.className = username ? (longitud ? "valido" : "invalid") : "";
    reqUsernameSinEspacios.className = username ? (sinEspacios ? "valido" : "invalid") : "";
    return username && longitud && sinEspacios;
}

function validarContrasena(contrasena) {
    const longitud = contrasena.length >= 8 && contrasena.length <= 18;
    const mayuscula = /[A-Z]/.test(contrasena);
    const numero = /\d/.test(contrasena);
    const especial = /[.,!@#$%^&*]/.test(contrasena);

    reqLength.className = contrasena ? (longitud ? "valido" : "invalid") : "";
    reqUpper.className = contrasena ? (mayuscula ? "valido" : "invalid") : "";
    reqNumber.className = contrasena ? (numero ? "valido" : "invalid") : "";
    reqSpecial.className = contrasena ? (especial ? "valido" : "invalid") : "";

    return contrasena && longitud && mayuscula && numero && especial;
}

function validarEmail(email) {
    email = email.trim();
    const formatoValido = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    const sinEspacios = email.indexOf(" ") === -1;
    const dominioValido =
        email.includes("@") && /^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(email.split("@")[1] || "");

    reqFormato.className = email ? (formatoValido ? "valido" : "invalid") : "";
    reqSinEspacios.className = email ? (sinEspacios ? "valido" : "invalid") : "";
    reqDominio.className = email ? (dominioValido ? "valido" : "invalid") : "";

    return email && formatoValido && sinEspacios && dominioValido;
}

function validarEdad(fecha) {
    const hoy = new Date();
    const cumple = new Date(fecha);
    let edad = hoy.getFullYear() - cumple.getFullYear();
    const m = hoy.getMonth() - cumple.getMonth();
    if (m < 0 || (m === 0 && hoy.getDate() < cumple.getDate())) edad--;
    return edad >= 13;
}

function validarCelular(celular) {
    const formatoValido = /^\d{9}$/.test(celular);
    celularError.textContent = formatoValido ? "" : "El número de celular debe tener 9 dígitos";
    celularError.style.display = formatoValido ? "none" : "block";
    return formatoValido;
}

function validarConfirmacionContrasena() {
    const password = passwordInput?.value || "";
    const confirmacion = password2Input?.value || "";

    if (!confirmacion.trim()) {
        password2Error.textContent = "Repita la contraseña";
        password2Error.style.display = "block";
        return false;
    }

    if (password !== confirmacion) {
        password2Error.textContent = "Las contraseñas no coinciden";
        password2Error.style.display = "block";
        return false;
    }

    password2Error.textContent = "";
    password2Error.style.display = "none";
    return true;
}

// Eventos de validación en tiempo real

nombreInput?.addEventListener("input", () => {
    validarNombreCompleto(nombreInput.value);
    nombreError.textContent = "";
});

usernameInput?.addEventListener("input", () => {
    validarUsername(usernameInput.value);
    usernameError.textContent = "";
});

passwordInput?.addEventListener("input", () => {
    validarContrasena(passwordInput.value);
    passwordError.textContent = "";
    if (password2Input?.value) {
        validarConfirmacionContrasena();
    }
});

password2Input?.addEventListener("input", () => {
    validarConfirmacionContrasena();
});

emailInput?.addEventListener("input", () => {
    validarEmail(emailInput.value);
    emailError.textContent = "";
});

celularInput?.addEventListener("input", () => {
    validarCelular(celularInput.value);
});

[nombreInput, usernameInput, fechaNacimiento, direccionInput, celularInput].forEach((input) => {
    input?.addEventListener("input", () => {
        const span = document.getElementById(input.id.replace("id_", "") + "-error");
        if (span) span.style.display = "none";
    });
});

form?.addEventListener("submit", (e) => {
    let valido = true;

    if (!nombreInput.value.trim() || !validarNombreCompleto(nombreInput.value)) {
        nombreError.textContent = "Ingrese un nombre completo valido";
        nombreError.style.display = "block";
        valido = false;
    }

    if (!nombreInput.value.trim()) {
        nombreError.textContent = "Ingrese su nombre completo";
        nombreError.style.display = "block";
        valido = false;
    }

    if (!usernameInput.value.trim() || !validarUsername(usernameInput.value)) {
        usernameError.textContent = "Ingrese un nombre de usuario valido";
        usernameError.style.display = "block";
        valido = false;
    }

    if (!usernameInput.value.trim()) {
        usernameError.textContent = "Ingrese un nombre de usuario";
        usernameError.style.display = "block";
        valido = false;
    }

    if (!emailInput.value.trim() || !validarEmail(emailInput.value)) {
        emailError.textContent = "Revise los requisitos del correo electrónico";
        emailError.style.display = "block";
        valido = false;
    }

    if (!passwordInput.value.trim() || !validarContrasena(passwordInput.value)) {
        passwordError.textContent = "Revise los requisitos de la contraseña";
        passwordError.style.display = "block";
        valido = false;
    }

    if (!validarConfirmacionContrasena()) {
        valido = false;
    }

    if (!fechaNacimiento.value || !validarEdad(fechaNacimiento.value)) {
        fechaError.textContent = "Debe tener al menos 13 años";
        fechaError.style.display = "block";
        valido = false;
    }

    if (!celularInput.value.trim() || !validarCelular(celularInput.value)) {
        celularError.textContent = "Ingrese un número de celular válido";
        celularError.style.display = "block";
        valido = false;
    }

    if (!valido) e.preventDefault();
});

function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    const icon = document.getElementById(`toggleIcon-${inputId}`);
    if (input.type === "password") {
        input.type = "text";
        icon.classList.remove("fa-eye");
        icon.classList.add("fa-eye-slash");
    } else {
        input.type = "password";
        icon.classList.remove("fa-eye-slash");
        icon.classList.add("fa-eye");
    }
}
