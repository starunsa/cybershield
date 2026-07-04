/* Dashboard Handler */

const API_BASE_URL = '/api';
let currentChatSessionId = null;
let chatInitialized = false;

document.addEventListener('DOMContentLoaded', () => {
    // Check authentication
    checkAuth();

    // Setup event listeners
    setupNavigation();
    setupTabNavigation();
    setupAnalysisTabs();
    setupSidebar();
    setupFloatingChat();

    // Load user data
    loadUserData();

    // Load chat history
    loadChatSessions();

    // Initialize chat
    initializeChat();
});

function checkAuth() {
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = '/';
        return;
    }
}

function handleAuthFailure(response) {
    if (response.status === 401 || response.status === 422) {
        logout();
        return true;
    }
    return false;
}

function setupNavigation() {
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            logout(e);
        });
    }
}

function setupTabNavigation() {
    const navLinks = document.querySelectorAll('.nav-link[data-tab]');
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const tab = e.currentTarget.dataset.tab;
            if (tab === 'chat') {
                openChatWidget(true);
                return;
            }
            switchTab(tab);
        });
    });
}

function setupFloatingChat() {
    const launcher = document.getElementById('chatLauncher');
    const closeBtn = document.getElementById('chatCloseBtn');
    const welcome = document.getElementById('chatWelcome');

    if (launcher) {
        launcher.addEventListener('click', () => openChatWidget(true));
    }

    if (closeBtn) {
        closeBtn.addEventListener('click', endChatSession);
    }

    setTimeout(() => {
        if (welcome) {
            welcome.classList.add('show');
        }
    }, 900);

    setTimeout(() => {
        if (welcome) {
            welcome.classList.remove('show');
        }
    }, 6500);
}

function openChatWidget(focusInput = false) {
    const panel = document.getElementById('chatPanel');
    const launcher = document.getElementById('chatLauncher');
    const welcome = document.getElementById('chatWelcome');

    if (panel) {
        panel.classList.add('open');
    }
    if (launcher) {
        launcher.classList.add('active');
    }
    if (welcome) {
        welcome.classList.remove('show');
    }
    if (focusInput) {
        setTimeout(() => {
            const input = document.getElementById('chatInput');
            if (input) input.focus();
        }, 180);
    }
}

function closeChatWidget() {
    const panel = document.getElementById('chatPanel');
    const launcher = document.getElementById('chatLauncher');

    if (panel) {
        panel.classList.remove('open');
    }
    if (launcher) {
        launcher.classList.remove('active');
    }
}

