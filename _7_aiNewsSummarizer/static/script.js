async function fetchNews() {
    let category = document.getElementById("category").value;
    let summaryDiv = document.getElementById("summary");
    let articlesDiv = document.getElementById("articles");

    let response = await fetch(`/fetch_news?category=${category}`);

    if (!response.ok) {
        summaryDiv.innerHTML = "<p style='color: red;'>Error: Failed to fetch news.</p>";
        return;
    }

    let data = await response.json();
    summaryDiv.innerHTML = `<p>${data.summary}</p>`;

    let articlesHTML = "";
    data.articles.forEach(article => {
        articlesHTML += `<p><strong>${article.title}</strong> (${article.source.name})<br><a href="${article.url}" target="_blank">Read more</a></p>`;
    });

    articlesDiv.innerHTML = articlesHTML;
}