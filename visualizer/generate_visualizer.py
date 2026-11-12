"""
Builds the upgraded, responsive, touch-friendly Synapse 3D Brain Cortex Web Studio.
Solves all congestion, screen-size scaling, mobile/tablet orientation issues,
and introduces clean collapsible drawers, decluttered node labels, and touch orbit gestures.
"""

import json
import os

def build_full_html():
    json_path = "/home/antigravity/synapse/examples/enriched_brain_graph.json"
    with open(json_path, "r", encoding="utf-8") as f:
        graph_data = json.load(f)

    graph_data_json = json.dumps(graph_data)

    html_content = f'''<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>Synapse // 3D Neural Cortex & Project Work Visualizer</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    @keyframes pulse-glow {{
      0%, 100% {{ opacity: 0.8; transform: scale(1); }}
      50% {{ opacity: 1; transform: scale(1.04); }}
    }}
    .glow-pulse {{ animation: pulse-glow 3s infinite ease-in-out; }}
    
    /* Sleek custom scrollbars */
    ::-webkit-scrollbar {{ width: 5px; height: 5px; }}
    ::-webkit-scrollbar-track {{ background: rgba(15, 23, 42, 0.4); }}
    ::-webkit-scrollbar-thumb {{ background: rgba(56, 189, 248, 0.35); border-radius: 4px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: rgba(56, 189, 248, 0.65); }}

    /* Drawer transitions for mobile/tablet */
    .drawer-panel {{
      transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.24s ease;
    }}
    .drawer-hidden-left {{
      transform: translateX(-110%);
      opacity: 0;
      pointer-events: none;
    }}
    .drawer-hidden-right {{
      transform: translateX(110%);
      opacity: 0;
      pointer-events: none;
    }}
  </style>
</head>
<body class="bg-[#070b14] text-slate-100 font-sans antialiased overflow-hidden select-none h-screen w-screen flex flex-col touch-none">

  <!-- COMPACT TOP NAVIGATION BAR -->
  <header class="h-13 min-h-[48px] border-b border-cyan-950/70 bg-slate-950/90 backdrop-blur-md px-3 sm:px-4 flex items-center justify-between z-30 shrink-0">
    <div class="flex items-center gap-2.5 min-w-0">
      <div class="w-8 h-8 rounded-lg bg-gradient-to-tr from-cyan-500 via-indigo-600 to-rose-500 flex items-center justify-center shadow-md shadow-cyan-500/20 shrink-0">
        <span class="text-base leading-none">🧠</span>
      </div>
      <div class="min-w-0">
        <div class="flex items-center gap-1.5 flex-wrap">
          <h1 class="text-xs sm:text-sm font-extrabold tracking-wider uppercase text-cyan-400 font-mono truncate">Synapse</h1>
          <span class="text-[9px] sm:text-[10px] px-1.5 py-0.2 rounded-full bg-cyan-950/90 text-cyan-300 border border-cyan-700/60 font-mono hidden xs:inline-block">v2.6</span>
          <span class="inline-flex items-center gap-1 text-[9px] sm:text-[10px] text-emerald-400 font-mono font-medium">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping"></span>
            ACTIVE
          </span>
        </div>
        <p class="text-[10px] text-slate-400 truncate hidden sm:block">Touch & drag to orbit • Click node to dive into sub-work</p>
      </div>
    </div>

    <!-- Center Compact Metrics Telemetry (Adaptive for medium/large displays) -->
    <div class="hidden xl:flex items-center gap-5 font-mono text-xs">
      <div class="flex flex-col items-end">
        <span class="text-slate-400 text-[9px] uppercase">Memory Nodes</span>
        <span class="text-cyan-300 font-bold text-xs" id="stat-nodes">34 Units</span>
      </div>
      <div class="h-5 w-px bg-slate-800"></div>
      <div class="flex flex-col items-end">
        <span class="text-slate-400 text-[9px] uppercase">Synaptic Axons</span>
        <span class="text-rose-400 font-bold text-xs" id="stat-edges">102 Pathways</span>
      </div>
      <div class="h-5 w-px bg-slate-800"></div>
      <div class="flex flex-col items-end">
        <span class="text-slate-400 text-[9px] uppercase">Context Saved</span>
        <span class="text-emerald-400 font-bold text-xs" id="stat-efficiency">82.4% Less Tokens</span>
      </div>
      <div class="h-5 w-px bg-slate-800"></div>
      <div class="flex flex-col items-end">
        <span class="text-slate-400 text-[9px] uppercase">Recall Latency</span>
        <span class="text-amber-300 font-bold text-xs">0.59 ms</span>
      </div>
    </div>

    <!-- Header Action Controls -->
    <div class="flex items-center gap-1.5 sm:gap-2 shrink-0">
      
      <!-- Drawer Toggles for Mobile / Tablet -->
      <button id="btn-toggle-left-drawer" class="lg:hidden p-1.5 rounded-lg bg-slate-900 border border-slate-700 hover:border-cyan-500 text-cyan-300 transition flex items-center justify-center text-xs" title="Toggle Search & Missions">
        <span>🔍 Missions</span>
      </button>

      <button id="btn-toggle-right-drawer" class="p-1.5 sm:px-2 sm:py-1 rounded-lg bg-slate-900 border border-slate-700 hover:border-cyan-500 text-emerald-300 transition flex items-center gap-1 text-xs" title="Toggle Sub-Work Inspector">
        <span>⚙️</span>
        <span class="hidden sm:inline">Inspector</span>
      </button>

      <!-- Label Clean Mode Switcher -->
      <button id="btn-toggle-titles" class="px-2 py-1 text-xs rounded-lg bg-slate-900 hover:bg-slate-800 border border-cyan-500/40 text-cyan-300 transition flex items-center gap-1">
        <span class="hidden md:inline">Mode:</span>
        <strong id="title-mode-status" class="text-emerald-400 font-mono text-[10px] sm:text-xs">FUN</strong>
      </button>

      <!-- Orbit Auto-Rotate Button -->
      <button id="btn-autorotate" class="p-1.5 sm:px-2.5 sm:py-1 text-xs rounded-lg bg-slate-800/80 hover:bg-slate-700 border border-slate-700 text-slate-300 transition flex items-center gap-1">
        <svg class="w-3.5 h-3.5 text-cyan-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
        <span class="hidden sm:inline font-mono text-[10px]" id="orbit-status">ON</span>
      </button>

      <!-- Reset Cam Button -->
      <button id="btn-reset-cam" class="px-2 py-1 text-xs rounded-lg bg-slate-800/80 hover:bg-slate-700 border border-slate-700 text-slate-300 transition text-[11px]">
        Reset
      </button>
    </div>
  </header>

  <!-- MAIN CANVAS & RESPONSIVE FLOATING DRAWER CONTAINER -->
  <div class="relative flex-1 w-full h-full overflow-hidden">
    
    <!-- 3D Canvas (Covers entire screen) -->
    <canvas id="brainCanvas" class="absolute inset-0 w-full h-full cursor-grab active:cursor-grabbing"></canvas>

    <!-- LEFT DRAWER: HippoRAG Query Launcher & Brain Lobes (Adaptive drawer on tablet/phone, pinned on desktop) -->
    <aside id="left-sidebar" class="drawer-panel drawer-hidden-left lg:translate-x-0 lg:opacity-100 lg:pointer-events-auto absolute top-2 sm:top-3 left-2 sm:left-3 w-[290px] sm:w-[310px] max-h-[calc(100vh-4.5rem)] flex flex-col gap-2.5 z-20 overflow-y-auto">
      
      <!-- Query & Mission Recall Card -->
      <div class="bg-slate-950/90 backdrop-blur-md border border-cyan-900/60 rounded-xl p-3 shadow-2xl flex flex-col gap-2.5">
        <div class="flex items-center justify-between border-b border-slate-800/80 pb-1.5">
          <div class="flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-rose-500 animate-pulse"></span>
            <span class="text-[11px] font-semibold text-rose-300 tracking-wider uppercase font-mono">HippoRAG 2 Recall</span>
          </div>
          <span class="text-[9px] text-slate-400 font-mono">&lt; 1ms PPR</span>
        </div>

        <div>
          <label class="text-[10px] text-slate-400 block mb-1">Simulate Agent Mission Query:</label>
          <div class="relative">
            <input id="query-input" type="text" value="Refactor token verification & authentication" 
                   class="w-full text-xs bg-slate-900/90 border border-slate-700 rounded-lg px-2.5 py-1.5 text-cyan-200 placeholder-slate-500 focus:outline-none focus:border-cyan-400 font-mono text-[11px]">
            <button id="btn-run-query" class="absolute right-1 top-1 bottom-1 px-2 bg-gradient-to-r from-cyan-600 to-rose-600 hover:from-cyan-500 hover:to-rose-500 text-white rounded text-[9px] font-semibold tracking-wider uppercase transition flex items-center gap-1 shadow">
              <span>Fire</span>
              <svg class="w-2 h-2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
            </button>
          </div>
        </div>

        <!-- Quick Preset Mission Chips -->
        <div class="flex flex-col gap-1">
          <span class="text-[9px] text-slate-400 uppercase tracking-wide">Quick Brain Missions:</span>
          <div class="flex flex-wrap gap-1">
            <button class="preset-btn text-[9px] px-2 py-1 rounded-md bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 transition hover:border-cyan-500/50 text-left"
                    data-q="Refactor token verification & authentication">
              🔐 Token & Auth
            </button>
            <button class="preset-btn text-[9px] px-2 py-1 rounded-md bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 transition hover:border-cyan-500/50 text-left"
                    data-q="Process customer charge & database transaction">
              💳 Payment Checkout
            </button>
            <button class="preset-btn text-[9px] px-2 py-1 rounded-md bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 transition hover:border-cyan-500/50 text-left"
                    data-q="Cache session invalidate on user logout">
              ⚡ Flash Cache Invalidation
            </button>
          </div>
        </div>

        <!-- Real-Time Token Telemetry Result -->
        <div id="query-result-card" class="bg-cyan-950/40 border border-cyan-800/40 rounded-lg p-2 flex flex-col gap-1">
          <div class="flex items-center justify-between text-[10px]">
            <span class="text-slate-300 font-medium">Activated Subgraph:</span>
            <span id="qr-nodes-count" class="text-cyan-300 font-mono font-bold">8 nodes / 4 hops</span>
          </div>
          <div class="grid grid-cols-2 gap-1.5 text-[9px] font-mono">
            <div class="bg-slate-900/80 rounded p-1 border border-slate-800">
              <span class="text-slate-400 block text-[8px]">Grep Scan:</span>
              <span id="qr-raw-tok" class="text-rose-400 font-semibold">984 tok</span>
            </div>
            <div class="bg-slate-900/80 rounded p-1 border border-slate-800">
              <span class="text-slate-400 block text-[8px]">Synapse:</span>
              <span id="qr-surr-tok" class="text-emerald-400 font-semibold">213 tok</span>
            </div>
          </div>
          <div class="w-full bg-slate-900 rounded-full h-1 overflow-hidden mt-0.5">
            <div id="qr-savings-bar" class="bg-gradient-to-r from-emerald-500 to-cyan-400 h-full rounded-full transition-all duration-700" style="width: 78.4%;"></div>
          </div>
          <div class="flex justify-between items-center text-[9px] text-slate-400 font-mono">
            <span>Context Efficiency:</span>
            <span id="qr-savings-pct" class="text-emerald-300 font-bold">+78.4% Saved</span>
          </div>
        </div>

        <!-- Temporal Invalidation Simulator -->
        <div class="border-t border-slate-800/80 pt-1.5 flex flex-col gap-1">
          <div class="flex items-center justify-between text-[10px]">
            <span class="font-medium text-amber-300 flex items-center gap-1 font-mono">
              <svg class="w-3 h-3 text-amber-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
              Graphiti Temporal
            </span>
            <span id="temporal-badge" class="text-[8px] px-1 rounded bg-slate-800 text-slate-400 font-mono">STABLE</span>
          </div>
          <button id="btn-toggle-refactor" class="w-full py-1 px-1.5 rounded-md bg-amber-950/40 hover:bg-amber-900/50 border border-amber-800/50 text-amber-200 text-[10px] font-medium transition flex items-center justify-center gap-1">
            <span id="refactor-btn-text">Simulate Code Refactor</span>
          </button>
        </div>

      </div>

      <!-- Functional Lobe Legend Accordion (Compact) -->
      <details class="bg-slate-950/85 backdrop-blur-md border border-slate-800 rounded-xl p-2.5 shadow-xl text-xs group">
        <summary class="text-[10px] font-semibold text-slate-400 uppercase tracking-wider font-mono cursor-pointer select-none flex items-center justify-between">
          <span>🧠 Cortex Lobes (5)</span>
          <span class="text-slate-500 text-[9px] group-open:rotate-180 transition">&darr;</span>
        </summary>
        <div class="grid grid-cols-1 gap-1 text-[10px] pt-2">
          <div class="flex items-center justify-between p-1 rounded hover:bg-slate-900/60">
            <div class="flex items-center gap-1.5">
              <span class="w-2 h-2 rounded-full bg-[#38bdf8]"></span>
              <span class="text-slate-200">Frontal Lobe</span>
            </div>
            <span class="text-[9px] text-slate-400 font-mono">Logic & Execution</span>
          </div>
          <div class="flex items-center justify-between p-1 rounded hover:bg-slate-900/60">
            <div class="flex items-center gap-1.5">
              <span class="w-2 h-2 rounded-full bg-[#f43f5e]"></span>
              <span class="text-slate-200">Hippocampus</span>
            </div>
            <span class="text-[9px] text-slate-400 font-mono">PPR Recall Hub</span>
          </div>
          <div class="flex items-center justify-between p-1 rounded hover:bg-slate-900/60">
            <div class="flex items-center gap-1.5">
              <span class="w-2 h-2 rounded-full bg-[#eab308]"></span>
              <span class="text-slate-200">Temporal Lobe</span>
            </div>
            <span class="text-[9px] text-slate-400 font-mono">Git Diffs</span>
          </div>
          <div class="flex items-center justify-between p-1 rounded hover:bg-slate-900/60">
            <div class="flex items-center gap-1.5">
              <span class="w-2 h-2 rounded-full bg-[#a855f7]"></span>
              <span class="text-slate-200">Parietal Lobe</span>
            </div>
            <span class="text-[9px] text-slate-400 font-mono">Schemas & Contracts</span>
          </div>
          <div class="flex items-center justify-between p-1 rounded hover:bg-slate-900/60">
            <div class="flex items-center gap-1.5">
              <span class="w-2 h-2 rounded-full bg-[#10b981]"></span>
              <span class="text-slate-200">Occipital Lobe</span>
            </div>
            <span class="text-[9px] text-slate-400 font-mono">Public APIs</span>
          </div>
        </div>
      </details>

    </aside>

    <!-- RIGHT DRAWER: ENRICHED NODE INSPECTOR & SUB-LEVEL WORK DRAWER (Responsive drawer) -->
    <aside id="inspector-panel" class="drawer-panel drawer-hidden-right lg:translate-x-0 lg:opacity-100 lg:pointer-events-auto absolute top-2 sm:top-3 right-2 sm:right-3 w-[300px] sm:w-[340px] md:w-[360px] max-h-[calc(100vh-4.5rem)] bg-slate-950/92 backdrop-blur-xl border border-cyan-800/60 rounded-xl p-3 sm:p-3.5 shadow-2xl flex flex-col gap-2.5 z-20 overflow-y-auto">
      
      <!-- Persona Header Card -->
      <div class="border-b border-slate-800/80 pb-2.5 flex flex-col gap-1">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-1.5 flex-wrap">
            <span id="inspect-lobe-pill" class="text-[9px] px-1.5 py-0.5 rounded font-mono font-semibold uppercase bg-cyan-950 text-cyan-300 border border-cyan-800">
              FRONTAL
            </span>
            <span id="inspect-vibe" class="text-[9px] px-1.5 py-0.5 rounded-full font-mono bg-indigo-950 text-indigo-300 border border-indigo-800/60">
              Vigilant • Shielded
            </span>
          </div>
          
          <div class="flex items-center gap-1.5">
            <span id="inspect-active" class="text-[9px] font-mono text-emerald-400 flex items-center gap-1">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span> ONLINE
            </span>
            <button id="btn-close-inspector" class="w-5 h-5 rounded bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white flex items-center justify-center text-xs transition" title="Close Panel">
              ✕
            </button>
          </div>
        </div>

        <div>
          <h2 id="inspect-friendly-title" class="text-sm sm:text-base font-extrabold text-white tracking-wide truncate">
            🔐 Token Verifier
          </h2>
          <div class="flex items-center gap-1.5 text-[11px] truncate">
            <span id="inspect-role" class="text-cyan-400 font-semibold font-mono">Cryptographic Sentinel</span>
            <span class="text-slate-600">•</span>
            <span id="inspect-domain" class="text-slate-400 text-[10px] truncate">Security & Cyber-Defense</span>
          </div>
          <span id="inspect-technical-name" class="text-[10px] text-slate-500 font-mono block truncate mt-0.5">
            auth.jwt_handler:JWTManager.verify_token
          </span>
        </div>

        <!-- Mission Statement -->
        <div class="bg-slate-900/80 border border-slate-800/80 rounded-lg p-2 text-[11px] text-slate-300 mt-0.5">
          <span class="text-[9px] text-slate-400 font-mono uppercase tracking-wider block mb-0.5">Project Role & Mission:</span>
          <p id="inspect-mission" class="leading-relaxed">
            Guards the perimeter, issues digital passports, and verifies cryptographic tokens.
          </p>
        </div>
      </div>

      <!-- SUB-LEVEL WORK ITEMS (The deep-dive visual!) -->
      <div class="flex flex-col gap-1.5">
        <div class="flex items-center justify-between">
          <span class="text-[10px] font-bold text-white uppercase tracking-wider font-mono flex items-center gap-1">
            <span>⚙️</span> Sub-Level Work (<span id="inspect-sub-count">3</span>)
          </span>
          <span class="text-[9px] text-cyan-400 font-mono">Active Units</span>
        </div>

        <div id="inspect-sub-items-container" class="flex flex-col gap-1.5 max-h-[175px] overflow-y-auto pr-0.5">
          <!-- Populated dynamically with rich sub-cards -->
        </div>
      </div>

      <!-- Real-Time Activity Log for this node -->
      <div class="bg-slate-900/70 border border-slate-800/90 rounded-lg p-2 flex flex-col gap-1">
        <span class="text-[9px] text-slate-400 uppercase tracking-wider font-mono flex items-center gap-1">
          <span>📡</span> Node Work Activity:
        </span>
        <ul id="inspect-work-logs" class="text-[10px] font-mono text-slate-300 space-y-0.5 list-disc list-inside">
          <!-- Populated dynamically -->
        </ul>
      </div>

      <!-- Technical AST & Token Telemetry Accordion -->
      <details class="bg-slate-900/60 border border-slate-800/80 rounded-lg p-2 text-xs text-slate-400 cursor-pointer group">
        <summary class="font-mono text-[10px] text-cyan-400 font-semibold select-none flex items-center justify-between">
          <span>Raw AST Signature & Tokens</span>
          <span class="text-slate-500 text-[9px] group-open:rotate-180 transition">&darr;</span>
        </summary>
        <div class="pt-1.5 flex flex-col gap-1.5">
          <pre id="inspect-sig" class="text-[9px] bg-slate-950 border border-slate-800 rounded p-1.5 text-cyan-300 font-mono overflow-x-auto whitespace-pre-wrap">def verify_token(self, raw_token: str) -> Optional[TokenPayload]:</pre>
          <div class="grid grid-cols-2 gap-1.5 text-[9px] font-mono">
            <div>
              <span class="text-slate-500 block">Full Code:</span>
              <span id="inspect-full-tok" class="text-rose-400 font-semibold">80 tok</span>
            </div>
            <div>
              <span class="text-slate-500 block">Surrogate:</span>
              <span id="inspect-surr-tok" class="text-emerald-400 font-semibold">31 tok</span>
            </div>
          </div>
        </div>
      </details>

      <!-- Synaptic Connections Links -->
      <div class="flex flex-col gap-1">
        <span class="text-[9px] text-slate-400 uppercase tracking-wider font-mono">Synaptic Neighborhood (<span id="inspect-deg">6</span>):</span>
        <div id="inspect-neighbors" class="flex flex-col gap-1 max-h-24 overflow-y-auto pr-0.5">
          <!-- Populated dynamically -->
        </div>
      </div>

    </aside>

    <!-- FLOATING BOTTOM MINIMAL BANNER (Tucks away neatly, non-blocking) -->
    <div class="absolute bottom-2 left-1/2 -translate-x-1/2 pointer-events-none z-10 w-auto max-w-[90vw]">
      <div class="pointer-events-auto bg-slate-950/85 backdrop-blur-md border border-slate-800/80 rounded-full px-3 py-1 shadow-lg flex items-center gap-2 text-[10px] sm:text-[11px] text-slate-400">
        <span class="text-cyan-400">💡</span>
        <span class="truncate">Click/tap node to inspect sub-work • Drag to rotate • Pinch/scroll to zoom</span>
      </div>
    </div>

    <!-- Hover/Touch Tooltip -->
    <div id="tooltip" class="absolute hidden pointer-events-none z-30 bg-slate-900/95 border border-cyan-500/80 rounded-lg p-2 shadow-2xl text-xs backdrop-blur font-mono transition-opacity duration-150 max-w-[220px]">
      <div id="tt-title" class="font-bold text-cyan-300 text-[11px] truncate"></div>
      <div id="tt-sub" class="text-[9px] text-slate-400 truncate"></div>
    </div>

  </div>

  <!-- SCRIPT: 3D ENGINE & NEURAL INTERACTION -->
  <script>
    const INITIAL_GRAPH_DATA = {graph_data_json};

    // Global state
    let graphData = JSON.parse(JSON.stringify(INITIAL_GRAPH_DATA));
    let nodes = graphData.nodes;
    let edges = graphData.edges;
    let useFriendlyTitles = true;

    // Responsive Canvas & 3D Math Setup
    const canvas = document.getElementById("brainCanvas");
    const ctx = canvas.getContext("2d");

    let width = 0;
    let height = 0;
    function resizeCanvas() {{
      const container = canvas.parentElement;
      width = container.clientWidth;
      height = container.clientHeight;
      const dpr = Math.min(window.devicePixelRatio || 1, 2); // Cap at 2 for mobile battery efficiency
      canvas.width = width * dpr;
      canvas.height = height * dpr;
      ctx.resetTransform();
      ctx.scale(dpr, dpr);
    }}
    window.addEventListener("resize", resizeCanvas);
    window.addEventListener("orientationchange", () => setTimeout(resizeCanvas, 150));
    resizeCanvas();

    // 3D Camera & Rotation
    let camPitch = 0.25;
    let camYaw = -0.6;
    let camDist = width < 768 ? 440 : 340; // Auto-scale camera distance based on viewport width
    let targetDist = camDist;
    let autoRotate = true;
    let isDragging = false;
    let lastMouseX = 0;
    let lastMouseY = 0;
    let hoveredNode = null;
    let selectedNode = nodes[0] || null;

    // Anatomical Brain Wireframe Particles
    const brainParticles = [];
    const NUM_BRAIN_PARTICLES = width < 640 ? 380 : 650;
    function initBrainEnvelope() {{
      brainParticles.length = 0;
      for (let i = 0; i < NUM_BRAIN_PARTICLES; i++) {{
        const u = Math.random() * Math.PI * 2;
        const v = (Math.random() - 0.5) * Math.PI * 0.95;
        const hemisphere = Math.random() > 0.5 ? 1 : -1;

        let a = 82; // Width (X)
        let b = 65; // Height (Y)
        let c = 98; // Length (Z)

        const ripple = 1.0 + 0.08 * Math.sin(7 * u) * Math.cos(5 * v);
        let x = (a * Math.cos(v) * Math.cos(u) * ripple) * 0.5 + hemisphere * 24;
        let y = b * Math.sin(v) * ripple + 12;
        let z = c * Math.cos(v) * Math.sin(u) * ripple;

        if (Math.abs(x) < 14) y -= 8;
        if (Math.random() < 0.15) {{
          x = (Math.random() - 0.5) * 60;
          y = -35 + (Math.random() - 0.5) * 18;
          z = -55 + (Math.random() - 0.5) * 25;
        }}

        brainParticles.push({{
          x: x, y: y, z: z,
          baseAlpha: 0.12 + Math.random() * 0.25,
          size: 1.0 + Math.random() * 1.5
        }});
      }}
    }}
    initBrainEnvelope();

    // Synaptic Pulses
    const pulses = [];
    for (let i = 0; i < 35; i++) {{
      pulses.push({{
        edgeIdx: Math.floor(Math.random() * edges.length),
        progress: Math.random(),
        speed: 0.004 + Math.random() * 0.008,
        color: Math.random() > 0.5 ? "#38bdf8" : "#f43f5e"
      }});
    }}

    // HippoRAG Query State
    let activeQuerySeedIds = [];
    let activeSubgraphsNodeIds = new Set();
    let queryWaveRadius = 0;
    let isQueryWaveActive = false;

    // Node lookup maps
    let nodeMap = {{}};
    function updateNodeMap() {{
      nodeMap = {{}};
      nodes.forEach(n => {{ nodeMap[n.id] = n; }});
    }}
    updateNodeMap();

    // 3D Projection Math
    function project(x, y, z) {{
      const cosY = Math.cos(camYaw);
      const sinY = Math.sin(camYaw);
      let x1 = x * cosY - z * sinY;
      let z1 = x * sinY + z * cosY;

      const cosP = Math.cos(camPitch);
      const sinP = Math.sin(camPitch);
      let y2 = y * cosP - z1 * sinP;
      let z2 = y * sinP + z1 * cosP;

      const dist = z2 + camDist;
      if (dist <= 1) return null;

      const fov = 420;
      const scale = fov / dist;
      return {{
        x: width / 2 + x1 * scale,
        y: height / 2 - y2 * scale,
        z: z2,
        scale: scale,
        visible: dist > 10
      }};
    }}

    // Main Render Loop
    let lastTime = performance.now();
    function render(now) {{
      const dt = (now - lastTime) / 1000;
      lastTime = now;

      camDist += (targetDist - camDist) * 0.1;
      if (autoRotate && !isDragging) {{
        camYaw += 0.35 * dt;
      }}

      if (isQueryWaveActive) {{
        queryWaveRadius += 90 * dt;
        if (queryWaveRadius > 240) isQueryWaveActive = false;
      }}

      ctx.clearRect(0, 0, width, height);

      // Ambient radial gradient
      const bgGrad = ctx.createRadialGradient(width/2, height/2, 40, width/2, height/2, Math.max(width, height)*0.6);
      bgGrad.addColorStop(0, "rgba(14, 27, 49, 0.45)");
      bgGrad.addColorStop(1, "rgba(7, 11, 20, 0)");
      ctx.fillStyle = bgGrad;
      ctx.fillRect(0, 0, width, height);

      // 1. Render Anatomical Brain Envelope
      ctx.fillStyle = "rgba(56, 189, 248, 0.35)";
      brainParticles.forEach(p => {{
        const pt = project(p.x, p.y, p.z);
        if (pt && pt.visible) {{
          const alpha = p.baseAlpha * Math.min(1.5, Math.max(0.15, (pt.z + 150) / 300));
          ctx.beginPath();
          ctx.arc(pt.x, pt.y, Math.max(0.5, p.size * pt.scale), 0, Math.PI * 2);
          ctx.fillStyle = `rgba(96, 165, 250, ${{alpha * 0.7}})`;
          ctx.fill();
        }}
      }});

      // 2. Render Synaptic Axons
      ctx.lineWidth = 1.0;
      edges.forEach((e) => {{
        const src = nodeMap[e.source];
        const tgt = nodeMap[e.target];
        if (!src || !tgt) return;

        const p1 = project(src.x, src.y, src.z);
        const p2 = project(tgt.x, tgt.y, tgt.z);
        if (!p1 || !p2 || !p1.visible || !p2.visible) return;

        const isSub = activeSubgraphsNodeIds.has(e.source) && activeSubgraphsNodeIds.has(e.target);
        const isHovered = hoveredNode && (hoveredNode.id === e.source || hoveredNode.id === e.target);
        const isSel = selectedNode && (selectedNode.id === e.source || selectedNode.id === e.target);

        let strokeColor = "rgba(56, 189, 248, 0.12)";
        let lineWidth = 0.8;

        if (!e.is_active) {{
          strokeColor = "rgba(239, 68, 68, 0.4)";
          ctx.setLineDash([3, 3]);
        }} else if (isSub) {{
          strokeColor = "rgba(244, 63, 94, 0.75)";
          lineWidth = 2.0;
          ctx.setLineDash([]);
        }} else if (isHovered || isSel) {{
          strokeColor = "rgba(56, 189, 248, 0.75)";
          lineWidth = 1.6;
          ctx.setLineDash([]);
        }} else {{
          ctx.setLineDash([]);
        }}

        ctx.strokeStyle = strokeColor;
        ctx.lineWidth = lineWidth;
        ctx.beginPath();
        ctx.moveTo(p1.x, p1.y);
        ctx.lineTo(p2.x, p2.y);
        ctx.stroke();
      }});
      ctx.setLineDash([]);

      // 3. Render Synaptic Pulses
      pulses.forEach(pulse => {{
        pulse.progress += pulse.speed;
        if (pulse.progress > 1) {{
          pulse.progress = 0;
          pulse.edgeIdx = Math.floor(Math.random() * edges.length);
        }}

        const edge = edges[pulse.edgeIdx];
        if (!edge || !edge.is_active) return;
        const src = nodeMap[edge.source];
        const tgt = nodeMap[edge.target];
        if (!src || !tgt) return;

        const p1 = project(src.x, src.y, src.z);
        const p2 = project(tgt.x, tgt.y, tgt.z);
        if (!p1 || !p2) return;

        const curX = p1.x + (p2.x - p1.x) * pulse.progress;
        const curY = p1.y + (p2.y - p1.y) * pulse.progress;
        const isSub = activeSubgraphsNodeIds.has(edge.source) && activeSubgraphsNodeIds.has(edge.target);

        ctx.beginPath();
        ctx.arc(curX, curY, isSub ? 2.5 : 1.5, 0, Math.PI * 2);
        ctx.fillStyle = isSub ? "#ffffff" : pulse.color;
        ctx.shadowColor = isSub ? "#f43f5e" : pulse.color;
        ctx.shadowBlur = isSub ? 8 : 4;
        ctx.fill();
        ctx.shadowBlur = 0;
      }});

      // 4. Render Memory Nodes (Depth-Sorted)
      const projectedNodes = [];
      nodes.forEach(n => {{
        const pt = project(n.x, n.y, n.z);
        if (pt && pt.visible) {{
          projectedNodes.push({{ node: n, pt: pt }});
        }}
      }});

      projectedNodes.sort((a, b) => b.pt.z - a.pt.z);

      projectedNodes.forEach(({{ node: n, pt }}) => {{
        const isHovered = hoveredNode && hoveredNode.id === n.id;
        const isSelected = selectedNode && selectedNode.id === n.id;
        const isSeed = activeQuerySeedIds.includes(n.id);
        const isSub = activeSubgraphsNodeIds.has(n.id);

        let baseRadius = (4.0 + Math.min(n.degree, 10) * 0.45 + (n.pagerank || 10) * 0.07) * pt.scale;
        baseRadius = Math.max(3.5, Math.min(20.0, baseRadius));

        if (isHovered || isSelected || isSeed) {{
          baseRadius *= 1.35;
        }}

        let alpha = 1.0;
        if (activeSubgraphsNodeIds.size > 0 && !isSub) {{
          alpha = 0.22;
        }}

        ctx.save();
        ctx.globalAlpha = alpha;

        // Outer Glow
        const glowGrad = ctx.createRadialGradient(pt.x, pt.y, baseRadius * 0.2, pt.x, pt.y, baseRadius * 2.3);
        glowGrad.addColorStop(0, n.color);
        glowGrad.addColorStop(1, "rgba(0,0,0,0)");
        ctx.fillStyle = glowGrad;
        ctx.beginPath();
        ctx.arc(pt.x, pt.y, baseRadius * 2.3, 0, Math.PI * 2);
        ctx.fill();

        // Node Body
        ctx.beginPath();
        ctx.arc(pt.x, pt.y, baseRadius, 0, Math.PI * 2);
        ctx.fillStyle = n.is_active ? n.color : "#ef4444";
        ctx.fill();

        // Border / Selection Ring
        if (isSelected) {{
          ctx.strokeStyle = "#ffffff";
          ctx.lineWidth = 2.5;
          ctx.stroke();

          ctx.beginPath();
          ctx.arc(pt.x, pt.y, baseRadius + 5, 0, Math.PI * 2);
          ctx.strokeStyle = "rgba(56, 189, 248, 0.75)";
          ctx.lineWidth = 1.2;
          ctx.stroke();
        }} else if (isSeed) {{
          ctx.strokeStyle = "#f43f5e";
          ctx.lineWidth = 3.0;
          ctx.stroke();
        }}

        // ANTI-CONGESTION: Display text label ONLY when Selected, Hovered, Seed, or High-Centrality Hub
        const shouldShowLabel = isSelected || isHovered || isSeed || (n.degree >= 9 && pt.scale > 1.05);

        if (shouldShowLabel) {{
          const displayLabel = useFriendlyTitles ? (n.friendly_title || n.name) : n.name;
          const fontSize = Math.max(10, Math.min(13, 11 * pt.scale));
          ctx.font = `${{fontSize}}px sans-serif`;
          
          // Measure and draw clean pill background to eliminate overlapping clutter
          const textWidth = ctx.measureText(displayLabel).width;
          const pillX = pt.x + baseRadius + 4;
          const pillY = pt.y - fontSize/2 - 3;
          const pillW = textWidth + 8;
          const pillH = fontSize + 6;

          ctx.fillStyle = "rgba(10, 15, 29, 0.85)";
          ctx.strokeStyle = isSelected ? "rgba(56, 189, 248, 0.8)" : "rgba(30, 41, 59, 0.8)";
          ctx.lineWidth = 1;
          ctx.beginPath();
          ctx.roundRect(pillX, pillY, pillW, pillH, 4);
          ctx.fill();
          ctx.stroke();

          ctx.fillStyle = isSelected ? "#ffffff" : (isSeed ? "#f43f5e" : "#e2e8f0");
          ctx.fillText(displayLabel, pillX + 4, pt.y + fontSize/3);
        }}

        ctx.restore();
      }});

      requestAnimationFrame(render);
    }}
    requestAnimationFrame(render);

    // ================= TOUCH & MOUSE GESTURES (FLUID ON ALL SCREENS) =================
    function getTouchDist(t1, t2) {{
      return Math.hypot(t1.clientX - t2.clientX, t1.clientY - t2.clientY);
    }}

    let isTouching = false;
    let lastTouchX = 0, lastTouchY = 0;
    let initialPinchDist = null;
    let touchStartTime = 0;
    let totalTouchMove = 0;

    canvas.addEventListener("touchstart", e => {{
      isTouching = true;
      touchStartTime = performance.now();
      totalTouchMove = 0;

      if (e.touches.length === 1) {{
        lastTouchX = e.touches[0].clientX;
        lastTouchY = e.touches[0].clientY;
        initialPinchDist = null;
      }} else if (e.touches.length === 2) {{
        initialPinchDist = getTouchDist(e.touches[0], e.touches[1]);
      }}
    }}, {{ passive: false }});

    canvas.addEventListener("touchmove", e => {{
      e.preventDefault();
      if (!isTouching) return;

      if (e.touches.length === 1 && initialPinchDist === null) {{
        const dx = e.touches[0].clientX - lastTouchX;
        const dy = e.touches[0].clientY - lastTouchY;
        totalTouchMove += Math.hypot(dx, dy);

        camYaw += dx * 0.008;
        camPitch = Math.max(-1.4, Math.min(1.4, camPitch + dy * 0.008));
        lastTouchX = e.touches[0].clientX;
        lastTouchY = e.touches[0].clientY;
        autoRotate = false;
        document.getElementById("orbit-status").innerText = "OFF";
      }} else if (e.touches.length === 2) {{
        const currentDist = getTouchDist(e.touches[0], e.touches[1]);
        if (initialPinchDist) {{
          const delta = initialPinchDist - currentDist;
          targetDist = Math.max(120, Math.min(800, targetDist + delta * 1.2));
          totalTouchMove += Math.abs(delta);
        }}
        initialPinchDist = currentDist;
      }}
    }}, {{ passive: false }});

    canvas.addEventListener("touchend", e => {{
      const touchDuration = performance.now() - touchStartTime;

      if (e.touches.length === 0) {{
        isTouching = false;
        // Tap detected if static
        if (touchDuration < 320 && totalTouchMove < 15) {{
          const hit = hitTestNodes(lastTouchX, lastTouchY, 28);
          if (hit) {{
            selectNode(hit);
            openInspectorDrawer();
          }}
        }}
      }} else if (e.touches.length === 1) {{
        lastTouchX = e.touches[0].clientX;
        lastTouchY = e.touches[0].clientY;
        initialPinchDist = null;
      }}
    }});

    // Mouse Interaction
    canvas.addEventListener("mousedown", e => {{
      isDragging = true;
      lastMouseX = e.clientX;
      lastMouseY = e.clientY;
    }});

    window.addEventListener("mouseup", () => {{
      isDragging = false;
    }});

    window.addEventListener("mousemove", e => {{
      const rect = canvas.getBoundingClientRect();
      const mouseX = e.clientX - rect.left;
      const mouseY = e.clientY - rect.top;

      if (isDragging) {{
        const dx = e.clientX - lastMouseX;
        const dy = e.clientY - lastMouseY;
        camYaw += dx * 0.008;
        camPitch = Math.max(-1.4, Math.min(1.4, camPitch + dy * 0.008));
        lastMouseX = e.clientX;
        lastMouseY = e.clientY;
        autoRotate = false;
        document.getElementById("orbit-status").innerText = "OFF";
      }} else {{
        const found = hitTestNodes(mouseX, mouseY, 20);
        const tooltip = document.getElementById("tooltip");
        if (found) {{
          hoveredNode = found;
          canvas.style.cursor = "pointer";
          tooltip.style.left = `${{Math.min(window.innerWidth - 230, e.clientX + 14)}}px`;
          tooltip.style.top = `${{Math.min(window.innerHeight - 80, e.clientY + 14)}}px`;
          tooltip.classList.remove("hidden");
          document.getElementById("tt-title").innerText = `${{found.friendly_title || found.name}}`;
          document.getElementById("tt-sub").innerText = `${{found.friendly_role || found.symbol_type}} • ${{found.file}}`;
        }} else {{
          hoveredNode = null;
          canvas.style.cursor = isDragging ? "grabbing" : "grab";
          tooltip.classList.add("hidden");
        }}
      }}
    }});

    canvas.addEventListener("wheel", e => {{
      e.preventDefault();
      targetDist = Math.max(120, Math.min(800, targetDist + e.deltaY * 0.5));
    }}, {{ passive: false }});

    canvas.addEventListener("click", () => {{
      if (hoveredNode) {{
        selectNode(hoveredNode);
        openInspectorDrawer();
      }}
    }});

    function hitTestNodes(screenX, screenY, maxDist) {{
      for (let i = 0; i < nodes.length; i++) {{
        const n = nodes[i];
        const pt = project(n.x, n.y, n.z);
        if (pt && pt.visible) {{
          const dist = Math.hypot(screenX - pt.x, screenY - pt.y);
          if (dist < maxDist) return n;
        }}
      }}
      return null;
    }}

    // ================= RESPONSIVE DRAWER CONTROLS =================
    const leftDrawer = document.getElementById("left-sidebar");
    const rightDrawer = document.getElementById("inspector-panel");

    function toggleLeftDrawer() {{
      const isHidden = leftDrawer.classList.contains("drawer-hidden-left");
      if (isHidden) {{
        leftDrawer.classList.remove("drawer-hidden-left");
        leftDrawer.classList.add("translate-x-0", "opacity-100", "pointer-events-auto");
        // On very small screens, auto-close the other drawer
        if (window.innerWidth < 1024) closeInspectorDrawer();
      }} else {{
        leftDrawer.classList.add("drawer-hidden-left");
        leftDrawer.classList.remove("translate-x-0", "opacity-100", "pointer-events-auto");
      }}
    }}

    function openInspectorDrawer() {{
      rightDrawer.classList.remove("drawer-hidden-right");
      rightDrawer.classList.add("translate-x-0", "opacity-100", "pointer-events-auto");
      if (window.innerWidth < 1024) {{
        leftDrawer.classList.add("drawer-hidden-left");
        leftDrawer.classList.remove("translate-x-0", "opacity-100", "pointer-events-auto");
      }}
    }}

    function closeInspectorDrawer() {{
      rightDrawer.classList.add("drawer-hidden-right");
      rightDrawer.classList.remove("translate-x-0", "opacity-100", "pointer-events-auto");
    }}

    function toggleRightDrawer() {{
      if (rightDrawer.classList.contains("drawer-hidden-right")) {{
        openInspectorDrawer();
      }} else {{
        closeInspectorDrawer();
      }}
    }}

    document.getElementById("btn-toggle-left-drawer").addEventListener("click", toggleLeftDrawer);
    document.getElementById("btn-toggle-right-drawer").addEventListener("click", toggleRightDrawer);
    document.getElementById("btn-close-inspector").addEventListener("click", closeInspectorDrawer);

    // Initial drawer state setup based on viewport
    if (window.innerWidth < 1024) {{
      leftDrawer.classList.add("drawer-hidden-left");
      rightDrawer.classList.add("drawer-hidden-right");
    }}

    // POPULATE ENRICHED INSPECTOR PANEL WITH SUB-ITEMS
    function selectNode(n) {{
      selectedNode = n;

      document.getElementById("inspect-friendly-title").innerText = n.friendly_title || n.name;
      document.getElementById("inspect-role").innerText = n.friendly_role || n.type.toUpperCase();
      document.getElementById("inspect-domain").innerText = n.friendly_domain || n.file;
      document.getElementById("inspect-technical-name").innerText = n.id;
      document.getElementById("inspect-mission").innerText = n.friendly_mission || n.docstring || "Executes application logic within project mesh.";
      document.getElementById("inspect-vibe").innerText = n.friendly_vibe || "Active • Nominal";
      document.getElementById("inspect-lobe-pill").innerText = n.lobe.toUpperCase();

      document.getElementById("inspect-sig").innerText = n.signature;
      document.getElementById("inspect-full-tok").innerText = `${{n.full_tokens}} tok`;
      document.getElementById("inspect-surr-tok").innerText = `${{n.surrogate_tokens}} tok`;

      // Render Sub-Level Work Items
      const subContainer = document.getElementById("inspect-sub-items-container");
      subContainer.innerHTML = "";
      const subItems = n.sub_items || [
        {{ "title": "Execution Core", "type": "AST Unit", "status": "Ready", "icon": "⚙️", "desc": "Handles core function invocation." }},
        {{ "title": "Interface Contract", "type": "Signature", "status": "Active", "icon": "📜", "desc": "Enforces typed parameters and return values." }},
        {{ "title": "Axon Connector", "type": "Edge", "status": "Linked", "icon": "🔗", "desc": "Maintains call graph connection to peers." }}
      ];
      document.getElementById("inspect-sub-count").innerText = subItems.length;

      subItems.forEach((sub) => {{
        const card = document.createElement("div");
        card.className = "bg-slate-900/90 border border-slate-800 hover:border-cyan-500/50 rounded-lg p-2 flex flex-col gap-0.5 transition shadow-sm";
        card.innerHTML = `
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-1.5 truncate">
              <span class="text-sm shrink-0">${{sub.icon}}</span>
              <span class="font-bold text-[11px] text-white truncate">${{sub.title}}</span>
            </div>
            <span class="text-[8px] px-1.5 py-0.2 rounded bg-cyan-950 text-cyan-300 border border-cyan-800/80 font-mono shrink-0">${{sub.status}}</span>
          </div>
          <p class="text-[10px] text-slate-400 pl-5 leading-snug">${{sub.desc}}</p>
          <div class="flex justify-between items-center text-[8px] text-slate-500 font-mono pl-5 pt-0.5">
            <span>Type: ${{sub.type}}</span>
            <span class="text-emerald-400">● HEALTHY</span>
          </div>
        `;
        subContainer.appendChild(card);
      }});

      // Render Node Work Logs
      const logsContainer = document.getElementById("inspect-work-logs");
      logsContainer.innerHTML = "";
      const logs = n.work_logs || [
        "Parsed via Zero-LLM AST programmatic pipeline",
        "Assigned to biological brain lobe coordinates",
        "Personalized PageRank diffusion ready"
      ];
      logs.forEach(log => {{
        const li = document.createElement("li");
        li.innerText = log;
        logsContainer.appendChild(li);
      }});

      // Render Connected Neighbors
      const neighborsDiv = document.getElementById("inspect-neighbors");
      neighborsDiv.innerHTML = "";
      const connectedEdges = edges.filter(e => e.source === n.id || e.target === n.id);
      document.getElementById("inspect-deg").innerText = connectedEdges.length;

      connectedEdges.forEach(e => {{
        const otherId = e.source === n.id ? e.target : e.source;
        const other = nodeMap[otherId];
        if (other) {{
          const item = document.createElement("button");
          item.className = "text-left text-[10px] p-1.5 rounded-lg bg-slate-900/90 hover:bg-slate-800 border border-slate-800 flex items-center justify-between text-slate-300 font-mono transition";
          item.innerHTML = `
            <div class="flex items-center gap-1.5 truncate">
              <span class="w-1.5 h-1.5 rounded-full shrink-0" style="background:${{other.color}}"></span>
              <span class="truncate">${{other.friendly_title || other.name}}</span>
            </div>
            <span class="text-[8px] text-slate-500 uppercase shrink-0">${{e.type}}</span>
          `;
          item.onclick = () => selectNode(other);
          neighborsDiv.appendChild(item);
        }}
      }});
    }}

    if (selectedNode) selectNode(selectedNode);

    // Toggle Fun/Friendly vs Technical Titles
    document.getElementById("btn-toggle-titles").addEventListener("click", () => {{
      useFriendlyTitles = !useFriendlyTitles;
      const status = document.getElementById("title-mode-status");
      status.innerText = useFriendlyTitles ? "FUN" : "AST";
      status.className = useFriendlyTitles ? "text-emerald-400 font-mono text-[10px] sm:text-xs" : "text-cyan-400 font-mono text-[10px] sm:text-xs";
    }});

    // HippoRAG Query Launcher
    function runHippoRAG(query) {{
      const qLower = query.toLowerCase();
      const qTokens = qLower.split(/\\s+|_|\\./).filter(t => t.length > 2);

      const seedScores = [];
      nodes.forEach(n => {{
        if (!n.is_active) return;
        let score = 0;
        const nameLower = (n.friendly_title + " " + n.name).toLowerCase();
        if (nameLower.includes(qLower) || qLower.includes(nameLower)) score += 5.0;
        qTokens.forEach(tok => {{
          if (nameLower.includes(tok)) score += 2.0;
          if (n.signature.toLowerCase().includes(tok)) score += 1.0;
          if (n.docstring && n.docstring.toLowerCase().includes(tok)) score += 0.8;
        }});
        if (score > 0) {{
          seedScores.push({{ node: n, score: score }});
        }}
      }});

      seedScores.sort((a, b) => b.score - a.score);
      const seeds = seedScores.slice(0, 3).map(s => s.node);
      if (seeds.length === 0 && nodes.length > 0) seeds.push(nodes[0]);

      activeQuerySeedIds = seeds.map(s => s.id);

      // Personalized PageRank (30 iterations)
      const N = nodes.length;
      const alpha = 0.85;
      let p = new Array(N).fill(1 / N);
      const teleport = new Array(N).fill(0);
      
      const seedIndices = seeds.map(s => nodes.indexOf(s));
      seedIndices.forEach(idx => {{
        teleport[idx] = 1.0 / seedIndices.length;
      }});

      const outDegrees = new Array(N).fill(0);
      const adj = Array.from({{ length: N }}, () => []);
      edges.forEach(e => {{
        if (!e.is_active) return;
        const u = nodes.findIndex(n => n.id === e.source);
        const v = nodes.findIndex(n => n.id === e.target);
        if (u !== -1 && v !== -1) {{
          adj[u].push(v);
          outDegrees[u]++;
          adj[v].push(u);
          outDegrees[v]++;
        }}
      }});

      for (let iter = 0; iter < 30; iter++) {{
        const nextP = teleport.map(t => (1 - alpha) * t);
        for (let u = 0; u < N; u++) {{
          if (outDegrees[u] > 0) {{
            const share = (alpha * p[u]) / outDegrees[u];
            adj[u].forEach(v => {{ nextP[v] += share; }});
          }} else {{
            for (let v = 0; v < N; v++) nextP[v] += (alpha * p[u]) / N;
          }}
        }}
        p = nextP;
      }}

      const ranked = nodes.map((n, i) => ({{ node: n, score: p[i] }}));
      ranked.sort((a, b) => b.score - a.score);

      const topNodes = ranked.slice(0, 9).map(r => r.node);
      activeSubgraphsNodeIds = new Set(topNodes.map(n => n.id));
      activeQuerySeedIds.forEach(id => activeSubgraphsNodeIds.add(id));

      isQueryWaveActive = true;
      queryWaveRadius = 0;

      const fullTokens = topNodes.reduce((acc, n) => acc + (n.full_tokens || 80), 0);
      const surrTokens = topNodes.reduce((acc, n) => acc + (n.surrogate_tokens || 20), 0);
      const savings = Math.round((1 - surrTokens / Math.max(1, fullTokens)) * 100);

      document.getElementById("qr-nodes-count").innerText = `${{activeSubgraphsNodeIds.size}} nodes / 4 hops`;
      document.getElementById("qr-raw-tok").innerText = `${{fullTokens}} tokens`;
      document.getElementById("qr-surr-tok").innerText = `${{surrTokens}} tokens`;
      document.getElementById("qr-savings-bar").style.width = `${{savings}}%`;
      document.getElementById("qr-savings-pct").innerText = `+${{savings}}% Saved`;

      if (seeds.length > 0) selectNode(seeds[0]);
    }}

    document.getElementById("btn-run-query").addEventListener("click", () => {{
      const q = document.getElementById("query-input").value;
      runHippoRAG(q);
    }});

    document.querySelectorAll(".preset-btn").forEach(btn => {{
      btn.addEventListener("click", () => {{
        const q = btn.getAttribute("data-q");
        document.getElementById("query-input").value = q;
        runHippoRAG(q);
      }});
    }});

    // Auto rotate toggle
    document.getElementById("btn-autorotate").addEventListener("click", () => {{
      autoRotate = !autoRotate;
      document.getElementById("orbit-status").innerText = autoRotate ? "ON" : "OFF";
    }});

    // Reset camera
    document.getElementById("btn-reset-cam").addEventListener("click", () => {{
      camPitch = 0.25;
      camYaw = -0.6;
      targetDist = width < 768 ? 440 : 340;
    }});

    setTimeout(() => {{
      runHippoRAG("Refactor token verification & authentication");
    }}, 400);

  </script>
</body>
</html>
'''
    target_path = "/home/antigravity/synapse/visualizer/index.html"
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Built visualizer at {target_path} ({len(html_content)} bytes)")

    # Also sync to artifact directory so user can open directly in IDE
    artifact_path = "/home/antigravity/.gemini/jetski/brain/v1/default/jetski_remote_agents_3p/6086e0b3-3e8c-4628-ad3f-93f16cd0d5e9/brain_memory_visualizer.html"
    with open(artifact_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Synced to artifact path {artifact_path}")

if __name__ == "__main__":
    build_full_html()
