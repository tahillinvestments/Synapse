"""
Unified CLI for SynapseGraph: Default Project Memory & 3D Brain Engine.
Supports: init, index, query, impact, view, and global git-template installation.
"""

import argparse
import json
import os
import sys
import hashlib
import time
from typing import Dict, Any, List

# Ensure synapse_graph package path is accessible
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from synapse_graph.engine import SynapseMemoryEngine
from synapse_graph.models import SymbolNode, MemoryEdge, LobeType, EdgeType


def get_synapse_dir(project_dir: str) -> str:
    return os.path.join(project_dir, ".synapse")


def compute_file_hash(path: str) -> str:
    hasher = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            while chunk := f.read(65536):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception:
        return ""


def load_synapse_engine(project_dir: str) -> tuple[SynapseMemoryEngine, dict]:
    synapse_dir = get_synapse_dir(project_dir)
    data_file = os.path.join(synapse_dir, "graph_data.json")
    manifest_file = os.path.join(synapse_dir, "manifest.json")

    engine = SynapseMemoryEngine()
    manifest = {"file_hashes": {}, "last_updated": 0, "commits": []}

    if os.path.exists(manifest_file):
        try:
            with open(manifest_file, "r", encoding="utf-8") as f:
                manifest = json.load(f)
        except Exception:
            pass

    if os.path.exists(data_file):
        try:
            with open(data_file, "r", encoding="utf-8") as f:
                saved = json.load(f)
            # Rehydrate nodes
            for nd in saved.get("nodes", []):
                lobe = LobeType(nd.get("lobe", "frontal"))
                node = SymbolNode(
                    id=nd["id"],
                    name=nd["name"],
                    symbol_type=nd.get("type", "function"),
                    file_path=nd.get("file", ""),
                    lobe=lobe,
                    line_start=1,
                    line_end=1,
                    signature=nd.get("signature", ""),
                    docstring=nd.get("docstring"),
                    surrogate=nd.get("surrogate", ""),
                    full_tokens=nd.get("full_tokens", 50),
                    surrogate_tokens=nd.get("surrogate_tokens", 15),
                    community_id=nd.get("community", 0),
                    pagerank_score=nd.get("pagerank", 1.0) / 1000.0,
                    commit_sha=nd.get("commit", "HEAD")
                )
                if not nd.get("is_active", True):
                    node.valid_to = time.time()
                engine.nodes[node.id] = node

            # Rehydrate edges
            for ed in saved.get("edges", []):
                edge = MemoryEdge(
                    source_id=ed["source"],
                    target_id=ed["target"],
                    edge_type=EdgeType(ed.get("type", "calls")),
                    weight=ed.get("weight", 1.0),
                    commit_sha=ed.get("commit", "HEAD")
                )
                if not ed.get("is_active", True):
                    edge.valid_to = time.time()
                engine.edges.append(edge)

        except Exception as e:
            print(f"[Warning] Could not load existing graph_data.json: {e}")

    return engine, manifest


def save_synapse_engine(project_dir: str, engine: SynapseMemoryEngine, manifest: dict):
    synapse_dir = get_synapse_dir(project_dir)
    os.makedirs(synapse_dir, exist_ok=True)
    data_file = os.path.join(synapse_dir, "graph_data.json")
    manifest_file = os.path.join(synapse_dir, "manifest.json")

    engine.rebuild_topology()
    exported = engine.export_3d_brain_data()

    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(exported, f, indent=2)

    manifest["last_updated"] = time.time()
    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    generate_project_visualizer(project_dir, exported)


def generate_project_visualizer(project_dir: str, graph_data: dict):
    """Generates a self-contained 3D brain visualizer HTML inside .synapse/"""
    synapse_dir = get_synapse_dir(project_dir)
    html_path = os.path.join(synapse_dir, "brain_memory.html")

    graph_json_str = json.dumps(graph_data)
    template_path = "/home/antigravity/.gemini/jetski/brain/v1/default/jetski_remote_agents_3p/6086e0b3-3e8c-4628-ad3f-93f16cd0d5e9/brain_memory_visualizer.html"

    try:
        with open(template_path, "r", encoding="utf-8") as bf:
            html_content = bf.read()
        
        import re
        html_custom = re.sub(
            r'const INITIAL_GRAPH_DATA = \{.*?\};',
            f'const INITIAL_GRAPH_DATA = {graph_json_str};',
            html_content,
            flags=re.DOTALL
        )
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_custom)
    except Exception as e:
        pass