async function endChatSession() {
    const sessionId = currentChatSessionId;
    closeChatWidget();
    currentChatSessionId = null;
    chatInitialized = false;

    const messagesContainer = document.getElementById('chatMessages');
    if (messagesContainer) {
        messagesContainer.innerHTML = '';
    }

    if (!sessionId) {
        loadChatSessions();
        return;
    }

    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`${API_BASE_URL}/chat/session/${sessionId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (handleAuthFailure(response)) return;
        loadChatSessions();
    } catch (error) {
        console.error('Error ending chat session:', error);
    }
}

function setupAnalysisTabs() {
    const analysisTabs = document.querySelectorAll('.analysis-tab-btn');
    analysisTabs.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const analysis = e.currentTarget.dataset.analysis;

            // Update active button
            analysisTabs.forEach(b => b.classList.remove('active'));
            e.currentTarget.classList.add('active');

            // Update active content
            document.querySelectorAll('.analysis-content').forEach(content => {
                content.classList.remove('active');
                content.style.display = 'none';
            });
            const activeContent = document.getElementById(`${analysis}-analysis`);
            if (activeContent) {
                activeContent.classList.add('active');
                activeContent.style.display = 'block';
            }
        });
    });

    // Set first tab as active
    if (analysisTabs.length > 0) {
        activateAnalysisTab(analysisTabs[0].dataset.analysis);
    }
}

function setupSidebar() {
    const sidebarLinks = document.querySelectorAll('.sidebar-link[data-action]');
    sidebarLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const action = e.currentTarget.dataset.action;
            handleSidebarAction(action);
        });
    });
}

function handleSidebarAction(action) {
    switch (action) {
        case 'new-chat':
            openChatWidget(true);
            currentChatSessionId = null;
            document.getElementById('chatMessages').innerHTML = '';
            chatInitialized = false;
            initializeChat();
            break;
        case 'chat-history':
            openChatWidget(true);
            loadChatSessions();
            break;
        case 'api-scan':
            switchTab('security');
            activateAnalysisTab('api');
            break;
        case 'image-scan':
            switchTab('security');
            activateAnalysisTab('image');
            break;
        case 'website-scan':
            switchTab('security');
            activateAnalysisTab('website');
            break;
    }
}

function activateAnalysisTab(tab) {
    const btn = document.querySelector(`.analysis-tab-btn[data-analysis="${tab}"]`);
    if (btn) {
        btn.click();
    }
}

function switchTab(tabName) {
    // Update nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    const activeLink = document.querySelector(`.nav-link[data-tab="${tabName}"]`);
    if (activeLink) {
        activeLink.classList.add('active');
    }

    // Update content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.style.display = 'none';
    });
    const activeTab = document.getElementById(tabName);
    if (activeTab) {
        activeTab.style.display = 'block';
    }
}

async function loadUserData() {
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`${API_BASE_URL}/user/profile`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (handleAuthFailure(response)) return;

        if (response.ok) {
            const data = await response.json();
            const user = data.user;

            document.getElementById('userDisplayName').textContent = user.full_name || user.username;
            document.getElementById('userEmail').textContent = user.email;
            document.getElementById('profileUsername').value = user.username;
            document.getElementById('profileFullName').value = user.full_name || user.username;
            document.getElementById('profileEmail').value = user.email;
            document.getElementById('chatUsername').textContent = user.username;
        }
    } catch (error) {
        console.error('Error loading user data:', error);
    }
}

async function loadChatSessions() {
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`${API_BASE_URL}/chat/sessions`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (handleAuthFailure(response)) return;

        if (response.ok) {
            const data = await response.json();
            const sessionsList = document.getElementById('recentChats');
            sessionsList.innerHTML = '';

            if (data.sessions.length === 0) {
                sessionsList.innerHTML = '<p style="color: var(--gray); font-size: 12px;">No chats yet</p>';
                return;
            }

            data.sessions.slice(0, 5).forEach(session => {
                const item = document.createElement('a');
                item.href = '#';
                item.className = 'recent-item';
                item.textContent = session.title || `Chat ${session.id}`;
                item.addEventListener('click', (e) => {
                    e.preventDefault();
                    openChatWidget(true);
                    loadChatHistory(session.id);
                });
                sessionsList.appendChild(item);
            });
        }
    } catch (error) {
        console.error('Error loading chat sessions:', error);
    }
}

async function loadChatHistory(sessionId) {
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`${API_BASE_URL}/chat/history/${sessionId}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (handleAuthFailure(response)) return;

        if (response.ok) {
            const data = await response.json();
            currentChatSessionId = sessionId;

            const messagesContainer = document.getElementById('chatMessages');
            messagesContainer.innerHTML = '';

            data.messages.forEach(msg => {
                displayMessage(msg.sender, msg.content);
            });

            // Scroll to bottom
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
    } catch (error) {
        console.error('Error loading chat history:', error);
    }
}

async function initializeChat() {
    if (chatInitialized) return;

    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`${API_BASE_URL}/chat/greeting`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (handleAuthFailure(response)) return;

        if (response.ok) {
            const data = await response.json();
            displayMessage('bot', data.greeting, data.bot_name);
            chatInitialized = true;
        }
    } catch (error) {
        console.error('Error initializing chat:', error);
    }
}

async function sendChatMessage(e) {
    e.preventDefault();

    const input = document.getElementById('chatInput');
    const message = input.value.trim();

    if (!message) return;

    // Display user message
    displayMessage('user', message);
    input.value = '';

    showLoading();

    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`${API_BASE_URL}/chat/send`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                session_id: currentChatSessionId
            })
        });

        if (handleAuthFailure(response)) return;

        if (response.ok) {
            const data = await response.json();
            currentChatSessionId = data.session_id;

            // Display bot response
            displayMessage('bot', data.bot_response, data.bot_name);

            // Reload chat sessions
            loadChatSessions();
        } else {
            const error = await response.json();
            displayMessage('bot', 'Error: ' + (error.error || error.msg || 'Failed to process message'));
        }
    } catch (error) {
        console.error('Error sending message:', error);
        displayMessage('bot', 'Error: ' + error.message);
    } finally {
        hideLoading();
    }
}

function displayMessage(sender, content, botName = 'CyberGuard') {
    const messagesContainer = document.getElementById('chatMessages');
    const messageItem = document.createElement('div');
    messageItem.className = `message-item ${sender}`;

    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    bubble.textContent = content;

    messageItem.appendChild(bubble);

    const time = document.createElement('div');
    time.className = 'message-time';
    time.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    messageItem.appendChild(time);

    messagesContainer.appendChild(messageItem);

    // Scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

async function analyzeAPI(e) {
    e.preventDefault();

    const url = document.getElementById('apiUrl').value;
    const method = document.getElementById('apiMethod').value;

    showLoading();

    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`${API_BASE_URL}/security/analyze-api`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url, method })
        });

        if (handleAuthFailure(response)) return;

        if (response.ok) {
            const data = await response.json();
            displayResults('apiResults', data.report);
        } else {
            const error = await response.json();
            showError('apiResults', error.error || error.msg || 'Failed to analyze API');
        }
    } catch (error) {
        console.error('Error analyzing API:', error);
        showError('apiResults', error.message);
    } finally {
        hideLoading();
    }
}

