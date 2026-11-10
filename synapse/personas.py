"""
Friendly Persona and Sub-Level Visual Generator for Synapse Nodes.
Transforms technical AST symbol data into fun, engaging, and rich project intelligence.
"""

import re
from typing import Dict, List, Any

# Map symbols to friendly personas, mission briefings, and subsystem micro-elements
def enrich_node_with_persona(node: Dict[str, Any], all_nodes: List[Dict[str, Any]] = None) -> Dict[str, Any]:
    name = node.get("name", "")
    nid = node.get("id", "")
    sym_type = node.get("type", "function")
    lobe = node.get("lobe", "frontal")
    doc = node.get("docstring", "") or ""
    file_p = node.get("file", "")

    n_low = (name + " " + nid + " " + file_p).lower()

    # Determine Domain & Personality
    if any(k in n_low for k in ["jwt", "verify", "sign", "token", "auth", "login", "credential"]):
        emoji = "🔐"
        domain = "Security & Cyber-Defense"
        role_title = "Cryptographic Sentinel"
        mission = "Guards the perimeter, issues digital passports, and verifies cryptographic tokens."
        power_stat = 94
        vibe = "Vigilant • Shielded"
        sub_items = [
            {"title": "HMAC-SHA256 Token Vault", "type": "Crypto Engine", "status": "Armored", "icon": "🛡️", "desc": "Validates cryptographic signatures against tampering."},
            {"title": "Claims Expiry Monitor", "type": "Epoch Clock", "status": "Syncing", "icon": "⏱️", "desc": "Enforces 3600-second session lifetimes."},
            {"title": "Role & Permission Gate", "type": "Access Layer", "status": "Active", "icon": "🎟️", "desc": "Grants 'admin' and 'user' tier capabilities."}
        ]
        work_logs = [
            "Validated inbound bearer payload without database trip (0.12ms)",
            "Dispatched refreshed token payload to Redis memory cache",
            "Blocked unauthenticated probe attempt"
        ]
    elif any(k in n_low for k in ["pay", "checkout", "charge", "billing", "price", "cents", "stripe"]):
        emoji = "💳"
        domain = "Fintech & Treasury Pipeline"
        role_title = "Vault Transaction Master"
        mission = "Executes idempotent charge workflows, handles merchant settlement, and upgrades customer tiers."
        power_stat = 98
        vibe = "High-Velocity • Idempotent"
        sub_items = [
            {"title": "Stripe & Network Bridge", "type": "Payment Rail", "status": "Live", "icon": "⚡", "desc": "Communicates with payment gateways."},
            {"title": "Billing Tier State Mutator", "type": "Entitlement Engine", "status": "Ready", "icon": "💎", "desc": "Flips customer status to 'premium_active'."},
            {"title": "Cache Invalidation Emitter", "type": "Session Sweeper", "status": "Armed", "icon": "🧹", "desc": "Evicts stale sessions to reload entitlements."}
        ]
        work_logs = [
            "Processed $49.00 payment intent payload successfully",
            "Updated PostgreSQL customer subscription status",
            "Evicted user cache to trigger immediate entitlement refresh"
        ]
    elif any(k in n_low for k in ["redis", "cache", "bridge", "store_session", "get_session"]):
        emoji = "⚡"
        domain = "Synaptic Flash Recall"
        role_title = "Sub-Millisecond Memory Core"
        mission = "Caches active sessions in high-speed volatile storage, cutting DB load by 98%."
        power_stat = 99
        vibe = "Ultra-Fast • Ephemeral"
        sub_items = [
            {"title": "Hot Key In-Memory Store", "type": "RAM Buffer", "status": "Optimal", "icon": "🔥", "desc": "Instantaneous dictionary lookup at memory speeds."},
            {"title": "TTL Eviction Sweeper", "type": "Garbage Collector", "status": "Running", "icon": "⏳", "desc": "Auto-expires inactive user sessions."},
            {"title": "Zero-Latency Bridge", "type": "I/O Multiplexer", "status": "Connected", "icon": "🔌", "desc": "Connects authentication layer directly to RAM."}
        ]
        work_logs = [
            "Served active token claims in 0.04ms (Cache Hit Rate: 99.4%)",
            "Purged invalidated token session:usr_88291 upon security signal",
            "Maintained 10,000 parallel connection descriptors"
        ]
    elif any(k in n_low for k in ["db", "pool", "database", "sql", "find_user", "get_user", "postgres"]):
        emoji = "🗄️"
        domain = "Deep Persistent Vault"
        role_title = "Master Database Overseer"
        mission = "Manages transactional ACID persistence, maintains connection pools, and guards primary records."
        power_stat = 91
        vibe = "ACID Compliant • Rock-Solid"
        sub_items = [
            {"title": "Active Connection Multiplexer", "type": "Pool Manager", "status": "10/10 Conns", "icon": "🏊", "desc": "Reuses pooled connections to eliminate handshake latency."},
            {"title": "Indexed User B-Tree Index", "type": "Storage Engine", "status": "Indexed", "icon": "🔍", "desc": "Primary lookup on credentials & UUIDs."},
            {"title": "Billing Status Transaction Worker", "type": "Write Pipeline", "status": "Ready", "icon": "✍️", "desc": "Commits account upgrades with row-level locks."}
        ]
        work_logs = [
            "Retrieved hydrated user entity usr_88291 in 0.45ms",
            "Committed tier update transaction to WAL log",
            "Healthy connection pool lifecycle maintained"
        ]
    elif any(k in n_low for k in ["route", "gateway", "api", "endpoint"]):
        emoji = "🌐"
        domain = "Sensory Cortex & Public Gateway"
        role_title = "Sensory Border Dispatcher"
        mission = "Listens to the outside world, inspects incoming HTTP/MCP payloads, and routes signals inward."
        power_stat = 93
        vibe = "Public-Facing • Reactive"
        sub_items = [
            {"title": "Sensory Request Decoder", "type": "Ingress Parser", "status": "Listening", "icon": "📡", "desc": "Unpacks JSON and headers from external callers."},
            {"title": "Bearer Auth Interceptor", "type": "Security Wire", "status": "Guarding", "icon": "🚦", "desc": "Requires token before hitting checkout workflows."},
            {"title": "Internal Service Dispatcher", "type": "Bus Router", "status": "Connected", "icon": "🔀", "desc": "Hands off tasks to payment and auth services."}
        ]
        work_logs = [
            "Intercepted POST /payments/checkout sensory packet",
            "Authenticated bearer header with Sentinel unit",
            "Dispatched order payload to Treasury Master"
        ]
    elif any(k in n_low for k in ["user", "payload", "dto", "model", "schema"]):
        emoji = "📐"
        domain = "Architectural Blueprints & Contracts"
        role_title = "Semantic Schema Weaver"
        mission = "Defines the exact shape of reality: typed parameters, token schemas, and data structures."
        power_stat = 88
        vibe = "Strictly-Typed • Harmonious"
        sub_items = [
            {"title": "TokenPayload Contract", "type": "Schema", "status": "Verified", "icon": "📜", "desc": "Strict types for user_id and authorization roles."},
            {"title": "UserDTO Data Crystal", "type": "Model", "status": "Immutable", "icon": "💎", "desc": "Hydrated representation of account state."},
            {"title": "PaymentRequest Spec", "type": "Intent Blueprint", "status": "Standardized", "icon": "📋", "desc": "Currency, amount_cents, and user bindings."}
        ]
        work_logs = [
            "Enforced structural contract on inbound JSON payload",
            "Prevented type-coercion error at compiler level",
            "Zero memory footprint surrogate interface cached"
        ]
    else:
        emoji = "🧠"
        domain = "Executive Processing"
        role_title = "Neural Cog"
        mission = "Executes programmatic domain logic within the application mesh."
        power_stat = 85
        vibe = "Algorithmic • Reliable"
        sub_items = [
            {"title": "Core Logic Circuit", "type": "AST Node", "status": "Active", "icon": "⚙️", "desc": "Direct syntactic execution path."},
            {"title": "Surrogate Interface", "type": "Token Saver", "status": "Compressed", "icon": "🗜️", "desc": "Preserves signatures while trimming body tokens."},
            {"title": "Axon Synapse Hub", "type": "Edge Connector", "status": "Linked", "icon": "🔗", "desc": "Relays data to peer modules."}
        ]
        work_logs = [
            "Parsed into Synapse AST graph with zero LLM API cost",
            "Assigned to functional brain lobe",
            "Connected in single-step HippoRAG PPR topological matrix"
        ]

    # Human-readable fun friendly title
    clean_name = name.replace("mod:", "").replace("__init__", "Init Constructor")
    clean_words = [w.capitalize() for w in re.split(r"[_\.]", clean_name) if w and w != "mod"]
    friendly_display = f"{emoji} {' '.join(clean_words)}"

    node["friendly_title"] = friendly_display
    node["friendly_domain"] = domain
    node["friendly_role"] = role_title
    node["friendly_mission"] = mission
    node["friendly_power"] = power_stat
    node["friendly_vibe"] = vibe
    node["sub_items"] = sub_items
    node["work_logs"] = work_logs
    return node