def install_git_hook(project_dir: str):
    """Installs post-commit hook for automated incremental indexing on commit."""
    git_dir = os.path.join(project_dir, ".git")
    if os.path.exists(git_dir):
        hooks_dir = os.path.join(git_dir, "hooks")
        os.makedirs(hooks_dir, exist_ok=True)
        post_commit = os.path.join(hooks_dir, "post-commit")
        hook_script = """#!/usr/bin/env bash
# SynapseGraph automated post-commit incremental memory updater
if command -v synapse &> /dev/null; then
    synapse index --incremental --quiet &
fi
"""
        with open(post_commit, "w", encoding="utf-8") as f:
            f.write(hook_script)
        os.chmod(post_commit, 0o755)
        return True
    return False


def setup_global_git_template():
    """Configures ~/.git-template so git init installs the synapse hook automatically."""
    template_dir = os.path.expanduser("~/.git-template")
    hooks_dir = os.path.join(template_dir, "hooks")
    os.makedirs(hooks_dir, exist_ok=True)
    post_commit = os.path.join(hooks_dir, "post-commit")
    hook_script = """#!/usr/bin/env bash
# SynapseGraph default post-commit hook for all new repositories
if command -v synapse &> /dev/null; then
    synapse index --incremental --quiet &
fi
"""
    with open(post_commit, "w", encoding="utf-8") as f:
        f.write(hook_script)
    os.chmod(post_commit, 0o755)

    os.system(f'git config --global init.templateDir "{template_dir}"')
    return template_dir


def cmd_init(args):
    project_dir = os.path.abspath(args.dir or ".")
    synapse_dir = get_synapse_dir(project_dir)
    os.makedirs(synapse_dir, exist_ok=True)

    print(f"\n🧠 [SynapseGraph] Initializing cognitive memory in {project_dir}")
    installed_hook = install_git_hook(project_dir)
    if installed_hook:
        print("  ✓ Git post-commit hook installed (.git/hooks/post-commit)")

    cmd_index(args)
    print(f"  ✓ 3D Cortex visualizer ready at {os.path.join(synapse_dir, 'brain_memory.html')}")
    print("  ✓ Project memory initialized successfully.\n")


def cmd_index(args):
    project_dir = os.path.abspath(getattr(args, "dir", None) or ".")
    quiet = getattr(args, "quiet", False)
    incremental = getattr(args, "incremental", False)

    engine, manifest = load_synapse_engine(project_dir)
    file_hashes = manifest.setdefault("file_hashes", {})

    indexed_count = 0
    for root, dirs, files in os.walk(project_dir):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("node_modules", "dist", "build", "__pycache__", "venv", ".venv")]
        for f in files:
            if f.endswith(".py"):
                full_p = os.path.join(root, f)
                rel_p = os.path.relpath(full_p, project_dir)
                curr_hash = compute_file_hash(full_p)

                if incremental and file_hashes.get(rel_p) == curr_hash:
                    continue

                try:
                    with open(full_p, "r", encoding="utf-8", errors="ignore") as fp:
                        code = fp.read()
                    engine.ingest_source_code(rel_p, code)
                    file_hashes[rel_p] = curr_hash
                    indexed_count += 1
                except Exception as e:
                    if not quiet:
                        print(f"  [!] Error parsing {rel_p}: {e}")

    save_synapse_engine(project_dir, engine, manifest)

    if not quiet:
        active_nodes = sum(1 for n in engine.nodes.values() if n.is_active)
        active_edges = sum(1 for e in engine.edges if e.is_active)
        print(f"🧠 [SynapseGraph] Indexed {indexed_count} files | {active_nodes} Active Symbols | {active_edges} Axons")


def cmd_query(args):
    project_dir = os.path.abspath(getattr(args, "dir", None) or ".")
    engine, _ = load_synapse_engine(project_dir)

    if not engine.nodes:
        print("No index found. Run 'synapse init' or 'synapse index' first.")
        return

    result = engine.query(args.query_text, top_k=args.top_k or 8)

    if getattr(args, "json", False):
        out = {
            "query": result.query,
            "seeds": result.seed_nodes,
            "tokens_original": result.tokens_original,
            "tokens_retrieved": result.tokens_retrieved,
            "token_savings_pct": result.token_savings_pct,
            "subgraph": [
                {
                    "name": n.name,
                    "lobe": n.lobe.value,
                    "signature": n.signature,
                    "file": n.file_path,
                    "ppr": round(result.ppr_scores.get(n.id, 0.0), 4)
                } for n in result.subgraph_nodes
            ]
        }
        print(json.dumps(out, indent=2))
        return

    print(f"\n🧠 [HippoRAG Query] '{args.query_text}'")
    print(f"Seeds: {result.seed_nodes}")
    print(f"Evidence Subgraph: {len(result.subgraph_nodes)} symbols, {len(result.subgraph_edges)} edges (PPR single-step in {result.execution_time_ms} ms)")
    print(f"Token Reduction: {result.tokens_original} -> {result.tokens_retrieved} tokens ({result.token_savings_pct}% SAVED)\n")
    print("Relevant Context Nodes:")
    for n in result.subgraph_nodes:
        ppr = result.ppr_scores.get(n.id, 0.0)
        print(f"  [{n.lobe.value.upper():<11}] {n.name:<25} (PPR: {ppr:.4f}) | {n.signature}")
    print()


