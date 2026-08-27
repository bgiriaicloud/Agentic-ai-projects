document.addEventListener("DOMContentLoaded", () => {
    const queryInput = document.getElementById("queryInput");
    const searchBtn = document.getElementById("searchBtn");
    const loading = document.getElementById("loading");
    const reasoningContainer = document.getElementById("reasoningContainer");
    const reasoningList = document.getElementById("reasoningList");
    const responseContainer = document.getElementById("responseContainer");
    const answerText = document.getElementById("answerText");
    const citationList = document.getElementById("citationList");
    const latencyBadge = document.getElementById("latencyBadge");

    const fileNameInput = document.getElementById("fileNameInput");
    const fileContentInput = document.getElementById("fileContentInput");
    const ingestBtn = document.getElementById("ingestBtn");
    const ingestResult = document.getElementById("ingestResult");

    searchBtn.addEventListener("click", async () => {
        const query = queryInput.value.trim();
        if (!query) return;

        loading.classList.remove("hidden");
        reasoningContainer.classList.add("hidden");
        responseContainer.classList.add("hidden");

        try {
            const res = await fetch("/api/rag/query", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query })
            });

            const data = await res.json();

            loading.classList.add("hidden");

            if (res.ok) {
                // Populate Reasoning
                reasoningList.innerHTML = data.reasoning_steps.map(step => `<li>${step}</li>`).join("");
                reasoningContainer.classList.remove("hidden");

                // Populate Response
                answerText.textContent = data.answer;
                citationList.innerHTML = data.citations.map(c => `<li>${c}</li>`).join("");
                latencyBadge.textContent = `Latency: ${data.latency_seconds}s | Query ID: ${data.query_id}`;
                responseContainer.classList.remove("hidden");
            } else {
                alert(`Error: ${data.detail}`);
            }
        } catch (err) {
            loading.classList.add("hidden");
            alert("Failed to reach GCP RAG Backend Server.");
        }
    });

    ingestBtn.addEventListener("click", async () => {
        const fileName = fileNameInput.value.trim();
        const content = fileContentInput.value.trim();

        if (!fileName || !content) return;

        try {
            const res = await fetch("/api/rag/ingest", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ file_name: fileName, content })
            });

            const data = await res.json();
            if (res.ok) {
                ingestResult.textContent = data.message;
                ingestResult.classList.remove("hidden");
            } else {
                alert(`Ingest Error: ${data.detail}`);
            }
        } catch (err) {
            alert("Failed to ingest document via Pub/Sub.");
        }
    });
});
