/* ─── SIH-26182 — SAHYOG Blockchain Intelligence Dashboard ─── */

// ─── Utility ────────────────────────────────────────────────────────────
function escapeHtml(str) {
  if (str == null) return "";
  return String(str)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;")
    .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

const API = "";
let currentWallet = null;
let currentChain  = "ethereum";
let network       = null;
let sessionCases  = [];

const CHAIN_COLORS = {
  ethereum: "#627EEA", bsc: "#F3BA2F",
  polygon:  "#8247E5", tron: "#EF0027", bitcoin: "#F7931A",
};

const WALLET_TYPE_ICONS = {
  exchange: "🏦", hot_wallet: "🔥", deposit_wallet: "📥",
  mixer: "🌀", defi_bridge: "🌉", cross_chain_swap: "🔀",
  darknet: "🕸️", sanctioned: "🚫", ransomware: "☠️",
  fraud: "⚠️", unknown_wallet: "❓",
};

// ═══════════════════════════════ STARTUP ═══════════════════════════════
(async function init() {
  // Default to demo mode so prototype always works out of the box
  document.getElementById("demoModeToggle").checked = true;
  await checkHealth();
  await loadDashboardStats();
  await loadHistory();
  await loadAlerts();
})();

// ═══════════════════════════════ NAVIGATION ════════════════════════════
function showPanel(name) {
  document.querySelectorAll(".panel-page").forEach(p => p.classList.add("hidden"));
  document.querySelectorAll(".nav-item").forEach(n => n.classList.remove("active"));

  const panelMap = {
    dashboard: "panelDashboard",
    trace:     "panelTrace",
    history:   "panelHistory",
    alerts:    "panelAlerts",
    vasps:     "panelVasps",
  };
  const navMap = {
    dashboard: "navDashboard", trace: "navTrace",
    history:   "navHistory",   alerts: "navAlerts", vasps: "navVasps",
  };
  const titleMap = {
    dashboard: "Dashboard", trace: "New Investigation",
    history:   "Case History", alerts: "Risk Alerts", vasps: "Known VASPs",
  };

  document.getElementById(panelMap[name])?.classList.remove("hidden");
  document.getElementById(navMap[name])?.classList.add("active");
  document.getElementById("pageTitle").textContent = titleMap[name] || name;

  if (name === "history") loadHistory();
  if (name === "alerts")  loadAlerts();
  if (name === "vasps")   loadVasps();
}

function toggleSidebar() {
  document.getElementById("sidebar").classList.toggle("sidebar-hidden");
}

function toggleDemoMode() {
  const cb = document.getElementById("demoModeToggle");
  const dot = document.getElementById("healthDot");
  const text = document.getElementById("healthText");
  if (cb.checked) {
    dot.className = "health-dot warn";
    text.textContent = "Demo mode";
  } else {
    dot.className = "health-dot ok";
    text.textContent = "Live API";
  }
}

// ═══════════════════════════════ HEALTH CHECK ══════════════════════════
async function checkHealth() {
  try {
    const data = await fetchJSON("/api/health");
    const dot  = document.getElementById("healthDot");
    const text = document.getElementById("healthText");
    if (data.api_key_configured) {
      dot.className  = "health-dot ok";
      const vaspK = data.known_vasp_count >= 1000
        ? `${(data.known_vasp_count / 1000).toFixed(0)}k VASPs`
        : `${data.known_vasp_count} VASPs`;
      text.textContent = vaspK;
    } else {
      dot.className  = "health-dot warn";
      text.textContent = "Demo mode";
    }
    document.getElementById("statVaspsVal").textContent =
      data.known_vasp_count.toLocaleString();
    document.getElementById("statChainsVal").textContent =
      (data.supported_chains || []).length;
  } catch (e) {
    document.getElementById("healthDot").className = "health-dot err";
    document.getElementById("healthText").textContent = "Offline";
  }
}

// ═══════════════════════════════ DASHBOARD ═════════════════════════════
async function loadDashboardStats() {
  try {
    const hist = await fetchJSON("/api/history?limit=5");
    sessionCases = hist.cases || [];
    document.getElementById("statCasesVal").textContent = hist.count || 0;
    document.getElementById("caseCounter").textContent  = `${hist.count || 0} Cases`;

    const alertData = await fetchJSON("/api/alerts/high-risk");
    const highCount = alertData.count || 0;
    document.getElementById("statHighRiskVal").textContent = highCount;
    const badge = document.getElementById("alertsBadge");
    if (highCount > 0) {
      badge.textContent = highCount;
      badge.style.display = "inline-block";
    }

    // Recent cases snippet
    const dcEl = document.getElementById("dashboardCases");
    if (sessionCases.length === 0) {
      dcEl.innerHTML = '<p class="muted small">No cases traced this session.</p>';
    } else {
      dcEl.innerHTML = "";
      sessionCases.slice(0, 4).forEach(c => {
        const row = document.createElement("div");
        row.style.cssText = "display:flex;justify-content:space-between;padding:7px 0;border-bottom:1px solid var(--border);font-size:12px;";
        const addr = document.createElement("span");
        addr.className = "mono";
        addr.style.color = "var(--text2)";
        addr.appendChild(document.createTextNode(`${(c.wallet||"").substring(0,16)}…`));
        const pill = document.createElement("span");
        pill.className = `risk-pill ${c.risk?.risk_level || "LOW"}`;
        pill.appendChild(document.createTextNode(c.risk?.risk_level || "LOW"));
        row.appendChild(addr);
        row.appendChild(pill);
        dcEl.appendChild(row);
      });
    }

    // Recent alerts snippet
    const daEl = document.getElementById("dashboardAlerts");
    const alerts = alertData.alerts || [];
    if (alerts.length === 0) {
      daEl.innerHTML = '<p class="muted small">No high-risk alerts yet.</p>';
    } else {
      daEl.innerHTML = "";
      alerts.slice(0, 4).forEach(a => {
        const row = document.createElement("div");
        row.style.cssText = "padding:7px 0;border-bottom:1px solid var(--border);";
        const addrEl = document.createElement("div");
        addrEl.className = "alert-addr";
        addrEl.style.cssText = "font-size:11px;";
        addrEl.appendChild(document.createTextNode(`${(a.wallet||"").substring(0,20)}…`));
        const typoEl = document.createElement("div");
        typoEl.style.cssText = "font-size:11px;color:var(--text3);margin-top:2px;";
        typoEl.appendChild(document.createTextNode((a.typologies||[]).join(", ") || "High risk"));
        row.appendChild(addrEl);
        row.appendChild(typoEl);
        daEl.appendChild(row);
      });
    }
  } catch(e) {}
}

// ═══════════════════════════════ QUICK TRACE ═══════════════════════════
function quickTrace() {
  const addr = document.getElementById("quickWallet").value.trim();
  if (!addr) return;
  document.getElementById("walletInput").value = addr;
  showPanel("trace");
  runTrace();
}

// ═══════════════════════════════ MAIN TRACE ════════════════════════════
async function runTrace() {
  const wallet = document.getElementById("walletInput").value.trim();
  const chain  = document.getElementById("chainSelect").value;
  const hops   = parseInt(document.getElementById("hopsInput").value, 10) || 3;

  if (!wallet) {
    setStatus("Please enter a wallet address.", "error"); return;
  }

  document.getElementById("traceBtn").disabled = true;
  document.getElementById("resultsArea").classList.add("hidden");
  document.getElementById("demoNotice")?.classList.add("hidden");
  setStatus(
    '<div class="spinner"></div> Tracing transaction graph across the blockchain… This may take a few seconds.',
    "loading"
  );

  try {
    const isDemo = document.getElementById("demoModeToggle")?.checked || false;
    const result = await fetchJSON(
      `/api/trace?wallet=${encodeURIComponent(wallet)}&chain=${chain}&max_hops=${hops}&demo_mode=${isDemo}`
    );
    currentWallet = result.wallet;
    currentChain  = result.chain;

    // Show demo mode notice if backend returned synthetic data
    if (result._demo_mode) {
      const notice = document.getElementById("demoNotice");
      if (notice) {
        notice.textContent = "⚡ Demo mode — showing synthetic trace data. Configure ETHERSCAN_API_KEY for live blockchain data.";
        notice.classList.remove("hidden");
      }
    }

    setStatus("", null);
    renderResults(result);
    await loadDashboardStats();
  } catch (e) {
    setStatus(`Error: ${e.message}`, "error");
  } finally {
    document.getElementById("traceBtn").disabled = false;
  }
}

function clearResults() {
  document.getElementById("resultsArea").classList.add("hidden");
  document.getElementById("walletInput").value = "";
  setStatus("", null);
  currentWallet = null;
}

// ═══════════════════════════════ RENDER RESULTS ════════════════════════
function renderResults(result) {
  const area = document.getElementById("resultsArea");
  area.classList.remove("hidden");

  renderRiskBanner(result);
  renderClassification(result);
  renderSahyogRouting(result);
  renderEvidence(result);   // evidence first (full width)
  renderMatches(result);    // VASP attribution (half width)
  renderGraph(result);      // graph (half width)
}

function renderRiskBanner(result) {
  const risk = result.risk || {};
  const lvl  = risk.risk_level || "LOW";
  const score = risk.risk_score || 0;
  const typos = (risk.typologies || []).join("  ·  ");

  const banner = document.getElementById("riskBanner");
  banner.className = `risk-banner ${lvl}`;

  document.getElementById("riskBadge").className = `risk-badge-large ${lvl}`;
  document.getElementById("riskBadge").textContent = `${lvl} RISK`;
  document.getElementById("riskWalletAddr").textContent = result.wallet;
  document.getElementById("riskTypologies").textContent =
    typos || "No suspicious typologies detected";

  const circle = document.getElementById("riskScoreCircle");
  circle.className = `risk-score-circle ${lvl}`;
  circle.textContent = score;
}

function renderClassification(result) {
  const cls = result.wallet_classification || {};
  const type = cls.type || "unknown_wallet";
  const icon = WALLET_TYPE_ICONS[type] || "❓";
  const el = document.getElementById("walletClassification");
  el.innerHTML = "";
  const pill = document.createElement("div");
  pill.className = `classification-pill type-${type}`;
  pill.appendChild(document.createTextNode(`${icon} ${cls.label || "Unknown"}`));
  el.appendChild(pill);
  const p1 = document.createElement("p");
  p1.style.cssText = "font-size:12px;color:var(--text2);margin-top:6px;";
  p1.appendChild(document.createTextNode(cls.reason || "—"));
  el.appendChild(p1);
  const p2 = document.createElement("p");
  p2.style.cssText = "font-size:11px;color:var(--text3);margin-top:8px;";
  p2.innerHTML = `Chain: <b style="color:var(--text)">${escapeHtml(result.chain?.toUpperCase())}</b> &nbsp;·&nbsp; Txs scanned: <b style="color:var(--text)">${result.total_transactions_scanned}</b> &nbsp;·&nbsp; Hops: <b style="color:var(--text)">${result.hops_searched}</b>`;
  el.appendChild(p2);
}

function renderSahyogRouting(result) {
  const r = result.sahyog_routing || {};
  const el = document.getElementById("sahyogRouting");
  el.innerHTML = "";
  const actionEl = document.createElement("div");
  actionEl.className = "sahyog-action";
  actionEl.appendChild(document.createTextNode(r.action || "—"));
  el.appendChild(actionEl);
  const noteEl = document.createElement("div");
  noteEl.className = "sahyog-note";
  noteEl.appendChild(document.createTextNode(r.disclosure_note || ""));
  el.appendChild(noteEl);
  if (r.vasp_name) {
    const vaspEl = document.createElement("div");
    vaspEl.style.cssText = "margin-top:8px;font-size:12px;color:var(--text2);";
    vaspEl.innerHTML = `Target VASP: <b style="color:var(--text)">${escapeHtml(r.vasp_name)}</b>`;
    el.appendChild(vaspEl);
  }
}

function renderMatches(result) {
  const el = document.getElementById("matchesList");
  el.innerHTML = "";
  const matches = result.matches || [];

  if (!matches.length) {
    const p = document.createElement("p");
    p.className = "muted small";
    p.appendChild(document.createTextNode(result.note || "No known VASP match found."));
    el.appendChild(p);
  }
  // Always show PDF button — report is useful even without VASP match
  document.getElementById("reportBtn").classList.remove("hidden");

  matches.slice(0, 8).forEach((m, idx) => {
    const conf = m.confidence;
    const cls  = conf >= 65 ? "c-high" : conf >= 35 ? "c-med" : "c-low";
    const card = document.createElement("div");
    card.className = `match-card${idx === 0 ? " top-match" : ""}`;
    const header = document.createElement("div");
    header.className = "match-header";
    const nameSpan = document.createElement("span");
    nameSpan.className = "match-name";
    nameSpan.appendChild(document.createTextNode(`${idx === 0 ? "⭐ " : ""}${m.vasp_name}`));
    const confPill = document.createElement("span");
    confPill.className = `confidence-pill ${cls}`;
    confPill.appendChild(document.createTextNode(`${conf}%`));
    header.appendChild(nameSpan);
    header.appendChild(confPill);
    card.appendChild(header);
    const barBg = document.createElement("div");
    barBg.className = "progress-bar-bg";
    const barFill = document.createElement("div");
    barFill.className = "progress-bar-fill";
    barFill.style.width = `${conf}%`;
    barBg.appendChild(barFill);
    card.appendChild(barBg);
    const meta = document.createElement("div");
    meta.className = "match-meta";
    meta.appendChild(document.createTextNode(`Hops: ${m.hops}  ·  ${m.address}`));
    card.appendChild(meta);
    const path = document.createElement("div");
    path.className = "path-text";
    path.appendChild(document.createTextNode(m.path.join(" → ")));
    card.appendChild(path);
    el.appendChild(card);
  });

  document.getElementById("reportBtn").classList.remove("hidden");
}

function renderEvidence(result) {
  const el = document.getElementById("evidenceList");
  if (!el) return;
  el.innerHTML = "";

  const items = result.evidence || [];
  if (!items.length) {
    const p = document.createElement("p");
    p.className = "muted small";
    p.appendChild(document.createTextNode("No transaction evidence available."));
    el.appendChild(p);
    return;
  }

  items.forEach(tx => {
    const row = document.createElement("div");
    row.className = "evidence-row";

    const isOut = tx.direction === "outbound";
    const dirClass = isOut ? "ev-dir out" : "ev-dir in";
    const dirText  = isOut ? "OUT" : "IN";

    const left = document.createElement("div");
    left.className = "ev-left";
    left.innerHTML = `<span class="${dirClass}">${dirText}</span>` +
      `<span class="ev-label" title="${escapeHtml(tx.counterparty_label || tx.counterparty || '')}">` +
      `${escapeHtml(tx.counterparty_label || tx.counterparty || '—')}</span>`;

    const right = document.createElement("div");
    right.className = "ev-right";
    const val = document.createElement("span");
    val.className = "ev-value";
    val.appendChild(document.createTextNode(
      (tx.value_eth != null ? parseFloat(tx.value_eth).toFixed(6) : "0.000000") + " ETH"
    ));
    right.appendChild(val);
    const ts = document.createElement("span");
    ts.className = "ev-ts";
    let tsStr = tx.timestamp || "";
    tsStr = tsStr.replace("T", " ").replace("Z", "").replace("+00:00", "");
    ts.appendChild(document.createTextNode(tsStr));
    right.appendChild(ts);

    row.appendChild(left);
    row.appendChild(right);

    if (tx.note) {
      const note = document.createElement("div");
      note.className = "ev-note muted small";
      note.appendChild(document.createTextNode(tx.note));
      row.appendChild(note);
    }

    el.appendChild(row);
  });
}

function renderGraph(result) {
  const container = document.getElementById("graphContainer");
  if (typeof vis === "undefined") {
    container.innerHTML = `<div style="text-align:center;padding:3rem;color:#64748b;font-size:0.9rem;">
      <p style="font-size:1.4rem;">⚠️</p>
      <p>Graph library failed to load. Please check your internet connection.</p></div>`;
    return;
  }
  const risk = result.risk || {};
  const riskLvl = risk.risk_level || "LOW";

  // Legend items
  const LEGEND = [
    { label: "Target (Root)",    color: "#3b82f6", shape: "star" },
    { label: "VASP / Exchange",  color: "#22c55e", shape: "diamond" },
    { label: "Hot Wallet",       color: "#eab308", shape: "triangle" },
    { label: "Deposit Wallet",   color: "#06b6d4", shape: "database" },
    { label: "Mixer",            color: "#ef4444", shape: "hexagon" },
    { label: "Ransomware",       color: "#be123c", shape: "hexagon" },
    { label: "Sanctioned",       color: "#a855f7", shape: "hexagon" },
    { label: "Darknet Market",   color: "#6366f1", shape: "hexagon" },
    { label: "DeFi Bridge",      color: "#f97316", shape: "triangle" },
    { label: "Cross-Chain Swap", color: "#14b8a6", shape: "diamond" },
    { label: "Fraud",            color: "#ec4899", shape: "triangle" },
    { label: "Unknown",          color: "#64748b", shape: "dot" },
  ];

  // Build legend HTML
  const legendEl = document.getElementById("graphLegend");
  if (legendEl) {
    legendEl.innerHTML = LEGEND.map(l =>
      `<span class="legend-item"><span class="legend-dot" style="background:${l.color};"></span>${l.label}</span>`
    ).join("");
  }

  const NODE_COLORS = {
    is_root:         "#3b82f6",  // blue
    exchange:        "#22c55e",  // green
    hot_wallet:      "#eab308",  // yellow
    deposit_wallet:  "#06b6d4",  // cyan
    mixer:           "#ef4444",  // red
    ransomware:      "#be123c",  // rose
    sanctioned:      "#a855f7",  // purple
    darknet:         "#6366f1",  // indigo
    defi_bridge:     "#f97316",  // orange
    cross_chain_swap:"#14b8a6",  // teal
    fraud:           "#ec4899",  // pink
    unknown_wallet:  "#64748b",  // slate
  };

  const NODE_SHAPES = {
    is_root:         "star",
    exchange:        "diamond",
    hot_wallet:      "triangle",
    mixer:           "hexagon",
    ransomware:      "hexagon",
    darknet:         "hexagon",
    sanctioned:      "hexagon",
    defi_bridge:     "triangle",
    cross_chain_swap:"diamond",
    deposit_wallet:  "database",
    fraud:           "triangle",
    unknown_wallet:  "dot",
  };

  // Build nodes — label with readable names
  const nodes = (result.nodes || []).map(n => {
    const wType = n.wallet_type || "unknown_wallet";
    const label = n.is_root
      ? "🎯 TARGET"
      : (n.is_known_vasp ? (n.vasp_name || n.label || n.id.substring(0,8)) : (n.label || wType.replace(/_/g, " ") || n.id.substring(0,8)));
    const color  = n.is_root ? "#4f8cff" : (NODE_COLORS[wType] || (n.is_known_vasp ? "#22c55e" : "#64748b"));
    const shape  = n.is_root ? "star" : (NODE_SHAPES[wType] || (n.is_known_vasp ? "diamond" : "dot"));
    const size   = n.is_root ? 28 : (n.is_known_vasp ? 20 : 12);
    const tooltip = `<b>${label}</b><br>` +
      `Type: ${wType.replace(/_/g, " ")}<br>` +
      `${n.is_known_vasp ? "✅ Known VASP: " + (n.vasp_name || "") + "<br>" : ""}` +
      `Address: ${n.id}<br>` +
      `Risk: ${riskLvl}`;

    return {
      id:    n.id,
      label: label,
      color: color,
      shape: shape,
      size:  size,
      font:  { color: "#e2e8f0", size: n.is_root ? 12 : 10, face: "Inter, sans-serif" },
      title: tooltip,
      borderWidth: n.is_root ? 4 : 2,
      borderWidthSelected: 6,
    };
  });

  // Build edges — only keep edges where both endpoints exist
  const nodeIds = new Set(nodes.map(n => n.id));
  const edgeSet = new Set();
  const edges = [];
  (result.edges || []).forEach(e => {
    if (!nodeIds.has(e.source) || !nodeIds.has(e.target)) return;
    const key = `${e.source}->${e.target}`;
    if (edgeSet.has(key)) return;
    edgeSet.add(key);
    const hasValue = e.value_eth > 0.001;
    edges.push({
      from:   e.source,
      to:     e.target,
      arrows: { to: { enabled: true, scaleFactor: 0.6 }},
      color:  { color: hasValue ? "#3b82f6" : "#1e2d45", highlight: "#60a5fa", hover: "#3b82f6" },
      width:  hasValue ? 2 : 1,
      label:  hasValue ? `${e.value_eth.toFixed(4)} ETH` : "",
      font:   { size: 8, color: "#94a3b8", strokeWidth: 0, face: "JetBrains Mono, monospace" },
      smooth: { type: "continuous" },
    });
  });

  if (network) network.destroy();

  const data = { nodes: new vis.DataSet(nodes), edges: new vis.DataSet(edges) };

  const options = {
    physics: {
      stabilization: { iterations: 200, fit: true },
      barnesHut: { gravitationalConstant: -3500, springLength: 100, springConstant: 0.04 },
    },
    interaction: {
      hover: true,
      tooltipDelay: 80,
      navigationButtons: false,
      keyboard: { enabled: true },
      multiselect: true,
    },
    layout: { improvedLayout: true },
    edges: { selectionWidth: 3 },
  };

  network = new vis.Network(container, data, options);

  // Click-to-highlight: highlight the clicked node and its neighbors
  network.on("click", function(params) {
    if (params.nodes.length === 0) {
      data.nodes.update(nodes.map(n => ({ id: n.id, opacity: 1.0 })));
      data.edges.update(edges.map(e => ({ id: `${e.from}->${e.to}`, width: e.width || 1, color: { color: "#1e2d45", highlight: "#3b82f6" } })));
      return;
    }
    const clickedId = params.nodes[0];
    // Find all neighbors
    const connected = network.getConnectedNodes(clickedId);
    const connectedSet = new Set(connected);
    connectedSet.add(clickedId);

    // Dim everything else
    data.nodes.update(nodes.map(n => ({
      id: n.id,
      opacity: connectedSet.has(n.id) ? 1.0 : 0.15,
      hidden: !connectedSet.has(n.id),
    })));

    data.edges.update(edges.map(e => {
      const isConnected = (e.from === clickedId || e.to === clickedId);
      return {
        id: `${e.from}->${e.to}`,
        hidden: !isConnected,
        width: isConnected ? 3 : 1,
        color: isConnected ? { color: "#60a5fa", highlight: "#93c5fd" } : { color: "#1e2d45" },
      };
    }));
  });

  network.on("deselectNode", function() {
    data.nodes.update(nodes.map(n => ({ id: n.id, opacity: 1.0, hidden: false })));
    data.edges.update(edges.map(e => ({
      id: `${e.from}->${e.to}`,
      hidden: false,
      width: (e.value_eth > 0.001 ? 2 : 1),
      color: { color: (e.value_eth > 0.001 ? "#3b82f6" : "#1e2d45"), highlight: "#60a5fa" },
    })));
  });
}

// ═══════════════════════════════ HISTORY ═══════════════════════════════
async function loadHistory() {
  const chain = document.getElementById("historyChainFilter")?.value || "";
  const risk  = document.getElementById("historyRiskFilter")?.value  || "";
  let url = `/api/history?limit=50`;
  if (chain) url += `&chain=${chain}`;
  if (risk)  url += `&risk_level=${risk}`;

  try {
    const data  = await fetchJSON(url);
    const cases = data.cases || [];
    const el    = document.getElementById("historyTable");

    if (!cases.length) {
      el.innerHTML = '<p class="muted small">No cases match the filter.</p>';
      return;
    }

    el.innerHTML = `
      <table class="history-table">
        <thead><tr>
          <th>Wallet</th><th>Chain</th><th>Type</th>
          <th>Risk</th><th>VASP Match</th><th>Confidence</th><th>Time</th>
        </tr></thead>
        <tbody>
          ${cases.map(c => {
            const lvl  = c.risk?.risk_level || "LOW";
            const top  = c.top_match;
            const cls  = c.wallet_classification;
            const ts   = c.timestamp ? new Date(c.timestamp).toLocaleTimeString() : "—";
            return `<tr>
              <td class="mono-cell">${c.wallet.substring(0,18)}…</td>
              <td><span class="chain-badge">${(c.chain||"ETH").toUpperCase()}</span></td>
              <td style="font-size:12px;">${WALLET_TYPE_ICONS[cls?.type]||"❓"} ${cls?.label||"—"}</td>
              <td><span class="risk-pill ${lvl}">${lvl}</span></td>
              <td style="font-size:12px;">${top?.vasp_name||"—"}</td>
              <td style="font-size:12px;">${top ? top.confidence+"%" : "—"}</td>
              <td style="font-size:11px;color:var(--text3);">${ts}</td>
            </tr>`;
          }).join("")}
        </tbody>
      </table>`;
  } catch(e) {
    document.getElementById("historyTable").innerHTML =
      '<p class="muted small">Failed to load history.</p>';
  }
}

// ═══════════════════════════════ ALERTS ════════════════════════════════
async function loadAlerts() {
  try {
    const data   = await fetchJSON("/api/alerts/high-risk");
    const alerts = data.alerts || [];
    const el     = document.getElementById("alertsList");
    const badge  = document.getElementById("alertsBadge");

    if (alerts.length > 0) {
      badge.textContent = alerts.length;
      badge.style.display = "inline-block";
    }

    if (!alerts.length) {
      el.innerHTML = '<p class="muted">No high-risk wallets flagged yet.</p>';
      return;
    }
    el.innerHTML = alerts.map(a => `
      <div class="alert-item">
        <div>
          <div class="alert-addr">${a.wallet}</div>
          <div class="alert-meta">
            <span class="chain-badge">${(a.chain||"ETH").toUpperCase()}</span> &nbsp;
            ${(a.typologies||[]).join(" · ") || "High Risk"}
          </div>
        </div>
        <div style="text-align:right;flex-shrink:0;">
          <span class="risk-pill HIGH">HIGH</span>
          <div style="font-size:11px;color:var(--text3);margin-top:4px;">
            ${a.vasp_match || "No VASP match"}
          </div>
          <div style="font-size:10px;color:var(--text3);margin-top:2px;">
            ${a.timestamp ? new Date(a.timestamp).toLocaleTimeString() : ""}
          </div>
        </div>
      </div>`).join("");
  } catch(e) {}
}

// ═══════════════════════════════ VASPs ═════════════════════════════════
async function loadVasps(search = "") {
  try {
    const url  = `/api/vasps?limit=100${search ? "&search="+encodeURIComponent(search) : ""}`;
    const data = await fetchJSON(url);
    document.getElementById("vaspCount").textContent =
      `Showing ${data.vasps.length} of ${data.count.toLocaleString()} total`;

    const el = document.getElementById("vaspList");
    if (!data.vasps.length) {
      el.innerHTML = '<p class="muted small">No results.</p>'; return;
    }
    el.innerHTML = `
      <table class="vasp-table">
        <thead><tr><th>Address</th><th>Name / Label</th></tr></thead>
        <tbody>
          ${data.vasps.map(v => `<tr>
            <td class="vasp-addr">${v.address}</td>
            <td style="font-size:13px;">${v.name}</td>
          </tr>`).join("")}
        </tbody>
      </table>`;
  } catch(e) {
    document.getElementById("vaspList").innerHTML = '<p class="muted small">Failed to load VASPs.</p>';
  }
}

function searchVasps() {
  const q = document.getElementById("vaspSearch").value.trim();
  loadVasps(q);
}

// ═══════════════════════════════ SAHYOG SUBMIT ═════════════════════════
async function submitToSahyog() {
  if (!currentWallet) return;
  try {
    const data = await fetchJSON(
      `/api/sahyog/submit?wallet=${encodeURIComponent(currentWallet)}&chain=${currentChain}`,
      { method: "POST" }
    );
    alert(`✅ SAHYOG Submitted\n\nReference ID: ${data.reference_id}\n\n${data.message}`);
  } catch(e) {
    alert(`❌ SAHYOG submission failed: ${e.message}`);
  }
}

// ═══════════════════════════════ PDF REPORT ════════════════════════════
function downloadReport() {
  if (!currentWallet) return;
  window.open(`${API}/api/report/${currentWallet}?chain=${currentChain}`, "_blank");
}

// ═══════════════════════════════ UTILITY ═══════════════════════════════
function setStatus(msg, type) {
  const el = document.getElementById("statusArea");
  if (!msg) { el.innerHTML = ""; return; }
  el.innerHTML = `<div class="status-msg ${type}">${msg}</div>`;
}

async function fetchJSON(url, opts = {}) {
  const res = await fetch(API + url, opts);
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }
  return res.json();
}

// Keyboard shortcuts
document.addEventListener("keydown", e => {
  if (e.key === "Enter" && document.activeElement.id === "walletInput") runTrace();
  if (e.key === "Enter" && document.activeElement.id === "quickWallet") quickTrace();
});
