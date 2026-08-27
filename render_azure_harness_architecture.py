"""
Ultra-High-Resolution Architecture Diagram Generator:
Azure Harness Architecture & Lifecycle for Agentic AI
Renders a 16:9 ultra-HD (5400x3000 px) dark-themed infographic with glassmorphism cards and neon accents.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def render_diagram():
    fig, ax = plt.subplots(figsize=(18, 10.125), dpi=300)
    
    # -------------------------------------------------------------------------
    # 1. Canvas & Background Grid
    # -------------------------------------------------------------------------
    bg_color = '#070c18'
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 10.125)
    ax.axis('off')

    # Subtle ambient background container with rounded border
    main_frame = patches.FancyBboxPatch(
        (0.4, 0.4), 17.2, 9.325,
        boxstyle="round,pad=0.1,rounding_size=0.3",
        facecolor='#0a1224',
        edgecolor='#0078d4',
        linewidth=2.0,
        alpha=0.9
    )
    ax.add_patch(main_frame)

    # Ambient grid lines
    for x in np.arange(1.0, 17.5, 1.0):
        ax.plot([x, x], [0.8, 9.4], color='#0078d4', alpha=0.03, linewidth=0.8)
    for y in np.arange(1.0, 9.5, 1.0):
        ax.plot([0.8, 17.2], [y, y], color='#0078d4', alpha=0.03, linewidth=0.8)

    # -------------------------------------------------------------------------
    # 2. Header & Title Block
    # -------------------------------------------------------------------------
    # Azure Cloud Logo Accent (4 squares)
    logo_x, logo_y = 0.9, 9.1
    ax.add_patch(patches.Rectangle((logo_x, logo_y), 0.16, 0.16, facecolor='#f25022', edgecolor='none'))
    ax.add_patch(patches.Rectangle((logo_x+0.2, logo_y), 0.16, 0.16, facecolor='#7fba00', edgecolor='none'))
    ax.add_patch(patches.Rectangle((logo_x, logo_y-0.2), 0.16, 0.16, facecolor='#00a4ef', edgecolor='none'))
    ax.add_patch(patches.Rectangle((logo_x+0.2, logo_y-0.2), 0.16, 0.16, facecolor='#ffb900', edgecolor='none'))

    ax.text(1.4, 9.15, "AZURE HARNESS ARCHITECTURE & LIFECYCLE", 
            color='#ffffff', fontsize=16, fontweight='bold', fontfamily='sans-serif')
    ax.text(1.4, 8.85, "ENTERPRISE AGENT PRODUCTION FRAMEWORK: SAFETY GUARDRAILS • SANDBOXED ACA SESSIONS • CIRCUIT BREAKERS • AI STUDIO EVALS", 
            color='#38bdf8', fontsize=8.5, fontweight='600', fontfamily='sans-serif')

    # Top Status Badges
    def draw_badge(bx, by, text, color):
        badge = patches.FancyBboxPatch((bx, by), 1.8, 0.4, boxstyle="round,pad=0.05,rounding_size=0.1",
                                      facecolor='#0f203c', edgecolor=color, linewidth=1.2)
        ax.add_patch(badge)
        ax.text(bx+0.9, by+0.2, text, color=color, fontsize=7.5, fontweight='bold', ha='center', va='center')

    draw_badge(11.8, 8.85, "AZURE AI STUDIO", "#00f2fe")
    draw_badge(13.8, 8.85, "ACA DYNAMIC SESSIONS", "#10b981")
    draw_badge(15.8, 8.85, "OPENTELEMETRY TRACING", "#a855f7")

    # -------------------------------------------------------------------------
    # 3. Main Stage Columns (5 Stages of Azure Harness Lifecycle)
    # -------------------------------------------------------------------------
    col_w = 3.0
    col_h = 6.2
    y_start = 2.1

    columns_data = [
        {
            "num": "STAGE 01",
            "title": "INPUT GUARDRAILS",
            "subtitle": "Azure AI Content Safety & Shields",
            "x": 0.8,
            "color": "#00f2fe",
            "items": [
                ("Azure Prompt Shield", "Blocks direct injection & jailbreak prompts"),
                ("Harmful Category Filter", "Toxicity, hate, self-harm & violence scoring (0-7)"),
                ("Indirect Injection Shield", "Sanitizes external data & document payloads"),
                ("Schema & Grammar Gate", "Enforces structured JSON/regex intent validation")
            ]
        },
        {
            "num": "STAGE 02",
            "title": "CIRCUIT BREAKERS",
            "subtitle": "Deterministic Runtime Controls",
            "x": 4.1,
            "color": "#f59e0b",
            "items": [
                ("Max Step Limiter", "Stops non-terminating reasoning & retry loops"),
                ("Token Budget Ledger", "Hard dollar/token quota per agent session"),
                ("Consecutive Error Breaker", "Halts execution upon repeated tool failures"),
                ("Session Timeout Guard", "Terminates hung async network operations")
            ]
        },
        {
            "num": "STAGE 03",
            "title": "AGENT & SANDBOX",
            "subtitle": "Azure OpenAI + ACA Sessions",
            "x": 7.4,
            "color": "#10b981",
            "items": [
                ("Azure OpenAI GPT-4o", "Core cognitive reasoning & function calling"),
                ("ACA Dynamic Sessions", "Hyper-V / MicroVM ephemeral Python sandbox"),
                ("Zero Host Access Policy", "Prevents unauthorized OS & filesystem calls"),
                ("State Checkpointing", "Deterministic replay & rollback snapshots")
            ]
        },
        {
            "num": "STAGE 04",
            "title": "OUTPUT GUARDRAILS",
            "subtitle": "Groundedness & Compliance",
            "x": 10.7,
            "color": "#ec4899",
            "items": [
                ("Azure Groundedness Verifier", "Detects hallucinations against source docs"),
                ("PII & Secrets Redaction", "Filters SSN, credit cards & API keys"),
                ("Policy Safety Filter", "Ensures compliance with enterprise policies"),
                ("Human-in-the-Loop (HITL)", "Approval gates for critical writes / transactions")
            ]
        },
        {
            "num": "STAGE 05",
            "title": "EVALS & TELEMETRY",
            "subtitle": "Azure Monitor & AI Studio Evals",
            "x": 14.0,
            "color": "#a855f7",
            "items": [
                ("OpenTelemetry Tracing", "Full trajectory spans in Application Insights"),
                ("Studio Relevance Eval", "LLM-as-a-judge scoring intent alignment"),
                ("Trajectory Efficiency", "Computes Pass@k and step economy metrics"),
                ("Continuous AI CI/CD", "Automated regression testing & benchmarks")
            ]
        }
    ]

    for col in columns_data:
        cx, cy = col["x"], y_start
        c_color = col["color"]
        
        # Outer Card Box
        card = patches.FancyBboxPatch(
            (cx, cy), col_w, col_h,
            boxstyle="round,pad=0.1,rounding_size=0.25",
            facecolor='#0d1b33',
            edgecolor=c_color,
            linewidth=1.6,
            alpha=0.95
        )
        ax.add_patch(card)

        # Top Accent Header Box
        header_box = patches.FancyBboxPatch(
            (cx+0.1, cy+col_h-1.0), col_w-0.2, 0.9,
            boxstyle="round,pad=0.05,rounding_size=0.15",
            facecolor='#13274a',
            edgecolor=c_color,
            linewidth=0.8
        )
        ax.add_patch(header_box)

        # Stage Number Badge
        ax.text(cx+0.25, cy+col_h-0.3, col["num"], color=c_color, fontsize=7.5, fontweight='bold')
        ax.text(cx+0.25, cy+col_h-0.55, col["title"], color='#ffffff', fontsize=10.5, fontweight='bold')
        ax.text(cx+0.25, cy+col_h-0.8, col["subtitle"], color='#94a3b8', fontsize=7.0, fontweight='500')

        # Feature Items Inside Card
        item_y = cy + col_h - 1.45
        for item_title, item_desc in col["items"]:
            item_box = patches.FancyBboxPatch(
                (cx+0.15, item_y-0.85), col_w-0.3, 0.95,
                boxstyle="round,pad=0.04,rounding_size=0.1",
                facecolor='#091322',
                edgecolor='#1e293b',
                linewidth=0.8
            )
            ax.add_patch(item_box)

            # Bullet Indicator
            ax.add_patch(patches.Circle((cx+0.35, item_y-0.25), 0.07, facecolor=c_color, edgecolor='none'))
            
            # Text
            ax.text(cx+0.52, item_y-0.25, item_title, color='#f1f5f9', fontsize=8.0, fontweight='bold', va='center')
            ax.text(cx+0.52, item_y-0.58, item_desc, color='#94a3b8', fontsize=6.5, fontweight='normal', wrap=True)
            
            item_y -= 1.15

    # -------------------------------------------------------------------------
    # 4. Connective Flow Arrows Between Stages
    # -------------------------------------------------------------------------
    arrow_positions = [3.85, 7.15, 10.45, 13.75]
    for ax_pos in arrow_positions:
        ax.annotate(
            '', xy=(ax_pos+0.2, 5.2), xytext=(ax_pos-0.05, 5.2),
            arrowprops=dict(facecolor='#38bdf8', edgecolor='#38bdf8', arrowstyle='-|>', lw=2.5, mutation_scale=16)
        )

    # -------------------------------------------------------------------------
    # 5. Bottom Architectural Paradigm Spectrum Bar
    # -------------------------------------------------------------------------
    bar_y = 0.8
    bar_box = patches.FancyBboxPatch(
        (0.8, bar_y), 16.2, 0.95,
        boxstyle="round,pad=0.08,rounding_size=0.2",
        facecolor='#0a1529',
        edgecolor='#38bdf8',
        linewidth=1.2
    )
    ax.add_patch(bar_box)

    ax.text(1.1, bar_y+0.6, "THE 4 EVOLUTIONARY PARADIGMS:", color='#ffffff', fontsize=8.5, fontweight='bold')
    ax.text(1.1, bar_y+0.25, "THE FULL SPECTRUM OF LLM SYSTEM ENGINEERING", color='#64748b', fontsize=7.0, fontweight='600')

    paradigms = [
        ("1. Prompt Engineering", "Input Optimization (Prompts / CoT)", 5.2, "#38bdf8"),
        ("2. Context Engineering", "Information & Memory (RAG / GraphRAG)", 8.2, "#818cf8"),
        ("3. Agent Engineering", "Cognition & Actions (Tools / Multi-Agent)", 11.4, "#34d399"),
        ("4. Harness Engineering", "Safety, Sandboxes & Evals (Azure Moat)", 14.6, "#f43f5e")
    ]

    for p_title, p_sub, px, p_color in paradigms:
        p_badge = patches.FancyBboxPatch((px-0.2, bar_y+0.12), 2.9, 0.7, boxstyle="round,pad=0.03,rounding_size=0.08",
                                        facecolor='#101f3d', edgecolor=p_color, linewidth=1.0)
        ax.add_patch(p_badge)
        ax.text(px+1.25, bar_y+0.52, p_title, color=p_color, fontsize=7.8, fontweight='bold', ha='center')
        ax.text(px+1.25, bar_y+0.25, p_sub, color='#94a3b8', fontsize=6.0, fontweight='500', ha='center')

    # Save High-DPI Output
    output_path = "/Users/biswanathgiri/GenAI&AgenticAI -Learing Roadmap/azure_harness_architecture.png"
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, facecolor=bg_color, edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"Diagram successfully rendered at: {output_path}")

if __name__ == "__main__":
    render_diagram()
