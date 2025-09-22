// POS XYZ System - Authentication Module

// Current user data
let currentUser = null;

// Check if user is logged in
function isLoggedIn() {
    return localStorage.getItem('access_token') !== null;
}

// Get current user info from token
function getCurrentUser() {
    const token = localStorage.getItem('access_token');
    if (!token) return null;

    try {
        // Decode JWT token (basic decode, not verification)
        const payload = JSON.parse(atob(token.split('.')[1]));
        return {
            id: payload.sub,
            email: payload.email,
            exp: payload.exp
        };
    } catch (error) {
        console.error('Error decoding token:', error);
        return null;
    }
}

// Check if token is expired
function isTokenExpired() {
    const user = getCurrentUser();
    if (!user) return true;

    const now = Math.floor(Date.now() / 1000);
    return user.exp < now;
}

// Redirect to login if not authenticated
function requireAuth() {
    if (!isLoggedIn() || isTokenExpired()) {
        window.location.href = '/login';
        return false;
    }
    return true;
}

// Redirect to dashboard if already authenticated
function redirectIfAuthenticated() {
    if (isLoggedIn() && !isTokenExpired()) {
        window.location.href = '/';
        return true;
    }
    return false;
}

// Handle login form
async function handleLogin(event) {
    event.preventDefault();
    
    const form = event.target;
    const email = form.email.value.trim();
    const password = form.password.value;
    const submitBtn = form.querySelector('button[type="submit"]');
    
    // Validation
    if (!email || !password) {
        showAlert('Por favor completa todos los campos', 'warning');
        return;
    }
    
    // Show loading
    showLoading(submitBtn);
    
    try {
        await api.login(email, password);
        showAlert('¡Inicio de sesión exitoso!', 'success');
        
        // Small delay to show success message
        setTimeout(() => {
            window.location.href = '/';
        }, 1000);
        
    } catch (error) {
        console.error('Login error:', error);
        showAlert(error.message || 'Error al iniciar sesión', 'danger');
    } finally {
        hideLoading(submitBtn, 'Iniciar Sesión');
    }
}

// Handle logout
function handleLogout() {
    if (confirm('¿Estás seguro de que deseas cerrar sesión?')) {
        api.logout();
    }
}

// Initialize auth on page load
document.addEventListener('DOMContentLoaded', () => {
    // Get current user info
    currentUser = getCurrentUser();
    
    // Set up auth-dependent UI
    const currentPath = window.location.pathname;
    
    // Login page - redirect if already authenticated
    if (currentPath === '/login') {
        redirectIfAuthenticated();
        
        // Set up login form
        const loginForm = document.getElementById('loginForm');
        if (loginForm) {
            loginForm.addEventListener('submit', handleLogin);
        }
        return;
    }
    
    // Other pages - require authentication
    if (currentPath !== '/login' && !requireAuth()) {
        return;
    }
    
    // Set up logout buttons
    const logoutBtns = document.querySelectorAll('.logout-btn');
    logoutBtns.forEach(btn => {
        btn.addEventListener('click', handleLogout);
    });
    
    // Update user info in UI
    updateUserInfo();
});

// Update user info in the UI
function updateUserInfo() {
    if (!currentUser) return;
    
    const userEmailElements = document.querySelectorAll('.user-email');
    const userIdElements = document.querySelectorAll('.user-id');
    
    userEmailElements.forEach(el => {
        el.textContent = currentUser.email;
    });
    
    userIdElements.forEach(el => {
        el.textContent = currentUser.id;
    });
}
