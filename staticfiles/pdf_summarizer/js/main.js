document.getElementById('uploadForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const pdfFile = document.getElementById('pdfFile').files[0];
    if (!pdfFile) {
        alert('Please select a PDF file.');
        return;
    }

    const formData = new FormData();
    formData.append('file', pdfFile);

    const summaryOutput = document.getElementById('summary');
    summaryOutput.innerHTML = '';

    try {
        const response = await fetch('/pdf_summarizer/api/summarize/', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.statusText}`);
        }

        const result = await response.json();
        if (result.summary) {
            summaryOutput.innerHTML = `<h2>Summary</h2><p>${result.summary}</p>`;
            document.getElementById('qa-section').style.display = 'block'; // Show QA section
        } else {
            summaryOutput.textContent = 'No summary available.';
        }
    } catch (error) {
        console.error('Error:', error);
        summaryOutput.textContent = `An error occurred: ${error.message}`;
    }
});

// Handle Question Submission
document.getElementById('askQuestionBtn').addEventListener('click', async function () {
    const questionInput = document.getElementById('questionInput');
    const question = questionInput.value.trim();

    if (!question) {
        alert('Please enter a question.');
        return;
    }

    try {
        const response = await fetch('/pdf_summarizer/api/ask-question/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question }),
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.statusText}`);
        }

        const result = await response.json();
        const answersDiv = document.getElementById('answers');

        // Display question & answer dynamically
        const questionBlock = document.createElement('div');
        questionBlock.innerHTML = `<p><strong>Q:</strong> ${question}</p><p><strong>A:</strong> ${result.answer}</p><hr>`;
        answersDiv.appendChild(questionBlock);

        questionInput.value = ''; // Clear input field
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to get an answer. Try again.');
    }
});
