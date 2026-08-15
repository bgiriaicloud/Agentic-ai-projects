document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const promptInput = document.getElementById('prompt-input');
    const btnSubmit = document.getElementById('btn-submit');
    const btnNewSession = document.getElementById('btn-new-session');
    const currentSessionTag = document.getElementById('current-session-id');
    const toolsListContainer = document.getElementById('tools-list');
    const modeBadge = document.getElementById('mode-text');

    const valLatency = document.getElementById('val-latency');
    const valTools = document.getElementById('val-tools');
    const valTraces = document.getElementById('val-traces');
    const valStatus = document.getElementById('val-status');

    const tabResponse = document.getElementById('tab-response');
    const tabMemory = document.getElementById('tab-memory');
    const tabTraces = document.getElementById('tab-traces');

    let currentSessionId = null;

    // Initialize System
    fetchHealth();
    fetchGatewayTools();
    createNewSession();

    // Preset Pill Click Handler
    document.querySelectorAll('.preset-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            promptInput.value = btn.getAttribute('data-prompt');
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

    // Button Handlers
    btnSubmit.addEventListener('click', runAgentTurn);
    btnNewSession.addEventListener('click', createNewSession);

    // Fetch Health
    async function fetchHealth() {
        try {
            const res = await fetch('/api/health');
            const data = await res.json();
            modeBadge.textContent = `Mode: ${data.execution_mode.toUpperCase()}`;
        } catch (e) {
            modeBadge.textContent = "Mode: Offline";
        }
    }

    // Fetch Gateway MCP Tools
    async function fetchGatewayTools() {
        try {
            const res = await fetch('/api/agent/tools');
            const data = await res.json();
            toolsListContainer.innerHTML = '';
            data.tools.forEach(t => {
                const item = document.createElement('div');
                item.className = 'tool-item';
                item.innerHTML = `
                    <div class="tool-name"><i class="fa-solid fa-gear"></i> ${t.name}</div>
                    <div class="tool-desc">${t.description}</div>
                `;
                toolsListContainer.appendChild(item);
            });
        } catch (e) {
            toolsListContainer.innerHTML = '<p style="color: var(--text-dim); font-size: 12px;">Failed to load tools.</p>';
        }
    }

    // Create New Session
    async function createNewSession() {
        try {
            const res = await fetch('/api/sessions', { method: 'POST' });
            const session = await res.json();
            currentSessionId = session.session_id;
            currentSessionTag.textContent = `Session: ${currentSessionId}`;
            
            // Clear outputs
            tabResponse.innerHTML = '<div class="empty-state"><i class="fa-solid fa-robot empty-icon"></i><p>New Amazon AgentCore session created. Ready for instructions.</p></div>';
            tabMemory.innerHTML = '<p class="empty-state">No memory facts stored yet.</p>';
            tabTraces.innerHTML = '<p class="empty-logs">Traces will appear here once agent runs.</p>';
            valLatency.textContent = '-- ms';
            valTools.textContent = '0';
            valTraces.textContent = '0';
        } catch (e) {
            currentSessionTag.textContent = "Session: Error";
        }
    }

    // Run Agent Turn
    async function runAgentTurn() {
        const prompt = promptInput.value.trim();
        if (!prompt) {
            alert('Please enter a prompt instruction.');
            return;
        }

        btnSubmit.disabled = true;
        btnSubmit.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Executing AgentCore Cycle...';

        try {
            const res = await fetch('/api/agent/run', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    session_id: currentSessionId,
                    prompt: prompt
                })
            });

            if (!res.ok) throw new Error("AgentCore turn execution failed");
            const data = await res.json();

            currentSessionId = data.session_id;
            currentSessionTag.textContent = `Session: ${currentSessionId}`;

            // Update Metrics
            valLatency.textContent = `${data.metrics.total_latency_ms} ms`;
            valTools.textContent = data.tool_results.length;
            valTraces.textContent = data.traces.length;

            // Render Tab Outputs
            renderResponse(data.response, data.tool_results);
            renderMemory(data.long_term_memory);
            renderTraces(data.traces);

        } catch (e) {
            alert('Error executing AgentCore agent: ' + e.message);
        } finally {
            btnSubmit.disabled = false;
            btnSubmit.innerHTML = '<i class="fa-solid fa-paper-plane"></i> Run AgentCore Cycle';
        }
    }

    function renderResponse(responseMarkdown, toolResults) {
        let toolsHtml = '';
        if (toolResults && toolResults.length > 0) {
            toolsHtml = `
                <div style="margin-top: 20px; border-top: 1px solid var(--border-color); padding-top: 16px;">
                    <h4 style="font-size: 13px; color: var(--text-muted); margin-bottom: 10px;">
                        <i class="fa-solid fa-screwdriver-wrench"></i> Amazon AgentCore Gateway Tool Call Executions
                    </h4>
                    ${toolResults.map(tr => `
                        <div style="background: rgba(13, 17, 23, 0.8); border: 1px solid var(--border-color); border-radius: 8px; padding: 12px; margin-bottom: 8px;">
                            <div style="font-family: var(--font-code); font-size: 12px; color: var(--primary);">Tool: ${tr.tool} [${tr.status.toUpperCase()}]</div>
                            <pre style="margin-top: 6px; font-size: 11px; color: #38bdf8;">${JSON.stringify(tr.output, null, 2)}</pre>
                        </div>
                    `).join('')}
                </div>
            `;
        }

        tabResponse.innerHTML = `
            <div class="response-box">
                <div style="white-space: pre-line;">${responseMarkdown}</div>
                ${toolsHtml}
            </div>
        `;
    }

    function renderMemory(longTermMemory) {
        if (!longTermMemory || Object.keys(longTermMemory).length === 0) {
            tabMemory.innerHTML = '<p class="empty-state">No long-term memory facts stored yet.</p>';
            return;
        }

        tabMemory.innerHTML = `
            <div class="memory-card">
                <div class="memory-title"><i class="fa-solid fa-brain"></i> AgentCore Long-Term Memory Facts</div>
                ${Object.entries(longTermMemory).map(([k, v]) => `
                    <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid var(--border-color); border-radius: 8px; padding: 10px; margin-bottom: 8px;">
                        <div style="font-family: var(--font-code); font-size: 12px; color: var(--accent);">${k}</div>
                        <div style="font-weight: 600; margin-top: 2px;">Value: ${v.value}</div>
                        <div style="font-size: 10px; color: var(--text-dim); margin-top: 2px;">Updated: ${v.updated_at}</div>
                    </div>
                `).join('')}
            </div>
        `;
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
                        <span class="trace-comp">[${t.component}]</span>
                        <span class="trace-action">${t.action}</span>
                        <span style="color: var(--text-muted); font-size: 11px;">(${t.duration_ms}ms)</span>
                        <pre style="margin-top: 4px; font-size: 11px; color: var(--text-muted);">${JSON.stringify(t.details, null, 2)}</pre>
                    </div>
                `).join('')}
            </div>
        `;
    }
});
