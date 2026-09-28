"""
CryptoGuard AI - SQLite Database Layer
Handles persistent storage for investigations, wallets, transactions,
VASPs, evidence items, timeline events, and audit logs.
"""

from __future__ import annotations
import sqlite3
import json
import os
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "cryptoguard.db")


def get_db_connection() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initializes tables and indexes."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Investigations
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS investigations (
        id TEXT PRIMARY KEY,
        case_ref TEXT,
        complaint_no TEXT,
        wallet_address TEXT NOT NULL,
        chain TEXT NOT NULL,
        status TEXT DEFAULT 'ACTIVE',
        risk_level TEXT,
        risk_score INTEGER DEFAULT 0,
        top_vasp TEXT,
        vasp_confidence REAL DEFAULT 0.0,
        hops_searched INTEGER DEFAULT 3,
        total_transactions INTEGER DEFAULT 0,
        is_demo INTEGER DEFAULT 0,
        investigator_notes TEXT DEFAULT '',
        result_json TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_inv_wallet ON investigations(wallet_address);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_inv_created ON investigations(created_at);")

    # 2. Wallets
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS wallets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        address TEXT NOT NULL UNIQUE,
        chain TEXT NOT NULL,
        wallet_type TEXT DEFAULT 'unknown_wallet',
        label TEXT,
        risk_score INTEGER DEFAULT 0,
        is_vasp INTEGER DEFAULT 0,
        vasp_name TEXT,
        first_seen TEXT,
        last_seen TEXT
    );
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_wallets_addr ON wallets(address);")

    # 3. Transactions
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        investigation_id TEXT NOT NULL,
        tx_hash TEXT NOT NULL,
        chain TEXT NOT NULL,
        from_address TEXT NOT NULL,
        to_address TEXT NOT NULL,
        value_eth REAL DEFAULT 0.0,
        block_number INTEGER DEFAULT 0,
        timestamp TEXT NOT NULL,
        note TEXT DEFAULT '',
        FOREIGN KEY (investigation_id) REFERENCES investigations(id)
    );
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tx_inv ON transactions(investigation_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tx_hash ON transactions(tx_hash);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tx_from ON transactions(from_address);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tx_to ON transactions(to_address);")

    # 4. VASPs Directory
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vasps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT DEFAULT 'Centralized Exchange',
        fiu_registered INTEGER DEFAULT 0,
        country TEXT DEFAULT 'Global',
        compliance_email TEXT DEFAULT '',
        address TEXT NOT NULL UNIQUE,
        chain TEXT DEFAULT 'ethereum',
        notes TEXT DEFAULT ''
    );
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_vasp_addr ON vasps(address);")

    # 5. Evidence Items
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS evidence (
        id TEXT PRIMARY KEY,
        investigation_id TEXT NOT NULL,
        evidence_type TEXT NOT NULL,
        wallet_address TEXT,
        tx_hash TEXT,
        timestamp TEXT NOT NULL,
        description TEXT NOT NULL,
        source TEXT NOT NULL,
        status TEXT DEFAULT 'Relevant',
        notes TEXT DEFAULT '',
        FOREIGN KEY (investigation_id) REFERENCES investigations(id)
    );
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ev_inv ON evidence(investigation_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ev_status ON evidence(status);")

    # 6. Investigation Events (Timeline)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS timeline_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        investigation_id TEXT NOT NULL,
        event_time TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        event_type TEXT DEFAULT 'transfer',
        wallet_address TEXT,
        tx_hash TEXT,
        amount REAL DEFAULT 0.0,
        FOREIGN KEY (investigation_id) REFERENCES investigations(id)
    );
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_timeline_inv ON timeline_events(investigation_id);")

    # 7. Audit Logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        action TEXT NOT NULL,
        investigation_id TEXT,
        details TEXT
    );
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_time ON audit_logs(timestamp);")

    conn.commit()
    conn.close()


