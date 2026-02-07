/**
 * Smart Document Assistant - Modern Reactive Frontend
 * Features: Multi-language, Glassmorphism UI, Streaming responses, Accessibility
 */

/* ============================================
   TRANSLATIONS
   ============================================ */

const translations = {
    en: {
        appTitle: 'Smart Assistant',
        navChat: 'Chat',
        navDocuments: 'Documents',
        language: 'Language',
        chatWithDocs: 'Chat with Your Documents',
        headerSubtitle: 'Upload a PDF and ask questions',
        uploadPDF: 'Upload PDF Document',
        dragDrop: 'Drop PDF here or click to select',
        uploadHint: 'Maximum 50MB',
        uploadBtn: 'Upload PDF',
        uploadSuccess: 'PDF uploaded successfully!',
        uploadError: 'Failed to upload PDF. Please try again.',
        fileRequired: 'Please select a PDF file first.',
        sendBtn: 'Send',
        welcomeMsg: 'Welcome! Upload a PDF to get started.',
        noDocs: 'No documents yet',
        uploadFirst: 'Upload a PDF to get started',
        inputHint: 'Press Enter to send or use the send button',
        chatError: 'Failed to get response. Please try again.',
    },
    hi: {
        appTitle: 'स्मार्ट सहायक',
        navChat: 'चैट',
        navDocuments: 'दस्तावेज़',
        language: 'भाषा',
        chatWithDocs: 'अपने दस्तावेज़ के साथ चैट करें',
        headerSubtitle: 'एक PDF अपलोड करें और प्रश्न पूछें',
        uploadPDF: 'PDF दस्तावेज़ अपलोड करें',
        dragDrop: 'यहां PDF छोड़ें या चुनने के लिए क्लिक करें',
        uploadHint: 'अधिकतम 50MB',
        uploadBtn: 'PDF अपलोड करें',
        uploadSuccess: 'PDF सफलतापूर्वक अपलोड हो गया!',
        uploadError: 'PDF अपलोड करने में विफल। कृपया पुनः प्रयास करें।',
        fileRequired: 'पहले कोई PDF फ़ाइल चुनें।',
        sendBtn: 'भेजें',
        welcomeMsg: 'स्वागत है! शुरू करने के लिए एक PDF अपलोड करें।',
        noDocs: 'अभी कोई दस्तावेज़ नहीं',
        uploadFirst: 'शुरू करने के लिए एक PDF अपलोड करें',
        inputHint: 'भेजने के लिए Enter दबाएं या भेजें बटन का उपयोग करें',
        chatError: 'प्रतिक्रिया प्राप्त करने में विफल। कृपया पुनः प्रयास करें।',
    },
    mr: {
        appTitle: 'स्मार्ट सहायक',
        navChat: 'चॅट',
        navDocuments: 'दस्तऐवज',
        language: 'भाषा',
        chatWithDocs: 'तुमच्या दस्तऐवजाशी बातचीत करा',
        headerSubtitle: 'PDF अपलोड करा आणि प्रश्न विचारा',
        uploadPDF: 'PDF दस्तऐवज अपलोड करा',
        dragDrop: 'येथे PDF सोडा किंवा निवडण्यासाठी क्लिक करा',
        uploadHint: 'जास्तीत जास्त 50MB',
        uploadBtn: 'PDF अपलोड करा',
        uploadSuccess: 'PDF यशस्वीरित्या अपलोड झाली!',
        uploadError: 'PDF अपलोड करण्यात अयशस्वी. कृपया पुन्हा प्रयत्न करा.',
        fileRequired: 'प्रथम PDF फाइल निवडा.',
        sendBtn: 'पाठवा',
        welcomeMsg: 'स्वागतम! सुरू करण्यासाठी PDF अपलोड करा.',
        noDocs: 'अद्याप कोणतेही दस्तऐवज नाहीत',
        uploadFirst: 'सुरू करण्यासाठी PDF अपलोड करा',
        inputHint: 'पाठवण्यासाठी Enter दाबा किंवा पाठवा बटन वापरा',
        chatError: 'प्रतिसाद मिळविण्यात अयशस्वी. कृपया पुन्हा प्रयत्न करा.',
    }
};

/* ============================================
   REACTIVE STATE MANAGEMENT
   ============================================ */

