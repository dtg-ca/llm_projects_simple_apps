async function SummarizeText() {
    let inputField = document.getElementById("text-input").value;
    let summaryDiv = document.getElementById("summary-output");
    summaryDiv.innerHTML = "Generating summary...";

    let formData = new FormData();
    formData.append("text", inputField);

    let response = await fetch("/summarize", {
        method: "POST",
        body: formData,
    });

    if (!response.ok) {
        summaryDiv.innerHTML = "<p><style='color :red;' Error: Failed to fetch response.</p>";
        return;
    }

    let data = await response.json();
    summaryDiv.innerHTML = "<p>${data.summary}</p>";
    if (data.error) {
        summaryDiv.innerHTML += `<p style='color: red;'>Error: ${data.error}</p>`;
    } else {
        summaryDiv.innerHTML = `<p>${data.summary}</p>`;
    }
    summaryDiv.style.display = "block";     
}
    