def save_investigation(
    inv_id: str,
    wallet: str,
    chain: str,
    case_ref: str,
    complaint_no: str,
    trace_data: dict,
    is_demo: bool = False
) -> None:
    """Persists an entire investigation result into SQLite."""
    conn = get_db_connection()
    cursor = conn.cursor()
    now_iso = datetime.now(timezone.utc).isoformat()

    risk = trace_data.get("risk", {})
    top_match = trace_data.get("top_match", {})
    top_vasp_name = top_match.get("vasp_name") if top_match else None
    vasp_conf = top_match.get("confidence", 0.0) if top_match else 0.0

    cursor.execute("""
    INSERT OR REPLACE INTO investigations (
        id, case_ref, complaint_no, wallet_address, chain, status,
        risk_level, risk_score, top_vasp, vasp_confidence, hops_searched,
        total_transactions, is_demo, investigator_notes, result_json,
        created_at, updated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        inv_id,
        case_ref,
        complaint_no,
        wallet.lower(),
        chain.lower(),
        "ACTIVE",
        risk.get("risk_level", "LOW"),
        risk.get("risk_score", 0),
        top_vasp_name,
        vasp_conf,
        trace_data.get("hops_searched", 3),
        trace_data.get("total_transactions_scanned", 0),
        1 if is_demo else 0,
        "",
        json.dumps(trace_data),
        now_iso,
        now_iso
    ))

    # Persist Transactions
    edges = trace_data.get("edges", [])
    for e in edges:
        cursor.execute("""
        INSERT INTO transactions (
            investigation_id, tx_hash, chain, from_address, to_address, value_eth, timestamp
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            inv_id,
            e.get("tx_hash", "0x" + os.urandom(8).hex()),
            chain.lower(),
            e.get("source", "").lower(),
            e.get("target", "").lower(),
            float(e.get("value_eth", 0.0)),
            now_iso
        ))

    # Persist Evidence
    evidence_list = trace_data.get("evidence", [])
    for idx, ev in enumerate(evidence_list):
        ev_id = f"EV-{inv_id[-6:]}-{idx+1:02d}"
        cursor.execute("""
        INSERT OR REPLACE INTO evidence (
            id, investigation_id, evidence_type, wallet_address, tx_hash,
            timestamp, description, source, status, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            ev_id,
            inv_id,
            "transaction" if ev.get("tx_hash") else "attribution",
            ev.get("counterparty") or wallet,
            ev.get("tx_hash") or "",
            ev.get("timestamp") or now_iso,
            ev.get("note") or f"Transaction involving {ev.get('counterparty_label') or ev.get('counterparty')}",
            "On-Chain Trace Engine" if not is_demo else "Deterministic Demo Fixture",
            "Relevant",
            ""
        ))

    # Persist Timeline Events
    timeline_events = trace_data.get("timeline", [])
    if not timeline_events and evidence_list:
        for ev in evidence_list:
            timeline_events.append({
                "time": ev.get("timestamp", now_iso),
                "title": f"Flow {ev.get('direction', 'outbound').upper()}",
                "desc": f"Observed {ev.get('value_eth', 0)} ETH to {ev.get('counterparty_label', ev.get('counterparty'))}",
                "type": "outflow" if ev.get("direction") == "outbound" else "inflow",
                "wallet": ev.get("counterparty"),
                "tx_hash": ev.get("tx_hash"),
                "amount": float(ev.get("value_eth", 0.0))
            })

    for te in timeline_events:
        cursor.execute("""
        INSERT INTO timeline_events (
            investigation_id, event_time, title, description, event_type, wallet_address, tx_hash, amount
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            inv_id,
            te.get("time", now_iso),
            te.get("title", "Fund Transfer"),
            te.get("desc", ""),
            te.get("type", "transfer"),
            te.get("wallet", ""),
            te.get("tx_hash", ""),
            float(te.get("amount", 0.0))
        ))

    # Log Audit
    cursor.execute("""
    INSERT INTO audit_logs (timestamp, action, investigation_id, details)
    VALUES (?, ?, ?, ?)
    """, (
        now_iso,
        "INVESTIGATION_CREATED",
        inv_id,
        f"Investigation initiated for wallet {wallet} on chain {chain} (Demo: {is_demo})"
    ))

    conn.commit()
    conn.close()


def get_investigations(limit: int = 50, chain: Optional[str] = None, risk: Optional[str] = None) -> List[Dict]:
    """Retrieves investigations list from SQLite."""
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM investigations WHERE 1=1"
    params = []

    if chain:
        query += " AND chain = ?"
        params.append(chain.lower())
    if risk:
        query += " AND risk_level = ?"
        params.append(risk.upper())

    query += " ORDER BY created_at DESC LIMIT ?"
    params.append(limit)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_investigation_by_id(inv_id: str) -> Optional[Dict]:
    """Retrieves full investigation including parsed result JSON."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM investigations WHERE id = ?", (inv_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    data = dict(row)
    if data.get("result_json"):
        try:
            data["result"] = json.loads(data["result_json"])
        except Exception:
            data["result"] = {}
    return data


def update_evidence_status(evidence_id: str, status: str, notes: str = "") -> bool:
    """Updates evidence verification status."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE evidence
    SET status = ?, notes = CASE WHEN ? != '' THEN ? ELSE notes END
    WHERE id = ?
    """, (status, notes, notes, evidence_id))
    affected = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return affected


def get_evidence_for_investigation(inv_id: str) -> List[Dict]:
    """Retrieves all evidence items for a given investigation."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM evidence WHERE investigation_id = ? ORDER BY id ASC", (inv_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_timeline_for_investigation(inv_id: str) -> List[Dict]:
    """Retrieves chronological timeline for a given investigation."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM timeline_events WHERE investigation_id = ? ORDER BY event_time ASC", (inv_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_dashboard_metrics() -> Dict[str, Any]:
    """Aggregates real-time statistics from SQLite database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM investigations")
    total_cases = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM investigations WHERE risk_level = 'HIGH'")
    high_risk = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM investigations WHERE risk_level = 'MEDIUM'")
    medium_risk = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM investigations WHERE top_vasp IS NOT NULL AND top_vasp != ''")
    vasp_hits = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT wallet_address) FROM investigations")
    wallets_analyzed = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM vasps")
    known_vasps = cursor.fetchone()[0]

    cursor.execute("SELECT * FROM investigations ORDER BY created_at DESC LIMIT 5")
    recent = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return {
        "total_cases": total_cases,
        "high_risk_count": high_risk,
        "medium_risk_count": medium_risk,
        "low_risk_count": max(0, total_cases - high_risk - medium_risk),
        "vasp_hits": vasp_hits,
        "wallets_analyzed": wallets_analyzed,
        "known_vasp_count": known_vasps,
        "recent_investigations": recent
    }


def seed_vasps_if_empty(vasp_dict: Dict[str, Dict]):
    """Seeds VASP directory table if empty."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM vasps")
    count = cursor.fetchone()[0]
    if count == 0:
        for addr, meta in vasp_dict.items():
            cursor.execute("""
            INSERT OR IGNORE INTO vasps (
                name, category, fiu_registered, country, compliance_email, address, chain, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                meta.get("name", "Unknown VASP"),
                meta.get("category", "Centralized Exchange"),
                1 if meta.get("fiu_registered") else 0,
                meta.get("country", "Global"),
                meta.get("compliance_email", ""),
                addr.lower(),
                meta.get("chain", "ethereum"),
                meta.get("notes", "")
            ))
        conn.commit()
    conn.close()