class ReactiveStore {
    constructor(initialState = {}) {
        this.state = initialState;
        this.watchers = new Map();
        this.initializeReactivity();
    }

    initializeReactivity() {
        this.state = new Proxy(this.state, {
            set: (target, property, value) => {
                const oldValue = target[property];
                if (oldValue !== value) {
                    target[property] = value;
                    this.notifyWatchers(property, value, oldValue);
                }
                return true;
            }
        });
    }

    watch(path, callback) {
        if (!this.watchers.has(path)) {
            this.watchers.set(path, []);
        }
        this.watchers.get(path).push(callback);
        return () => {
            const callbacks = this.watchers.get(path);
            callbacks.splice(callbacks.indexOf(callback), 1);
        };
    }

    notifyWatchers(property, newValue, oldValue) {
        if (this.watchers.has(property)) {
            this.watchers.get(property).forEach(callback => {
                try {
                    callback(newValue, oldValue);
                } catch (error) {
                    console.error('Watcher error:', error);
                }
            });
        }
    }
}

const appState = new ReactiveStore({
    currentLanguage: localStorage.getItem('preferredLanguage') || 'en',
    isWaitingForResponse: false,
    isChatEnabled: false,
    uploadedFileName: null,
    currentSection: 'chat'
});

/* ============================================
   DOM ELEMENTS
   ============================================ */

const elements = {
    // Sidebar
    sidebar: document.querySelector('.sidebar'),
    navItems: document.querySelectorAll('.nav-item'),
    langSelect: document.getElementById('language-select'),
    
    // Header
    menuToggle: document.querySelector('.menu-toggle'),
    
    // Upload
    uploadArea: document.getElementById('upload-area'),
    fileInput: document.getElementById('file-input'),
    uploadBtn: document.getElementById('upload-btn'),
    fileName: document.getElementById('file-name'),
    uploadMessage: document.getElementById('upload-message'),
    uploadIndicator: document.getElementById('upload-indicator'),
    
    // Chat
    chatMessages: document.getElementById('chat-messages'),
    questionInput: document.getElementById('question-input'),
    sendBtn: document.getElementById('send-btn'),
    inputHint: document.getElementById('input-hint'),
    
    // Sections
    sections: document.querySelectorAll('.section'),
    
    // Toast
    toastContainer: document.getElementById('toast-container')
};

/* ============================================
   TRANSLATION & LANGUAGE
   ============================================ */

function t(key) {
    return translations[appState.state.currentLanguage]?.[key] || translations.en[key] || key;
}

function updateUILanguage() {
    document.querySelectorAll('[data-i18n]').forEach((el) => {
        const key = el.getAttribute('data-i18n');
        el.textContent = t(key);
    });

    elements.questionInput.placeholder = t('dragDrop');
    elements.inputHint.textContent = t('inputHint');
}

appState.watch('currentLanguage', (newLang, oldLang) => {
    if (newLang !== oldLang) {
        localStorage.setItem('preferredLanguage', newLang);
        updateUILanguage();
    }
});

/* ============================================
   UI UTILITIES
   ============================================ */

function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    toast.setAttribute('role', 'status');
    toast.setAttribute('aria-live', 'polite');
    
    elements.toastContainer.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideOutToast 0.3s ease-out forwards';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

function scrollChatToBottom() {
    requestAnimationFrame(() => {
        elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;
    });
}

function switchSection(sectionName) {
    // Update nav items
    elements.navItems.forEach(item => {
        item.classList.toggle('active', item.dataset.section === sectionName);
    });
    
    // Update sections
    elements.sections.forEach(section => {
        section.classList.toggle('active', section.id === `${sectionName}-section`);
    });
    
    appState.state.currentSection = sectionName;
}

/* ============================================
   MESSAGE HANDLING
   ============================================ */

