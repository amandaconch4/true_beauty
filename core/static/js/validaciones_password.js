document.addEventListener('DOMContentLoaded', function () {
    const password1 = document.getElementById('id_new_password1');
    const password2 = document.getElementById('id_new_password2');

    if (!password1 || !password2) {
        return;
    }

    const requirements = {
        length: document.getElementById('req-length'),
        letter: document.getElementById('req-letter'),
        number: document.getElementById('req-number'),
        special: document.getElementById('req-special'),
    };

    function toggleState(element, isValid) {
        if (!element) {
            return;
        }

        element.style.color = isValid ? '#2d7249' : '#5d4a39';
        element.style.fontWeight = isValid ? '700' : '400';
    }

    function validatePassword() {
        const value = password1.value || '';

        toggleState(requirements.length, value.length >= 8);
        toggleState(requirements.letter, /[A-Za-z]/.test(value));
        toggleState(requirements.number, /\d/.test(value));
        toggleState(requirements.special, /[^A-Za-z0-9]/.test(value));
    }

    function validateMatch() {
        if (!password2.value) {
            password2.setCustomValidity('');
            return;
        }

        password2.setCustomValidity(
            password1.value === password2.value ? '' : 'Las contrasenas no coinciden.'
        );
    }

    password1.addEventListener('input', function () {
        validatePassword();
        validateMatch();
    });

    password2.addEventListener('input', validateMatch);

    validatePassword();
});
