/* ─── SIH-26182 — SAHYOG Blockchain Intelligence Dashboard ─── */

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
  document.getElementById("sidebar").classList.toggle("open");
}

// ═══════════════════════════════ HEALTH CHECK ══════════════════════════
async function checkHealth() {
  try {
    const data = await fetchJSON("/api/health");
    const dot  = document.getElementById("healthDot");
    const text = document.getElementById("healthText");
    if (data.api_key_configured) {
      dot.className  = "health-dot ok";
      text.textContent = `${(data.known_vasp_count / 1000).toFixed(0)}k VASPs`;
    } else {
      dot.className  = "health-dot err";
      text.textContent = "No API key";
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
      dcEl.innerHTML = sessionCases.slice(0, 4).map(c => {
        const lvl = c.risk?.risk_level || "LOW";
        return `<div style="display:flex;justify-content:space-between;padding:7px 0;border-bottom:1px solid var(--border);font-size:12px;">
          <span class="mono" style="color:var(--text2)">${c.wallet.substring(0,16)}…</span>
          <span class="risk-pill ${lvl}">${lvl}</span>
        </div>`;
      }).join("");
    }

    // Recent alerts snippet
    const daEl = document.getElementById("dashboardAlerts");
    const alerts = alertData.alerts || [];
    if (alerts.length === 0) {
      daEl.innerHTML = '<p class="muted small">No high-risk alerts yet.</p>';
    } else {
      daEl.innerHTML = alerts.slice(0, 4).map(a =>
        `<div style="padding:7px 0;border-bottom:1px solid var(--border);">
          <div class="alert-addr" style="font-size:11px;">${a.wallet.substring(0,20)}…</div>
          <div style="font-size:11px;color:var(--text3);margin-top:2px;">${(a.typologies||[]).join(", ") || "High risk"}</div>
        </div>`
      ).join("");
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
  setStatus(
    '<div class="spinner"></div> Tracing transaction graph across the blockchain… This may take a few seconds.',
    "loading"
  );

  try {
    const result = await fetchJSON(
      `/api/trace?wallet=${encodeURIComponent(wallet)}&chain=${chain}&max_hops=${hops}`
    );
    currentWallet = result.wallet;
    currentChain  = result.chain;
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
  renderMatches(result);
  renderGraph(result);
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
  el.innerHTML = `
    <div class="classification-pill type-${type}">${icon} ${cls.label || "Unknown"}</div>
    <p style="font-size:12px;color:var(--text2);margin-top:6px;">${cls.reason || "—"}</p>
    <p style="font-size:11px;color:var(--text3);margin-top:8px;">
      Chain: <b style="color:var(--text)">${result.chain?.toUpperCase()}</b> &nbsp;·&nbsp;
      Txs scanned: <b style="color:var(--text)">${result.total_transactions_scanned}</b> &nbsp;·&nbsp;
      Hops: <b style="color:var(--text)">${result.hops_searched}</b>
    </p>`;
}

function renderSahyogRouting(result) {
  const r = result.sahyog_routing || {};
  const el = document.getElementById("sahyogRouting");
  el.innerHTML = `
    <div class="sahyog-action">${r.action || "—"}</div>
    <div class="sahyog-note">${r.disclosure_note || ""}</div>
    ${r.vasp_name ? `<div style="margin-top:8px;font-size:12px;color:var(--text2);">
      Target VASP: <b style="color:var(--text)">${r.vasp_name}</b></div>` : ""}`;
}

function renderMatches(result) {
  const el = document.getElementById("matchesList");
  el.innerHTML = "";
  const matches = result.matches || [];

  if (!matches.length) {
    el.innerHTML = `<p class="muted small">${result.note || "No known VASP match found."}</p>`;
    document.getElementById("reportBtn").classList.add("hidden");
    return;
  }

  matches.slice(0, 8).forEach((m, idx) => {
    const conf = m.confidence;
    const cls  = conf >= 65 ? "c-high" : conf >= 35 ? "c-med" : "c-low";
    const card = document.createElement("div");
    card.className = `match-card${idx === 0 ? " top-match" : ""}`;
    card.innerHTML = `
      <div class="match-header">
        <span class="match-name">${idx === 0 ? "⭐ " : ""}${m.vasp_name}</span>
        <span class="confidence-pill ${cls}">${conf}%</span>
      </div>
      <div class="progress-bar-bg">
        <div class="progress-bar-fill" style="width:${conf}%"></div>
      </div>
      <div class="match-meta">Hops: ${m.hops} &nbsp;·&nbsp; ${m.address}</div>
      <div class="path-text">${m.path.join(" → ")}</div>`;
    el.appendChild(card);
  });

  document.getElementById("reportBtn").classList.remove("hidden");
}

function renderGraph(result) {
  const container = document.getElementById("graphContainer");

  // Guard: vis-network library must be loaded
  if (typeof vis === "undefined") {
    container.innerHTML = `
      <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
                  height:100%;color:var(--text3);font-size:13px;gap:10px;padding:20px;text-align:center;">
        <span style="font-size:32px;">📡</span>
        <b style="color:var(--text2);">Graph library failed to load</b>
        <span>Check your internet connection or reload the page.</span>
        <button class="btn-secondary" style="margin-top:8px;"
          onclick="location.reload()">↺ Reload Page</button>
      </div>`;
    return;
  }

  // Clear previous content and show loading state
  container.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;height:100%;color:var(--text3);font-size:13px;"><div class="spinner"></div>&nbsp; Rendering graph…</div>';

  // Delay initialization so the browser can reflow and the container gets real dimensions
  requestAnimationFrame(() => {
    setTimeout(() => _initVisGraph(result, container), 100);
  });
}

function _initVisGraph(result, container) {
  const NODE_COLORS = {
    is_root:          "#4f8cff",
    exchange:         "#22c55e",
    hot_wallet:       "#f59e0b",
    mixer:            "#ef4444",
    ransomware:       "#ef4444",
    darknet:          "#a78bfa",
    sanctioned:       "#ef4444",
    defi_bridge:      "#f97316",
    cross_chain_swap: "#c4b5fd",
    deposit_wallet:   "#3b82f6",
    fraud:            "#f97316",
    unknown_wallet:   "#334059",
  };

  // Limit nodes for performance (keep root + VASPs + high-risk first, then fill)
  let rawNodes = result.nodes || [];
  const MAX_NODES = 150;
  if (rawNodes.length > MAX_NODES) {
    const priority = rawNodes.filter(n => n.is_root || n.is_known_vasp || n.wallet_type === "mixer" || n.wallet_type === "sanctioned");
    const rest     = rawNodes.filter(n => !n.is_root && !n.is_known_vasp && n.wallet_type !== "mixer" && n.wallet_type !== "sanctioned");
    rawNodes = [...priority, ...rest].slice(0, MAX_NODES);
  }

  const nodeIdSet = new Set(rawNodes.map(n => n.id));

  // Map for quick node-data lookup on hover
  const nodeDataMap = new Map(rawNodes.map(n => [n.id, n]));

  const nodes = rawNodes.map(n => ({
    id:    n.id,
    label: n.is_root ? "🎯 TARGET" : (n.label || n.id.substring(0, 8)),
    color: n.is_root
      ? "#4f8cff"
      : (NODE_COLORS[n.wallet_type] || (n.is_known_vasp ? "#22c55e" : "#334059")),
    font:  { color: "#e2e8f0", size: 10 },
    shape: n.is_root
      ? "star"
      : (n.is_known_vasp ? "diamond" : (n.wallet_type === "mixer" ? "hexagon" : "dot")),
    size:  n.is_root ? 28 : (n.is_known_vasp ? 20 : 10),
    // No title — we use our own custom tooltip below
    borderWidth: n.is_root ? 3 : 1,
    borderWidthSelected: 4,
  }));

  // Deduplicate and filter edges to only nodes in our set
  const edgeSet = new Set();
  const edges   = [];
  const MAX_EDGES = 200;
  for (const e of (result.edges || [])) {
    if (edges.length >= MAX_EDGES) break;
    const key = `${e.source}->${e.target}`;
    if (edgeSet.has(key)) continue;
    // Only include edges whose both endpoints are in our visible node set
    if (!nodeIdSet.has(e.source) || !nodeIdSet.has(e.target)) continue;
    edgeSet.add(key);
    edges.push({
      from:   e.source,
      to:     e.target,
      arrows: "to",
      color:  { color: "#1e2d45", highlight: "#3b82f6" },
      label:  e.value_eth > 0.001 ? `${e.value_eth.toFixed(4)}` : "",
      font:   { size: 8, color: "#64748b", strokeWidth: 0 },
    });
  }

  // Clear loading message
  container.innerHTML = "";

  const data = {
    nodes: new vis.DataSet(nodes),
    edges: new vis.DataSet(edges),
  };

  const isLargeGraph = nodes.length > 80;

  const options = {
    physics: {
      enabled: true,
      stabilization: {
        enabled: true,
        iterations: isLargeGraph ? 80 : 150,
        updateInterval: 25,
      },
      barnesHut: {
        gravitationalConstant: isLargeGraph ? -2000 : -4000,
        springLength: isLargeGraph ? 120 : 80,
        springConstant: 0.04,
        damping: 0.3,
      },
    },
    interaction: { hover: true, tooltipDelay: 9999999, zoomView: true, dragView: true },
    layout: {
      improvedLayout: nodes.length < 50,
      randomSeed: 42,
    },
  };

  if (network) network.destroy();
  network = new vis.Network(container, data, options);

  // ── Custom tooltip ──────────────────────────────────────────────────────
  // Create a single floating tooltip div reused for every node
  let graphTooltip = document.getElementById("graphTooltip");
  if (!graphTooltip) {
    graphTooltip = document.createElement("div");
    graphTooltip.id = "graphTooltip";
    graphTooltip.style.cssText = [
      "position:fixed",
      "z-index:9999",
      "pointer-events:none",
      "display:none",
      "background:#0d1b2e",
      "border:1px solid #2563eb",
      "border-radius:10px",
      "padding:10px 14px",
      "font-family:Inter,sans-serif",
      "font-size:12px",
      "color:#e2e8f0",
      "line-height:1.65",
      "max-width:280px",
      "box-shadow:0 8px 32px rgba(0,0,0,.7)",
    ].join(";");
    document.body.appendChild(graphTooltip);
  }

  // Track mouse position relative to viewport
  container.addEventListener("mousemove", (e) => {
    const pad = 16;
    let x = e.clientX + pad;
    let y = e.clientY + pad;
    // Keep tooltip inside viewport
    if (x + 300 > window.innerWidth)  x = e.clientX - 300 - pad;
    if (y + 160 > window.innerHeight) y = e.clientY - 160 - pad;
    graphTooltip.style.left = x + "px";
    graphTooltip.style.top  = y + "px";
  });

  network.on("hoverNode", ({ node }) => {
    const n = nodeDataMap.get(node);
    if (!n) return;
    const typeLabel = (n.wallet_type || "unknown_wallet").replace(/_/g, " ");
    const fullAddr  = n.label || n.id;
    const shortAddr = fullAddr.length > 20
      ? fullAddr.substring(0, 10) + "…" + fullAddr.slice(-6)
      : fullAddr;

    let badge = "";
    if (n.is_root)       badge = `<span style="background:#1e3a5f;color:#60a5fa;border-radius:4px;padding:1px 6px;font-size:10px;margin-left:6px;">🎯 Target</span>`;
    else if (n.is_known_vasp) badge = `<span style="background:#14532d;color:#4ade80;border-radius:4px;padding:1px 6px;font-size:10px;margin-left:6px;">✅ VASP</span>`;

    graphTooltip.innerHTML = `
      <div style="font-weight:700;color:#60a5fa;margin-bottom:6px;display:flex;align-items:center;gap:4px;">
        <span style="font-family:monospace;font-size:11px;">${shortAddr}</span>${badge}
      </div>
      <div style="display:flex;gap:16px;">
        <span style="color:#94a3b8;">Type</span>
        <span style="color:#e2e8f0;font-weight:500;text-transform:capitalize;">${typeLabel}</span>
      </div>`;
    graphTooltip.style.display = "block";
  });

  network.on("blurNode", () => { graphTooltip.style.display = "none"; });
  network.on("dragStart", () => { graphTooltip.style.display = "none"; });
  network.on("zoom",      () => { graphTooltip.style.display = "none"; });
  // ────────────────────────────────────────────────────────────────────────

  // Stop physics after stabilization to prevent ongoing CPU use
  network.on("stabilizationIterationsDone", () => {
    network.setOptions({ physics: { enabled: false } });
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