function addMessage(text, sender = 'bot') {
    const messageGroup = document.createElement('div');
    messageGroup.className = `message-group ${sender}-message`;
    
    const avatar = document.createElement('div');
    avatar.className = `message-avatar ${sender}`;
    
    if (sender === 'bot') {
        avatar.innerHTML = `<svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm3.5-9c.83 0 1.5-.67 1.5-1.5S16.33 8 15.5 8 14 8.67 14 9.5s.67 1.5 1.5 1.5zm-7 0c.83 0 1.5-.67 1.5-1.5S9.33 8 8.5 8 7 8.67 7 9.5 7.67 11 8.5 11zm3.5 6.5c2.33 0 4.31-1.46 5.11-3.5H6.89c.8 2.04 2.78 3.5 5.11 3.5z"></path>
        </svg>`;
    } else {
        avatar.textContent = 'U';
    }
    
    const content = document.createElement('div');
    content.className = `message-content ${sender}`;
    
    const messageText = document.createElement('p');
    messageText.className = 'message-text';
    messageText.textContent = text;
    
    content.appendChild(messageText);
    messageGroup.appendChild(avatar);
    messageGroup.appendChild(content);
    
    elements.chatMessages.appendChild(messageGroup);
    scrollChatToBottom();
    
    return messageGroup;
}

function addTypingIndicator() {
    const messageGroup = document.createElement('div');
    messageGroup.className = 'message-group bot-message';
    messageGroup.id = 'typing-indicator';
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar bot';
    avatar.innerHTML = `<svg viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm3.5-9c.83 0 1.5-.67 1.5-1.5S16.33 8 15.5 8 14 8.67 14 9.5s.67 1.5 1.5 1.5zm-7 0c.83 0 1.5-.67 1.5-1.5S9.33 8 8.5 8 7 8.67 7 9.5 7.67 11 8.5 11zm3.5 6.5c2.33 0 4.31-1.46 5.11-3.5H6.89c.8 2.04 2.78 3.5 5.11 3.5z"></path>
    </svg>`;
    
    const content = document.createElement('div');
    content.className = 'message-content bot';
    const indicator = document.createElement('div');
    indicator.className = 'typing-indicator';
    
    for (let i = 0; i < 3; i++) {
        const dot = document.createElement('div');
        dot.className = 'typing-dot';
        indicator.appendChild(dot);
    }
    
    content.appendChild(indicator);
    messageGroup.appendChild(avatar);
    messageGroup.appendChild(content);
    
    elements.chatMessages.appendChild(messageGroup);
    scrollChatToBottom();
}

function removeTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) indicator.remove();
}

/* ============================================
   FILE UPLOAD HANDLER
   ============================================ */

function setupUploadHandlers() {
    // Click to upload
    elements.uploadArea.addEventListener('click', () => elements.fileInput.click());
    elements.uploadArea.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' || e.code === 'Space') elements.fileInput.click();
    });

    // Drag and drop
    elements.uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        elements.uploadArea.classList.add('dragover');
    });

    elements.uploadArea.addEventListener('dragleave', () => {
        elements.uploadArea.classList.remove('dragover');
    });

    elements.uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        elements.uploadArea.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length > 0) handleFileSelect(files[0]);
    });

    // File input change
    elements.fileInput.addEventListener('change', (e) => {
        if (e.target.files[0]) handleFileSelect(e.target.files[0]);
    });

    // Upload button
    elements.uploadBtn.addEventListener('click', handleUpload);
}

function handleFileSelect(file) {
    if (file.type !== 'application/pdf') {
        showToast('Please select a valid PDF file', 'error');
        return;
    }
    
    appState.state.uploadedFileName = file.name;
    elements.fileName.textContent = file.name;
    elements.uploadMessage.textContent = '';
    elements.uploadMessage.className = 'upload-message';
}

async function handleUpload() {
    if (!elements.fileInput.files[0]) {
        showToast(t('fileRequired'), 'error');
        return;
    }

    const file = elements.fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);

    elements.uploadBtn.disabled = true;
    elements.uploadBtn.setAttribute('aria-busy', 'true');
    elements.uploadIndicator.classList.add('active');

    try {
        const response = await fetch('http://localhost:8000/upload', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) throw new Error('Upload failed');

        showToast(t('uploadSuccess'), 'success');
        
        // Reset upload form
        elements.fileInput.value = '';
        elements.fileName.textContent = '';
        
        // Enable chat
        appState.state.isChatEnabled = true;
        elements.questionInput.disabled = false;
        
        // Clear old messages and show welcome
        elements.chatMessages.innerHTML = '';
        addMessage(t('welcomeMsg'), 'bot');
        
        elements.uploadBtn.disabled = false;
        elements.uploadBtn.setAttribute('aria-busy', 'false');
    } catch (error) {
        console.error('Upload error:', error);
        showToast(t('uploadError'), 'error');
        elements.uploadBtn.disabled = false;
        elements.uploadBtn.setAttribute('aria-busy', 'false');
    } finally {
        elements.uploadIndicator.classList.remove('active');
    }
}

