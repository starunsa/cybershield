/* Authentication Handler */

document.addEventListener('DOMContentLoaded', () => {
    if (new URLSearchParams(window.location.search).has('logout')) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
        sessionStorage.clear();
        window.history.replaceState({}, document.title, '/');
    }

    setupEventListeners();
});

function setupEventListeners() {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const toggleRegisterBtn = document.getElementById('toggleRegister');
    const toggleLoginBtn = document.getElementById('toggleLogin');

    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }

    if (toggleRegisterBtn) {
        toggleRegisterBtn.addEventListener('click', (e) => {
            e.preventDefault();
            toggleForms('register');
        });
    }

    if (toggleLoginBtn) {
        toggleLoginBtn.addEventListener('click', (e) => {
            e.preventDefault();
            toggleForms('login');
        });
    }
}

function toggleForms(form) {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const messageArea = document.getElementById('messageArea');

    messageArea.innerHTML = '';

    if (form === 'register') {
        loginForm.style.display = 'none';
        registerForm.style.display = 'block';
    } else {
        loginForm.style.display = 'block';
        registerForm.style.display = 'none';
    }
}

async function handleLogin(e) {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const messageArea = document.getElementById('messageArea');

    try {
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (response.ok) {
            // Store token
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('user', JSON.stringify(data.user));

            // Show success message
            showMessage('Login successful! Redirecting...', 'success', messageArea);

            // Redirect to dashboard
            setTimeout(() => {
                window.location.href = '/dashboard';
            }, 1000);
        } else {
            showMessage(data.error || 'Login failed', 'error', messageArea);
        }
    } catch (error) {
        showMessage('An error occurred: ' + error.message, 'error', messageArea);
    }
}

async function handleRegister(e) {
    e.preventDefault();

    const username = document.getElementById('reg-username').value;
    const email = document.getElementById('reg-email').value;
    const fullName = document.getElementById('reg-fullname').value;
    const password = document.getElementById('reg-password').value;
    const messageArea = document.getElementById('messageArea');

    try {
        const response = await fetch('/api/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, email, full_name: fullName, password })
        });

        const data = await response.json();

        if (response.ok) {
            showMessage('Registration successful! Please login.', 'success', messageArea);

            // Clear form
            document.getElementById('registerForm').reset();

            // Switch back to login
            setTimeout(() => {
                toggleForms('login');
            }, 1500);
        } else {
            showMessage(data.error || 'Registration failed', 'error', messageArea);
        }
    } catch (error) {
        showMessage('An error occurred: ' + error.message, 'error', messageArea);
    }
}

function showMessage(message, type, container) {
    const messageEl = document.createElement('div');
    messageEl.className = `message ${type}`;
    messageEl.textContent = message;
    container.innerHTML = '';
    container.appendChild(messageEl);
}

// Check if already logged in
window.addEventListener('load', () => {
    const token = localStorage.getItem('access_token');
    if (token && window.location.pathname === '/') {
        window.location.href = '/dashboard';
    }
});
