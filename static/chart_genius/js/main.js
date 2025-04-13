// Wait for DOM to be fully loaded
document.addEventListener("DOMContentLoaded", function () {
    // Upload Form Submission
    document.getElementById("upload-form").addEventListener("submit", function (event) {
        event.preventDefault();
        let formData = new FormData(this);
        let uploadUrl = this.dataset.url; // Get correct upload URL

        let uploadStatus = document.getElementById("upload-status");
        uploadStatus.innerHTML = "Uploading... ⏳"; // Show loading state

        fetch(uploadUrl, {
            method: "POST",
            body: formData,
            headers: { "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value }
        })
        .then(response => response.json())
        .then(data => {
            if (data.dataset_id) {
                localStorage.setItem("dataset_id", data.dataset_id); // Store dataset ID
                uploadStatus.innerHTML = `<strong>✅ File Uploaded:</strong> ${data.filename}`;
            } else {
                uploadStatus.innerHTML = `<span style="color:red;">❌ Upload Failed! Please try again.</span>`;
            }
        })
        .catch(error => {
            console.error("Upload Error:", error);
            uploadStatus.innerHTML = `<span style="color:red;">❌ Error Uploading File!</span>`;
        });
    });

    // Question Form Submission
    document.getElementById("question-form").addEventListener("submit", function (event) {
        event.preventDefault();
        let question = document.getElementById("question-input").value.trim();
        let dataset_id = localStorage.getItem("dataset_id");

        let responseContainer = document.getElementById("response-container");
        responseContainer.innerHTML = "<p>Processing... ⏳</p>"; // Show loading state

        if (!dataset_id) {
            alert("Please upload a dataset first!");
            responseContainer.innerHTML = "<p style='color:red;'>❌ No dataset uploaded!</p>";
            return;
        }

        if (question === "") {
            alert("Please enter a question!");
            responseContainer.innerHTML = "<p style='color:red;'>❌ Question cannot be empty!</p>";
            return;
        }

        let analyzeUrl = `/chart_genius/analyze/${dataset_id}/`;

        fetch(analyzeUrl, {
            method: "POST",
            body: JSON.stringify({ question: question }),
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
            }
        })
        .then(response => response.json())
        .then(data => {
            responseContainer.innerHTML = ""; // Clear previous results

            if (data.text) {
                responseContainer.innerHTML += `<h3>📊 Answer:</h3><p>${data.text}</p>`;
            } else {
                responseContainer.innerHTML += `<p style="color:red;">❌ No answer generated!</p>`;
            }
        })
        .catch(error => {
            console.error("Analysis Error:", error);
            responseContainer.innerHTML = `<span style="color:red;">❌ Error Analyzing Data! Please try again.</span>`;
        });
    });
});
