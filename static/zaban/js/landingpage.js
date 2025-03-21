const alreadyAccountButtonAnimation = () => {
    document.getElementById("already-have-account-button").classList.toggle('clicked');
    setTimeout(() => document.getElementById("already-have-account-button").classList.toggle('clicked'), 300)
    window.location.href = "login/"; // تغییر به URL جنگو
}

const getStartedButtonAnimation = () => {
    document.getElementById("get-started-button").classList.toggle('clicked');
    setTimeout(() => document.getElementById("get-started-button").classList.toggle('clicked'), 300);
    animationLoader();
    window.location.href = "language-select/"; // تغییر به URL جنگو
}

const showNextItem = () => {
    document.getElementById("footer-button").classList.toggle('clicked');
    setTimeout(() => document.getElementById("footer-button").classList.toggle('clicked'), 300)
}

const setIndexSiteLanguage = (path, language) => {
    fetch(path)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            document.getElementById('header-text').textContent = data['header-text'];
            document.getElementById('get-started-text').textContent = data['get-started-text'];
            document.getElementById('already-have-account-text').textContent = data['already-have-account-text'];
            document.getElementById('feature-head-1').textContent = data['feature-head-1'];
            document.getElementById('feature-body-1').textContent = data['feature-body-1'];
            document.getElementById('feature-head-2').textContent = data['feature-head-2'];
            document.getElementById('feature-body-2').textContent = data['feature-body-2'];
            document.getElementById('feature-head-3').textContent = data['feature-head-3'];
            document.getElementById('feature-body-3').textContent = data['feature-body-3'];
            document.getElementById('feature-head-4').textContent = data['feature-head-4'];
            document.getElementById('feature-body-4').textContent = data['feature-body-4'];
            document.getElementById('float-heading').textContent = data['float-heading'];
            document.getElementById('bottom-get-started-text').textContent = data['bottom-get-started-text'];
            document.getElementById('site-language').textContent = data['site-language'];
            localStorage.setItem("translateLanguage", language);
        })
        .catch(error => {
            console.error('Error fetching JSON:', error);
            // Fallback به زبان انگلیسی
            setIndexSiteLanguage(`${STATIC_URL}JSON/landing-english.json`, 'english');
        });
};

// مقداردهی اولیه زبان
let translateLanguage = localStorage.getItem("translateLanguage");
if (translateLanguage) {
    setIndexSiteLanguage(`${STATIC_URL}JSON/landing-${translateLanguage}.json`, translateLanguage);
} else {
    setIndexSiteLanguage(`${STATIC_URL}JSON/landing-english.json`, 'english');
}