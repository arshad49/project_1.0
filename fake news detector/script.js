const analyzeBtn = document.getElementById('analyzeBtn');
const newsInput = document.getElementById('newsInput');
const resultDiv = document.getElementById('result');

analyzeBtn.addEventListener('click', async () => {
  const text = newsInput.value.trim();
  if (!text) return alert("Please enter some text.");

  resultDiv.textContent = "Analyzing... 🔍";

  try {
    const response = await fetch('/analyze', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ text })


});

    const data = await response.json();
    resultDiv.textContent = data.result;

  } catch (err) {
    resultDiv.textContent = "Error connecting to server.";
    console.error(err);
  }
});
