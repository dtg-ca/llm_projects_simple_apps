async function generateCode() {
    let inputText = document.getElementById("code-input").value;
    let mode = document.getElementById("mode").value;
    let outputArea = document.getElementById("output");

    let formData = new FormData();
    formData.append("prompt", inputText);
    formData.append("mode", mode);

    let response = await fetch("/generate_code", {
        method: "POST",
        body: formData
    });

    if (!response.ok) {
    outputArea.textContent = "Error: Failed to fetch response from server.";
    return;
    }

    let data = await response.json();
    outputArea.textContent = data.generated_code;
    
    
    if (data.error) {
        outputArea.textContent = data.error;
    } else {
        outputArea.textContent = data.generated_code;
    }
    outputArea.style.display = "block";     
}     