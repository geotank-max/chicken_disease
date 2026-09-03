/**
 * IDNS - Core Application Scripts
 * Features: Dark/Light Mode Theme Toggle, Form Validations, UI Utilities
 */

// ── Theme Manager ───────────────────────────────────────────────
window.getStoredTheme = function() {
    try {
        return localStorage.getItem('theme') || 'light';
    } catch(e) {
        return 'light';
    }
};

window.setStoredTheme = function(theme) {
    try {
        localStorage.setItem('theme', theme);
    } catch(e) {}
};

window.applyTheme = function(theme) {
    const isDark = theme === 'dark';
    document.documentElement.setAttribute('data-theme', theme);
    document.documentElement.setAttribute('data-bs-theme', theme);

    // Update all theme toggle buttons across the DOM
    const toggleButtons = document.querySelectorAll('.theme-toggle-btn, #themeToggleBtn, #themeToggleBtnDiagnose, #themeToggleBtnLogin, #themeToggleBtnRegister');
    toggleButtons.forEach(btn => {
        const titleLight = btn.getAttribute('data-title-light') || 'Switch to light mode';
        const titleDark = btn.getAttribute('data-title-dark') || 'Switch to dark mode';
        const newTitle = isDark ? titleLight : titleDark;
        
        btn.setAttribute('title', newTitle);
        btn.setAttribute('aria-label', newTitle);

        const icon = btn.querySelector('i');
        if (icon) {
            if (isDark) {
                icon.className = 'bi bi-sun-fill text-warning';
            } else {
                icon.className = 'bi bi-moon-stars-fill text-secondary';
            }
        }
    });

    // Dispatch custom event for charts or components that need theme changes
    try {
        window.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme: theme, isDark: isDark } }));
    } catch(e) {}
};

let _lastThemeToggleTime = 0;
window.toggleTheme = function() {
    const now = Date.now();
    if (now - _lastThemeToggleTime < 300) {
        return; // Prevent duplicate rapid invocations from event bubbling or double clicks
    }
    _lastThemeToggleTime = now;

    const currentTheme = document.documentElement.getAttribute('data-theme') || window.getStoredTheme();
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    window.setStoredTheme(newTheme);
    window.applyTheme(newTheme);
};

function initThemeToggle() {
    // Initial sync
    const currentTheme = window.getStoredTheme();
    window.applyTheme(currentTheme);

    // Fallback click listener for any theme button without inline onclick
    document.addEventListener('click', (e) => {
        const btn = e.target.closest('.theme-toggle-btn, #themeToggleBtn, #themeToggleBtnDiagnose, #themeToggleBtnLogin, #themeToggleBtnRegister');
        if (btn && !btn.hasAttribute('onclick')) {
            e.preventDefault();
            window.toggleTheme();
        }
    });
}

// ── DOM Initialization ──────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
    // Initialize Theme Switcher
    initThemeToggle();

    // Password strength helper
    const pwd = document.querySelector('input[name="password"]');
    if (pwd) {
        pwd.addEventListener("input", () => {
            const msg = document.querySelector("#passwordHelp");
            if (!msg) return;

            const v = pwd.value;
            const strong =
                v.length >= 8 &&
                /[A-Z]/.test(v) &&
                /[a-z]/.test(v) &&
                /[0-9]/.test(v) &&
                /[!@#$%^&*(),.?":{}|<>_\-+=]/.test(v);

            msg.textContent = strong
                ? "ពាក្យសម្ងាត់រឹងមាំ ✅"
                : "ប្រើយ៉ាងហោចណាស់ ៨ តួអក្សរ រួមមានអក្សរធំ តូច លេខ និងសញ្ញាពិសេស";
            msg.className = strong ? "form-text text-success" : "form-text text-danger";
        });
    }
});
