document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const promptInput = document.getElementById('prompt-input');
    const btnSubmit = document.getElementById('btn-submit');
    const btnNewSession = document.getElementById('btn-new-session');
    const currentSessionTag = document.getElementById('current-session-id');
    const extensionsListContainer = document.getElementById('extensions-list');
    const modeBadge = document.getElementById('mode-text');

    const valLatency = document.getElementById('val-latency');
    const valGrounding = document.getElementById('val-grounding');
    const valSafety = document.getElementById('val-safety');
    const valCost = document.getElementById('val-cost');

    const tabResponse = document.getElementById('tab-response');
    const tabGovern = document.getElementById('tab-govern');
    const tabExtensions = document.getElementById('tab-extensions');
    const tabTraces = document.getElementById('tab-traces');

    let currentSessionId = null;

    // Initialize System
    fetchHealth();
    fetchExtensions();
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

    // Button Event Handlers
    btnSubmit.addEventListener('click', runAgentPlatformCycle);
    btnNewSession.addEventListener('click', createNewSession);

    // Fetch Health
    async function fetchHealth() {
        try {
            const res = await fetch('/api/health');
            const data = await res.json();
            modeBadge.textContent = `Mode: ${data.execution_mode.toUpperCase()} (${data.project_id})`;
        } catch (e) {
            modeBadge.textContent = "Mode: Offline";
        }
    }

    // Fetch Vertex Extensions
    async function fetchExtensions() {
        try {
            const res = await fetch('/api/agent/extensions');
            const data = await res.json();
            extensionsListContainer.innerHTML = '';
            data.extensions.forEach(e => {
                const item = document.createElement('div');
                item.className = 'extension-item';
                item.innerHTML = `
                    <div class="ext-name"><i class="fa-solid fa-puzzle-piece"></i> ${e.name} (${e.type})</div>
                    <div class="ext-desc">${e.description}</div>
                `;
                extensionsListContainer.appendChild(item);
            });
        } catch (e) {
            extensionsListContainer.innerHTML = '<p style="color: var(--text-dim); font-size: 12px;">Failed to load extensions.</p>';
        }
    }

    // Create New Session
    async function createNewSession() {
        try {
            const res = await fetch('/api/sessions', { method: 'POST' });
            const session = await res.json();
            currentSessionId = session.session_id;
            currentSessionTag.textContent = `Session: ${currentSessionId}`;

            // Reset UI
            tabResponse.innerHTML = '<div class="empty-state"><i class="fa-solid fa-layer-group empty-icon"></i><p>New GCP session container initialized. Ready for enterprise query.</p></div>';
            tabGovern.innerHTML = '<p class="empty-state">No governance evaluation yet.</p>';
            tabExtensions.innerHTML = '<p class="empty-state">No extension outputs to display.</p>';
            tabTraces.innerHTML = '<p class="empty-logs">Telemetry traces will appear here.</p>';

            valLatency.textContent = '-- ms';
            valGrounding.textContent = '-- %';
            valSafety.textContent = 'PASSED';
            valCost.textContent = '$0.0000';
        } catch (e) {
            currentSessionTag.textContent = "Session: Error";
        }
    }

    // Run Agent Platform Cycle
    async function runAgentPlatformCycle() {
        const prompt = promptInput.value.trim();
        if (!prompt) {
            alert('Please enter a query or select a preset.');
            return;
        }

        btnSubmit.disabled = true;
        btnSubmit.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Executing GCP Agent Platform...';

        try {
            const res = await fetch('/api/agent/run', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    session_id: currentSessionId,
                    prompt: prompt
                })
            });

            if (!res.ok) throw new Error("GCP Agent execution failed");
            const data = await res.json();

            currentSessionId = data.session_id;
            currentSessionTag.textContent = `Session: ${currentSessionId}`;

            // Metrics Update
            valLatency.textContent = `${data.metrics.total_latency_ms} ms`;
            valGrounding.textContent = `${(data.governance.grounding_score * 100).toFixed(0)}%`;
            valSafety.textContent = data.governance.safety_passed ? "PASSED" : "BLOCKED";
            valCost.textContent = `$${data.metrics.cost_optimization.estimated_cost_usd.toFixed(6)}`;

            // Render Tabs
            renderResponse(data.response);
            renderGovernance(data.governance);
            renderExtensions(data.extension_results);
            renderTraces(data.traces);

        } catch (e) {
            alert('Error running GCP Agent Platform: ' + e.message);
        } finally {
            btnSubmit.disabled = false;
            btnSubmit.innerHTML = '<i class="fa-solid fa-paper-plane"></i> Execute Agent Platform Cycle';
        }
    }

    function renderResponse(responseMarkdown) {
        tabResponse.innerHTML = `
            <div class="response-box">
                <div style="white-space: pre-line;">${responseMarkdown}</div>
            </div>
        `;
    }

    function renderGovernance(gov) {
        tabGovern.innerHTML = `
            <div class="govern-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <h3><i class="fa-solid fa-shield-halved"></i> Governance & Safety Audit</h3>
                    <span class="govern-badge">${gov.grounding_status}</span>
                </div>
                <div style="font-size: 13px; line-height: 1.6;">
                    <div><strong>Grounding Score:</strong> ${(gov.grounding_score * 100).toFixed(1)}%</div>
                    <div><strong>Responsible AI Safety:</strong> ${gov.safety_passed ? '<span style="color: var(--gcp-green);">PASS</span>' : '<span style="color: var(--gcp-red);">FAIL</span>'}</div>
                    <div><strong>PII Redaction:</strong> ${gov.pii_redacted ? 'Active' : 'Disabled'}</div>
                    <div style="margin-top: 10px; color: var(--text-muted); font-size: 12px;">${gov.compliance_notes}</div>
                </div>
            </div>
        `;
    }

    function renderExtensions(extensionResults) {
        if (!extensionResults || extensionResults.length === 0) {
            tabExtensions.innerHTML = '<p class="empty-state">No extensions invoked for this query.</p>';
            return;
        }

        tabExtensions.innerHTML = extensionResults.map(er => `
            <div style="background: rgba(10, 14, 23, 0.8); border: 1px solid var(--border-color); border-radius: 10px; padding: 14px; margin-bottom: 12px;">
                <div style="font-family: var(--font-code); font-size: 13px; color: var(--gcp-blue); font-weight: 600;">
                    Extension: ${er.extension} [${er.status.toUpperCase()}]
                </div>
                <pre style="margin-top: 8px; font-family: var(--font-code); font-size: 11px; color: #38bdf8; overflow-x: auto;">${JSON.stringify(er.output, null, 2)}</pre>
            </div>
        `).join('');
    }

    function renderTraces(traces) {
        if (!traces || traces.length === 0) {
            tabTraces.innerHTML = '<p class="empty-logs">No telemetry traces available.</p>';
            return;
        }

        tabTraces.innerHTML = `
            <div class="logs-wrapper">
                ${traces.map(t => `
                    <div class="trace-item">
                        <span style="color: var(--text-dim);">[${t.timestamp}]</span>
                        <span class="trace-pillar ${t.pillar}">${t.pillar}</span>
                        <span style="color: var(--text-main); font-weight: 600;">${t.action}</span>
                        <span style="color: var(--text-muted); font-size: 11px;">(${t.latency_ms}ms)</span>
                        <pre style="margin-top: 4px; font-size: 11px; color: var(--text-muted);">${JSON.stringify(t.details, null, 2)}</pre>
                    </div>
                `).join('')}
            </div>
        `;
    }
});
