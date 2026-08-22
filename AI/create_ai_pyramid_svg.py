"""
===============================================================================
AI PARADIGM HIERARCHY PYRAMID & CIRCULAR SVG INFOGRAPHIC GENERATOR
===============================================================================
Renders a high-resolution, modern study infographic image showing:
Artificial Intelligence -> Machine Learning -> Deep Learning -> Generative AI -> Agentic AI
===============================================================================
"""

svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800" width="100%" height="100%">
  <defs>
    <!-- Background Gradient -->
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0b0f19" />
      <stop offset="50%" stop-color="#111827" />
      <stop offset="100%" stop-color="#070a12" />
    </linearGradient>

    <!-- Concentric Ring Gradients -->
    <linearGradient id="gradAI" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#3b82f6" />
      <stop offset="100%" stop-color="#1d4ed8" />
    </linearGradient>
    <linearGradient id="gradML" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#06b6d4" />
      <stop offset="100%" stop-color="#0e7490" />
    </linearGradient>
    <linearGradient id="gradDL" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#8b5cf6" />
      <stop offset="100%" stop-color="#6d28d9" />
    </linearGradient>
    <linearGradient id="gradGenAI" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ec4899" />
      <stop offset="100%" stop-color="#be185d" />
    </linearGradient>
    <linearGradient id="gradAgentic" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f59e0b" />
      <stop offset="100%" stop-color="#d97706" />
    </linearGradient>

    <!-- Glow Filters -->
    <filter id="glowGold" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="8" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>

  <!-- Background -->
  <rect width="1200" height="800" fill="url(#bgGrad)" />

  <!-- Header -->
  <text x="600" y="50" font-family="'Inter', system-ui, sans-serif" font-size="26" font-weight="800" fill="#ffffff" text-anchor="middle" letter-spacing="1">
    THE HIERARCHY OF ARTIFICIAL INTELLIGENCE (2026 ROADMAP)
  </text>
  <text x="600" y="78" font-family="'Inter', system-ui, sans-serif" font-size="14" fill="#94a3b8" text-anchor="middle">
    Concentric &amp; Pyramid Relationship: AI ⊃ ML ⊃ Deep Learning ⊃ Generative AI ⊃ Agentic AI
  </text>

  <!-- LEFT SIDE: CONCENTRIC CIRCLE HIERARCHY -->
  <g transform="translate(300, 440)">
    <!-- Level 1: AI Circle -->
    <circle cx="0" cy="0" r="320" fill="url(#gradAI)" opacity="0.15" stroke="#3b82f6" stroke-width="2" />
    <text x="0" y="-295" font-family="sans-serif" font-size="14" font-weight="700" fill="#60a5fa" text-anchor="middle">1. ARTIFICIAL INTELLIGENCE (AI)</text>

    <!-- Level 2: ML Circle -->
    <circle cx="0" cy="20" r="255" fill="url(#gradML)" opacity="0.2" stroke="#06b6d4" stroke-width="2" />
    <text x="0" y="-210" font-family="sans-serif" font-size="14" font-weight="700" fill="#22d3ee" text-anchor="middle">2. MACHINE LEARNING (ML)</text>

    <!-- Level 3: Deep Learning Circle -->
    <circle cx="0" cy="40" r="190" fill="url(#gradDL)" opacity="0.25" stroke="#8b5cf6" stroke-width="2" />
    <text x="0" y="-125" font-family="sans-serif" font-size="14" font-weight="700" fill="#a78bfa" text-anchor="middle">3. DEEP LEARNING (DL)</text>

    <!-- Level 4: GenAI Circle -->
    <circle cx="0" cy="60" r="125" fill="url(#gradGenAI)" opacity="0.3" stroke="#ec4899" stroke-width="2" />
    <text x="0" y="-40" font-family="sans-serif" font-size="13" font-weight="700" fill="#f472b6" text-anchor="middle">4. GENERATIVE AI (GenAI)</text>

    <!-- Level 5: Agentic AI Apex Core -->
    <circle cx="0" cy="80" r="65" fill="url(#gradAgentic)" opacity="0.9" stroke="#fbbf24" stroke-width="2.5" filter="url(#glowGold)" />
    <text x="0" y="75" font-family="sans-serif" font-size="13" font-weight="800" fill="#ffffff" text-anchor="middle">5. AGENTIC AI</text>
    <text x="0" y="93" font-family="sans-serif" font-size="10" font-weight="600" fill="#1e293b" text-anchor="middle">Autonomous Core</text>
  </g>

  <!-- RIGHT SIDE: DETAILED SPECIFICATION CARDS -->
  <g transform="translate(680, 110)">
    <!-- 1. AI Card -->
    <rect x="0" y="0" width="480" height="110" rx="12" fill="#1e293b" stroke="#3b82f6" stroke-width="1.5" />
    <rect x="12" y="12" width="8" height="86" rx="4" fill="#3b82f6" />
    <text x="32" y="32" font-family="sans-serif" font-size="15" font-weight="700" fill="#60a5fa">1. ARTIFICIAL INTELLIGENCE (AI)</text>
    <text x="32" y="55" font-family="sans-serif" font-size="12" fill="#e2e8f0">Broad umbrella field: Simulating human cognitive intelligence.</text>
    <text x="32" y="78" font-family="sans-serif" font-size="11" fill="#94a3b8">Key Concepts: Symbolic Logic, Rule Engine Expert Systems, Heuristics.</text>

    <!-- 2. ML & Feature Engineering Card -->
    <rect x="0" y="125" width="480" height="120" rx="12" fill="#1e293b" stroke="#06b6d4" stroke-width="1.5" />
    <rect x="12" y="137" width="8" height="96" rx="4" fill="#06b6d4" />
    <text x="32" y="157" font-family="sans-serif" font-size="15" font-weight="700" fill="#22d3ee">2. MACHINE LEARNING &amp; FEATURE ENG.</text>
    <text x="32" y="180" font-family="sans-serif" font-size="12" fill="#e2e8f0">Learning patterns from data without explicit manual rules.</text>
    <text x="32" y="203" font-family="sans-serif" font-size="11" fill="#94a3b8">Key Concepts: Supervised/Unsupervised/RL, Scaling, One-Hot, Feature Store.</text>

    <!-- 3. Deep Learning Card -->
    <rect x="0" y="260" width="480" height="110" rx="12" fill="#1e293b" stroke="#8b5cf6" stroke-width="1.5" />
    <rect x="12" y="272" width="8" height="86" rx="4" fill="#8b5cf6" />
    <text x="32" y="292" font-family="sans-serif" font-size="15" font-weight="700" fill="#a78bfa">3. DEEP LEARNING (DL)</text>
    <text x="32" y="315" font-family="sans-serif" font-size="12" fill="#e2e8f0">Multi-layer Neural Networks extracting hierarchical features.</text>
    <text x="32" y="338" font-family="sans-serif" font-size="11" fill="#94a3b8">Key Concepts: Transformers, Self-Attention, CNNs, Backpropagation.</text>

    <!-- 4. Generative AI Card -->
    <rect x="0" y="385" width="480" height="110" rx="12" fill="#1e293b" stroke="#ec4899" stroke-width="1.5" />
    <rect x="12" y="397" width="8" height="86" rx="4" fill="#ec4899" />
    <text x="32" y="417" font-family="sans-serif" font-size="15" font-weight="700" fill="#f472b6">4. GENERATIVE AI (GenAI)</text>
    <text x="32" y="440" font-family="sans-serif" font-size="12" fill="#e2e8f0">Foundation models creating new text, code, images, &amp; audio.</text>
    <text x="32" y="463" font-family="sans-serif" font-size="11" fill="#94a3b8">Key Concepts: LLMs (Gemini/GPT-4o), LoRA/PEFT, Quantization.</text>

    <!-- 5. Agentic AI Apex Card -->
    <rect x="0" y="510" width="480" height="145" rx="12" fill="#1e293b" stroke="#f59e0b" stroke-width="2" filter="url(#glowGold)" />
    <rect x="12" y="522" width="8" height="121" rx="4" fill="#f59e0b" />
    <text x="32" y="542" font-family="sans-serif" font-size="16" font-weight="800" fill="#fbbf24">5. AGENTIC AI (AUTONOMOUS CORE)</text>
    <text x="32" y="565" font-family="sans-serif" font-size="12" font-weight="600" fill="#ffffff">Goal-directed autonomous agents executing multi-step tools.</text>
    <text x="32" y="590" font-family="sans-serif" font-size="11" fill="#fbbf24">• Loop Engineering (ReAct, Plan-Execute-Reflect, HITL)</text>
    <text x="32" y="608" font-family="sans-serif" font-size="11" fill="#fbbf24">• Test Harness Engineering (LLM-as-a-Judge, Mocks)</text>
    <text x="32" y="626" font-family="sans-serif" font-size="11" fill="#fbbf24">• Protocols: RAG, MCP Client-Server, A2A Tool Swarms</text>
  </g>

  <!-- Footnote -->
  <text x="600" y="775" font-family="sans-serif" font-size="11" fill="#64748b" text-anchor="middle">
    Antigravity AI Engineering Reference Guide • 2026 Edition
  </text>
</svg>
"""

with open("ai_hierarchy_pyramid_diagram.svg", "w", encoding="utf-8") as f:
    f.write(svg_content)

print("✅ High-Resolution AI Hierarchy Concentric & Pyramid SVG Diagram Generated Successfully!")
