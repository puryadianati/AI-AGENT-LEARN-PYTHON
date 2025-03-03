const validate = (event) => {
    event.preventDefault();
    const fields = {
        age: document.getElementById('age-input'),
        name: document.getElementById('name-input'),
        email: document.getElementById('email-input'),
        password: document.getElementById('password-input')
    };

    const errorMessages = {
        age: document.getElementById('age-error-message'),
        name: document.getElementById('name-error-message'),
        email: document.getElementById('email-error-message'),
        password: document.getElementById('password-error-message')
    };

    // Reset all styles and messages
    Object.values(errorMessages).forEach(msg => msg.innerHTML = '');
    Object.values(fields).forEach(field => field.style.border = '');

    let isValid = true;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;

    // Age validation
    if (!fields.age.value || fields.age.value < 13) {
        showError(fields.age, errorMessages.age, 'Please enter a valid age (minimum 13 years).');
        isValid = false;
    }

    // Name validation
    if (!fields.name.value.trim()) {
        showError(fields.name, errorMessages.name, 'Please enter your name.');
        isValid = false;
    }

    // Email validation
    if (!fields.email.value) {
        showError(fields.email, errorMessages.email, 'Please enter your email.');
        isValid = false;
    } else if (!emailRegex.test(fields.email.value)) {
        showError(fields.email, errorMessages.email, 'Please enter a valid email address.');
        isValid = false;
    }

    // Password validation
    if (!fields.password.value) {
        showError(fields.password, errorMessages.password, 'Please enter your password.');
        isValid = false;
    } else if (!passwordRegex.test(fields.password.value)) {
        showError(fields.password, errorMessages.password, 'Password must be at least 8 characters with at least one letter and one number.');
        isValid = false;
    }

    if (isValid) {
        submitForm(event);
    }
};

const showError = (field, errorElement, message) => {
    errorElement.innerHTML = `
        <img src="{% static 'zaban/assets/svg/error-message-icon.svg' %}" alt="error">
        <span>${message}</span>
    `;
    field.style.border = '2px solid #ff0000';
};

const submitForm = async (event) => {
    const form = event.target;
    const button = document.getElementById('create-account-button');
    const loader = document.getElementById('loading-balls-container');
    const mainText = document.getElementById('create-account-span');

    toggleButtonState(button, loader, mainText, true);

    try {
        const response = await fetch("{% url 'signup' %}", {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Accept': 'application/json',
            },
            body: new FormData(form)
        });

        const data = await response.json();
        
        if (data.success) {
            window.location.href = "{% url 'dashboard' %}";
        } else {
            handleServerErrors(data.errors);
        }
    } catch (error) {
        console.error('Error:', error);
        showErrorNotification('An error occurred. Please try again.');
    } finally {
        toggleButtonState(button, loader, mainText, false);
    }
};

const toggleButtonState = (button, loader, textElement, isLoading) => {
    button.disabled = isLoading;
    loader.classList.toggle('hidden', !isLoading);
    textElement.classList.toggle('hidden', isLoading);
};

const loginButtonAnimation = () => {
    window.location.href = LOGIN_URL;
};

// Helper function to get CSRF token
const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

// Initialize form submission handler
document.getElementById('main-form').addEventListener('submit', validate);