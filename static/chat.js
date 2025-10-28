const chatBox = document.getElementById('chatBox');
const chatForm = document.getElementById('chatForm');
const userInput = document.getElementById('userInput');
const speedRange = document.getElementById('speedRange');

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const text = userInput.value.trim();
    if(!text) return;

    addMessage(text, 'user');
    userInput.value = '';

    // Бот "набуває" з анімацією
    const botMsg = addMessage('', 'bot');
    const typingDots = createTyping();
    botMsg.appendChild(typingDots);

    // Швидкість набору
    const speed = parseInt(speedRange.value);

    // Імітація відповіді бота
    const botResponse = await fakeBotResponse(text);
    botMsg.removeChild(typingDots);
    await typeText(botMsg, botResponse, speed);

    chatBox.scrollTop = chatBox.scrollHeight;
});

function addMessage(text, cls) {
    const msg = document.createElement('div');
    msg.className = 'msg ' + cls;
    msg.textContent = text;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
    return msg;
}

function createTyping() {
    const typing = document.createElement('div');
    typing.className = 'msg typing';
    for(let i=0;i<3;i++){
        const span = document.createElement('span');
        typing.appendChild(span);
    }
    return typing;
}

function typeText(element, text, speed) {
    return new Promise(resolve => {
        let i = 0;
        const interval = setInterval(() => {
            element.textContent += text.charAt(i);
            i++;
            chatBox.scrollTop = chatBox.scrollHeight;
            if(i >= text.length) clearInterval(interval) || resolve();
        }, speed);
    });
}

function fakeBotResponse(input) {
    // Тут можна інтегрувати свій API
    return new Promise(resolve => {
        setTimeout(() => {
            resolve("Це відповідь бота на: " + input);
        }, 800);
    });
}

// Тема
function setTheme(theme) {
    if(theme === 'dark') {
        document.documentElement.style.setProperty('--bg-body', '#1c1c1c');
        document.documentElement.style.setProperty('--text-body', '#e6eef6');
        document.documentElement.style.setProperty('--bg-container', '#2b2b2b');
        document.documentElement.style.setProperty('--bg-user', '#3a3a3a');
        document.documentElement.style.setProperty('--bg-bot', '#444');
        document.documentElement.style.setProperty('--text-bot', '#e6eef6');
    } else if(theme === 'light') {
        document.documentElement.style.setProperty('--bg-body', '#f5f5f5');
        document.documentElement.style.setProperty('--text-body', '#222');
        document.documentElement.style.setProperty('--bg-container', '#fff');
        document.documentElement.style.setProperty('--bg-user', '#ddd');
        document.documentElement.style.setProperty('--bg-bot', '#eee');
        document.documentElement.style.setProperty('--text-bot', '#222');
    }
}
