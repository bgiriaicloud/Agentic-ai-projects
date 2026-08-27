"""
Generates pixel-perfect visual node canvas diagram matching the user's Agent Builder canvas screenshot
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def draw_canvas_tree():
    fig, ax = plt.subplots(figsize=(20, 9), dpi=300)
    
    # Background Canvas: Clean Light Theme with subtle dot grid
    fig.patch.set_facecolor('#f8fafc')
    ax.set_facecolor('#f8fafc')

    # Draw light dotted grid pattern
    for x in np.arange(0, 20, 0.4):
        for y in np.arange(0, 9, 0.4):
            ax.plot(x, y, 'o', color='#e2e8f0', markersize=1.2, alpha=0.7)

    # -------------------------------------------------------------------------
    # Helper to draw a modern Agent Node Card
    # -------------------------------------------------------------------------
    def draw_agent_card(x, y, width, height, title, desc, is_root=False):
        # Drop shadow
        shadow = patches.FancyBboxPatch((x + 0.04, y - 0.04), width, height, 
                                        boxstyle="round,pad=0.08,rounding_size=0.15", 
                                        facecolor='#000000', alpha=0.04, edgecolor='none')
        ax.add_patch(shadow)

        # Card Body (White)
        card_body = patches.FancyBboxPatch((x, y), width, height, 
                                           boxstyle="round,pad=0.08,rounding_size=0.15", 
                                           facecolor='#ffffff', edgecolor='#cbd5e1', linewidth=1.2)
        ax.add_patch(card_body)

        # Header Bar
        header_color = '#bfdbfe' if is_root else '#f3e8ff'  # Soft Blue for Root, Soft Lavender for Children
        header_border = '#93c5fd' if is_root else '#e9d5ff'
        header_h = height * 0.38
        header_y = y + height - header_h
        
        header_rect = patches.FancyBboxPatch((x, header_y), width, header_h, 
                                             boxstyle="round,pad=0.06,rounding_size=0.12", 
                                             facecolor=header_color, edgecolor=header_border, linewidth=0.8)
        ax.add_patch(header_rect)

        # Header Text (Title with sparkle icon)
        title_color = '#1e3a8a' if is_root else '#581c87'
        ax.text(x + 0.12, header_y + header_h * 0.5, f"✦ {title}", 
                color=title_color, fontsize=9.5 if is_root else 8.5, fontweight='bold', va='center')

        # Description Body Text
        ax.text(x + 0.12, y + height * 0.38, desc, 
                color='#475569', fontsize=7.2, va='top', wrap=True)

        # Google / GCP Logo Simulation Badge at bottom left
        circle_bg = patches.Circle((x + 0.22, y + 0.18), 0.09, facecolor='#ffffff', edgecolor='#e2e8f0', linewidth=0.5)
        ax.add_patch(circle_bg)
        ax.text(x + 0.22, y + 0.18, "G", color='#4285F4', fontsize=6.5, fontweight='bold', ha='center', va='center')

    # -------------------------------------------------------------------------
    # Draw Root Node: Hospital AI Assistant
    # -------------------------------------------------------------------------
    root_w, root_h = 3.2, 1.8
    root_x, root_y = 10.0 - (root_w / 2), 6.0
    draw_agent_card(root_x, root_y, root_w, root_h, 
                    "Hospital AI Assistant", 
                    "Agent to help interact with my\ndata.", 
                    is_root=True)

    # -------------------------------------------------------------------------
    # Draw 7 Domain Child Nodes
    # -------------------------------------------------------------------------
    children = [
        ("Patient", "Agent that handles a specific task", 0.6),
        ("lab test", "Lab test related answers can be\ngiven from here", 3.3),
        ("hospital admin", "manages hospital admin related\ntasks", 6.0),
        ("Doctor", "Doctor details are here", 8.7),
        ("Insurance", "All about insurance can be\nsupported", 11.4),
        ("Nursing", "Nursing will communicate with\ndoctor and patients", 14.1),
        ("IT-admin-ai-agent", "Play the IT Admin role", 16.8),
    ]

    child_w, child_h = 2.4, 1.6
    child_y = 1.8

    root_bottom_x = 10.0
    root_bottom_y = root_y

    for title, desc, cx in children:
        # Draw Child Card
        draw_agent_card(cx, child_y, child_w, child_h, title, desc, is_root=False)

        # Draw Connector Arc / Spline
        child_top_x = cx + (child_w / 2)
        child_top_y = child_y + child_h + 0.08

        # Draw smooth dotted bezier curve connecting Root to Child
        # Mid-control point
        ctrl_y = (root_bottom_y + child_top_y) / 2
        
        # Plot curve using quadratic bezier interpolation
        t_vals = np.linspace(0, 1, 40)
        curve_x = (1 - t_vals)**2 * root_bottom_x + 2 * (1 - t_vals) * t_vals * ((root_bottom_x + child_top_x) / 2) + t_vals**2 * child_top_x
        curve_y = (1 - t_vals)**2 * root_bottom_y + 2 * (1 - t_vals) * t_vals * ctrl_y + t_vals**2 * child_top_y

        ax.plot(curve_x, curve_y, color='#94a3b8', linestyle='--', linewidth=1.2, alpha=0.85)

        # Small anchor dot at child top
        ax.plot(child_top_x, child_top_y, 'o', color='#cbd5e1', markersize=3.5)

    # Small anchor dot at root bottom
    ax.plot(root_bottom_x, root_bottom_y, 'o', color='#93c5fd', markersize=4.5)

    # Limits and formatting
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 9)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig('hospital_ai_assistant_agent_tree_canvas.png', dpi=300, facecolor='#f8fafc', bbox_inches='tight')
    print("✅ Visual Agent Tree Canvas Diagram rendered successfully!")

if __name__ == "__main__":
    draw_canvas_tree()
