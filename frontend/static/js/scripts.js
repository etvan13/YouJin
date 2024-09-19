function sendMessage() {
    const chatbox = document.getElementById('chatbox');
    const inputbox = document.getElementById('inputbox');
    const message = inputbox.value.trim();

    if (message === '') return;

    //append user messages to chat area
    const userMessageDiv = document.createElement('div');
    userMessageDiv.classList.add('message', 'user-message');
    userMessageDiv.textContent = message;
    chatbox.appendChild(userMessageDiv);

    //clear input box
    inputbox.value = '';

    //temporary response placeholder
    const chatBotResponse = "Howdy! Thanks for your message!";
    const botMessageDiv = document.createElement('div');
    botMessageDiv.classList.add('message', 'bot-message');
    botMessageDiv.textContent = chatBotResponse;
    chatbox.appendChild(botMessageDiv);

    //scroll to the bottom of the chat area to see new messages
    chatbox.scrollTop = chatbox.scrollHeight;

}


document.getElementById('inputbox').addEventListener('keypress', function(event) {
    //check if enter is pressed
    if (event.key === "Enter") {
        event.preventDefault(); //prevent default action (new line or form submission)
        sendMessage();
    }
});

function toggleTheme() {
    const checkbox = document.getElementById('theme-checkbox');
    document.body.classList.toggle('light-theme');
    
    //save theme preference
    if (checkbox.checked) {
        localStorage.setItem('theme', 'light');
    } else {
        localStorage.setItem('theme', 'dark');
    }
}

window.onload = function() {
    const checkbox = document.getElementById('theme-checkbox');
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {
        document.body.classList.add('light-theme');
        checkbox.checked = true;
    }
}

document.getElementById('theme-checkbox').addEventListener('change', toggleTheme);