async function scanImage(e) {
    e.preventDefault();

    const image = document.getElementById('imageName').value;

    showLoading();

    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`${API_BASE_URL}/security/scan-image`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ image })
        });

        if (handleAuthFailure(response)) return;

        if (response.ok) {
            const data = await response.json();
            displayResults('imageResults', data.report);
        } else {
            const error = await response.json();
            showError('imageResults', error.error || error.msg || 'Failed to scan image');
        }
    } catch (error) {
        console.error('Error scanning image:', error);
        showError('imageResults', error.message);
    } finally {
        hideLoading();
    }
}

async function scanWebsite(e) {
    e.preventDefault();

    const url = document.getElementById('websiteUrl').value;

    showLoading();

    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`${API_BASE_URL}/security/scan-website`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url })
        });

        if (handleAuthFailure(response)) return;

        if (response.ok) {
            const data = await response.json();
            displayResults('websiteResults', data.report);
        } else {
            const error = await response.json();
            showError('websiteResults', error.error || error.msg || 'Failed to scan website');
        }
    } catch (error) {
        console.error('Error scanning website:', error);
        showError('websiteResults', error.message);
    } finally {
        hideLoading();
    }
}

async function generateReport(e) {
    e.preventDefault();

    const apis = document.getElementById('reportApis').value.split(',').filter(a => a.trim());
    const images = document.getElementById('reportImages').value.split(',').filter(i => i.trim());
    const websites = document.getElementById('reportWebsites').value.split(',').filter(w => w.trim());

    if (apis.length === 0 && images.length === 0 && websites.length === 0) {
        showError('reportResults', 'Please enter at least one API URL, image name, or website URL');
        return;
    }

    showLoading();

    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`${API_BASE_URL}/security/report`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ api_urls: apis, images: images, websites: websites })
        });

        if (handleAuthFailure(response)) return;

        if (response.ok) {
            const data = await response.json();
            displayResults('reportResults', data.report);
        } else {
            const error = await response.json();
            showError('reportResults', error.error || error.msg || 'Failed to generate report');
        }
    } catch (error) {
        console.error('Error generating report:', error);
        showError('reportResults', error.message);
    } finally {
        hideLoading();
    }
}

async function updateProfile(e) {
    e.preventDefault();

    const fullName = document.getElementById('profileFullName').value;
    const email = document.getElementById('profileEmail').value;

    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`${API_BASE_URL}/user/profile`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ full_name: fullName, email })
        });

        if (handleAuthFailure(response)) return;

        if (response.ok) {
            showToast('Profile updated successfully', 'success');
            loadUserData();
        } else {
            const error = await response.json();
            showToast(error.error || error.msg || 'Failed to update profile', 'error');
        }
    } catch (error) {
        console.error('Error updating profile:', error);
        showToast(error.message, 'error');
    }
}

async function changePassword(e) {
    e.preventDefault();

    const oldPassword = document.getElementById('currentPassword').value;
    const newPassword = document.getElementById('newPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    if (newPassword !== confirmPassword) {
        showToast('Passwords do not match', 'error');
        return;
    }

    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`${API_BASE_URL}/user/change-password`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ old_password: oldPassword, new_password: newPassword })
        });

        if (handleAuthFailure(response)) return;

        if (response.ok) {
            showToast('Password changed successfully', 'success');
            document.getElementById('passwordForm').reset();
        } else {
            const error = await response.json();
            showToast(error.error || error.msg || 'Failed to change password', 'error');
        }
    } catch (error) {
        console.error('Error changing password:', error);
        showToast(error.message, 'error');
    }
}

function displayResults(containerId, data) {
    const container = document.getElementById(containerId);
    container.classList.add('show');
    container.innerHTML = '';

    const resultItem = document.createElement('div');
    resultItem.className = 'result-item';

    const pre = document.createElement('pre');
    pre.style.margin = '0';
    pre.style.whiteSpace = 'pre-wrap';
    pre.style.wordWrap = 'break-word';
    pre.textContent = JSON.stringify(data, null, 2);

    resultItem.appendChild(pre);
    container.appendChild(resultItem);
}

function showError(containerId, message) {
    const container = document.getElementById(containerId);
    container.classList.add('show');
    container.innerHTML = '';

    const resultItem = document.createElement('div');
    resultItem.className = 'result-item error';
    resultItem.innerHTML = `<strong>Error:</strong> ${message}`;

    container.appendChild(resultItem);
}

function showLoading() {
    document.getElementById('loadingSpinner').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loadingSpinner').style.display = 'none';
}

function showToast(message, type) {
    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `<i class="fas fa-check-circle"></i> ${message}`;

    container.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 3000);
}

function logout(e) {
    if (e) {
        e.preventDefault();
    }
    currentChatSessionId = null;
    chatInitialized = false;
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    sessionStorage.clear();
    window.location.replace('/?logout=1');
}