/* ============================================
   CHAT HANDLER
   ============================================ */

function setupChatHandlers() {
    elements.questionInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !appState.state.isWaitingForResponse && appState.state.isChatEnabled) {
            handleSendMessage();
        }
    });

    elements.sendBtn.addEventListener('click', handleSendMessage);
}

async function handleSendMessage() {
    const question = elements.questionInput.value.trim();

    if (!question || appState.state.isWaitingForResponse || !appState.state.isChatEnabled) {
        return;
    }

    appState.state.isWaitingForResponse = true;
    elements.sendBtn.disabled = true;
    elements.questionInput.disabled = true;

    addMessage(question, 'user');
    addTypingIndicator();
    elements.questionInput.value = '';

    try {
        const response = await fetch('http://localhost:8000/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                question: question,
                lang: appState.state.currentLanguage,
            }),
        });

        removeTypingIndicator();

        if (!response.ok) throw new Error('Request failed');

        const contentType = response.headers.get('content-type');

        if (contentType && contentType.includes('text/event-stream')) {
            await handleStreamingResponse(response);
        } else {
            const data = await response.json();
            const botResponse = data.answer || data.response || 'No response received';
            addMessage(botResponse, 'bot');
        }
    } catch (error) {
        console.error('Chat error:', error);
        removeTypingIndicator();
        showToast(t('chatError'), 'error');
        addMessage(t('chatError'), 'bot');
    } finally {
        appState.state.isWaitingForResponse = false;
        elements.sendBtn.disabled = false;
        elements.questionInput.disabled = false;
        elements.questionInput.focus();
    }
}

async function handleStreamingResponse(response) {
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let messageEl = null;
    let fullResponse = '';

    try {
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value, { stream: true });
            const lines = chunk.split('\n');

            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    try {
                        const jsonData = JSON.parse(line.slice(6));
                        if (jsonData.text) {
                            fullResponse += jsonData.text;

                            if (!messageEl) {
                                messageEl = addMessage(fullResponse, 'bot');
                            } else {
                                const textEl = messageEl.querySelector('.message-text');
                                textEl.textContent = fullResponse;
                                scrollChatToBottom();
                            }
                        }
                    } catch (e) {
                        // Skip parse errors
                    }
                }
            }
        }

        if (!messageEl && fullResponse) {
            addMessage(fullResponse, 'bot');
        }
    } catch (error) {
        console.error('Streaming error:', error);
        removeTypingIndicator();
        addMessage(t('chatError'), 'bot');
    }
}

/* ============================================
   SIDEBAR NAVIGATION
   ============================================ */

function setupSidebarNavigation() {
    elements.navItems.forEach(item => {
        item.addEventListener('click', () => {
            const section = item.dataset.section;
            switchSection(section);
        });
    });

    // Mobile menu toggle
    elements.menuToggle.addEventListener('click', () => {
        elements.sidebar.classList.toggle('open');
    });

    // Close sidebar on section select (mobile)
    elements.navItems.forEach(item => {
        item.addEventListener('click', () => {
            if (window.innerWidth <= 768) {
                elements.sidebar.classList.remove('open');
            }
        });
    });
}

/* ============================================
   REACTIVE WATCHERS
   ============================================ */

appState.watch('isWaitingForResponse', (isWaiting) => {
    elements.sendBtn.disabled = isWaiting || !appState.state.isChatEnabled;
    elements.questionInput.disabled = !appState.state.isChatEnabled || isWaiting;
});

appState.watch('isChatEnabled', (isEnabled) => {
    elements.questionInput.disabled = !isEnabled;
    elements.sendBtn.disabled = !isEnabled || appState.state.isWaitingForResponse;
});

/* ============================================
   INITIALIZATION
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {
    updateUILanguage();
    
    // Set language selector
    elements.langSelect.value = appState.state.currentLanguage;
    elements.langSelect.addEventListener('change', (e) => {
        appState.state.currentLanguage = e.target.value;
    });

    setupUploadHandlers();
    setupChatHandlers();
    setupSidebarNavigation();

    // Show initial welcome message
    addMessage(t('welcomeMsg'), 'bot');
});

/* ============================================
   ACCESSIBILITY & ERROR HANDLING
   ============================================ */

window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
});

window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
});
