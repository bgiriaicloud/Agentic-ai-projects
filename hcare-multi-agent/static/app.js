document.addEventListener("DOMContentLoaded", () => {
    const patientIdInput = document.getElementById("patientIdInput");
    const userRoleSelect = document.getElementById("userRoleSelect");
    const queryInput = document.getElementById("queryInput");
    const dispatchBtn = document.getElementById("dispatchBtn");

    const loading = document.getElementById("loading");
    const responseContainer = document.getElementById("responseContainer");
    const agentBadge = document.getElementById("agentBadge");
    const answerText = document.getElementById("answerText");
    const clinicalReasoningText = document.getElementById("clinicalReasoningText");
    const redactionsBox = document.getElementById("redactionsBox");

    const traceContainer = document.getElementById("traceContainer");
    const fhirBox = document.getElementById("fhirBox");
    const fhirContent = document.getElementById("fhirContent");

    // Dynamic prompt suggestions based on role change
    userRoleSelect.addEventListener("change", (e) => {
        const role = e.target.value;
        if (role === "Patient") {
            queryInput.value = "What are my latest blood test and HbA1c glucose lab results?";
        } else if (role === "Doctor") {
            queryInput.value = "Access doctor clinical notes and physician recommendation.";
        } else if (role === "Nurse") {
            queryInput.value = "Coordinate nursing shift handoff and medication administration schedule.";
        } else if (role === "Admin") {
            queryInput.value = "Check hospital ICU bed occupancy and staffing metrics.";
        } else if (role === "Insurance") {
            queryInput.value = "Verify insurance claim pre-authorization status and specialist copay.";
        } else if (role === "IT") {
            queryInput.value = "Run IT system diagnostics and check Cloud Healthcare FHIR API latency.";
        }
    });

    dispatchBtn.addEventListener("click", async () => {
        const query = queryInput.value.trim();
        const patient_id = patientIdInput.value.trim();
        const user_role = userRoleSelect.value;

        if (!query) return;

        loading.classList.remove("hidden");
        responseContainer.classList.add("hidden");
        fhirBox.classList.add("hidden");

        try {
            const res = await fetch("/api/agents/query", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    patient_id,
                    user_role,
                    query,
                    include_raw_fhir: true
                })
            });

            const data = await res.json();
            loading.classList.add("hidden");

            if (res.ok) {
                // Populate Response
                agentBadge.textContent = `Assigned Specialist: ${data.routed_agent}`;
                answerText.textContent = data.final_response;
                clinicalReasoningText.textContent = data.clinical_reasoning;

                if (data.redacted_phi_entities && data.redacted_phi_entities.length > 0) {
                    redactionsBox.textContent = `🛡️ HIPAA De-identified Entities: ${data.redacted_phi_entities.join(", ")}`;
                    redactionsBox.classList.remove("hidden");
                } else {
                    redactionsBox.classList.add("hidden");
                }

                responseContainer.classList.remove("hidden");

                // Populate Live Execution Trace
                traceContainer.innerHTML = data.execution_trace.map(step => `
                    <div class="trace-card">
                        <div class="trace-title">
                            <span>${step.agent_name}</span>
                            <span class="trace-latency">${step.latency_ms}ms</span>
                        </div>
                        <div class="trace-desc"><strong>Action:</strong> ${step.action}</div>
                        <div class="trace-desc" style="color: #94a3b8; margin-top: 0.2rem;"><strong>Observation:</strong> ${step.observation}</div>
                    </div>
                `).join("");

                // Populate FHIR Resources if present
                if (data.fhir_resources && data.fhir_resources.length > 0) {
                    fhirContent.textContent = JSON.stringify(data.fhir_resources, null, 2);
                    fhirBox.classList.remove("hidden");
                }
            } else {
                alert(`Error: ${data.detail}`);
            }
        } catch (err) {
            loading.classList.add("hidden");
            alert("Failed to reach Healthcare Multi-Agent API.");
        }
    });
});
