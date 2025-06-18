async function proofreadText() {
    let inputText = document.getElementById("text-input").value;
    let outputArea = document.getElementById("output");

    let formData = new FormData();
    formData.append("text", inputText);
    

    let response = await fetch("/proofread_text", {
        method: "POST",
        body: formData
    });

    if (!response.ok) {
    outputArea.textContent = "Error: Failed to fetch response from server.";
    return;
    }

    let data = await response.json();
    outputArea.textContent = data.returned_text;
    
    
    if (data.error) {
        outputArea.textContent = data.error;
    } else {
        outputArea.textContent = data.returned_text;
    }
    outputArea.style.display = "block";     
}