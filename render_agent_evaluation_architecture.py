"""
Renders High-Resolution Architecture Diagram for Agent Evaluation on Google Cloud
Architecture: Dataset -> Agent Under Test -> Evaluation Engine (LLM-as-a-Judge) -> Metrics & Governance
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_agent_evaluation_architecture():
    fig, ax = plt.subplots(figsize=(18, 10.5), dpi=300)
    fig.patch.set_facecolor('#090e17')
    ax.set_facecolor('#090e17')

    # Title
    ax.text(9.0, 9.9, "AGENT EVALUATION & BENCHMARKING ARCHITECTURE", 
            color='#00f2fe', fontsize=20, fontweight='bold', ha='center', fontfamily='sans-serif')
    ax.text(9.0, 9.5, "Continuous Evaluation • LLM-as-a-Judge • Multi-Metric Grounding • Cloud Build CI/CD", 
            color='#94a3b8', fontsize=11, ha='center', fontfamily='sans-serif')

    # Helper: Card Box
    def draw_card(x, y, w, h, title, subtitle, bg_color='#131f37', border_color='#38bdf8', badge=None):
        card = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15,rounding_size=0.2",
                                      facecolor=bg_color, edgecolor=border_color, linewidth=1.8)
        ax.add_patch(card)
        ax.text(x + w/2, y + h - 0.35, title, color='#ffffff', fontsize=10.5, fontweight='bold', ha='center', va='center')
        ax.text(x + w/2, y + h*0.45, subtitle, color='#94a3b8', fontsize=8.0, ha='center', va='center', wrap=True)
        if badge:
            bx = x + w - 0.4
            by = y + h - 0.25
            badge_circle = patches.Circle((bx, by), 0.22, facecolor='#10b981', edgecolor='none', zorder=5)
            ax.add_patch(badge_circle)
            ax.text(bx, by, badge, color='#ffffff', fontsize=7.0, fontweight='bold', ha='center', va='center', zorder=6)

    # -------------------------------------------------------------------------
    # Stage 1: Evaluation Inputs & Benchmarking Datasets (x: 0.8 to 4.2)
    # -------------------------------------------------------------------------
    s1_box = patches.FancyBboxPatch((0.6, 1.2), 3.8, 7.8, boxstyle="round,pad=0.2",
                                    facecolor='#0f172a', edgecolor='#38bdf8', linewidth=2.0, linestyle='--')
    ax.add_patch(s1_box)
    ax.text(2.5, 8.6, "1. EVALUATION DATASETS", color='#38bdf8', fontsize=12, fontweight='bold', ha='center')

    draw_card(0.9, 6.7, 3.2, 1.5, "Golden Test Dataset", "Curated Ground Truth QA\nEdge Cases & Challenging Scenarios", bg_color='#1e293b', border_color='#38bdf8')
    draw_card(0.9, 4.8, 3.2, 1.5, "Synthetic Simulation", "Multi-turn Synthetic User\nPersona Dialogue Generator", bg_color='#1e293b', border_color='#38bdf8', badge="New")
    draw_card(0.9, 2.9, 3.2, 1.5, "Production Traffic Replay", "Anonymized Cloud Logging Logs\nReal Customer Inquiries", bg_color='#1e293b', border_color='#38bdf8')
    draw_card(0.9, 1.4, 3.2, 1.2, "Red-Teaming Suite", "Jailbreak & Prompt Injection\nAdversarial Attack Vectors", bg_color='#450a0a', border_color='#ef4444')

    # -------------------------------------------------------------------------
    # Stage 2: Agent Under Test & Execution (x: 4.8 to 8.2)
    # -------------------------------------------------------------------------
    s2_box = patches.FancyBboxPatch((4.8, 1.2), 3.8, 7.8, boxstyle="round,pad=0.2",
                                    facecolor='#0f172a', edgecolor='#818cf8', linewidth=2.0)
    ax.add_patch(s2_box)
    ax.text(6.7, 8.6, "2. AGENT UNDER TEST", color='#818cf8', fontsize=12, fontweight='bold', ha='center')

    draw_card(5.1, 6.7, 3.2, 1.5, "Gemini Agent Core", "Multi-Turn ReAct Reasoning\nGemini 2.0 Flash / Pro", bg_color='#1e1b4b', border_color='#818cf8')
    draw_card(5.1, 4.8, 3.2, 1.5, "ADK Skills & Tools", "Tool Calling Function Schema\nOpenAPI / MCP Tool Handlers", bg_color='#1e1b4b', border_color='#818cf8')
    draw_card(5.1, 2.9, 3.2, 1.5, "Grounding & Vector RAG", "Vertex AI Vector Search (HNSW)\nDocument Context Retrieval", bg_color='#1e1b4b', border_color='#818cf8')
    draw_card(5.1, 1.4, 3.2, 1.2, "Execution Trace Logger", "Captures Thoughts, Tool Calls,\nLatency & Token Costs", bg_color='#1e1b4b', border_color='#818cf8')

    # -------------------------------------------------------------------------
    # Stage 3: Multi-Metric Evaluation Engine (x: 9.0 to 13.0)
    # -------------------------------------------------------------------------
    s3_box = patches.FancyBboxPatch((9.0, 1.2), 4.2, 7.8, boxstyle="round,pad=0.2",
                                    facecolor='#0f172a', edgecolor='#10b981', linewidth=2.0)
    ax.add_patch(s3_box)
    ax.text(11.1, 8.6, "3. EVALUATION ENGINE (LLM JUDGE)", color='#10b981', fontsize=12, fontweight='bold', ha='center')

    draw_card(9.3, 7.0, 3.6, 1.3, "Groundedness / Faithfulness", "Checks if claims are 100% supported\nby retrieved document context", bg_color='#064e3b', border_color='#10b981')
    draw_card(9.3, 5.5, 3.6, 1.3, "Answer Relevance", "Measures if answer directly addresses\nthe user's original objective", bg_color='#064e3b', border_color='#10b981')
    draw_card(9.3, 4.0, 3.6, 1.3, "Tool Selection Accuracy", "Evaluates correct tool chosen &\nvalid JSON parameter arguments", bg_color='#064e3b', border_color='#10b981')
    draw_card(9.3, 2.5, 3.6, 1.3, "Safety & Policy Alignment", "Scored against Model Armor policies\n(Zero toxic output & PII leaks)", bg_color='#064e3b', border_color='#10b981')
    draw_card(9.3, 1.4, 3.6, 0.9, "Latency & Efficiency Metric", "Token efficiency & p99 response time", bg_color='#064e3b', border_color='#10b981')

    # -------------------------------------------------------------------------
    # Stage 4: CI/CD Quality Gates & Reporting (x: 13.6 to 17.4)
    # -------------------------------------------------------------------------
    s4_box = patches.FancyBboxPatch((13.6, 1.2), 3.8, 7.8, boxstyle="round,pad=0.2",
                                    facecolor='#0f172a', edgecolor='#f59e0b', linewidth=2.0, linestyle='--')
    ax.add_patch(s4_box)
    ax.text(15.5, 8.6, "4. QUALITY GATES & CI/CD", color='#f59e0b', fontsize=12, fontweight='bold', ha='center')

    draw_card(13.9, 6.7, 3.2, 1.5, "Cloud Build CI/CD Gate", "Automated regression tests\nPass Threshold: Score >= 4.5/5.0", bg_color='#451a03', border_color='#f59e0b')
    draw_card(13.9, 4.8, 3.2, 1.5, "Vertex Model Monitoring", "Detects real-time prompt drift &\naccuracy decay in production", bg_color='#451a03', border_color='#f59e0b')
    draw_card(13.9, 2.9, 3.2, 1.5, "Looker Studio Dashboard", "Executive accuracy trends,\nper-agent latency & cost graphs", bg_color='#451a03', border_color='#f59e0b')
    draw_card(13.9, 1.4, 3.2, 1.2, "Automated Rollback Hook", "Auto-reverts deployment if\naccuracy drops below baseline", bg_color='#451a03', border_color='#ef4444')

    # -------------------------------------------------------------------------
    # Connecting Arrows
    # -------------------------------------------------------------------------
    arrow_s1 = dict(arrowstyle="->,head_width=0.4,head_length=0.6", color='#38bdf8', lw=2.5)
    arrow_s2 = dict(arrowstyle="->,head_width=0.4,head_length=0.6", color='#818cf8', lw=2.5)
    arrow_s3 = dict(arrowstyle="->,head_width=0.4,head_length=0.6", color='#10b981', lw=2.5)

    ax.annotate("", xy=(4.8, 5.0), xytext=(4.4, 5.0), arrowprops=arrow_s1)
    ax.annotate("", xy=(9.0, 5.0), xytext=(8.6, 5.0), arrowprops=arrow_s2)
    ax.annotate("", xy=(13.6, 5.0), xytext=(13.2, 5.0), arrowprops=arrow_s3)

    # Limits and Output
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 10.5)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig('agent_evaluation_architecture.png', dpi=300, facecolor='#090e17', bbox_inches='tight')
    print("✅ High-Resolution Agent Evaluation Architecture PNG generated successfully!")

if __name__ == "__main__":
    draw_agent_evaluation_architecture()
