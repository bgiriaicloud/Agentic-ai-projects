"""
===============================================================================
HIGH-RESOLUTION PNG DIAGRAM RENDERER (MATPLOTLIB + PIL)
===============================================================================
Renders crisp PNG image files:
1. ai_circular_roadmap_diagram.png
2. ai_hierarchy_pyramid_diagram.png
===============================================================================
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Set dark theme style
plt.style.use('dark_background')

# -----------------------------------------------------------------------------
# 1. RENDER 360° CIRCULAR ROADMAP PNG
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 12), facecolor='#0b0f19')
ax.set_facecolor('#0b0f19')

# Center Hub
center_circle = plt.Circle((0, 0), 0.28, color='#1e293b', ec='#f59e0b', lw=3)
ax.add_patch(center_circle)
ax.text(0, 0.08, "2026 ROADMAP", color='#f59e0b', fontsize=12, fontweight='bold', ha='center', va='center')
ax.text(0, 0.0, "AGENTIC AI", color='#ffffff', fontsize=18, fontweight='bold', ha='center', va='center')
ax.text(0, -0.07, "CORE HUB", color='#fbbf24', fontsize=11, fontweight='bold', ha='center', va='center')
ax.text(0, -0.14, "Autonomy & Tools", color='#94a3b8', fontsize=9, ha='center', va='center')

nodes = [
    ("01", "AI & ML Fundamentals", "Supervised, Unsupervised, RL", "#3b82f6", "FOUNDATION"),
    ("02", "Feature Engineering", "Scaling, Encoding, Feature Stores", "#06b6d4", "DATA PIPELINE"),
    ("03", "Deep Learning & Transformers", "Neural Nets, Self-Attention", "#8b5cf6", "ARCHITECTURE"),
    ("04", "Generative AI & LLMs", "Gemini 2.0, LoRA, Quantization", "#ec4899", "MODELS"),
    ("05", "RAG Architecture", "Hybrid Search, HNSW, BM25", "#10b981", "RETRIEVAL"),
    ("06", "Agentic AI & AI Agents", "Brain, Memory, Planning, Tools", "#f59e0b", "AUTONOMY"),
    ("07", "Loop & Harness Eng.", "ReAct, HITL, LLM-as-a-Judge", "#ef4444", "CONTROL & TEST"),
    ("08", "MCP & A2A Protocols", "JSON-RPC, stdio/SSE, Swarms", "#6366f1", "PROTOCOLS"),
]

r_wheel = 0.75
num_nodes = len(nodes)

# Outer dashed wheel circle
wheel_circle = plt.Circle((0, 0), r_wheel, fill=False, color='white', alpha=0.2, ls='--', lw=1.5)
ax.add_patch(wheel_circle)

for i, (num, title, sub, color, badge) in enumerate(nodes):
    angle_deg = (i * (360 / num_nodes)) - 90
    angle_rad = np.radians(angle_deg)
    
    nx = r_wheel * np.cos(angle_rad)
    ny = r_wheel * np.sin(angle_rad)
    
    # Connection line
    ax.plot([0, nx], [0, ny], color=color, alpha=0.4, lw=2)
    
    # Node Circle
    node_circle = plt.Circle((nx, ny), 0.1, color='#1e293b', ec=color, lw=2.5)
    ax.add_patch(node_circle)
    ax.text(nx, ny + 0.02, num, color=color, fontsize=12, fontweight='bold', ha='center', va='center')
    ax.text(nx, ny - 0.03, badge, color='#ffffff', fontsize=6, fontweight='bold', ha='center', va='center')
    
    # Text Placement
    tx = (r_wheel + 0.22) * np.cos(angle_rad)
    ty = (r_wheel + 0.22) * np.sin(angle_rad)
    
    ha = 'center'
    if tx > 0.1: ha = 'left'
    elif tx < -0.1: ha = 'right'
    
    ax.text(tx, ty + 0.02, title, color=color, fontsize=11, fontweight='bold', ha=ha, va='center')
    ax.text(tx, ty - 0.03, sub, color='#94a3b8', fontsize=8, ha=ha, va='center')

ax.set_xlim(-1.25, 1.25)
ax.set_ylim(-1.25, 1.25)
ax.set_aspect('equal')
ax.axis('off')

plt.title("AI & AGENTIC AI 360° CIRCULAR ROADMAP", color='#ffffff', fontsize=16, fontweight='bold', pad=20)
plt.savefig("ai_circular_roadmap_diagram.png", dpi=200, bbox_inches='tight', facecolor='#0b0f19')
plt.close()


# -----------------------------------------------------------------------------
# 2. RENDER CONCENTRIC CIRCLES & PYRAMID PNG
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(14, 8), facecolor='#0b0f19')
ax.set_facecolor('#0b0f19')

# Left Side: Concentric Rings
circle_specs = [
    (0.85, "#3b82f6", "1. AI"),
    (0.68, "#06b6d4", "2. ML & Feature Eng."),
    (0.51, "#8b5cf6", "3. Deep Learning"),
    (0.34, "#ec4899", "4. GenAI"),
    (0.17, "#f59e0b", "5. Agentic AI"),
]

cx_c = -0.55
for r, color, label in circle_specs:
    c = plt.Circle((cx_c, 0), r, fill=False, color=color, lw=3)
    ax.add_patch(c)
    ax.text(cx_c, r - 0.06, label, color=color, fontsize=10, fontweight='bold', ha='center', va='center')

# Inner Core Glow
core_c = plt.Circle((cx_c, 0), 0.16, color='#1e293b', ec='#f59e0b', lw=2)
ax.add_patch(core_c)
ax.text(cx_c, 0, "AGENTIC AI\nCORE", color='#fbbf24', fontsize=9, fontweight='bold', ha='center', va='center')

# Right Side: Detailed Cards
cards_data = [
    ("1. ARTIFICIAL INTELLIGENCE (AI)", "Simulating human cognitive intelligence.", "Symbolic Logic, Expert Systems, Rules.", "#3b82f6", 0.75),
    ("2. MACHINE LEARNING & FEATURE ENG.", "Learning patterns directly from data.", "Supervised/Unsupervised/RL, Scaling, Feature Store.", "#06b6d4", 0.40),
    ("3. DEEP LEARNING (DL)", "Multi-layer Neural Networks extracting features.", "Transformers, Self-Attention, Backpropagation.", "#8b5cf6", 0.05),
    ("4. GENERATIVE AI (GenAI)", "Foundation models generating text, code, images.", "LLMs (Gemini/GPT-4o), LoRA/PEFT, Quantization.", "#ec4899", -0.30),
    ("5. AGENTIC AI (AUTONOMOUS CORE)", "Goal-directed autonomous agents executing tools.", "ReAct Loop, HITL, Test Harness, MCP, A2A Tools.", "#f59e0b", -0.65),
]

for title, desc, detail, color, y_pos in cards_data:
    rect = patches.FancyBboxPatch((0.2, y_pos - 0.12), 0.75, 0.22, boxstyle="round,pad=0.03", fc='#1e293b', ec=color, lw=1.5)
    ax.add_patch(rect)
    ax.text(0.25, y_pos + 0.04, title, color=color, fontsize=11, fontweight='bold', va='center')
    ax.text(0.25, y_pos - 0.02, desc, color='#e2e8f0', fontsize=9, va='center')
    ax.text(0.25, y_pos - 0.07, detail, color='#94a3b8', fontsize=8, va='center')

ax.set_xlim(-1.5, 1.05)
ax.set_ylim(-1.0, 1.0)
ax.axis('off')

plt.title("THE HIERARCHY OF ARTIFICIAL INTELLIGENCE (2026 ROADMAP)", color='#ffffff', fontsize=16, fontweight='bold', pad=20)
plt.savefig("ai_hierarchy_pyramid_diagram.png", dpi=200, bbox_inches='tight', facecolor='#0b0f19')
plt.close()

print("✅ High-Resolution PNG Diagrams Rendered Successfully!")
