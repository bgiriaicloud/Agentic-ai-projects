"""
Google Cloud Official Best Practice Architecture Diagram: Agent Evaluation
Adheres strictly to Google Cloud Design System (GCP Palette, Roboto/Google Sans typography, clean white canvas)
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_gcp_agent_evaluation():
    # 16:9 Standard widescreen presentation ratio
    fig, ax = plt.subplots(figsize=(18, 10.5), dpi=300)
    
    # Official GCP Clean Background
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')

    # -------------------------------------------------------------------------
    # GCP Official Header
    # -------------------------------------------------------------------------
    # Google Cloud Sparkle / Logo Accent
    sparkle = patches.Polygon([
        [1.2, 9.8], [1.32, 9.68], [1.44, 9.8], [1.32, 9.92]
    ], closed=True, facecolor='#4285F4', edgecolor='none')
    ax.add_patch(sparkle)

    ax.text(1.6, 9.8, "Google Cloud", color='#5f6368', fontsize=18, fontweight='500', va='center')
    ax.text(4.2, 9.8, "|  Agent Evaluation Architecture Blueprint", color='#202124', fontsize=18, fontweight='bold', va='center')
    ax.text(1.6, 9.4, "Continuous Automated Quality Gates, LLM-as-a-Judge Evaluation & Vertex AI Monitoring", color='#5f6368', fontsize=10, va='center')

    # Main Project Perimeter (Google Cloud Project Boundary)
    proj_box = patches.FancyBboxPatch((0.8, 0.6), 16.4, 8.5, boxstyle="round,pad=0.15,rounding_size=0.25",
                                      facecolor='#ffffff', edgecolor='#dadce0', linewidth=1.8)
    ax.add_patch(proj_box)
    ax.text(1.2, 8.8, "Google Cloud Project Perimeter", color='#5f6368', fontsize=10, fontweight='bold')

    # -------------------------------------------------------------------------
    # Helper: GCP Official Architecture Card
    # -------------------------------------------------------------------------
    def draw_gcp_card(x, y, w, h, title, desc, bg_color='#e8f0fe', border_color='#1a73e8', badge=None):
        card = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08,rounding_size=0.12",
                                      facecolor=bg_color, edgecolor=border_color, linewidth=1.4)
        ax.add_patch(card)
        ax.text(x + w/2, y + h - 0.32, title, color='#202124', fontsize=9.5, fontweight='bold', ha='center', va='center')
        ax.text(x + w/2, y + h*0.42, desc, color='#5f6368', fontsize=7.8, ha='center', va='center')
        
        if badge:
            bx = x + w - 0.35
            by = y + h - 0.22
            badge_circle = patches.Circle((bx, by), 0.16, facecolor='#1a73e8', edgecolor='none', zorder=5)
            ax.add_patch(badge_circle)
            ax.text(bx, by, badge, color='#ffffff', fontsize=6.5, fontweight='bold', ha='center', va='center', zorder=6)

    # -------------------------------------------------------------------------
    # Column 1: Test Datasets & Inputs (Storage & Analytics - Light Blue/Grey)
    # -------------------------------------------------------------------------
    col1 = patches.FancyBboxPatch((1.1, 0.9), 3.6, 7.6, boxstyle="round,pad=0.1,rounding_size=0.18",
                                 facecolor='#f8f9fa', edgecolor='#dadce0', linewidth=1.2, linestyle='--')
    ax.add_patch(col1)
    ax.text(2.9, 8.2, "1. Evaluation Datasets", color='#1a73e8', fontsize=11, fontweight='bold', ha='center')

    draw_gcp_card(1.3, 6.5, 3.2, 1.4, "Golden Benchmark Dataset", "Curated Ground-Truth QA\nComplex Domain Edge Cases", bg_color='#e8f0fe', border_color='#4285f4')
    draw_gcp_card(1.3, 4.7, 3.2, 1.4, "Synthetic User Simulation", "Multi-turn Persona Simulator\nEdge-Case Dialogue Generator", bg_color='#e8f0fe', border_color='#4285f4', badge="New")
    draw_gcp_card(1.3, 2.9, 3.2, 1.4, "Production Traffic Replay", "Anonymized Cloud Logging\nReal Customer Query Logs", bg_color='#e8f0fe', border_color='#4285f4')
    draw_gcp_card(1.3, 1.2, 3.2, 1.3, "Red-Teaming Security Set", "Adversarial Prompt Injections\nJailbreak Attack Vectors", bg_color='#fce8e6', border_color='#ea4335')

    # -------------------------------------------------------------------------
    # Column 2: Agent Under Test (AI/ML Core - Google Blue)
    # -------------------------------------------------------------------------
    col2 = patches.FancyBboxPatch((5.1, 0.9), 3.6, 7.6, boxstyle="round,pad=0.1,rounding_size=0.18",
                                 facecolor='#f8f9fa', edgecolor='#dadce0', linewidth=1.2)
    ax.add_patch(col2)
    ax.text(6.9, 8.2, "2. Agent Under Test", color='#1a73e8', fontsize=11, fontweight='bold', ha='center')

    draw_gcp_card(5.3, 6.5, 3.2, 1.4, "Gemini Agent Core", "Gemini 2.0 Flash / Pro\nMulti-turn ReAct Reasoning", bg_color='#e8f0fe', border_color='#1a73e8')
    draw_gcp_card(5.3, 4.7, 3.2, 1.4, "ADK Skills & Tools", "OpenAPI & MCP Handlers\nTool Calling Validation", bg_color='#e8f0fe', border_color='#1a73e8')
    draw_gcp_card(5.3, 2.9, 3.2, 1.4, "Vertex AI Vector Search", "HNSW Index (<50ms Latency)\nGrounding Document Chunks", bg_color='#e8f0fe', border_color='#1a73e8')
    draw_gcp_card(5.3, 1.2, 3.2, 1.3, "Cloud Trace & Logging", "Captures Thoughts, Tool Calls\nLatency & Token Costs", bg_color='#e8f0fe', border_color='#1a73e8')

    # -------------------------------------------------------------------------
    # Column 3: Evaluation Engine (LLM Judge - Google Green)
    # -------------------------------------------------------------------------
    col3 = patches.FancyBboxPatch((9.1, 0.9), 3.8, 7.6, boxstyle="round,pad=0.1,rounding_size=0.18",
                                 facecolor='#f8f9fa', edgecolor='#dadce0', linewidth=1.2)
    ax.add_patch(col3)
    ax.text(11.0, 8.2, "3. LLM-as-a-Judge Engine", color='#137333', fontsize=11, fontweight='bold', ha='center')

    draw_gcp_card(9.3, 6.7, 3.4, 1.2, "Groundedness / Faithfulness", "100% supported by retrieved facts\nZero Hallucination Tolerance", bg_color='#e6f4ea', border_color='#34a853')
    draw_gcp_card(9.3, 5.3, 3.4, 1.2, "Answer Relevance", "Directly resolves original objective\nScored on 1 - 5 point scale", bg_color='#e6f4ea', border_color='#34a853')
    draw_gcp_card(9.3, 3.9, 3.4, 1.2, "Tool Selection Accuracy", "Valid tool choice & schema-valid\nJSON parameter arguments", bg_color='#e6f4ea', border_color='#34a853')
    draw_gcp_card(9.3, 2.5, 3.4, 1.2, "Safety & Policy Alignment", "Model Armor compliance\nZero toxic output & PII leaks", bg_color='#e6f4ea', border_color='#34a853')
    draw_gcp_card(9.3, 1.2, 3.4, 1.1, "Latency & Cost Efficiency", "p95/p99 latency & token budget", bg_color='#e6f4ea', border_color='#34a853')

    # -------------------------------------------------------------------------
    # Column 4: CI/CD Quality Gates & Monitoring (Google Yellow / Amber)
    # -------------------------------------------------------------------------
    col4 = patches.FancyBboxPatch((13.3, 0.9), 3.6, 7.6, boxstyle="round,pad=0.1,rounding_size=0.18",
                                 facecolor='#f8f9fa', edgecolor='#dadce0', linewidth=1.2, linestyle='--')
    ax.add_patch(col4)
    ax.text(15.1, 8.2, "4. Quality Gates & CI/CD", color='#b06000', fontsize=11, fontweight='bold', ha='center')

    draw_gcp_card(13.5, 6.5, 3.2, 1.4, "Cloud Build CI/CD Gate", "Automated regression tests\nPass: Score >= 4.5/5.0", bg_color='#fef7e0', border_color='#f9ab00')
    draw_gcp_card(13.5, 4.7, 3.2, 1.4, "Vertex Model Monitoring", "Real-time prompt drift detection\nProduction accuracy monitoring", bg_color='#fef7e0', border_color='#f9ab00')
    draw_gcp_card(13.5, 2.9, 3.2, 1.4, "Looker Studio Dashboard", "Executive accuracy analytics\nPer-agent latency trends", bg_color='#fef7e0', border_color='#f9ab00')
    draw_gcp_card(13.5, 1.2, 3.2, 1.3, "Automated Rollback Hook", "Auto-reverts canary deploy if\naccuracy falls below baseline", bg_color='#fce8e6', border_color='#ea4335')

    # -------------------------------------------------------------------------
    # Connecting Arrows (Google Grey with standard GCP arrowhead)
    # -------------------------------------------------------------------------
    arrow_style = dict(arrowstyle="->,head_width=0.35,head_length=0.5", color='#5f6368', lw=2.0)
    ax.annotate("", xy=(5.1, 4.7), xytext=(4.7, 4.7), arrowprops=arrow_style)
    ax.annotate("", xy=(9.1, 4.7), xytext=(8.7, 4.7), arrowprops=arrow_style)
    ax.annotate("", xy=(13.3, 4.7), xytext=(12.9, 4.7), arrowprops=arrow_style)

    # Output
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 10.5)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig('agent_evaluation_architecture.png', dpi=300, facecolor='#ffffff', bbox_inches='tight')
    print("✅ Official GCP Best Practice Agent Evaluation Architecture PNG generated successfully!")

if __name__ == "__main__":
    draw_gcp_agent_evaluation()
