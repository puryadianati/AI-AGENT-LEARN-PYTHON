// فراخوانی ایونت‌ها با استفاده از Django URL
const loginAccountButtonAnimation = (event) => {
    event.preventDefault();
    const button = document.getElementById("create-account-button");
    const loadingIndicator = document.getElementById("loading-balls-container");
    const loginText = document.getElementById("login-span");

    toggleButtonState(button, loadingIndicator, loginText, true);
    
    setTimeout(() => {
        validateEntry(event);
        toggleButtonState(button, loadingIndicator, loginText, false);
    }, 1000);
};

const signupButtonAnimation = () => {
    const button = document.getElementById("login-button");
    button.classList.add('clicked');
    
    setTimeout(() => {
        button.classList.remove('clicked');
        window.location.href = SIGNUP_URL; // استفاده از متغیر全局
    }, 300);
};

// اعتبارسنجی پیشرفته با استفاده از Django Messages
const validateEntry = async (event) => {
    event.preventDefault();
    const form = event.target.closest('form');
    const formData = new FormData(form);
    
    try {
        const response = await fetch("{% url 'login' %}", {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Accept': 'application/json',
            },
            body: formData
        });

        const data = await response.json();
        
        if (data.success) {
            window.location.href = "{% url 'dashboard' %}";
        } else {
            handleValidationErrors(data.errors);
        }
    } catch (error) {
        console.error('Error:', error);
        showGeneralError();
    }
};

// توابع کمکی
const toggleButtonState = (button, loader, textElement, isLoading) => {
    button.classList.toggle('clicked', isLoading);
    loader.classList.toggle('hidden', !isLoading);
    textElement.classList.toggle('hidden', isLoading);
};

const handleValidationErrors = (errors) => {
    // مدیریت خطاهای سرور
    const errorMapping = {
        username: 'emailInput',
        password: 'passInput'
    };

    for (const [field, messages] of Object.entries(errors)) {
        const elementId = errorMapping[field] || field;
        const input = document.getElementById(elementId);
        const errorDiv = document.getElementById(`error${field.charAt(0).toUpperCase() + field.slice(1)}`);
        
        showError(input, errorDiv, messages.join(', '));
    }
};

const showError = (inputElement, errorElement, message) => {
    errorElement.innerHTML = `
        <img src="{% static 'zaban/assets/svg/error-message-icon.svg' %}" alt="error">
        <span>${message}</span>
    `;
    inputElement.style.border = '2px solid #ff0000';
};

const showGeneralError = () => {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'global-error';
    errorDiv.innerHTML = `
        <img src="{% static 'zaban/assets/svg/error-message-icon.svg' %}" alt="error">
        <span>خطایی در ارتباط با سرور رخ داده است</span>
    `;
    document.body.prepend(errorDiv);
};

// تابع دریافت کوکی CSRF
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

// تنظیم ایونت لیسنرها
document.getElementById('login-form').addEventListener('submit', validateEntry);
document.getElementById('signup-button').addEventListener('click', signupButtonAnimation);