def cmd_impact(args):
    project_dir = os.path.abspath(getattr(args, "dir", None) or ".")
    engine, _ = load_synapse_engine(project_dir)

    target_name = args.symbol.lower()
    matches = [n for n in engine.nodes.values() if target_name in n.name.lower() or target_name in n.id.lower()]

    if not matches:
        print(f"Symbol '{args.symbol}' not found in memory graph.")
        return

    root = matches[0]
    print(f"\n⚡ [Blast Radius Impact] Symbol: {root.name} ({root.signature})")
    
    callers = [engine.nodes[e.source_id] for e in engine.edges if e.target_id == root.id and e.source_id in engine.nodes and e.is_active]
    callees = [engine.nodes[e.target_id] for e in engine.edges if e.source_id == root.id and e.target_id in engine.nodes and e.is_active]

    print(f"Direct Inbound Callers ({len(callers)}):")
    for c in callers:
        print(f"  <- [{c.lobe.value.upper()}] {c.name} in {c.file_path}")

    print(f"\nDirect Outbound Dependencies ({len(callees)}):")
    for c in callees:
        print(f"  -> [{c.lobe.value.upper()}] {c.name} in {c.file_path}")
    print()


def cmd_view(args):
    project_dir = os.path.abspath(getattr(args, "dir", None) or ".")
    synapse_dir = get_synapse_dir(project_dir)
    html_path = os.path.join(synapse_dir, "brain_memory.html")

    if not os.path.exists(html_path):
        print(f"Visualizer not found in {html_path}. Running 'synapse init' first...")
        cmd_init(args)

    print(f"\n🧠 3D Brain Cortex Visualizer available at:")
    print(f"file://{html_path}\n")


def cmd_setup_global(args):
    tmpl = setup_global_git_template()
    print(f"\n✓ SynapseGraph configured as default template for all new git projects!")
    print(f"  Template path: {tmpl}")
    print(f"  Whenever you run 'git init', the post-commit memory hook is installed automatically.\n")


def main():
    parser = argparse.ArgumentParser(description="SynapseGraph CLI: Modern Code Memory & 3D Brain")
    subparsers = parser.add_subparsers(dest="command")

    p_init = subparsers.add_parser("init", help="Initialize SynapseGraph memory for a project")
    p_init.add_argument("--dir", type=str, default=".", help="Project directory")
    p_init.add_argument("--quiet", action="store_true")
    p_init.add_argument("--incremental", action="store_true")

    p_index = subparsers.add_parser("index", help="Re-index codebase symbols & call graph")
    p_index.add_argument("--dir", type=str, default=".", help="Project directory")
    p_index.add_argument("--incremental", action="store_true", help="Only parse changed files")
    p_index.add_argument("--quiet", action="store_true")

    p_query = subparsers.add_parser("query", help="Query memory graph via HippoRAG PPR")
    p_query.add_argument("query_text", type=str, help="Natural language query or symbol")
    p_query.add_argument("--dir", type=str, default=".")
    p_query.add_argument("--top-k", type=int, default=8)
    p_query.add_argument("--json", action="store_true")

    p_impact = subparsers.add_parser("impact", help="Inspect blast radius and callers of a symbol")
    p_impact.add_argument("symbol", type=str, help="Symbol name or substring")
    p_impact.add_argument("--dir", type=str, default=".")

    p_view = subparsers.add_parser("view", help="Get 3D Brain Cortex visualization path")
    p_view.add_argument("--dir", type=str, default=".")

    p_global = subparsers.add_parser("setup-global", help="Configure Git default template for all new repos")

    args = parser.parse_args()

    if args.command == "init":
        cmd_init(args)
    elif args.command == "index":
        cmd_index(args)
    elif args.command == "query":
        cmd_query(args)
    elif args.command == "impact":
        cmd_impact(args)
    elif args.command == "view":
        cmd_view(args)
    elif args.command == "setup-global":
        cmd_setup_global(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
