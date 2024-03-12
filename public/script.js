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
        div.textContent = example; // Adjust based on your example structure
        div.onclick = function() { selectExample(div, index); };
        container.appendChild(div);
    });
}

function selectExample(div, index) {
    // Optional: Highlight the selected example
    document.querySelectorAll('.example').forEach(el => el.classList.remove('selected'));
    div.classList.add('selected');
    console.log(`Example ${index} selected.`);
}

async function submitSelection() {
    const selectedExampleText = document.querySelector('.example.selected').textContent;
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
