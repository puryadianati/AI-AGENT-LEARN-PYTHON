let emailInput = document.getElementById("email-input");
let passwordInput = document.getElementById("password-input");
let mainForm = document.getElementById("main-form");

let emailErrorMessage = document.getElementById('email-error-message');
let passwordErrorMessage = document.getElementById('password-error-message');

let signInUser = (event) => {
  console.log("Reached Signin");
  event.preventDefault();

  if (!validateEntry(event)) {
    return;
  }

  // Fetch the CSRF token from the cookies or HTML meta tag
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  fetch('/zaban/login/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken, // Include CSRF token
    },
    body: JSON.stringify({
      email: emailInput.value,
      password: passwordInput.value,
    }),
  })
    .then((response) => {
      if (!response.ok) {
        throw response;
      }
      return response.json();
    })
    .then((data) => {
      console.log("Login successful", data);
      sessionStorage.setItem("user-info", JSON.stringify(data));
      window.location.href = "./learn.html";
    })
    .catch((error) => {
      error.json().then((errorData) => {
        switch (errorData.message) {
          case "Invalid email or password.":
            emailErrorMessage.innerHTML =
              '<img src="/static/zaban/assets/svg/error-message-icon.svg" alt=""> <span>Invalid Credentials</span>';
            emailInput.style.border = "2px solid #ff0000";
            passwordInput.style.border = "2px solid #ff0000";
            break;
        }
      });
    });
};

const validateEntry = (event) =>{
    event.preventDefault();

    let isValid = true;
    if (!emailInput.value) {
        emailErrorMessage.innerHTML = '<img src="/static/zaban/assets/svg/error-message-icon.svg" alt=""> <span>Enter an Email</span>';
        emailInput.style.border = '2px solid #ff0000';
        isValid = false;
    }
    else{
        emailErrorMessage.innerHTML = '';
        emailInput.style.border = '';
    }

    if (!passwordInput.value) {
        passwordErrorMessage.innerHTML = '<img src="/static/zaban/assets/svg/error-message-icon.svg" alt=""> <span>Enter a Password.</span>';
        passwordInput.style.border = '2px solid #ff0000';
        isValid = false;
    }
    else{
        passwordErrorMessage.innerHTML = '';
        passwordInput.style.border = '';
    }
    return isValid;
}

mainForm.addEventListener("submit", signInUser);