document.addEventListener('DOMContentLoaded', () => {
    const promptInput = document.getElementById('prompt-input');
    const btnSubmit = document.getElementById('btn-submit');
    const btnReset = document.getElementById('btn-reset-session');
    const currentSessionTag = document.getElementById('current-session-id');
    const mcpToolsListContainer = document.getElementById('mcp-tools-list');
    const modeBadge = document.getElementById('mode-text');

    const valLatency = document.getElementById('val-latency');
    const valSubagents = document.getElementById('val-subagents');
    const valMcpCalls = document.getElementById('val-mcp-calls');
    const valStatus = document.getElementById('val-status');

    const tabResponse = document.getElementById('tab-response');
    const tabA2a = document.getElementById('tab-a2a');
    const tabTraces = document.getElementById('tab-traces');

    let currentSessionId = null;

    fetchHealth();
    fetchMcpTools();

    document.querySelectorAll('.preset-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            promptInput.value = btn.getAttribute('data-prompt');
        });
    });

    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            
            btn.classList.add('active');
            const targetTab = btn.getAttribute('data-tab');
            document.getElementById(targetTab).classList.add('active');
        });
    });

    btnSubmit.addEventListener('click', runOrchestration);
    btnReset.addEventListener('click', () => {
        currentSessionId = null;
        currentSessionTag.textContent = "Session: Auto";
        tabResponse.innerHTML = '<div class="empty-state"><i class="fa-solid fa-network-wired empty-icon"></i><p>Session reset. Submit a prompt to start.</p></div>';
        tabA2a.innerHTML = '<p class="empty-state">No subagent delegations.</p>';
        tabTraces.innerHTML = '<p class="empty-logs">Traces reset.</p>';
        valLatency.textContent = '-- ms';
        valSubagents.textContent = '0';
        valMcpCalls.textContent = '0';
        valStatus.textContent = 'READY';
    });

    async function fetchHealth() {
        try {
            const res = await fetch('/api/health');
            const data = await res.json();
            modeBadge.textContent = `Mode: ${data.execution_mode.toUpperCase()}`;
        } catch (e) {
            modeBadge.textContent = "Mode: Offline";
        }
    }

    async function fetchMcpTools() {
        try {
            const res = await fetch('/api/mcp/tools');
            const data = await res.json();
            mcpToolsListContainer.innerHTML = '';
            data.tools.forEach(t => {
                const item = document.createElement('div');
                item.className = 'mcp-item';
                item.innerHTML = `
                    <div class="mcp-name"><i class="fa-solid fa-server"></i> ${t.name}</div>
                    <div class="mcp-desc">${t.description}</div>
                `;
                mcpToolsListContainer.appendChild(item);
            });
        } catch (e) {
            mcpToolsListContainer.innerHTML = '<p style="color: var(--text-dim); font-size: 12px;">Failed to load MCP tools.</p>';
        }
    }

    async function runOrchestration() {
        const prompt = promptInput.value.trim();
        if (!prompt) {
            alert('Please enter a prompt instruction.');
            return;
        }

        btnSubmit.disabled = true;
        btnSubmit.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Running A2A Orchestration...';

        try {
            const res = await fetch('/api/orchestrate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    prompt: prompt,
                    session_id: currentSessionId
                })
            });

            if (!res.ok) throw new Error("Orchestration failed");
            const data = await res.json();

            currentSessionId = data.session_id;
            currentSessionTag.textContent = `Session: ${currentSessionId}`;

            valLatency.textContent = `${data.metrics.total_latency_ms} ms`;
            valSubagents.textContent = data.metrics.subagents_count;
            valMcpCalls.textContent = '2';
            valStatus.textContent = 'SUCCESS';

            renderResponse(data.grounded_response);
            renderA2a(data.subagent_outputs);
            renderTraces(data.traces);

        } catch (e) {
            alert('Error running A2A Orchestration: ' + e.message);
            valStatus.textContent = 'ERROR';
        } finally {
            btnSubmit.disabled = false;
            btnSubmit.innerHTML = '<i class="fa-solid fa-paper-plane"></i> Run A2A Orchestration';
        }
    }

    function renderResponse(resp) {
        tabResponse.innerHTML = `
            <div class="response-box">
                <div style="white-space: pre-line;">${resp}</div>
            </div>
        `;
    }

    function renderA2a(subagentOutputs) {
        if (!subagentOutputs || subagentOutputs.length === 0) {
            tabA2a.innerHTML = '<p class="empty-state">No subagent delegations.</p>';
            return;
        }

        tabA2a.innerHTML = subagentOutputs.map(s => `
            <div class="a2a-card">
                <div class="a2a-header">
                    <span class="a2a-agent-name"><i class="fa-solid fa-robot"></i> ${s.subagent} (${s.role})</span>
                    <span style="font-size: 11px; color: var(--text-dim);">${s.latency_ms}ms</span>
                </div>
                <div style="font-size: 13px; margin-bottom: 8px;">${s.summary}</div>
                <pre style="font-family: var(--font-code); font-size: 11px; color: #38bdf8; overflow-x: auto;">${JSON.stringify(s, null, 2)}</pre>
            </div>
        `).join('');
    }

    function renderTraces(traces) {
        if (!traces || traces.length === 0) {
            tabTraces.innerHTML = '<p class="empty-logs">No traces available.</p>';
            return;
        }

        tabTraces.innerHTML = `
            <div class="logs-wrapper">
                ${traces.map(t => `
                    <div class="trace-item">
                        <span style="color: var(--text-dim);">[${t.timestamp}]</span>
                        <span style="color: var(--primary); font-weight: 600;">[${t.agent}]</span>
                        <span style="color: var(--accent);">${t.action}</span>
                        <pre style="margin-top: 4px; font-size: 11px; color: var(--text-muted);">${JSON.stringify(t.details, null, 2)}</pre>
                    </div>
                `).join('')}
            </div>
        `;
    }
});
