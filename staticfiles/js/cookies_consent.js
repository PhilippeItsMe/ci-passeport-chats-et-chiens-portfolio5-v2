function setCookieConsent(analytics, marketing) {
    let consentData = {
        essential: true,
        analytics: analytics,
        marketing: marketing
    };

    // Save consent in cookies
    document.cookie = "cookie_consent=" + JSON.stringify(consentData) + "; path=/; max-age=" + (365 * 24 * 60 * 60) + "; Secure; SameSite=Lax";

    // Send consent to Django backend
    fetch("/grpd/save-cookie-consent/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken() // Needed for Django protection
        },
        body: JSON.stringify(consentData)
    });

    document.getElementById("cookie-banner").style.display = "none";
}

// Get CSRF token for secure requests
function getCSRFToken() {
    let csrfToken = document.cookie.split("; ").find(row => row.startsWith("csrftoken="));
    return csrfToken ? csrfToken.split("=")[1] : "";
}

window.onload = function () {
    let cookies = document.cookie.split("; ");
    let consentGiven = cookies.find(row => row.startsWith("cookie_consent="));

    if (!consentGiven) {
        document.getElementById("cookie-banner").style.display = "block";
    }
};

// Function to reopen the cookie banner when clicking "Gérer les cookies"
function openCookieBanner() {
    document.getElementById("cookie-banner").style.display = "block";
}