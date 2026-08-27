"""
Pixel-perfect replication of Google Gemini Enterprise Agent Platform Architecture
Tiers: Build, Scale, Govern, Optimize
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_gemini_platform():
    # Set wide aspect ratio
    fig, ax = plt.subplots(figsize=(18, 10.5), dpi=300)
    
    # Clean background
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')

    # -------------------------------------------------------------------------
    # Helper: Draw Diamond/Sparkle Icon
    # -------------------------------------------------------------------------
    def draw_sparkle(center_x, center_y, size=0.25):
        sparkle = patches.Polygon([
            [center_x, center_y + size],
            [center_x + size*0.4, center_y + size*0.25],
            [center_x + size, center_y],
            [center_x + size*0.4, center_y - size*0.25],
            [center_x, center_y - size],
            [center_x - size*0.4, center_y - size*0.25],
            [center_x - size, center_y],
            [center_x - size*0.4, center_y + size*0.25],
        ], closed=True, facecolor='#2563eb', edgecolor='none')
        ax.add_patch(sparkle)

    # -------------------------------------------------------------------------
    # Draw Header Title
    # -------------------------------------------------------------------------
    draw_sparkle(4.6, 9.8, size=0.22)
    ax.text(5.0, 9.8, "Gemini Enterprise", color='#202124', fontsize=26, fontweight='bold', va='center', fontfamily='sans-serif')
    ax.text(10.6, 9.8, "Agent Platform", color='#5f6368', fontsize=26, fontweight='normal', va='center', fontfamily='sans-serif')

    # -------------------------------------------------------------------------
    # Main Container Box
    # -------------------------------------------------------------------------
    main_box = patches.FancyBboxPatch((0.8, 0.5), 16.4, 8.8, boxstyle="round,pad=0.15,rounding_size=0.35",
                                      facecolor='#ffffff', edgecolor='#2563eb', linewidth=4.0)
    ax.add_patch(main_box)

    # Helper: Badge (New / GA)
    def draw_badge(bx, by, text="New"):
        badge = patches.Circle((bx, by), 0.18, facecolor='#1a73e8', edgecolor='none', zorder=5)
        ax.add_patch(badge)
        ax.text(bx, by, text, color='#ffffff', fontsize=7.5, fontweight='bold', ha='center', va='center', zorder=6)

    # Helper: Pill Block
    def draw_pill(px, py, pw, ph, text, badge=None, fontsize=9.0):
        pill = patches.FancyBboxPatch((px, py), pw, ph, boxstyle="round,pad=0.06,rounding_size=0.12",
                                      facecolor='#e8f0fe', edgecolor='#d2e3fc', linewidth=1.0)
        ax.add_patch(pill)
        ax.text(px + pw/2, py + ph/2, text, color='#202124', fontsize=fontsize, fontweight='500', 
                ha='center', va='center', fontfamily='sans-serif')
        if badge:
            draw_badge(px + pw - 0.05, py + ph - 0.05, text=badge)

    # Horizontal Divider Line
    def draw_divider(y_pos):
        ax.plot([0.8, 17.2], [y_pos, y_pos], color='#2563eb', linewidth=2.5)

    # -------------------------------------------------------------------------
    # 1. BUILD SECTION (y: 5.7 to 9.3)
    # -------------------------------------------------------------------------
    ax.text(9.0, 9.0, "Build", color='#202124', fontsize=15, fontweight='bold', ha='center', va='center')

    # Top Row in Build:
    draw_pill(1.8, 8.35, 2.6, 0.45, "Agent Development Kit", badge="New", fontsize=8.5)
    draw_pill(4.8, 8.35, 2.6, 0.45, "3P agent frameworks", fontsize=8.5)
    draw_pill(9.8, 8.35, 2.6, 0.45, "Agent Studio", badge="New", fontsize=8.5)
    draw_pill(12.8, 8.35, 2.6, 0.45, "Agent Garden", fontsize=8.5)

    # Sub-headers
    ax.text(4.6, 7.85, "Gemini API and Model Garden", color='#0284c7', fontsize=10.5, fontweight='bold', ha='center')
    ax.text(12.6, 7.85, "Tools, data, and other agents", color='#0284c7', fontsize=10.5, fontweight='bold', ha='center')

    # Left Column Grid (Model Garden)
    draw_pill(1.8, 7.15, 2.6, 0.45, "Gemini models", fontsize=8.5)
    draw_pill(4.8, 7.15, 2.6, 0.45, "3P and open models", fontsize=8.5)
    draw_pill(1.8, 6.55, 2.6, 0.45, "Model training", fontsize=8.5)
    draw_pill(4.8, 6.55, 2.6, 0.45, "Model inference", fontsize=8.5)

    # Right Column Grid (Tools, data, and other agents)
    draw_pill(9.2, 7.15, 1.8, 0.42, "A2A", fontsize=8.5)
    draw_pill(11.3, 7.15, 1.8, 0.42, "Grounding", fontsize=8.5)
    draw_pill(13.4, 7.15, 1.8, 0.42, "RAG", fontsize=8.5)

    draw_pill(9.2, 6.55, 1.8, 0.42, "MCP", fontsize=8.5)
    draw_pill(11.3, 6.55, 1.8, 0.42, "Search", fontsize=8.5)
    draw_pill(13.4, 6.55, 2.2, 0.42, "APIs and connectors", fontsize=8.0)

    draw_pill(9.2, 5.95, 1.8, 0.42, "A2UI", fontsize=8.5)
    draw_pill(11.3, 5.95, 1.8, 0.42, "AP2 and UCP", fontsize=8.0)
    draw_pill(13.4, 5.95, 2.2, 0.42, "Cloud Marketplace", fontsize=8.0)

    draw_divider(5.7)

    # -------------------------------------------------------------------------
    # 2. SCALE SECTION (y: 4.2 to 5.7)
    # -------------------------------------------------------------------------
    ax.text(9.0, 5.4, "Scale", color='#202124', fontsize=15, fontweight='bold', ha='center', va='center')

    draw_pill(1.8, 4.6, 3.0, 0.5, "Agent Runtime", badge="GA", fontsize=9.0)
    draw_pill(5.5, 4.6, 3.0, 0.5, "Agent Sessions", badge="GA", fontsize=9.0)
    draw_pill(9.2, 4.6, 3.0, 0.5, "Agent Sandbox", badge="GA", fontsize=9.0)
    draw_pill(12.9, 4.6, 3.0, 0.5, "Agent Memory Bank", badge="GA", fontsize=9.0)

    draw_divider(4.2)

    # -------------------------------------------------------------------------
    # 3. GOVERN SECTION (y: 2.0 to 4.2)
    # -------------------------------------------------------------------------
    ax.text(9.0, 3.9, "Govern", color='#202124', fontsize=15, fontweight='bold', ha='center', va='center')

    # Row 1
    draw_pill(1.8, 3.15, 3.0, 0.5, "Agent Gateway", badge="New", fontsize=9.0)
    draw_pill(5.5, 3.15, 3.0, 0.5, "Agent Identity", badge="GA", fontsize=9.0)
    draw_pill(9.2, 3.15, 3.0, 0.5, "Agent Registry", badge="New", fontsize=9.0)
    draw_pill(12.9, 3.15, 3.3, 0.5, "Agent Anomaly Detection", badge="New", fontsize=8.5)

    # Row 2
    draw_pill(1.8, 2.4, 3.0, 0.5, "Model Armor", fontsize=9.0)
    draw_pill(5.5, 2.4, 3.0, 0.5, "Agent Policy", fontsize=9.0)
    draw_pill(9.2, 2.4, 3.0, 0.5, "Agent Security", badge="New", fontsize=9.0)
    draw_pill(12.9, 2.4, 3.3, 0.5, "Agent Compliance", fontsize=9.0)

    draw_divider(2.0)

    # -------------------------------------------------------------------------
    # 4. OPTIMIZE SECTION (y: 0.5 to 2.0)
    # -------------------------------------------------------------------------
    ax.text(9.0, 1.7, "Optimize", color='#202124', fontsize=15, fontweight='bold', ha='center', va='center')

    draw_pill(1.8, 0.9, 3.0, 0.5, "Agent Evaluation", badge="New", fontsize=9.0)
    draw_pill(5.5, 0.9, 3.0, 0.5, "Agent Simulation", badge="New", fontsize=9.0)
    draw_pill(9.2, 0.9, 3.0, 0.5, "Agent Observability", badge="New", fontsize=9.0)
    draw_pill(12.9, 0.9, 3.0, 0.5, "Agent Optimizer", badge="New", fontsize=9.0)

    # Limits and Output
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 10.5)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig('gemini_enterprise_agent_platform_architecture.png', dpi=300, facecolor='#ffffff', bbox_inches='tight')
    print("✅ High-Resolution Gemini Enterprise Agent Platform Architecture PNG generated successfully!")

if __name__ == "__main__":
    draw_gemini_platform()
