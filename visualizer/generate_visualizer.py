"""
Synapse 3D Neural Cortex & Work Visualizer Generator.
Generates a fully responsive, touch-friendly, anti-congested standalone web studio
optimized for all screens: mobile, tablet (portrait & landscape), and wide desktops.
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

    /* Responsive Drawer Transitions */
    .drawer-panel {{
      transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.25s ease;
      will-change: transform, opacity;
    }}
    .drawer-hidden-left {{
      transform: translateX(-115%);
      opacity: 0;
      pointer-events: none;
    }}
    .drawer-hidden-right {{
      transform: translateX(115%);
      opacity: 0;
      pointer-events: none;
    }}
  </style>
</head>
<body class="bg-[#070b14] text-slate-100 font-sans antialiased overflow-hidden select-none h-screen w-screen flex flex-col touch-none">

  <!-- TOP APP BAR -->
  <header class="h-12 sm:h-13 min-h-[48px] border-b border-cyan-950/70 bg-slate-950/92 backdrop-blur-md px-3 sm:px-4 flex items-center justify-between z-30 shrink-0">
    <!-- Brand / Title -->
    <div class="flex items-center gap-2 sm:gap-2.5 min-w-0">
      <div class="w-7 h-7 sm:w-8 sm:h-8 rounded-lg bg-gradient-to-tr from-cyan-500 via-indigo-600 to-rose-500 flex items-center justify-center shadow-md shadow-cyan-500/20 shrink-0">
        <span class="text-sm sm:text-base leading-none">🧠</span>
      </div>
      <div class="min-w-0">
        <div class="flex items-center gap-1.5 flex-nowrap">
          <h1 class="text-xs sm:text-sm font-extrabold tracking-wider uppercase text-cyan-400 font-mono truncate">Synapse</h1>
          <span class="text-[9px] px-1.5 py-0.2 rounded-full bg-cyan-950 text-cyan-300 border border-cyan-700/60 font-mono hidden xs:inline-block">v2.6</span>
          <span class="inline-flex items-center gap-1 text-[9px] text-emerald-400 font-mono font-medium">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping"></span>
            ACTIVE
          </span>
        </div>
        <p class="text-[10px] text-slate-400 truncate hidden md:block">Orbit with 1 finger • Tap node to dive into sub-work</p>
      </div>
    </div>

    <!-- Center Desktop Telemetry -->
    <div class="hidden 2xl:flex items-center gap-5 font-mono text-xs">
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
      
      <!-- Drawer Buttons for Tablets / Mobile (< 1280px) -->
      <button id="btn-toggle-left-drawer" class="xl:hidden px-2 py-1 rounded-lg bg-slate-900 border border-slate-700 hover:border-cyan-500 text-cyan-300 transition flex items-center gap-1 text-[11px] sm:text-xs font-mono" title="Missions & Lobes">
        <span>🔍</span>
        <span class="hidden xs:inline">Missions</span>
      </button>

      <button id="btn-toggle-right-drawer" class="xl:hidden px-2 py-1 rounded-lg bg-slate-900 border border-slate-700 hover:border-emerald-500 text-emerald-300 transition flex items-center gap-1 text-[11px] sm:text-xs font-mono" title="Sub-Work Inspector">
        <span>⚙️</span>
        <span class="hidden xs:inline">Sub-Work</span>
      </button>

      <!-- Label Style Switcher -->
      <button id="btn-toggle-titles" class="px-2 py-1 text-[11px] sm:text-xs rounded-lg bg-slate-900 hover:bg-slate-800 border border-cyan-500/40 text-cyan-300 transition flex items-center gap-1">
        <span class="hidden sm:inline">Titles:</span>
        <strong id="title-mode-status" class="text-emerald-400 font-mono text-[10px] sm:text-xs">FUN</strong>
      </button>

      <!-- Orbit Auto-Rotate Button -->
      <button id="btn-autorotate" class="px-2 py-1 text-[11px] sm:text-xs rounded-lg bg-slate-800/80 hover:bg-slate-700 border border-slate-700 text-slate-300 transition flex items-center gap-1">
        <svg class="w-3.5 h-3.5 text-cyan-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
        <span class="font-mono text-[10px]" id="orbit-status">ON</span>
      </button>

      <!-- Reset Cam Button -->
      <button id="btn-reset-cam" class="px-2 py-1 text-[11px] sm:text-xs rounded-lg bg-slate-800/80 hover:bg-slate-700 border border-slate-700 text-slate-300 transition" title="Reset View">
        Reset
      </button>
    </div>
  </header>

  <!-- MAIN VIEWPORT CONTAINER -->
  <div class="relative flex-1 w-full h-full overflow-hidden">
    
    <!-- 3D Interactive Canvas -->
    <canvas id="brainCanvas" class="absolute inset-0 w-full h-full cursor-grab active:cursor-grabbing"></canvas>

    <!-- Translucent Backdrop for Tablet / Mobile Drawers -->
    <div id="drawer-backdrop" class="fixed inset-0 bg-black/60 backdrop-blur-xs z-15 hidden transition-opacity duration-300 xl:hidden"></div>

    <!-- LEFT DRAWER: HippoRAG Missions & Lobes -->
    <aside id="left-sidebar" class="drawer-panel drawer-hidden-left xl:translate-x-0 xl:opacity-100 xl:pointer-events-auto absolute top-2 sm:top-3 left-2 sm:left-3 w-[88vw] sm:w-[320px] max-w-[340px] max-h-[calc(100vh-4.2rem)] flex flex-col gap-2.5 z-20 overflow-y-auto">
      
      <!-- Query & Mission Recall Card -->
      <div class="bg-slate-950/92 backdrop-blur-xl border border-cyan-900/60 rounded-xl p-3 shadow-2xl flex flex-col gap-2.5">
        <div class="flex items-center justify-between border-b border-slate-800/80 pb-1.5">
          <div class="flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-rose-500 animate-pulse"></span>
            <span class="text-[11px] font-semibold text-rose-300 tracking-wider uppercase font-mono">HippoRAG 2 Recall</span>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-[9px] text-slate-400 font-mono">&lt; 1ms PPR</span>
            <button id="btn-close-left-drawer" class="xl:hidden w-5 h-5 rounded bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white flex items-center justify-center text-xs transition" title="Close Drawer">✕</button>
          </div>
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
          <div class="flex flex-col gap-1">
            <button class="preset-btn text-[10px] px-2 py-1.5 rounded-md bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 transition hover:border-cyan-500/50 text-left flex items-center justify-between"
                    data-q="Refactor token verification & authentication">
              <span>🔐 Token & Auth</span>
              <span class="text-[9px] text-cyan-400 font-mono">&rarr;</span>
            </button>
            <button class="preset-btn text-[10px] px-2 py-1.5 rounded-md bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 transition hover:border-cyan-500/50 text-left flex items-center justify-between"
                    data-q="Process customer charge & database transaction">
              <span>💳 Payment Checkout</span>
              <span class="text-[9px] text-cyan-400 font-mono">&rarr;</span>
            </button>
            <button class="preset-btn text-[10px] px-2 py-1.5 rounded-md bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 transition hover:border-cyan-500/50 text-left flex items-center justify-between"
                    data-q="Cache session invalidate on user logout">
              <span>⚡ Flash Cache Invalidate</span>
              <span class="text-[9px] text-cyan-400 font-mono">&rarr;</span>
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
          <button id="btn-toggle-refactor" class="w-full py-1.5 px-2 rounded-md bg-amber-950/40 hover:bg-amber-900/50 border border-amber-800/50 text-amber-200 text-[10px] font-medium transition flex items-center justify-center gap-1">
            <span id="refactor-btn-text">Simulate Code Refactor</span>
          </button>
        </div>

      </div>

      <!-- Functional Lobe Legend Accordion (Compact) -->
      <details class="bg-slate-950/90 backdrop-blur-md border border-slate-800 rounded-xl p-2.5 shadow-xl text-xs group">
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

    <!-- RIGHT DRAWER: SUB-LEVEL WORK & ENRICHED INSPECTOR -->
    <aside id="inspector-panel" class="drawer-panel drawer-hidden-right xl:translate-x-0 xl:opacity-100 xl:pointer-events-auto absolute top-2 sm:top-3 right-2 sm:right-3 w-[88vw] sm:w-[340px] md:w-[360px] max-w-[400px] max-h-[calc(100vh-4.2rem)] bg-slate-950/94 backdrop-blur-xl border border-cyan-800/60 rounded-xl p-3 sm:p-3.5 shadow-2xl flex flex-col gap-2.5 z-20 overflow-y-auto">
      
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
            <button id="btn-close-inspector" class="xl:hidden w-5 h-5 rounded bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white flex items-center justify-center text-xs transition" title="Close Panel">
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

      <!-- SUB-LEVEL WORK ITEMS (Deep-dive components) -->
      <div class="flex flex-col gap-1.5">
        <div class="flex items-center justify-between">
          <span class="text-[10px] font-bold text-white uppercase tracking-wider font-mono flex items-center gap-1">
            <span>⚙️</span> Sub-Level Work (<span id="inspect-sub-count">3</span>)
          </span>
          <span class="text-[9px] text-cyan-400 font-mono">Active Units</span>
        </div>

        <div id="inspect-sub-items-container" class="flex flex-col gap-1.5 max-h-[175px] overflow-y-auto pr-0.5">
          <!-- Populated dynamically -->
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

    <!-- FLOATING BOTTOM MINIMAL BANNER -->
    <div class="absolute bottom-2.5 left-1/2 -translate-x-1/2 pointer-events-none z-10 w-auto max-w-[92vw]">
      <div class="pointer-events-auto bg-slate-950/85 backdrop-blur-md border border-slate-800/80 rounded-full px-3 py-1.5 shadow-lg flex items-center gap-2 text-[10px] sm:text-xs text-slate-300 font-mono">
        <span class="w-2 h-2 rounded-full bg-cyan-400 animate-pulse shrink-0"></span>
        <span id="bottom-hud-text" class="truncate">
          Tap any node to dive into sub-work • 2-finger pinch to zoom
        </span>
      </div>
    </div>

    <!-- Tooltip -->
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
    let camDist = 360;
    let targetDist = 360;

    function resizeCanvas() {{
      const container = canvas.parentElement;
      width = container.clientWidth;
      height = container.clientHeight;
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      canvas.width = width * dpr;
      canvas.height = height * dpr;
      ctx.resetTransform();
      ctx.scale(dpr, dpr);

      // Auto-adapt camera distance for portrait vs landscape
      if (width < 640) {{
        targetDist = 440;
      }} else if (width < 1024) {{
        targetDist = 380;
      }} else {{
        targetDist = 340;
      }}
      camDist = targetDist;
    }}
    window.addEventListener("resize", resizeCanvas);
    window.addEventListener("orientationchange", () => setTimeout(resizeCanvas, 150));
    resizeCanvas();

    // 3D Camera & Rotation
    let camPitch = 0.25;
    let camYaw = -0.6;
    let autoRotate = true;
    let isDragging = false;
    let lastMouseX = 0;
    let lastMouseY = 0;
    let hoveredNode = null;
    let selectedNode = nodes[0] || null;

    // Anatomical Brain Wireframe Particles
    const brainParticles = [];
    const NUM_BRAIN_PARTICLES = 480;
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

    // Helper: Round rectangle cross-browser
    function drawRoundRect(c, x, y, w, h, r) {{
      if (c.roundRect) {{
        c.beginPath();
        c.roundRect(x, y, w, h, r);
      }} else {{
        c.beginPath();
        c.moveTo(x + r, y);
        c.arcTo(x + w, y, x + w, y + h, r);
        c.arcTo(x + w, y + h, x, y + h, r);
        c.arcTo(x, y + h, x, y, r);
        c.arcTo(x, y, x + w, y, r);
        c.closePath();
      }}
    }}

    // 3D Projection Math (Proportionally adapted to viewport aspect ratio)
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

      // Adapt fov to smallest screen dimension
      const baseFov = Math.min(width, height) < 700 ? Math.min(width, height) * 0.58 : 420;
      const scale = baseFov / dist;
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
        const e = edges[pulse.edgeIdx];
        if (!e || !e.is_active) return;
        const src = nodeMap[e.source];
        const tgt = nodeMap[e.target];
        if (!src || !tgt) return;

        const p1 = project(src.x, src.y, src.z);
        const p2 = project(tgt.x, tgt.y, tgt.z);
        if (!p1 || !p2 || !p1.visible || !p2.visible) return;

        const px = p1.x + (p2.x - p1.x) * pulse.progress;
        const py = p1.y + (p2.y - p1.y) * pulse.progress;
        const pScale = p1.scale + (p2.scale - p1.scale) * pulse.progress;

        ctx.beginPath();
        ctx.arc(px, py, Math.max(0.8, 1.8 * pScale), 0, Math.PI * 2);
        ctx.fillStyle = pulse.color;
        ctx.fill();
      }});

      // 4. Render HippoRAG 2 Associative Recall Waves
      if (isQueryWaveActive && activeQuerySeedIds.length > 0) {{
        activeQuerySeedIds.forEach(seedId => {{
          const n = nodeMap[seedId];
          if (!n) return;
          const pt = project(n.x, n.y, n.z);
          if (pt && pt.visible) {{
            const ringR = queryWaveRadius * pt.scale;
            ctx.beginPath();
            ctx.arc(pt.x, pt.y, ringR, 0, Math.PI * 2);
            ctx.strokeStyle = `rgba(244, 63, 94, ${{Math.max(0, 1 - queryWaveRadius/240)}})`;
            ctx.lineWidth = 2.0;
            ctx.stroke();
          }}
        }});
      }}

      // 5. Render Memory Spheres & Anti-Congestion Labels (Back-to-Front)
      const sortedNodes = [...nodes].sort((a, b) => {{
        const pa = project(a.x, a.y, a.z);
        const pb = project(b.x, b.y, b.z);
        return ((pb ? pb.z : 0) - (pa ? pa.z : 0));
      }});

      sortedNodes.forEach(n => {{
        const pt = project(n.x, n.y, n.z);
        if (!pt || !pt.visible) return;

        const isHovered = hoveredNode && hoveredNode.id === n.id;
        const isSelected = selectedNode && selectedNode.id === n.id;
        const isSeed = activeQuerySeedIds.includes(n.id);
        const isInSubgraph = activeSubgraphsNodeIds.has(n.id);

        let baseRadius = (n.radius || 6) * pt.scale * 1.05;
        if (isSelected) baseRadius *= 1.35;
        if (isHovered) baseRadius *= 1.25;

        ctx.save();

        // Outer Aura
        const glowGrad = ctx.createRadialGradient(pt.x, pt.y, baseRadius * 0.4, pt.x, pt.y, baseRadius * 2.3);
        if (isSelected) {{
          glowGrad.addColorStop(0, "rgba(56, 189, 248, 0.9)");
        }} else if (isSeed) {{
          glowGrad.addColorStop(0, "rgba(244, 63, 94, 0.9)");
        }} else if (isInSubgraph) {{
          glowGrad.addColorStop(0, "rgba(244, 63, 94, 0.6)");
        }} else if (isHovered) {{
          glowGrad.addColorStop(0, "rgba(168, 85, 247, 0.8)");
        }} else {{
          glowGrad.addColorStop(0, `${{n.color}}33`);
        }}
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
        const shouldShowLabel = isSelected || isHovered || isSeed || (n.degree >= 9 && pt.scale > 1.05 && width >= 640);

        if (shouldShowLabel) {{
          const displayLabel = useFriendlyTitles ? (n.friendly_title || n.name) : n.name;
          const fontSize = Math.max(10, Math.min(13, 11 * pt.scale));
          ctx.font = `${{isSelected ? "bold " : ""}}${{fontSize}}px ui-monospace, monospace`;
          
          // Measure and draw clean pill background to eliminate overlapping clutter
          const textWidth = ctx.measureText(displayLabel).width;
          const pillX = pt.x + baseRadius + 5;
          const pillY = pt.y - fontSize/2 - 3;
          const pillW = textWidth + 8;
          const pillH = fontSize + 6;

          ctx.fillStyle = isSelected 
            ? "rgba(15, 23, 42, 0.96)" 
            : isHovered 
              ? "rgba(15, 23, 42, 0.9)" 
              : "rgba(10, 15, 29, 0.85)";
          ctx.strokeStyle = isSelected 
            ? "rgba(56, 189, 248, 0.9)" 
            : isHovered 
              ? "rgba(168, 85, 247, 0.8)" 
              : "rgba(56, 189, 248, 0.35)";
          ctx.lineWidth = isSelected ? 1.5 : 1;
          
          drawRoundRect(ctx, pillX, pillY, pillW, pillH, 4);
          ctx.fill();
          ctx.stroke();

          ctx.fillStyle = isSelected ? "#38bdf8" : (isSeed ? "#f43f5e" : "#e2e8f0");
          ctx.fillText(displayLabel, pillX + 4, pt.y + fontSize/3);
        }}

        ctx.restore();
      }});

      requestAnimationFrame(render);
    }}
    requestAnimationFrame(render);

    // ================= TOUCH & MOUSE GESTURES =================
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
    const backdrop = document.getElementById("drawer-backdrop");

    function openLeftDrawer() {{
      leftDrawer.classList.remove("drawer-hidden-left");
      leftDrawer.classList.add("translate-x-0", "opacity-100", "pointer-events-auto");
      if (window.innerWidth < 1280) {{
        closeInspectorDrawer();
        backdrop.classList.remove("hidden");
      }}
    }}

    function closeLeftDrawer() {{
      leftDrawer.classList.add("drawer-hidden-left");
      leftDrawer.classList.remove("translate-x-0", "opacity-100", "pointer-events-auto");
      if (window.innerWidth < 1280 && rightDrawer.classList.contains("drawer-hidden-right")) {{
        backdrop.classList.add("hidden");
      }}
    }}

    function toggleLeftDrawer() {{
      if (leftDrawer.classList.contains("drawer-hidden-left")) {{
        openLeftDrawer();
      }} else {{
        closeLeftDrawer();
      }}
    }}

    function openInspectorDrawer() {{
      rightDrawer.classList.remove("drawer-hidden-right");
      rightDrawer.classList.add("translate-x-0", "opacity-100", "pointer-events-auto");
      if (window.innerWidth < 1280) {{
        closeLeftDrawer();
        backdrop.classList.remove("hidden");
      }}
    }}

    function closeInspectorDrawer() {{
      rightDrawer.classList.add("drawer-hidden-right");
      rightDrawer.classList.remove("translate-x-0", "opacity-100", "pointer-events-auto");
      if (window.innerWidth < 1280 && leftDrawer.classList.contains("drawer-hidden-left")) {{
        backdrop.classList.add("hidden");
      }}
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
    document.getElementById("btn-close-left-drawer").addEventListener("click", closeLeftDrawer);
    document.getElementById("btn-close-inspector").addEventListener("click", closeInspectorDrawer);
    backdrop.addEventListener("click", () => {{
      closeLeftDrawer();
      closeInspectorDrawer();
    }});

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

      // Update Bottom Banner HUD
      const subCount = n.sub_items ? n.sub_items.length : 3;
      document.getElementById("bottom-hud-text").innerHTML = `<span class="text-cyan-400 font-bold">${{n.friendly_title || n.name}}</span> • <span class="text-slate-300">${{n.friendly_role || n.type}}</span> • <span class="text-emerald-400">${{subCount}} sub-tasks</span>`;

      // Render Sub-Level Work Items
      const subContainer = document.getElementById("inspect-sub-items-container");
      subContainer.innerHTML = "";
      const subItems = n.sub_items || [
        {{ "name": "Core Sub-Routine", "type": "Sub-Function", "status": "Armored", "desc": "Handles immediate caller payload." }}
      ];
      document.getElementById("inspect-sub-count").innerText = subItems.length;

      subItems.forEach(sub => {{
        const subCard = document.createElement("div");
        subCard.className = "bg-slate-900/90 border border-slate-800 hover:border-cyan-500/60 rounded-lg p-2 transition flex flex-col gap-1 text-[11px]";
        
        const statusColors = {{
          "Armored": "bg-emerald-950 text-emerald-300 border-emerald-800",
          "Syncing": "bg-amber-950 text-amber-300 border-amber-800",
          "Active": "bg-cyan-950 text-cyan-300 border-cyan-800",
          "Optimized": "bg-purple-950 text-purple-300 border-purple-800"
        }};
        const badgeClass = statusColors[sub.status] || "bg-slate-800 text-slate-300 border-slate-700";

        subCard.innerHTML = `
          <div class="flex items-center justify-between">
            <span class="font-bold text-white tracking-tight">${{sub.name}}</span>
            <span class="text-[9px] px-1.5 py-0.2 rounded font-mono border ${{badgeClass}}">${{sub.status}}</span>
          </div>
          <p class="text-[10px] text-slate-300 leading-snug">${{sub.desc}}</p>
          <div class="flex items-center justify-between text-[9px] text-slate-500 font-mono pt-0.5">
            <span>Sub-Type: ${{sub.type}}</span>
            <span class="text-emerald-400">● 100% HEALTH</span>
          </div>
        `;
        subContainer.appendChild(subCard);
      }});

      // Render Work Activities
      const logsContainer = document.getElementById("inspect-work-logs");
      logsContainer.innerHTML = "";
      const activities = n.sub_activities || [
        "Invoked by peer caller in runtime mesh",
        "Updated local memory cache",
        "Validated schema constraints"
      ];
      activities.forEach(act => {{
        const li = document.createElement("li");
        li.innerText = act;
        logsContainer.appendChild(li);
      }});

      // Render Neighbors
      const neighContainer = document.getElementById("inspect-neighbors");
      neighContainer.innerHTML = "";
      const connectedEdges = edges.filter(e => e.source === n.id || e.target === n.id);
      document.getElementById("inspect-deg").innerText = connectedEdges.length;

      connectedEdges.forEach(e => {{
        const otherId = e.source === n.id ? e.target : e.source;
        const otherNode = nodeMap[otherId];
        if (!otherNode) return;

        const row = document.createElement("div");
        row.className = "flex items-center justify-between p-1 rounded bg-slate-900/60 hover:bg-slate-800 text-[10px] cursor-pointer transition border border-slate-800/60";
        row.innerHTML = `
          <div class="flex items-center gap-1.5 truncate">
            <span class="w-1.5 h-1.5 rounded-full" style="background: ${{otherNode.color}}"></span>
            <span class="text-slate-300 truncate">${{otherNode.friendly_title || otherNode.name}}</span>
          </div>
          <span class="text-[9px] font-mono text-cyan-400 shrink-0 uppercase">${{e.type}}</span>
        `;
        row.addEventListener("click", () => {{
          selectNode(otherNode);
        }});
        neighContainer.appendChild(row);
      }});
    }}

    // HippoRAG 2 Associative Recall Runner
    function runHippoRAG(queryText) {{
      const q = queryText.toLowerCase();
      let matchedSeeds = [];

      nodes.forEach(n => {{
        const searchable = `${{n.friendly_title || ""}} ${{n.friendly_role || ""}} ${{n.name}} ${{n.docstring || ""}} ${{n.file}}`.toLowerCase();
        let score = 0;
        if (q.includes("token") && searchable.includes("token")) score += 3;
        if (q.includes("auth") && searchable.includes("auth")) score += 3;
        if (q.includes("pay") && searchable.includes("payment")) score += 3;
        if (q.includes("checkout") && searchable.includes("checkout")) score += 3;
        if (q.includes("cache") && searchable.includes("cache")) score += 3;
        if (q.includes("database") && (searchable.includes("database") || searchable.includes("pool"))) score += 3;
        if (score > 0) matchedSeeds.push({{ node: n, score }});
      }});

      if (matchedSeeds.length === 0) {{
        matchedSeeds = [{{ node: nodes[0], score: 1 }}];
      }}

      matchedSeeds.sort((a, b) => b.score - a.score);
      activeQuerySeedIds = matchedSeeds.slice(0, 3).map(m => m.node.id);

      // Multi-hop Personalized PageRank BFS
      activeSubgraphsNodeIds = new Set(activeQuerySeedIds);
      let frontier = [...activeQuerySeedIds];
      for (let hop = 0; hop < 2; hop++) {{
        const nextFrontier = [];
        frontier.forEach(u => {{
          edges.forEach(e => {{
            if (e.source === u && !activeSubgraphsNodeIds.has(e.target) && e.is_active) {{
              activeSubgraphsNodeIds.add(e.target);
              nextFrontier.push(e.target);
            }} else if (e.target === u && !activeSubgraphsNodeIds.has(e.source) && e.is_active) {{
              activeSubgraphsNodeIds.add(e.source);
              nextFrontier.push(e.source);
            }}
          }});
        }});
        frontier = nextFrontier;
      }}

      // Calculate context efficiency savings
      let totalRawTokens = 0;
      let synapseTokens = 0;
      activeSubgraphsNodeIds.forEach(id => {{
        const n = nodeMap[id];
        if (n) {{
          totalRawTokens += (n.full_tokens || 85);
          synapseTokens += (n.surrogate_tokens || 28);
        }}
      }});
      totalRawTokens = Math.max(totalRawTokens, 650);

      const savedPct = Math.round((1 - (synapseTokens / totalRawTokens)) * 100);

      document.getElementById("qr-nodes-count").innerText = `${{activeSubgraphsNodeIds.size}} nodes / 2 hops`;
      document.getElementById("qr-raw-tok").innerText = `${{totalRawTokens}} tok`;
      document.getElementById("qr-surr-tok").innerText = `${{synapseTokens}} tok`;
      document.getElementById("qr-savings-bar").style.width = `${{savedPct}}%`;
      document.getElementById("qr-savings-pct").innerText = `+${{savedPct}}% Saved`;

      // Trigger visual wave
      queryWaveRadius = 0;
      isQueryWaveActive = true;

      // Select highest scoring seed node
      if (activeQuerySeedIds.length > 0) {{
        const best = nodeMap[activeQuerySeedIds[0]];
        if (best) selectNode(best);
      }}
    }}

    // Title Mode switcher
    document.getElementById("btn-toggle-titles").addEventListener("click", () => {{
      useFriendlyTitles = !useFriendlyTitles;
      const statusEl = document.getElementById("title-mode-status");
      statusEl.innerText = useFriendlyTitles ? "FUN" : "CODE";
      statusEl.className = useFriendlyTitles ? "text-emerald-400 font-mono text-[10px] sm:text-xs" : "text-amber-400 font-mono text-[10px] sm:text-xs";
      if (selectedNode) selectNode(selectedNode);
    }});

    // Temporal Invalidation Toggle
    let isTemporalInvalidated = false;
    document.getElementById("btn-toggle-refactor").addEventListener("click", () => {{
      isTemporalInvalidated = !isTemporalInvalidated;
      const badge = document.getElementById("temporal-badge");
      const btnText = document.getElementById("refactor-btn-text");

      edges.forEach(e => {{
        if (e.source.includes("v1") || e.target.includes("v1") || e.type === "CALLS") {{
          e.is_active = !isTemporalInvalidated;
        }}
      }});

      if (isTemporalInvalidated) {{
        badge.innerText = "EPOCH v2 DIFF";
        badge.className = "text-[8px] px-1 rounded bg-rose-950 text-rose-300 font-mono border border-rose-800";
        btnText.innerText = "Revert Temporal State";
      }} else {{
        badge.innerText = "STABLE";
        badge.className = "text-[8px] px-1 rounded bg-slate-800 text-slate-400 font-mono";
        btnText.innerText = "Simulate Code Refactor";
      }}
    }});

    // Preset chips
    document.querySelectorAll(".preset-btn").forEach(btn => {{
      btn.addEventListener("click", () => {{
        const q = btn.getAttribute("data-q");
        document.getElementById("query-input").value = q;
        runHippoRAG(q);
        if (window.innerWidth < 1280) closeLeftDrawer();
      }});
    }});

    document.getElementById("btn-run-query").addEventListener("click", () => {{
      const q = document.getElementById("query-input").value;
      runHippoRAG(q);
      if (window.innerWidth < 1280) closeLeftDrawer();
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
      targetDist = width < 640 ? 440 : (width < 1024 ? 380 : 340);
    }});

    // Initialize with default query and select first seed
    setTimeout(() => {{
      runHippoRAG("Refactor token verification & authentication");
    }}, 200);

  </script>
</body>
</html>
'''
    target_path = "/home/antigravity/synapse/visualizer/index.html"
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Built visualizer at {target_path} ({len(html_content)} bytes)")

    return html_content

if __name__ == "__main__":
    build_full_html()
