"""
===============================================================================
NANO BANANA ARCHITECTURE DIAGRAM GENERATOR (HIGH-RES VISUAL ENGINE)
===============================================================================
Renders a publication-grade enterprise architecture diagram PNG for:
"END-TO-END AGENTIC RAG, MCP & MULTI-CLOUD EVENT PIPELINE"
===============================================================================
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Canvas Setup: 16:9 ultra-crisp resolution
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(18, 10.125), facecolor='#080c14')
ax.set_facecolor('#080c14')

# Title Banner
ax.text(0.5, 0.96, "ENTERPRISE AGENTIC RAG & MCP PLATFORM ARCHITECTURE", 
        color='#00f0ff', fontsize=18, fontweight='heavy', ha='center', va='center', fontfamily='sans-serif',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#0f172a', edgecolor='#00f0ff', lw=2))

ax.text(0.5, 0.915, "Event-Driven Ingestion • Multi-Cloud Lake • HNSW Hybrid Search • Autonomous Agent Loop • MCP Tool Server", 
        color='#94a3b8', fontsize=10, ha='center', va='center', fontfamily='sans-serif')

def draw_glass_box(ax, x, y, w, h, title, color='#3b82f6', bg='#0f172a', alpha=0.9):
    """Draws a glowing glassmorphic card container."""
    # Outer glow border
    glow = patches.FancyBboxPatch((x-0.004, y-0.004), w+0.008, h+0.008, boxstyle="round,pad=0.01",
                                  facecolor=color, alpha=0.2, zorder=1)
    ax.add_patch(glow)
    
    # Main container box
    box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.01",
                                 facecolor=bg, edgecolor=color, lw=1.8, alpha=alpha, zorder=2)
    ax.add_patch(box)
    
    # Title badge
    ax.text(x + w/2, y + h - 0.025, title, color=color, fontsize=10, fontweight='bold',
            ha='center', va='center', zorder=3, fontfamily='sans-serif')

def draw_pill(ax, x, y, w, h, text, subtext="", color='#ffffff', bg='#1e293b', border='#475569'):
    """Draws a sub-component node inside a container."""
    pill = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.006",
                                  facecolor=bg, edgecolor=border, lw=1.2, zorder=4)
    ax.add_patch(pill)
    if subtext:
        ax.text(x + w/2, y + h/2 + 0.012, text, color=color, fontsize=8.5, fontweight='bold',
                ha='center', va='center', zorder=5, fontfamily='sans-serif')
        ax.text(x + w/2, y + h/2 - 0.012, subtext, color='#94a3b8', fontsize=7,
                ha='center', va='center', zorder=5, fontfamily='sans-serif')
    else:
        ax.text(x + w/2, y + h/2, text, color=color, fontsize=8.5, fontweight='bold',
                ha='center', va='center', zorder=5, fontfamily='sans-serif')

# =============================================================================
# COLUMN 1: DATA SOURCES & INGESTION (X: 0.03 - 0.22)
# =============================================================================
draw_glass_box(ax, 0.03, 0.48, 0.18, 0.39, "1. DATA SOURCES (ANY)", color='#38bdf8')
draw_pill(ax, 0.045, 0.77, 0.15, 0.06, "SharePoint / Office 365", ".docx, .pdf, .pptx, Wikis", color='#38bdf8', border='#0284c7')
draw_pill(ax, 0.045, 0.69, 0.15, 0.06, "Azure DevOps & Git Repos", "Markdown (.md), Code, PRs", color='#60a5fa', border='#2563eb')
draw_pill(ax, 0.045, 0.61, 0.15, 0.06, "GitHub Enterprise", "Issues, Wikis, Gollum Hooks", color='#a78bfa', border='#7c3aed')
draw_pill(ax, 0.045, 0.53, 0.15, 0.06, "Cloud Storage / On-Prem", "GCS, S3, MySQL Binlog", color='#34d399', border='#059669')

draw_glass_box(ax, 0.03, 0.08, 0.18, 0.36, "2. EVENT STREAMING QUEUE", color='#f59e0b')
draw_pill(ax, 0.045, 0.34, 0.15, 0.055, "Webhook Ingress Receiver", "<100ms Instant 200 OK ACK", color='#fbbf24', border='#d97706')
draw_pill(ax, 0.045, 0.26, 0.15, 0.055, "Cloud Pub/Sub / Service Bus", "Buffer, Throttle & Deduplicate", color='#f59e0b', border='#b45309')
draw_pill(ax, 0.045, 0.18, 0.15, 0.055, "Dead-Letter Queue (DLQ)", "Failed Payload Quarantine", color='#f87171', border='#dc2626')
draw_pill(ax, 0.045, 0.10, 0.15, 0.055, "Event Grid / EventBridge", "Real-Time Object Triggers", color='#fcd34d', border='#f59e0b')

# =============================================================================
# COLUMN 2: PROCESSING, OCR & DATA LAKE (X: 0.26 - 0.46)
# =============================================================================
draw_glass_box(ax, 0.26, 0.48, 0.20, 0.39, "3. STREAM PROCESSING & OCR", color='#a855f7')
draw_pill(ax, 0.275, 0.77, 0.17, 0.06, "Dataflow / Azure Functions", "Serverless Streaming Workers", color='#c084fc', border='#9333ea')
draw_pill(ax, 0.275, 0.69, 0.17, 0.06, "Document AI / Form Parser", "Layout Model & HTML Tables", color='#e879f9', border='#c026d3')
draw_pill(ax, 0.275, 0.61, 0.17, 0.06, "GPT-4o Vision OCR", "Figure & Diagram Captioning", color='#f472b6', border='#db2777')
draw_pill(ax, 0.275, 0.53, 0.17, 0.06, "Embeddings Generator", "text-embedding-3 / 004 (3072d)", color='#a855f7', border='#7e22ce')

draw_glass_box(ax, 0.26, 0.08, 0.20, 0.36, "4. ENTERPRISE DATA LAKE", color='#10b981')
draw_pill(ax, 0.275, 0.34, 0.17, 0.055, "Bronze Container (Raw Landing)", "Immutable Raw Files & Blobs", color='#6ee7b7', border='#059669')
draw_pill(ax, 0.275, 0.26, 0.17, 0.055, "Silver Container (Curated)", "Clean Markdown & OCR Captions", color='#34d399', border='#047857')
draw_pill(ax, 0.275, 0.18, 0.17, 0.055, "Gold Container (Vector Chunks)", "Vector Payloads for Upsert", color='#10b981', border='#065f46')
draw_pill(ax, 0.275, 0.10, 0.17, 0.055, "BigQuery / Cosmos DB Store", "Analytics Lake & State Catalog", color='#a7f3d0', border='#10b981')

# =============================================================================
# COLUMN 3: VECTOR SEARCH & AGENTIC BRAIN (X: 0.51 - 0.73)
# =============================================================================
draw_glass_box(ax, 0.51, 0.48, 0.22, 0.39, "5. VECTOR SEARCH ENGINE", color='#06b6d4')
draw_pill(ax, 0.525, 0.77, 0.19, 0.06, "Dense Vector Index (HNSW)", "Sub-50ms Cosine/IP Search", color='#22d3ee', border='#0891b2')
draw_pill(ax, 0.525, 0.69, 0.19, 0.06, "Sparse Keyword Index (BM25)", "Exact SKU, Term & ID Matches", color='#38bdf8', border='#0284c7')
draw_pill(ax, 0.525, 0.61, 0.19, 0.06, "Reciprocal Rank Fusion (RRF)", "Hybrid Weighted Score Merge", color='#06b6d4', border='#0e7490')
draw_pill(ax, 0.525, 0.53, 0.19, 0.06, "L2 Semantic Cross-Reranker", "Deep Neural Relevance Scoring", color='#67e8f9', border='#06b6d4')

draw_glass_box(ax, 0.51, 0.08, 0.22, 0.36, "6. AGENTIC AI CORE (BRAIN)", color='#ec4899')
draw_pill(ax, 0.525, 0.34, 0.19, 0.055, "Foundation LLM Engine", "Gemini 2.0 Pro / GPT-4o", color='#f472b6', border='#db2777')
draw_pill(ax, 0.525, 0.26, 0.19, 0.055, "Loop Engineering (ReAct)", "Thought -> Act -> Observe Loop", color='#ec4899', border='#be185d')
draw_pill(ax, 0.525, 0.18, 0.19, 0.055, "Short & Long-Term Memory", "Context Window + Cosmos Session", color='#fb7185', border='#e11d48')
draw_pill(ax, 0.525, 0.10, 0.19, 0.055, "Guardrails & Human-in-the-Loop", "Safety Checks & Approval Hooks", color='#fda4af', border='#f43f5e')

# =============================================================================
# COLUMN 4: MCP PROTOCOL & APPLICATION UI (X: 0.77 - 0.97)
# =============================================================================
draw_glass_box(ax, 0.77, 0.48, 0.20, 0.39, "7. MODEL CONTEXT PROTOCOL", color='#fbbf24')
draw_pill(ax, 0.785, 0.77, 0.17, 0.06, "MCP Client (Host Agent)", "JSON-RPC 2.0 Protocol Engine", color='#fde047', border='#ca8a04')
draw_pill(ax, 0.785, 0.69, 0.17, 0.06, "MCP Tool Server: Database", "PostgreSQL / BigQuery Querying", color='#facc15', border='#a16207')
draw_pill(ax, 0.785, 0.61, 0.17, 0.06, "MCP Tool Server: Git / DevOps", "Code Search, PRs & Work Items", color='#fbbf24', border='#d97706')
draw_pill(ax, 0.785, 0.53, 0.17, 0.06, "A2A Tool Swarm Supervisor", "Multi-Agent Delegation Network", color='#f59e0b', border='#b45309')

draw_glass_box(ax, 0.77, 0.08, 0.20, 0.36, "8. USER APPLICATION & UI", color='#10b981')
draw_pill(ax, 0.785, 0.34, 0.17, 0.055, "FastAPI Microservice (8004)", "REST API & Streaming SSE Server", color='#6ee7b7', border='#059669')
draw_pill(ax, 0.785, 0.26, 0.17, 0.055, "Glassmorphic Web Dashboard", "Live Chat & Visual Query Console", color='#34d399', border='#047857')
draw_pill(ax, 0.785, 0.18, 0.17, 0.055, "Grounded Citations Engine", "Verifiable Links & Snippet View", color='#10b981', border='#065f46')
draw_pill(ax, 0.785, 0.10, 0.17, 0.055, "Test Harness (LLM-as-Judge)", "Automated CI/CD Benchmarking", color='#a7f3d0', border='#10b981')

# =============================================================================
# CONNECTING FLOW ARROWS & DATA HIGHWAYS
# =============================================================================
arrow_style = dict(arrowstyle="->", color='#00f0ff', lw=2.2, mutation_scale=15)
gold_arrow = dict(arrowstyle="->", color='#f59e0b', lw=2.2, mutation_scale=15)
purple_arrow = dict(arrowstyle="->", color='#a855f7', lw=2.2, mutation_scale=15)
green_arrow = dict(arrowstyle="<->", color='#10b981', lw=2.2, mutation_scale=15)

# 1. Sources -> Streaming Queue
ax.annotate("", xy=(0.12, 0.44), xytext=(0.12, 0.48), arrowprops=arrow_style)

# 2. Queue -> Processing Engine
ax.annotate("", xy=(0.26, 0.68), xytext=(0.21, 0.26),
            arrowprops=dict(arrowstyle="->", color='#f59e0b', lw=2, mutation_scale=14,
                            connectionstyle="arc3,rad=-0.2"))

# 3. Processing Engine -> Data Lake & Vector Search
ax.annotate("", xy=(0.36, 0.44), xytext=(0.36, 0.48), arrowprops=purple_arrow)
ax.annotate("", xy=(0.51, 0.68), xytext=(0.46, 0.68), arrowprops=purple_arrow)

# 4. Vector Search <-> Agentic Brain
ax.annotate("", xy=(0.62, 0.44), xytext=(0.62, 0.48), arrowprops=green_arrow)

# 5. Agentic Brain <-> MCP Tool Server
ax.annotate("", xy=(0.77, 0.68), xytext=(0.73, 0.26),
            arrowprops=dict(arrowstyle="<->", color='#fbbf24', lw=2, mutation_scale=14,
                            connectionstyle="arc3,rad=-0.2"))

# 6. Agentic Brain <-> Web Application UI
ax.annotate("", xy=(0.77, 0.26), xytext=(0.73, 0.26), arrowprops=green_arrow)

# Footer Info
ax.text(0.5, 0.03, "Nano Banana Visual Architecture Engine • Generated for Antigravity AI Roadmap • 2026 Edition",
        color='#475569', fontsize=9, ha='center', va='center', fontfamily='sans-serif')

ax.set_xlim(0, 1.0)
ax.set_ylim(0, 1.0)
ax.axis('off')

plt.tight_layout()
output_path = "nano_banana_agentic_rag_mcp_architecture.png"
plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor='#080c14')
plt.close()

print(f"✅ Nano Banana Architecture Diagram Rendered: {output_path}")
