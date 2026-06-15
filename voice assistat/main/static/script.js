const speakBtn = document.getElementById('speakBtn');
const messages = document.getElementById('messages');

function addMessage(text, sender) {
  const p = document.createElement('p');
  p.textContent = text;
  p.className = sender;
  messages.appendChild(p);
  messages.scrollTop = messages.scrollHeight;
}

// Use Web Speech API for voice input
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = 'en-US';

speakBtn.addEventListener('click', () => {
  recognition.start();
  addMessage("Listening...", "assistant");
});

recognition.onresult = async (event) => {
  const transcript = event.results[0][0].transcript;
  addMessage(transcript, 'user');

  // Send to Flask backend
  try {
    const response = await fetch('http://127.0.0.1:5000/speak', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ command: transcript })
    });
    const result = await response.json();
    addMessage(result.message, 'assistant');

  } catch (err) {
    addMessage("Error connecting to backend.", 'assistant');
  }
};
