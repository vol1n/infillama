async function generateExamples() {
    const instructions = document.getElementById('instructionsInput').value;
    try {
        const response = await fetch(`http://your-backend-api/generate-examples?instructions=${encodeURIComponent(instructions)}`);
        const examples = await response.json();
        displayExamples(examples);
    } catch (error) {
        console.error("Failed to generate examples:", error);
    }
}

function displayExamples(examples) {
    const container = document.getElementById('examplesContainer');
    container.innerHTML = ''; // Clear previous examples
    examples.forEach((example, index) => {
        let div = document.createElement('div');
        div.className = 'example';
        div.textContent = example.text; // Assuming each example has a 'text' property
        div.onclick = function() { selectExample(example, index); };
        container.appendChild(div);
    });
}

async function selectExample(example, index) {
    // Optionally highlight the selected example or disable other examples
    console.log(`Example ${index + 1} selected:`, example);
    // You could also update the UI to reflect the selection
}

async function submitSelection() {
    const selectedExampleText = document.querySelector('.example.selected').textContent; // Ensure you have a way to identify the selected example
    try {
        const response = await fetch('http://your-backend-api/submit-selection', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ selectedExample: selectedExampleText })
        });
        const result = await response.json();
        console.log("Submission result:", result);
    } catch (error) {
        console.error("Failed to submit selection:", error);
    }
}

async function submitFeedback() {
    const feedback = document.getElementById('feedbackInput').value;
    try {
        const response = await fetch('http://your-backend-api/submit-feedback', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ feedback: feedback })
        });
        const result = await response.json();
        console.log("Feedback result:", result);
    } catch (error) {
        console.error("Failed to submit feedback:", error);
    }
}
