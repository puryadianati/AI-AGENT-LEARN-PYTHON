document.addEventListener('DOMContentLoaded', () => {
let ageInp = document.getElementById('age-input');
let nameInp = document.getElementById('name-input');
let emailInp = document.getElementById('email-input');
let passwordInp = document.getElementById('password-input');
let mainForm = document.getElementById('main-form');

let ageErrorMessage = document.getElementById('age-error-message');
let nameErrorMessage = document.getElementById('name-error-message');
let emailErrorMessage = document.getElementById('email-error-message');
let passwordErrorMessage = document.getElementById('password-error-message');

let RegisterUser = async (event) => {
    event.preventDefault();
    if (!ageInp || !nameInp || !emailInp || !passwordInp) {
        console.error('One or more input elements are missing in DOM.');
        return;
    }

    // اعتبارسنجی داده‌های ورودی
    if (!validate()) {
        return;
    }

    // نمایش وضعیت بارگذاری
    document.getElementById('loading-balls-container').classList.remove('hidden');
    document.getElementById('create-account-span').classList.add('hidden');
    console.log(JSON.stringify({
        age: ageInp.value,
        name: nameInp.value,
        email: emailInp.value,
        password: passwordInp.value,
    }));

    const userData = {
        age: ageInp.value,
        name: nameInp.value,
        email: emailInp.value,
        password: passwordInp.value,
    };

    console.log("Data being sent:", JSON.stringify(userData)); // بررسی داده‌های ارسال‌شده

    try {
        const response = await fetch('/zaban/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData), // تبدیل داده‌ها به JSON
        });


        // بررسی وضعیت پاسخ
        if (!response.ok) {
            throw response;
        }

        // دریافت داده‌های پاسخ
        const data = await response.json();

        console.log("Account created successfully:", data);

        // ذخیره اطلاعات کاربر در sessionStorage
        sessionStorage.setItem("user-info", JSON.stringify(data));

        // هدایت به صفحه یادگیری
        window.location.href = "./learn.html";
    } catch (error)  {
        // نمایش یا مخفی کردن وضعیت بارگذاری
        document.getElementById('create-account-span').classList.toggle('hidden');
        document.getElementById('loading-balls-container').classList.toggle('hidden');
    
        // بررسی ساختار خطا و استخراج داده‌ها
        let errorData = null;
    
        try {
            // اگر خطا یک پاسخ از سرور باشد، داده‌های JSON را استخراج کنید
            errorData = await error.json();
        } catch (e) {
            console.error("Error parsing JSON from error response:", e);
            errorData = { message: "An unknown error occurred" }; // مقدار پیش‌فرض برای خطاهای غیرمنتظره
        }
    
        console.log("Error data received:", errorData);
    
        // مدیریت خطاها بر اساس پیام
        switch (errorData.message) {
            case "email-already-in-use":
                emailErrorMessage.innerHTML = '<img src="../assets/svg/error-message-icon.svg" alt=""> <span>Email Already In Use.</span>';
                emailInp.style.border = '2px solid #ff0000'; // تغییر رنگ حاشیه به قرمز
                break;
    
            case "invalid-email":
                emailErrorMessage.innerHTML = '<img src="../assets/svg/error-message-icon.svg" alt=""> <span>Invalid Email Id</span>';
                emailInp.style.border = '2px solid #ff0000'; // تغییر رنگ حاشیه به قرمز
                break;
    
            case "weak-password":
                passwordErrorMessage.innerHTML = '<img src="../assets/svg/error-message-icon.svg" alt=""> <span>Weak Password</span>';
                passwordInp.style.border = '2px solid #ff0000'; // تغییر رنگ حاشیه به قرمز
                break;
    
            default:
                console.error("Unhandled error message:", errorData.message);
                alert("An error occurred: " + errorData.message); // نمایش پیام خطا
        }
    
        // چاپ اطلاعات خطا در کنسول برای اشکال‌زدایی
        console.log("Error code:", errorData.code || "No code provided");
        console.log("Error message:", errorData.message || "No message provided");
    }
};

// تابع اعتبارسنجی داده‌های ورودی
const validate = () => {
    let isValid = true;

    // پاک کردن پیام‌های خطای قبلی
    ageErrorMessage.textContent = '';
    nameErrorMessage.textContent = '';
    emailErrorMessage.textContent = '';
    passwordErrorMessage.textContent = '';


    // اعتبارسنجی سن
    if (!ageInp.value) {
        ageErrorMessage.innerHTML = '<img src="../assets/svg/error-message-icon.svg" alt=""> <span>Please enter your age.</span>';
        ageInp.style.border = '2px solid #ff0000';
        isValid = false;
    } else {
        ageErrorMessage.innerHTML = '';
        ageInp.style.border = '';
    }

    // اعتبارسنجی نام
    if (!nameInp.value) {
        nameErrorMessage.innerHTML = '<img src="../assets/svg/error-message-icon.svg" alt=""> <span>Please enter your Name.</span>';
        nameInp.style.border = '2px solid #ff0000';
        isValid = false;
    } else {
        nameErrorMessage.innerHTML = '';
        nameInp.style.border = '';
    }

    // اعتبارسنجی ایمیل
    if (!emailInp.value) {
        emailErrorMessage.innerHTML = '<img src="../assets/svg/error-message-icon.svg" alt=""> <span>Please enter your Email.</span>';
        emailInp.style.border = '2px solid #ff0000';
        isValid = false;
    } else {
        emailErrorMessage.innerHTML = '';
        emailInp.style.border = '';
    }

    // اعتبارسنجی رمز عبور
    if (!passwordInp.value) {
        passwordErrorMessage.innerHTML = '<img src="../assets/svg/error-message-icon.svg" alt=""> <span>Please enter your Password.</span>';
        passwordInp.style.border = '2px solid #ff0000';
        isValid = false;
    } else {
        passwordErrorMessage.innerHTML = '';
        passwordInp.style.border = '';
    }



    return isValid;
};

mainForm.addEventListener('submit', RegisterUser);
});