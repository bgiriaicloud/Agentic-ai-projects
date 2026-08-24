"""
Futuristic Glassmorphic / Cyberpunk Architecture Blueprint Generator for Gemini Enterprise Agent Platform
Renders high-end holographic dark-themed project structure with native vector graphic icons.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def draw_futuristic_structure():
    fig, ax = plt.subplots(figsize=(16, 16), dpi=300)
    
    # -------------------------------------------------------------------------
    # 1. Dark Tech/Sci-Fi Canvas Background
    # -------------------------------------------------------------------------
    bg_color = '#060a12'
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    # Outer Ambient Cyan Glow Background Box
    ambient_glow = patches.FancyBboxPatch((0.5, 0.5), 15.0, 15.0, boxstyle="round,pad=0.3,rounding_size=0.6",
                                         facecolor='#091322', edgecolor='#00f2fe', linewidth=2.5, alpha=0.95)
    ax.add_patch(ambient_glow)

    # Subtle Circuit Grid Lines in Background
    for y in np.arange(1.5, 14.5, 1.2):
        ax.plot([1.0, 15.0], [y, y], color='#00f2fe', alpha=0.04, linewidth=0.8)
    for x in np.arange(1.5, 15.0, 1.2):
        ax.plot([x, x], [1.0, 15.0], color='#00f2fe', alpha=0.04, linewidth=0.8)

    # Mini Sci-Fi HUD Radar / Telemetry Widgets in background
    hud_circle = patches.Circle((13.5, 11.5), 0.9, facecolor='none', edgecolor='#00f2fe', linewidth=1.0, alpha=0.3)
    ax.add_patch(hud_circle)
    hud_inner = patches.Circle((13.5, 11.5), 0.45, facecolor='none', edgecolor='#00f2fe', linewidth=0.6, alpha=0.25, linestyle='--')
    ax.add_patch(hud_inner)
    ax.plot([12.3, 14.7], [11.5, 11.5], color='#00f2fe', alpha=0.2, linewidth=0.8)
    ax.plot([13.5, 13.5], [10.3, 12.7], color='#00f2fe', alpha=0.2, linewidth=0.8)

    # Mini Telemetry Waveform Bars
    for i, bar_h in enumerate([0.2, 0.4, 0.7, 0.9, 0.6, 0.8, 1.1, 0.5, 0.3]):
        ax.plot([12.8 + i*0.16, 12.8 + i*0.16], [4.5, 4.5 + bar_h*0.6], color='#00f2fe', alpha=0.35, linewidth=2.5)

    # -------------------------------------------------------------------------
    # 2. Header & Title Block
    # -------------------------------------------------------------------------
    ax.text(1.2, 14.4, "GEMINI ENTERPRISE AGENT PLATFORM: PROJECT STRUCTURE", 
            color='#ffffff', fontsize=17, fontweight='bold', fontfamily='sans-serif')
    ax.text(1.2, 13.9, "FILE & FOLDER DIRECTORY TREE • GOOGLE CLOUD VERTEX AI MULTI-AGENT ARCHITECTURE", 
            color='#38bdf8', fontsize=9.5, fontweight='500', fontfamily='sans-serif')

    # -------------------------------------------------------------------------
    # 3. Native Vector Icon Helpers
    # -------------------------------------------------------------------------
    def draw_vector_folder(ix, iy, size=0.22, color='#00f2fe'):
        # Folder Tab + Body
        tab = patches.Polygon([[ix, iy+size*0.4], [ix+size*0.4, iy+size*0.4], [ix+size*0.6, iy+size*0.7], [ix+size*1.1, iy+size*0.7], [ix+size*1.1, iy]], closed=True, facecolor=color, edgecolor='none')
        body = patches.FancyBboxPatch((ix, iy - size*0.5), size*1.2, size*0.9, boxstyle="round,pad=0.02,rounding_size=0.04", facecolor=color, edgecolor='none')
        ax.add_patch(tab)
        ax.add_patch(body)

    def draw_vector_py_badge(ix, iy, size=0.18):
        # Python dual color badge
        top_hook = patches.FancyBboxPatch((ix-size*0.5, iy), size, size*0.6, boxstyle="round,pad=0.02", facecolor='#38bdf8', edgecolor='none')
        bot_hook = patches.FancyBboxPatch((ix-size*0.5, iy-size*0.6), size, size*0.6, boxstyle="round,pad=0.02", facecolor='#f59e0b', edgecolor='none')
        ax.add_patch(top_hook)
        ax.add_patch(bot_hook)

    def draw_vector_file_icon(ix, iy, size=0.22, color='#38bdf8'):
        doc = patches.FancyBboxPatch((ix-size*0.4, iy-size*0.5), size*0.8, size*1.0, boxstyle="round,pad=0.02,rounding_size=0.04", facecolor='none', edgecolor=color, linewidth=1.2)
        ax.add_patch(doc)
        # horizontal lines
        ax.plot([ix-size*0.25, ix+size*0.25], [iy+size*0.2, iy+size*0.2], color=color, lw=1.0)
        ax.plot([ix-size*0.25, ix+size*0.25], [iy, iy], color=color, lw=1.0)
        ax.plot([ix-size*0.25, ix+size*0.1], [iy-size*0.2, iy-size*0.2], color=color, lw=1.0)

    # Helper: Glass Box
    def draw_glass_box(x, y, w, h, title, is_root=False, is_folder=True):
        # Outer Glow Layer
        glow = patches.FancyBboxPatch((x-0.03, y-0.03), w+0.06, h+0.06, 
                                     boxstyle="round,pad=0.08,rounding_size=0.2",
                                     facecolor='none', edgecolor='#00f2fe', linewidth=2.2 if is_root else 1.2, alpha=0.7)
        ax.add_patch(glow)

        # Card Body (Dark Translucent Glass)
        fill_color = '#0e223d' if is_root else '#0c1a2e'
        card = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08,rounding_size=0.2",
                                     facecolor=fill_color, edgecolor='#38bdf8', linewidth=1.2, alpha=0.92)
        ax.add_patch(card)

        # Draw Icon
        if is_folder:
            draw_vector_folder(x + 0.25, y + h*0.5, size=0.22, color='#00f2fe')
            ax.text(x + 0.68, y + h/2, title, color='#ffffff', fontsize=10 if is_root else 8.8, 
                    fontweight='bold' if is_root else '500', va='center', fontfamily='sans-serif')
        else:
            draw_vector_py_badge(x + 0.35, y + h*0.5, size=0.2)
            ax.text(x + 0.65, y + h/2, title, color='#ffffff', fontsize=8.2, 
                    fontweight='500', va='center', fontfamily='sans-serif')

    # Glowing Cyan Branching Lines
    def draw_glow_line(x_pts, y_pts, has_arrow=True):
        ax.plot(x_pts, y_pts, color='#00f2fe', linewidth=3.5, alpha=0.25)
        ax.plot(x_pts, y_pts, color='#38bdf8', linewidth=1.8, alpha=0.95)
        if has_arrow:
            ax.annotate("", xy=(x_pts[-1], y_pts[-1]), xytext=(x_pts[-2], y_pts[-2]),
                        arrowprops=dict(arrowstyle="-|>,head_width=0.3,head_length=0.4", color='#00f2fe', lw=1.8))

    # -------------------------------------------------------------------------
    # 4. Root Node: gemini-agent-platform/
    # -------------------------------------------------------------------------
    root_x, root_y, root_w, root_h = 5.6, 11.5, 4.8, 1.1
    draw_glass_box(root_x, root_y, root_w, root_h, "gemini-agent-platform/", is_root=True, is_folder=True)

    # -------------------------------------------------------------------------
    # 5. Middle Tier: 4 Key Module Folders
    # -------------------------------------------------------------------------
    folders = [
        ("agents/", 1.2, 9.2, 2.9, 0.9),
        ("mcp_servers/", 4.7, 9.2, 3.1, 0.9),
        ("tools_and_rag/", 8.2, 9.2, 3.2, 0.9),
        ("evals_and_ci/", 11.8, 9.2, 3.0, 0.9),
    ]

    root_mid_x = root_x + root_w/2
    root_bottom_y = root_y - 0.05
    bus_y = 10.5

    draw_glow_line([root_mid_x, root_mid_x], [root_bottom_y, bus_y], has_arrow=False)
    draw_glow_line([2.65, 13.3], [bus_y, bus_y], has_arrow=False)

    for title, fx, fy, fw, fh in folders:
        f_mid_x = fx + fw/2
        draw_glow_line([f_mid_x, f_mid_x], [bus_y, fy + fh + 0.05], has_arrow=True)
        draw_glass_box(fx, fy, fw, fh, title, is_root=False, is_folder=True)

    # -------------------------------------------------------------------------
    # 6. Child Python Microservices & Handlers
    # -------------------------------------------------------------------------
    # Column 1 Children (agents/)
    draw_glow_line([1.7, 1.7, 2.0], [9.2, 7.8, 7.8], has_arrow=True)
    draw_glass_box(2.0, 7.3, 2.8, 0.75, "supervisor_agent.py", is_folder=False)

    draw_glow_line([1.7, 1.7, 2.0], [7.8, 6.3, 6.3], has_arrow=True)
    draw_glass_box(2.0, 5.8, 2.8, 0.75, "worker_agents.py", is_folder=False)

    # Column 2 Children (mcp_servers/)
    draw_glow_line([6.25, 6.25], [9.2, 7.6], has_arrow=True)
    draw_glass_box(4.8, 6.8, 2.9, 0.75, "mcp_gcp_server.py", is_folder=False)

    # Column 3 Children (tools_and_rag/)
    draw_glow_line([9.8, 9.8], [9.2, 7.6], has_arrow=True)
    draw_glass_box(8.3, 6.8, 2.9, 0.75, "vector_search_rag.py", is_folder=False)

    # Column 4 Children (evals_and_ci/)
    draw_glow_line([13.3, 13.3], [9.2, 7.6], has_arrow=True)
    draw_glass_box(11.8, 6.8, 2.9, 0.75, "llm_judge_eval.py", is_folder=False)

    # -------------------------------------------------------------------------
    # 7. Bottom Row: Root Configuration & Deployment Files
    # -------------------------------------------------------------------------
    bottom_files = [
        ("config.yaml", 1.2, False),
        ("cloudbuild.yaml", 3.2, False),
        ("Dockerfile", 5.2, False),
        ("main.py", 7.2, True),
        ("README.md", 9.2, False),
        ("requirements.txt", 11.2, False),
        ("setup.py", 13.2, True),
    ]

    bottom_bus_y = 3.6
    draw_glow_line([root_mid_x, root_mid_x], [bus_y, bottom_bus_y], has_arrow=False)
    draw_glow_line([2.0, 14.0], [bottom_bus_y, bottom_bus_y], has_arrow=False)

    for fname, bx, is_py in bottom_files:
        fx_mid = bx + 0.8
        draw_glow_line([fx_mid, fx_mid], [bottom_bus_y, 2.5], has_arrow=True)
        
        fcard = patches.FancyBboxPatch((bx, 1.45), 1.6, 1.05, boxstyle="round,pad=0.06,rounding_size=0.15",
                                      facecolor='#091426', edgecolor='#38bdf8', linewidth=1.1, alpha=0.9)
        ax.add_patch(fcard)
        
        if is_py:
            draw_vector_py_badge(bx + 0.8, 2.05, size=0.22)
        else:
            draw_vector_file_icon(bx + 0.8, 2.05, size=0.25, color='#00f2fe')
            
        ax.text(bx + 0.8, 1.62, fname, color='#e2e8f0', fontsize=6.8, fontweight='500', ha='center', va='center')

    # -------------------------------------------------------------------------
    # 8. Render & Save High-Resolution Image
    # -------------------------------------------------------------------------
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 16)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig('gemini_enterprise_futuristic_project_structure.png', dpi=300, facecolor=bg_color, bbox_inches='tight')
    print("✅ High-Resolution Futuristic Architecture Structure PNG rendered with zero font warnings!")

if __name__ == "__main__":
    draw_futuristic_structure()
