"use strict";

// استفاده از متغیر STATIC_URL تعریف شده در تمپلیت HTML
const headerPath = `${STATIC_URL}json-animations/header.json`;
const floatingPhone = `${STATIC_URL}json-animations/floating-phone.json`;
const stayMotivated = `${STATIC_URL}json-animations/stay-motivated.json`;
const personalisedLearning = `${STATIC_URL}json-animations/personalised-learning.json`;
const backedByScience = `${STATIC_URL}json-animations/backed-by-science.json`;
const freeFunEffective = `${STATIC_URL}json-animations/free-fun-effective.json`;

const animationLoader = (id, path, autoplays = false) => {
    const options = {
        container: document.getElementById(id),
        renderer: 'svg',
        loop: true,
        autoplay: autoplays,
        path: path,
    };
    bodymovin.loadAnimation(options);
};

// بارگذاری انیمیشن‌ها با مسیرهای اصلاح شده
animationLoader("left-logging-header", headerPath, true);
animationLoader("phone-animation", floatingPhone, true);
animationLoader("duolingo-feature-animation-stay-motivated", stayMotivated, true);
animationLoader("duolingo-feature-animation-personalised-learning", personalisedLearning, true);
animationLoader("duolingo-feature-animation-backed-by-science", backedByScience, true);
animationLoader("duolingo-feature-animation-free-fun-effective", freeFunEffective, true);