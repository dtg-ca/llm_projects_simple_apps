async function generateContent() {
    let topic = document.getElementById("topic").value;
    let style = document.getElementById("style").value;
    let outputArea = document.getElementById("output");

    let formData = new FormData();
    formData.append("topic", topic);
    formData.append("style", style);

    let response = await fetch("/generate", {
        method: "POST",
        body: formData
    });

    if (!response.ok) {
        outputArea.value = "Error: Failed to generate content.";
        return;
    }

    let data = await response.json();
    outputArea.value = data.content;
}