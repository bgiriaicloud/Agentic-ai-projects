document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const queryInput = document.getElementById('query-input');
    const reasoningSelect = document.getElementById('reasoning-effort');
    const btnSubmit = document.getElementById('btn-submit');
    const ksListContainer = document.getElementById('ks-list');
    const modeBadge = document.getElementById('mode-text');

    const valLatency = document.getElementById('val-latency');
    const valSubqueries = document.getElementById('val-subqueries');
    const valChunks = document.getElementById('val-chunks');
    const valCost = document.getElementById('val-cost');

    const tabAnswer = document.getElementById('tab-answer');
    const tabPlanning = document.getElementById('tab-planning');
    const tabRerank = document.getElementById('tab-rerank');
    const tabLogs = document.getElementById('tab-logs');

    const btnViewPayload = document.getElementById('btn-view-payload');
    const payloadModal = document.getElementById('payload-modal');
    const modalClose = document.getElementById('modal-close');
    const payloadCode = document.getElementById('payload-code');

    // Initialize System
    fetchHealth();
    fetchKnowledgeSources();

    // Preset Pill Click Handler
    document.querySelectorAll('.preset-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            queryInput.value = btn.getAttribute('data-query');
        });
    });

    // Tab Navigation Handler
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            
            btn.classList.add('active');
            const targetTab = btn.getAttribute('data-tab');
            document.getElementById(targetTab).classList.add('active');
        });
    });

    // Submit Query Handler
    btnSubmit.addEventListener('click', runAgenticRetrieval);

    // Payload Modal Handlers
    btnViewPayload.addEventListener('click', async () => {
        payloadModal.classList.add('active');
        const queryText = queryInput.value.trim() || "Find me a beachfront hotel with 24/7 airport shuttle";
        try {
            const res = await fetch('/api/simulate-azure-payload', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: queryText, reasoning_effort: reasoningSelect.value })
            });
            const data = await res.json();
            payloadCode.textContent = JSON.stringify(data, null, 2);
        } catch (e) {
            payloadCode.textContent = "Error fetching REST payload: " + e.message;
        }
    });

    modalClose.addEventListener('click', () => {
        payloadModal.classList.remove('active');
    });

    // Fetch Health Status
    async function fetchHealth() {
        try {
            const res = await fetch('/api/health');
            const data = await res.json();
            modeBadge.textContent = `Mode: ${data.execution_mode.toUpperCase()}`;
        } catch (e) {
            modeBadge.textContent = "Mode: Offline";
        }
    }

    // Fetch Registered Knowledge Sources
    async function fetchKnowledgeSources() {
        try {
            const res = await fetch('/api/knowledge-sources');
            const data = await res.json();
            ksListContainer.innerHTML = '';
            data.knowledge_sources.forEach(ks => {
                const item = document.createElement('div');
                item.className = 'ks-item';
                item.innerHTML = `
                    <div>
                        <div class="ks-name">${ks.name}</div>
                        <div style="font-size: 11px; color: var(--text-dim);">Search Type: ${ks.search_type}</div>
                    </div>
                    <span class="ks-badge">${ks.doc_count} Docs</span>
                `;
                ksListContainer.appendChild(item);
            });
        } catch (e) {
            ksListContainer.innerHTML = '<p style="color: var(--text-dim); font-size: 12px;">Failed to load sources.</p>';
        }
    }

    // Execute Agentic Retrieval Pipeline
    async function runAgenticRetrieval() {
        const query = queryInput.value.trim();
        if (!query) {
            alert('Please enter a query or select a preset query.');
            return;
        }

        btnSubmit.disabled = true;
        btnSubmit.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Executing Pipeline...';

        try {
            const res = await fetch('/api/retrieval', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    query: query,
                    reasoning_effort: reasoningSelect.value
                })
            });

            if (!res.ok) throw new Error("Retrieval failed");
            const data = await res.json();

            // Render Results
            updateMetrics(data.metrics);
            renderGroundedAnswer(data.grounded_answer, data.citations);
            renderQueryPlan(data.subqueries);
            renderSemanticRerank(data.retrieved_chunks);
            renderActivityLogs(data.activity_log);

        } catch (e) {
            alert('Error running agentic retrieval: ' + e.message);
        } finally {
            btnSubmit.disabled = false;
            btnSubmit.innerHTML = '<i class="fa-solid fa-paper-plane"></i> Run Agentic Retrieval';
        }
    }

    function updateMetrics(m) {
        valLatency.textContent = `${m.latency_ms} ms`;
        valSubqueries.textContent = m.subquery_count;
        valChunks.textContent = m.chunks_reranked;
        valCost.textContent = `$${m.estimated_cost_usd.toFixed(4)}`;
    }

    function renderGroundedAnswer(answer, citations) {
        let citationsHtml = '';
        if (citations && citations.length > 0) {
            citationsHtml = `
                <div class="citations-box">
                    <h4 style="font-size: 14px; margin-bottom: 10px; color: var(--text-muted);">
                        <i class="fa-solid fa-bookmark"></i> Grounded Citations & Sources
                    </h4>
                    ${citations.map(c => `
                        <div class="citation-card">
                            <div><span class="citation-tag">${c.citation_id}</span> <strong>${c.title}</strong> (${c.category})</div>
                            <div style="font-size: 12px; color: var(--text-muted); margin-top: 4px;">"${c.snippet}"</div>
                        </div>
                    `).join('')}
                </div>
            `;
        }

        tabAnswer.innerHTML = `
            <div class="answer-box">
                <div style="white-space: pre-line;">${answer}</div>
                ${citationsHtml}
            </div>
        `;
    }

    function renderQueryPlan(subqueries) {
        if (!subqueries || subqueries.length === 0) {
            tabPlanning.innerHTML = '<p class="empty-state">No subquery plan available.</p>';
            return;
        }

        tabPlanning.innerHTML = subqueries.map(sq => `
            <div class="subquery-card">
                <div class="subquery-header">
                    <span class="subquery-id">${sq.id} &#8226; Target: ${sq.target_source_id}</span>
                    <span class="ks-badge">${sq.search_type.toUpperCase()}</span>
                </div>
                <div style="font-weight: 600; margin-bottom: 4px;">"${sq.query_text}"</div>
                <div style="font-size: 12px; color: var(--text-dim);"><i class="fa-solid fa-lightbulb"></i> ${sq.rationale}</div>
            </div>
        `).join('');
    }

    function renderSemanticRerank(chunks) {
        if (!chunks || chunks.length === 0) {
            tabRerank.innerHTML = '<p class="empty-state">No chunks reranked.</p>';
            return;
        }

        tabRerank.innerHTML = chunks.map((c, idx) => `
            <div class="rerank-item">
                <div>
                    <div style="font-size: 11px; color: var(--text-dim);">Rank #${idx + 1} &#8226; Document: ${c.doc_id}</div>
                    <div style="font-weight: 600;">${c.title}</div>
                    <div style="font-size: 12px; color: var(--text-muted);">${c.content}</div>
                </div>
                <div class="score-pill">L2 Score: ${c.semantic_rerank_score.toFixed(2)}</div>
            </div>
        `).join('');
    }

    function renderActivityLogs(logs) {
        if (!logs || logs.length === 0) {
            tabLogs.innerHTML = '<p class="empty-logs">No activity log.</p>';
            return;
        }

        tabLogs.innerHTML = `
            <div class="logs-wrapper">
                ${logs.map(l => `
                    <div class="log-entry">
                        <span class="log-time">[${l.timestamp}]</span>
                        <span class="log-step">[${l.step}]</span>
                        <span>${l.detail}</span>
                    </div>
                `).join('')}
            </div>
        `;
    }
});
