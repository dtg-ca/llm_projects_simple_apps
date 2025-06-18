async function generateContent() {
    let topic = document.getElementById("topic").value;
    let style = document.getElementById("style").value;
    let outputDiv = document.getElementById("output");
    outputDiv.innerHTML = "Generating content...";

    let formData = new FormData();
    formData.append("text",  topic);
    formData.append("style", style);

    let response = await fetch("/generate", {
        method: "POST",
        body: formData,
    });

    
    let data = await response.json();
        if (data.error) {
        outputDiv.innerHTML = `<p style='color: red;'>Error: ${data.error}</p>`;
    } else {
        outputDiv.innerHTML = `<p>${data.content}</p>`;
    }
    }

    