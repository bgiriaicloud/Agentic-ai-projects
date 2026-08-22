"""
===============================================================================
AI 360° CIRCULAR ROADMAP SVG STUDY INFOGRAPHIC GENERATOR
===============================================================================
Renders a modern, high-resolution circular wheel roadmap SVG image for:
"AI & AGENTIC AI 360° STUDY ROADMAP (2026 EDITION)"
===============================================================================
"""

import math

# Radial positions for 8 nodes around a center (cx=500, cy=500, r=320)
cx, cy, r_wheel = 500, 500, 310

nodes_data = [
    {
        "num": "01",
        "title": "AI & ML Fundamentals",
        "sub": "Supervised, Unsupervised, RL",
        "color": "#3b82f6",
        "badge": "FOUNDATION"
    },
    {
        "num": "02",
        "title": "Feature Engineering",
        "sub": "Scaling, Encoding, Feature Stores",
        "color": "#06b6d4",
        "badge": "DATA PIPELINE"
    },
    {
        "num": "03",
        "title": "Deep Learning & Transformers",
        "sub": "Neural Nets, Self-Attention",
        "color": "#8b5cf6",
        "badge": "ARCHITECTURE"
    },
    {
        "num": "04",
        "title": "Generative AI & LLMs",
        "sub": "Gemini 2.0, LoRA, Quantization",
        "color": "#ec4899",
        "badge": "MODELS"
    },
    {
        "num": "05",
        "title": "RAG Architecture",
        "sub": "Hybrid Search, HNSW, BM25",
        "color": "#10b981",
        "badge": "RETRIEVAL"
    },
    {
        "num": "06",
        "title": "Agentic AI & AI Agents",
        "sub": "Brain, Memory, Planning, Tools",
        "color": "#f59e0b",
        "badge": "AUTONOMY"
    },
    {
        "num": "07",
        "title": "Loop & Harness Eng.",
        "sub": "ReAct, HITL, LLM-as-a-Judge",
        "color": "#ef4444",
        "badge": "CONTROL & TEST"
    },
    {
        "num": "08",
        "title": "MCP & A2A Tool Protocols",
        "sub": "JSON-RPC, stdio/SSE, Swarms",
        "color": "#6366f1",
        "badge": "PROTOCOLS"
    }
]

svg_lines = []
svg_lines.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="100%" height="100%">')
svg_lines.append('  <defs>')
svg_lines.append('    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">')
svg_lines.append('      <stop offset="0%" stop-color="#0b0f19" />')
svg_lines.append('      <stop offset="50%" stop-color="#111827" />')
svg_lines.append('      <stop offset="100%" stop-color="#070a12" />')
svg_lines.append('    </linearGradient>')
svg_lines.append('    <filter id="glowCenter" x="-20%" y="-20%" width="140%" height="140%">')
svg_lines.append('      <feGaussianBlur stdDeviation="12" result="blur" />')
svg_lines.append('      <feComposite in="SourceGraphic" in2="blur" operator="over" />')
svg_lines.append('    </filter>')
svg_lines.append('  </defs>')

# Canvas
svg_lines.append('  <rect width="1000" height="1000" fill="url(#bgGrad)" />')

# Header
svg_lines.append('  <text x="500" y="55" font-family="sans-serif" font-size="24" font-weight="800" fill="#ffffff" text-anchor="middle" letter-spacing="1.5">AI &amp; AGENTIC AI 360° CIRCULAR ROADMAP</text>')
svg_lines.append('  <text x="500" y="82" font-family="sans-serif" font-size="13" fill="#94a3b8" text-anchor="middle">Master Study Wheel: From Machine Learning &amp; Feature Engineering to RAG, Agentic Loops &amp; MCP Protocols</text>')

# Outer Wheel Ring
svg_lines.append(f'  <circle cx="{cx}" cy="{cy}" r="{r_wheel}" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="2" stroke-dasharray="6,6" />')

# Render 8 Radial Spikes & Nodes
num_nodes = len(nodes_data)
for i, node in enumerate(nodes_data):
    angle_deg = (i * (360 / num_nodes)) - 90
    angle_rad = math.radians(angle_deg)
    
    nx = cx + r_wheel * math.cos(angle_rad)
    ny = cy + r_wheel * math.sin(angle_rad)
    
    # Connection line from center
    svg_lines.append(f'  <line x1="{cx}" y1="{cy}" x2="{nx}" y2="{ny}" stroke="{node["color"]}" stroke-width="2" opacity="0.4" />')

    # Radial Circle Node
    svg_lines.append(f'  <circle cx="{nx}" cy="{ny}" r="48" fill="#1e293b" stroke="{node["color"]}" stroke-width="3" />')
    svg_lines.append(f'  <text x="{nx}" y="{ny - 5}" font-family="sans-serif" font-size="16" font-weight="bold" fill="{node["color"]}" text-anchor="middle">{node["num"]}</text>')
    svg_lines.append(f'  <text x="{nx}" y="{ny + 15}" font-family="sans-serif" font-size="9" font-weight="700" fill="#ffffff" text-anchor="middle">{node["badge"]}</text>')

    # Label Text Card positioning
    text_offset_r = r_wheel + 95
    tx = cx + text_offset_r * math.cos(angle_rad)
    ty = cy + text_offset_r * math.sin(angle_rad)
    
    text_anchor = "middle"
    if tx > cx + 50: text_anchor = "start"
    elif tx < cx - 50: text_anchor = "end"

    svg_lines.append(f'  <text x="{tx}" y="{ty - 8}" font-family="sans-serif" font-size="13" font-weight="bold" fill="{node["color"]}" text-anchor="{text_anchor}">{node["title"]}</text>')
    svg_lines.append(f'  <text x="{tx}" y="{ty + 10}" font-family="sans-serif" font-size="10" fill="#94a3b8" text-anchor="{text_anchor}">{node["sub"]}</text>')

# Center Hub (Agentic AI Core)
svg_lines.append(f'  <circle cx="{cx}" cy="{cy}" r="90" fill="#1e293b" stroke="#f59e0b" stroke-width="4" filter="url(#glowCenter)" />')
svg_lines.append(f'  <circle cx="{cx}" cy="{cy}" r="82" fill="#0f172a" stroke="#fbbf24" stroke-width="1.5" />')

svg_lines.append(f'  <text x="{cx}" y="{cy - 22}" font-family="sans-serif" font-size="13" font-weight="bold" fill="#f59e0b" text-anchor="middle">2026 ROADMAP</text>')
svg_lines.append(f'  <text x="{cx}" y="{cy + 2}" font-family="sans-serif" font-size="16" font-weight="800" fill="#ffffff" text-anchor="middle">AGENTIC AI</text>')
svg_lines.append(f'  <text x="{cx}" y="{cy + 22}" font-family="sans-serif" font-size="11" font-weight="600" fill="#fbbf24" text-anchor="middle">CORE HUB</text>')
svg_lines.append(f'  <text x="{cx}" y="{cy + 40}" font-family="sans-serif" font-size="9" fill="#94a3b8" text-anchor="middle">Autonomy &amp; Tools</text>')

# Footer
svg_lines.append('  <text x="500" y="975" font-family="sans-serif" font-size="11" fill="#64748b" text-anchor="middle">Antigravity AI Engineering Reference Guide • 360° Study Wheel</text>')
svg_lines.append('</svg>')

final_svg = "\n".join(svg_lines)

with open("ai_circular_roadmap_diagram.svg", "w", encoding="utf-8") as f:
    f.write(final_svg)

print("✅ High-Resolution AI 360° Circular Roadmap SVG Infographic Generated Successfully!")
