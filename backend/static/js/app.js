/**
 * CryptoGuard AI — Investigation & VASP Attribution Console
 * Professional Frontend Client Logic
 */

// ── Application State ──
const STATE = {
  currentView: "dashboard",
  currentWsTab: "overview",
  demoMode: true,
  activeInvestigation: null,
  network: null,
  graphData: { nodes: null, edges: null, rawNodes: [], rawEdges: [] },
  vaspDirectory: [],
  fiuFilterActive: false
};

const DEMO_WALLET = "0x742d35cc6634c0532925a3b844bc454e4438f44e";

// ── Startup ──
document.addEventListener("DOMContentLoaded", async () => {
  await initHealth();
  await loadDashboardMetrics();
  await loadRecentInvestigations();
  await loadHighRiskAlerts();
  await loadVaspDirectory();

  // Pre-load demo investigation for immediate access
  await runInvestigation(DEMO_WALLET, "ethereum", 3, "NCRP-2026-849102", true, false);
});

// ═══════════════════════════════ NAVIGATION ═══════════════════════════
function navigateTo(viewName) {
  STATE.currentView = viewName;
  document.querySelectorAll("main > section").forEach(sec => sec.classList.add("hidden"));
  document.querySelectorAll(".top-nav .nav-link").forEach(btn => btn.classList.remove("active"));

  if (viewName === "dashboard") {
    document.getElementById("viewDashboard").classList.remove("hidden");
    document.getElementById("navDashboard")?.classList.add("active");
    loadDashboardMetrics();
    loadRecentInvestigations();
  } else if (viewName === "workspace") {
    document.getElementById("viewWorkspace").classList.remove("hidden");
    document.getElementById("navWorkspace")?.classList.add("active");
    if (!STATE.activeInvestigation) {
      loadDemoTarget();
    } else {
      renderActiveInvestigation();
    }
  } else if (viewName === "vasps") {
    document.getElementById("viewVasps").classList.remove("hidden");
    document.getElementById("navVasps")?.classList.add("active");
    renderVaspDirectory();
  } else if (viewName === "reports") {
    document.getElementById("viewReports").classList.remove("hidden");
    document.getElementById("navReports")?.classList.add("active");
    loadReportsView();
  }
}

function switchWsTab(tabName) {
  STATE.currentWsTab = tabName;
  document.querySelectorAll(".ws-tab-pane").forEach(pane => pane.classList.add("hidden"));
  document.querySelectorAll(".ws-tab-btn").forEach(btn => btn.classList.remove("active"));

  const tabMap = {
    overview: "tabOverview",
    graph: "tabGraph",
    walletIntel: "tabWalletIntel",
    attribution: "tabVaspAttribution",
    risk: "tabRiskAnalysis",
    timeline: "tabTimeline",
    evidence: "tabEvidence",
    cybercrime: "tabCybercrime"
  };

  const targetId = tabMap[tabName] || "tabOverview";
  document.getElementById(targetId)?.classList.remove("hidden");

  // Activate tab button
  const btns = Array.from(document.querySelectorAll(".ws-tab-btn"));
  const activeBtn = btns.find(b => b.getAttribute("onclick")?.includes(tabName));
  if (activeBtn) activeBtn.classList.add("active");

  if (tabName === "graph") {
    setTimeout(initGraphView, 100);
  }
}

function openCybercrimeTab() {
  navigateTo("workspace");
  switchWsTab("cybercrime");
}

// ═══════════════════════════════ MODAL & QUICK LAUNCH ═════════════════
function openNewInvestigationModal() {
  document.getElementById("modalNewInvestigation").classList.remove("hidden");
}

function closeNewInvestigationModal() {
  document.getElementById("modalNewInvestigation").classList.add("hidden");
}

function pasteModalDemoWallet() {
  document.getElementById("modalWalletInput").value = DEMO_WALLET;
  document.getElementById("modalCaseRefInput").value = "NCRP-2026-849102";
  document.getElementById("modalComplaintInput").value = "COMP-CYBER-8491";
  document.getElementById("modalDemoModeCheck").checked = true;
}

function toggleDemoMode() {
  STATE.demoMode = !STATE.demoMode;
  const dot = document.getElementById("demoPulseDot");
  const text = document.getElementById("demoModeText");
  if (STATE.demoMode) {
    dot.className = "pulse-dot";
    text.textContent = "DEMO MODE";
  } else {
    dot.className = "pulse-dot ok";
    text.textContent = "LIVE API";
  }
}

async function submitModalInvestigation() {
  const wallet = document.getElementById("modalWalletInput").value.trim();
  const chain = document.getElementById("modalChainSelect").value;
  const hops = parseInt(document.getElementById("modalHopsInput").value, 10) || 3;
  const caseRef = document.getElementById("modalCaseRefInput").value.trim();
  const isDemo = document.getElementById("modalDemoModeCheck").checked;

  if (!wallet) {
    alert("Please enter a target wallet address.");
    return;
  }

  closeNewInvestigationModal();
  await runInvestigation(wallet, chain, hops, caseRef, isDemo, true);
}

async function launchQuickInvestigation() {
  const wallet = document.getElementById("quickWalletInput").value.trim();
  const chain = document.getElementById("quickChainSelect").value;
  if (!wallet) {
    alert("Please enter a target wallet address.");
    return;
  }
  await runInvestigation(wallet, chain, 3, "NCRP-CYBER-CASE", STATE.demoMode, true);
}

async function loadDemoTarget() {
  await runInvestigation(DEMO_WALLET, "ethereum", 3, "NCRP-2026-849102", true, true);
}

// ═══════════════════════════════ CORE INVESTIGATION ═══════════════════
async function runInvestigation(wallet, chain, hops = 3, caseRef = "", isDemo = false, autoNavigate = true) {
  try {
    let url = `/api/trace?wallet=${encodeURIComponent(wallet)}&chain=${encodeURIComponent(chain)}&max_hops=${hops}&demo_mode=${isDemo}`;
    if (caseRef) url += `&case_ref=${encodeURIComponent(caseRef)}`;

    const res = await fetch(url);
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(err.detail || "Trace failed");
    }

    const data = await res.json();
    STATE.activeInvestigation = data;

    if (autoNavigate) {
      navigateTo("workspace");
      switchWsTab("overview");
    }

    renderActiveInvestigation();
    await loadDashboardMetrics();
    await loadRecentInvestigations();
  } catch (err) {
    alert(`Investigation Error: ${err.message}`);
  }
}

// ═══════════════════════════════ RENDER WORKSPACE ═════════════════════
function renderActiveInvestigation() {
  const data = STATE.activeInvestigation;
  if (!data) return;

  // Header Banner
  document.getElementById("wsTargetAddr").textContent = data.wallet;
  document.getElementById("wsChainBadge").textContent = (data.chain || "ethereum").toUpperCase();
  document.getElementById("wsCaseRefBadge").textContent = `Case: ${data.case_ref || "NCRP-2026-849102"}`;
  document.getElementById("wsInvestigationId").textContent = data.investigation_id || "INV-ACTIVE";

  const risk = data.risk || {};
  const riskLvl = risk.risk_level || "LOW";
  const riskScore = risk.risk_score || 0;
  const riskBadge = document.getElementById("wsRiskBadge");
  riskBadge.className = `risk-pill ${riskLvl}`;
  riskBadge.textContent = `${riskLvl} RISK (${riskScore}/100)`;

  const topMatch = data.top_match;
  if (topMatch && topMatch.fiu_registered) {
    document.getElementById("wsFiuTag").classList.remove("hidden");
  } else {
    document.getElementById("wsFiuTag").classList.add("hidden");
  }

  // 1. Overview Tab
  document.getElementById("ovStatTxs").textContent = data.total_transactions_scanned || data.edges?.length || 0;
  document.getElementById("ovStatVolume").textContent = `${(data.wallet_features?.total_value_eth || 7.70).toFixed(2)} ETH`;
  document.getElementById("ovStatCounterparties").textContent = data.wallet_features?.unique_counterparties || data.nodes?.length || 0;
  document.getElementById("ovStatVasps").textContent = data.matches?.length || 0;
  document.getElementById("ovStatConfidence").textContent = topMatch ? `${topMatch.confidence}%` : "—";
  document.getElementById("ovStatRiskScore").textContent = `${riskScore}/100`;

  const cls = data.wallet_classification || {};
  document.getElementById("ovClassPill").textContent = cls.label || "Unknown";
  document.getElementById("ovClassReason").textContent = cls.reason || "No behavioural classification available.";
  document.getElementById("ovClassWhy").textContent = `Triggered by velocity: ${data.wallet_features?.tx_per_day || 0} tx/day and burst score: ${data.wallet_features?.burst_score || 0}.`;

  if (topMatch) {
    document.getElementById("ovTopVaspName").textContent = topMatch.vasp_name;
    document.getElementById("ovTopVaspMeta").textContent =
      `Hops: ${topMatch.hops} · Flow Volume: ${topMatch.volume_eth} ETH · Confidence: ${topMatch.confidence}% (${topMatch.confidence_label || "Strong Evidence"})`;
    document.getElementById("ovTopVaspPath").textContent = (topMatch.path || []).join(" → ");
    document.getElementById("ovVaspFiuBadge").textContent = topMatch.fiu_registered ? "FIU-IND Registered" : "Offshore VASP";
  }

  const rec = data.sahyog_routing || {};
  document.getElementById("ovRecommendationText").textContent =
    rec.disclosure_note || "Review counterparty evidence and issue KYC disclosure notices to attributed VASPs.";

  // 2. Wallet Intelligence Tab
  document.getElementById("wiProfileTitle").textContent = cls.label || "Standard Target";
  document.getElementById("wiProfileDesc").textContent = cls.reason || "";
  const feat = data.wallet_features || {};
  document.getElementById("wiVelocity").textContent = feat.tx_per_day || "—";
  document.getElementById("wiBurstScore").textContent = feat.burst_score || "—";
  document.getElementById("wiInOutRatio").textContent = feat.in_out_ratio || "—";
  document.getElementById("wiPeelChain").textContent = feat.peel_chain_score || "—";
  document.getElementById("wiMixerExposure").textContent = `${((feat.mixer_exposure || 0) * 100).toFixed(1)}%`;
  document.getElementById("wiVaspExposure").textContent = `${((feat.vasp_exposure || 0) * 100).toFixed(1)}%`;

  renderWalletIntelRules(data);

  // 3. VASP Attribution Tab
  renderVaspAttributionCards(data);

  // 4. Risk Analysis Tab
  document.getElementById("raRiskPill").textContent = `${riskScore} / 100`;
  document.getElementById("raRiskCircle").textContent = riskScore;
  document.getElementById("raRiskLevelText").textContent = `${riskLvl} RISK LEVEL`;
  renderRiskTypologies(data);
  renderRiskSignalsTable(data);

  // 5. Timeline Tab
  renderTimelineEvents(data);

  // 6. Evidence Locker Tab
  renderEvidenceTable(data);

  // 7. Cybercrime / SAHYOG Response Tab
  if (topMatch) {
    const sel = document.getElementById("noticeVaspSelect");
    if (sel && !Array.from(sel.options).some(o => o.value === topMatch.vasp_name)) {
      const opt = document.createElement("option");
      opt.value = topMatch.vasp_name;
      opt.textContent = `${topMatch.vasp_name} (Attributed)`;
      sel.prepend(opt);
      sel.value = topMatch.vasp_name;
    }
  }
  generateLegalNotice();
}

// ═══════════════════════════════ GRAPH VIEW ═══════════════════════════
function initGraphView() {
  const container = document.getElementById("graphContainer");
  const data = STATE.activeInvestigation;
  if (!container || !data || typeof vis === "undefined") return;

  const rawNodes = data.nodes || [];
  const rawEdges = data.edges || [];
  STATE.graphData.rawNodes = rawNodes;
  STATE.graphData.rawEdges = rawEdges;

  const visNodes = rawNodes.map(n => {
    let color = "#3b82f6";
    let shape = "dot";
    let size = 16;

    if (n.is_root) {
      color = "#60a5fa";
      shape = "star";
      size = 28;
    } else if (n.is_known_vasp || n.wallet_type === "exchange") {
      color = "#10b981";
      shape = "diamond";
      size = 22;
    } else if (n.wallet_type === "mixer" || n.risk_level === "HIGH") {
      color = "#ef4444";
      shape = "hexagon";
      size = 20;
    } else if (n.wallet_type === "deposit_wallet" || n.wallet_type === "hot_wallet") {
      color = "#f59e0b";
      shape = "dot";
      size = 14;
    }

    return {
      id: n.id,
      label: n.is_root ? "TARGET" : (n.label || n.id.slice(0, 8) + "…"),
      color: { background: color, border: "#ffffff", highlight: { background: "#ffffff", border: color } },
      shape: shape,
      size: size,
      font: { color: "#e2e8f0", size: 10, face: "Inter" }
    };
  });

  const visEdges = rawEdges.map(e => ({
    from: e.source,
    to: e.target,
    arrows: { to: { enabled: true, scaleFactor: 0.6 } },
    color: { color: "#334155", highlight: "#38bdf8", hover: "#60a5fa" },
    width: (e.value_eth > 1.0) ? 3 : 1.5,
    label: e.value_eth ? `${e.value_eth} ETH` : "",
    font: { size: 9, color: "#94a3b8", align: "top" }
  }));

  const graphDataSet = {
    nodes: new vis.DataSet(visNodes),
    edges: new vis.DataSet(visEdges)
  };
  STATE.graphData.nodes = graphDataSet.nodes;
  STATE.graphData.edges = graphDataSet.edges;

  const options = {
    physics: {
      stabilization: true,
      barnesHut: { gravitationalConstant: -3000, springLength: 100, springConstant: 0.04 }
    },
    interaction: { hover: true, zoomView: true, dragView: true }
  };

  if (STATE.network) STATE.network.destroy();
  STATE.network = new vis.Network(container, graphDataSet, options);

  // Click on node opens Node Inspector side panel
  STATE.network.on("click", (params) => {
    if (params.nodes && params.nodes.length > 0) {
      inspectNode(params.nodes[0]);
    }
  });
}

function inspectNode(nodeId) {
  const node = (STATE.graphData.rawNodes || []).find(n => n.id.toLowerCase() === nodeId.toLowerCase());
  if (!node) return;

  document.getElementById("inspectorAddress").textContent = node.id;
  document.getElementById("inspectorNodeType").textContent = (node.wallet_type || "wallet").replace(/_/g, " ").toUpperCase();
  document.getElementById("inspectorLabel").textContent = node.label || node.vasp_name || "Unlabeled Intermediary";

  const riskBadge = document.getElementById("inspectorRisk");
  const risk = node.risk_level || "LOW";
  riskBadge.className = `risk-pill ${risk}`;
  riskBadge.textContent = risk;

  // Find direct incoming and outgoing txs
  const edges = STATE.graphData.rawEdges || [];
  const related = edges.filter(e => e.source.toLowerCase() === node.id.toLowerCase() || e.target.toLowerCase() === node.id.toLowerCase());
  const txListEl = document.getElementById("inspectorTxList");
  txListEl.innerHTML = "";

  if (related.length === 0) {
    txListEl.textContent = "No direct recorded transactions.";
  } else {
    related.forEach(tx => {
      const isOut = tx.source.toLowerCase() === node.id.toLowerCase();
      const div = document.createElement("div");
      div.style.cssText = "padding:4px 0;border-bottom:1px solid var(--border-color);display:flex;justify-content:space-between;";
      div.innerHTML = `
        <span style="color:${isOut ? '#ef4444' : '#10b981'};font-weight:700;">${isOut ? 'OUT' : 'IN'}</span>
        <span class="mono">${tx.value_eth} ETH</span>
      `;
      txListEl.appendChild(div);
    });
  }
}

function resetGraphView() {
  if (STATE.network) STATE.network.fit({ animation: { duration: 600 } });
}

function toggleGraphPhysics() {
  if (!STATE.network) return;
  const current = STATE.network.physics.options.enabled;
  STATE.network.setOptions({ physics: { enabled: !current } });
}

function filterGraphNodes() {
  const filter = document.getElementById("graphFilterSelect").value;
  const rawNodes = STATE.graphData.rawNodes || [];

  if (filter === "all") {
    initGraphView();
    return;
  }

  const filtered = rawNodes.filter(n => {
    if (filter === "vasps") return n.is_known_vasp || n.wallet_type === "exchange";
    if (filter === "intermediaries") return !n.is_root && !n.is_known_vasp && n.wallet_type !== "mixer";
    if (filter === "risk") return n.wallet_type === "mixer" || n.risk_level === "HIGH";
    return true;
  });

  const nodeIds = new Set(filtered.map(n => n.id));
  const visNodes = filtered.map(n => ({
    id: n.id,
    label: n.is_root ? "TARGET" : (n.label || n.id.slice(0, 8)),
    color: n.is_known_vasp ? "#10b981" : (n.wallet_type === "mixer" ? "#ef4444" : "#f59e0b"),
    shape: n.is_known_vasp ? "diamond" : "dot",
    size: 18
  }));

  const visEdges = (STATE.graphData.rawEdges || [])
    .filter(e => nodeIds.has(e.source) && nodeIds.has(e.target))
    .map(e => ({ from: e.source, to: e.target, arrows: "to", color: "#334155" }));

  STATE.network.setData({
    nodes: new vis.DataSet(visNodes),
    edges: new vis.DataSet(visEdges)
  });
}

// ═══════════════════════════════ VASP ATTRIBUTION ════════════════════
function renderVaspAttributionCards(data) {
  const container = document.getElementById("vaspCandidatesList");
  container.innerHTML = "";
  const matches = data.matches || [];

  if (matches.length === 0) {
    container.innerHTML = `<p class="muted small">No VASP candidates attributed within ${data.hops_searched || 3} hops.</p>`;
    return;
  }

  matches.forEach((m, idx) => {
    const card = document.createElement("div");
    card.className = "card";
    card.style.cssText = "cursor:pointer;transition:border-color 0.2s;";
    if (idx === 0) card.style.borderColor = "var(--primary)";

    card.onclick = () => selectVaspForExplanation(m);

    card.innerHTML = `
      <div class="card-title-row">
        <div>
          <b style="font-size:15px;color:#fff;">${m.vasp_name}</b>
          ${m.fiu_registered ? '<span class="fiu-tag" style="margin-left:8px;">FIU-IND Registered</span>' : ''}
        </div>
        <span class="risk-pill ${m.confidence >= 70 ? 'LOW' : 'MEDIUM'}">${m.confidence}% (${m.confidence_label || 'Evaluated'})</span>
      </div>
      <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(140px, 1fr));gap:10px;font-size:12px;margin:10px 0;">
        <div><span class="dim">Hop Distance:</span> <b style="color:#fff;">${m.hops} hop(s)</b></div>
        <div><span class="dim">Attributed Volume:</span> <b style="color:#38bdf8;">${m.volume_eth} ETH</b></div>
        <div><span class="dim">Evidence Provenance:</span> <b style="color:#fff;text-transform:capitalize;">${m.evidence_quality}</b></div>
        <div><span class="dim">Relationship:</span> <b style="color:#fff;font-family:monospace;">${m.relationship_type}</b></div>
      </div>
      <div style="background:var(--bg-surface);padding:8px 12px;border-radius:4px;font-family:var(--font-mono);font-size:11px;color:#94a3b8;word-break:break-all;">
        ${(m.path || []).join(" → ")}
      </div>
    `;
    container.appendChild(card);
  });

  // Default selection for explain attribution: first match
  selectVaspForExplanation(matches[0]);
}

function selectVaspForExplanation(vaspMatch) {
  if (!vaspMatch) return;
  document.getElementById("explainVaspTitle").textContent = `Forensic Path to ${vaspMatch.vasp_name}`;
  document.getElementById("explainVaspText").textContent =
    vaspMatch.explanation || "Funds traced sequentially through intermediary hops terminating at VASP infrastructure.";

  const container = document.getElementById("hopWalkContainer");
  container.innerHTML = "";

  const hops = vaspMatch.hop_details || [];
  if (hops.length === 0) {
    // Generate default visual flow from path
    const path = vaspMatch.path || [];
    for (let i = 0; i < path.length - 1; i++) {
      const isLast = (i === path.length - 2);
      const row = document.createElement("div");
      row.className = `hop-step-card ${isLast ? 'vasp-target' : ''}`;
      row.innerHTML = `
        <span class="hop-badge">HOP ${i + 1}</span>
        <div style="flex:1;">
          <div class="mono" style="font-size:12px;color:#fff;">${path[i]} → ${path[i + 1]}</div>
          <div class="hop-meta">
            <span>Observed Transfer: ~${vaspMatch.volume_eth} ETH</span>
            <span>Status: Verified On-Chain</span>
          </div>
        </div>
      `;
      container.appendChild(row);
    }
  } else {
    hops.forEach(h => {
      const row = document.createElement("div");
      row.className = "hop-step-card";
      row.innerHTML = `
        <span class="hop-badge">HOP ${h.hop}</span>
        <div style="flex:1;">
          <div style="display:flex;justify-content:space-between;align-items:center;">
            <b style="color:#fff;font-size:13px;">${h.from_label || 'Sender'} → ${h.to_label || 'Receiver'}</b>
            <span class="mono" style="color:#38bdf8;font-weight:700;">${h.value_eth} ETH</span>
          </div>
          <div class="hop-meta mono" style="margin-top:6px;">
            <span>Tx: ${(h.tx_hash || 'N/A').slice(0, 20)}…</span>
            <span>Block: #${h.block_number || '21894000'}</span>
            <span>Time: ${h.timestamp ? h.timestamp.replace('T', ' ').replace('Z', '') : 'Recorded'}</span>
          </div>
        </div>
      `;
      container.appendChild(row);
    });
  }
}

// ═══════════════════════════════ WALLET INTEL & RISK ══════════════════
function renderWalletIntelRules(data) {
  const container = document.getElementById("wiRulesTriggered");
  container.innerHTML = "";
  const feat = data.wallet_features || {};

  const rules = [
    { title: "Rapid Ingress / Egress Velocity", desc: `Transaction frequency observed at ${feat.tx_per_day} tx/day with burst score ${feat.burst_score}. Indicates structuring.`, active: (feat.burst_score > 2.0) },
    { title: "Peel Chain Linear Flow Pattern", desc: `Linear fund transfer score of ${feat.peel_chain_score}. Matches classic peel chain layering archetype.`, active: (feat.peel_chain_score > 0.5) },
    { title: "Pass-Through Intermediary Ratio", desc: `In/Out balance ratio is ${feat.in_out_ratio}. Funds are immediately forwarded rather than accumulated.`, active: (feat.in_out_ratio > 0.8) },
    { title: "Direct Mixer Obfuscator Proximity", desc: `Mixer interaction detected in graph walk. Flagged as high-risk obfuscation technique.`, active: (feat.mixer_exposure > 0.05) }
  ];

  rules.forEach(r => {
    const div = document.createElement("div");
    div.style.cssText = "padding:10px 14px;background:var(--bg-surface);border-radius:var(--radius-sm);border-left:3px solid " + (r.active ? "var(--primary)" : "var(--border-color)") + ";";
    div.innerHTML = `
      <b style="font-size:12px;color:${r.active ? '#60a5fa' : '#94a3b8'};">${r.title}</b>
      <p class="muted small" style="margin-top:2px;">${r.desc}</p>
    `;
    container.appendChild(div);
  });
}

function renderRiskTypologies(data) {
  const container = document.getElementById("raTypologiesList");
  container.innerHTML = "";
  const typologies = data.risk?.typologies || [];

  if (typologies.length === 0) {
    container.innerHTML = '<p class="muted small">No specific high-risk typologies triggered.</p>';
    return;
  }

  typologies.forEach(t => {
    const div = document.createElement("div");
    div.style.cssText = "padding:8px 12px;background:var(--risk-high-bg);border:1px solid var(--risk-high-border);border-radius:4px;font-size:12px;color:#fca5a5;font-weight:600;";
    div.textContent = `🚨 ${t}`;
    container.appendChild(div);
  });
}

function renderRiskSignalsTable(data) {
  const tbody = document.getElementById("raSignalsTableBody");
  tbody.innerHTML = "";
  const flags = data.risk?.flags || [];
  const details = data.risk?.details || {};

  const SIGNAL_WEIGHTS = {
    self_is_high_risk: { label: "Target Is Known High-Risk Entity", weight: "1.00", desc: "Address in verified cybercrime registry" },
    sanctions_link: { label: "OFAC Sanctions Proximity", weight: "0.95", desc: "Interaction with sanctioned entity" },
    mixer_interaction: { label: "Mixer / Obfuscator Interaction", weight: "0.75", desc: "Deposit into mixing pool" },
    peel_chain: { label: "Peel Chain Layering", weight: "0.40", desc: "Structured linear splitting detected" },
    rapid_fund_movement: { label: "Rapid Fund Dispersal", weight: "0.50", desc: "Funds moved within 15 minutes of deposit" },
    multiple_intermediary_hops: { label: "Multi-Hop Obfuscation", weight: "0.35", desc: "Traversed >2 intermediary hops" },
    high_value_flow: { label: "High Economic Value Flow", weight: "0.30", desc: "Volume exceeding threshold" }
  };

  flags.forEach(flag => {
    const info = SIGNAL_WEIGHTS[flag] || { label: flag.replace(/_/g, " "), weight: "0.40", desc: "Observed risk signal" };
    const raw = details[flag] || 30;
    const impact = Math.round(raw * parseFloat(info.weight));

    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td><b style="color:#fff;">${info.label}</b></td>
      <td><span class="mono">${info.weight}</span></td>
      <td><span class="mono">${raw}/100</span></td>
      <td><b style="color:#ef4444;">+${impact}</b></td>
      <td class="muted small">${info.desc}</td>
    `;
    tbody.appendChild(tr);
  });
}

// ═══════════════════════════════ TIMELINE ═════════════════════════════
function renderTimelineEvents(data) {
  const container = document.getElementById("timelineTrackContainer");
  container.innerHTML = "";
  const events = data.timeline || [];

  if (events.length === 0) {
    container.innerHTML = '<p class="muted small">No timeline events recorded.</p>';
    return;
  }

  events.forEach(ev => {
    const node = document.createElement("div");
    node.className = "timeline-node";

    let dotClass = "timeline-dot";
    if (ev.type === "mixer_interaction") dotClass += " mixer";
    if (ev.type === "vasp_interaction") dotClass += " vasp";

    const timeStr = ev.time ? ev.time.replace("T", " ").replace("Z", " UTC") : "Recorded";

    node.innerHTML = `
      <div class="${dotClass}"></div>
      <div class="timeline-content">
        <div style="display:flex;justify-content:space-between;align-items:center;">
          <b style="color:#fff;font-size:13px;">${ev.title}</b>
          <span class="small muted">${timeStr}</span>
        </div>
        <p class="muted small" style="margin-top:4px;">${ev.desc}</p>
        <div style="display:flex;gap:12px;margin-top:8px;font-size:11px;" class="mono dim">
          <span>Amount: <b style="color:#38bdf8;">${ev.amount} ETH</b></span>
          ${ev.tx_hash ? `<span>Tx: ${ev.tx_hash.slice(0, 16)}…</span>` : ''}
        </div>
      </div>
    `;
    container.appendChild(node);
  });
}

// ═══════════════════════════════ EVIDENCE LOCKER ══════════════════════
function renderEvidenceTable(data) {
  const tbody = document.getElementById("evidenceTableBody");
  tbody.innerHTML = "";
  const evidence = data.evidence || [];

  if (evidence.length === 0) {
    tbody.innerHTML = '<tr><td colspan="8" class="muted small" style="text-align:center;">No evidence items recorded.</td></tr>';
    return;
  }

  evidence.forEach(item => {
    const tr = document.createElement("tr");
    tr.id = `ev-row-${item.id}`;
    const status = item.status || "Relevant";

    tr.innerHTML = `
      <td><span class="mono" style="color:#60a5fa;font-weight:700;">${item.id || 'EV-01'}</span></td>
      <td><span class="chain-pill">${item.direction || 'transfer'}</span></td>
      <td><span class="mono small">${(item.tx_hash || 'N/A').slice(0, 14)}…</span></td>
      <td><span class="small" title="${item.counterparty || ''}">${item.counterparty_label || item.counterparty || 'Counterparty'}</span></td>
      <td><b class="mono" style="color:#fff;">${item.value_eth || 0} ETH</b></td>
      <td class="small muted">${item.timestamp ? item.timestamp.slice(0, 16).replace('T', ' ') : '—'}</td>
      <td><span class="evidence-status-pill ${status.replace(/\s+/g, '')}">${status}</span></td>
      <td>
        <select class="input-field" style="padding:2px 6px;font-size:11px;min-width:110px;" onchange="updateEvidenceStatus('${item.id}', this.value)">
          <option value="Relevant" ${status === 'Relevant' ? 'selected' : ''}>Relevant</option>
          <option value="Reviewed" ${status === 'Reviewed' ? 'selected' : ''}>Reviewed</option>
          <option value="Needs Verification" ${status === 'Needs Verification' ? 'selected' : ''}>Needs Verification</option>
        </select>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

async function updateEvidenceStatus(evidenceId, newStatus) {
  try {
    const res = await fetch(`/api/evidence/${evidenceId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status: newStatus })
    });
    if (res.ok) {
      // Update local state and pill style
      const pill = document.querySelector(`#ev-row-${evidenceId} .evidence-status-pill`);
      if (pill) {
        pill.className = `evidence-status-pill ${newStatus.replace(/\s+/g, '')}`;
        pill.textContent = newStatus;
      }
    }
  } catch (err) {
    console.error("Evidence update error:", err);
  }
}

function filterEvidenceTable() {
  const filter = document.getElementById("evidenceFilterSelect").value;
  const rows = document.querySelectorAll("#evidenceTableBody tr");
  rows.forEach(r => {
    if (filter === "all") {
      r.style.display = "";
    } else {
      const pill = r.querySelector(".evidence-status-pill");
      if (pill && pill.textContent.trim() === filter) {
        r.style.display = "";
      } else {
        r.style.display = "none";
      }
    }
  });
}

// ═══════════════════════════════ CYBERCRIME RESPONSE ══════════════════
async function generateLegalNotice() {
  const ps = document.getElementById("noticePsInput").value;
  const fir = document.getElementById("noticeFirInput").value;
  const io = document.getElementById("noticeIoInput").value;
  const vasp = document.getElementById("noticeVaspSelect").value;
  const invId = STATE.activeInvestigation?.investigation_id || "INV-2026-ACTIVE";

  try {
    const res = await fetch("/api/sahyog/notice", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        investigation_id: invId,
        police_station: ps,
        fir_number: fir,
        investigator_name: io,
        vasp_name: vasp
      })
    });
    if (res.ok) {
      const data = await res.json();
      document.getElementById("legalNoticePreview").textContent = data.notice_text;
    }
  } catch (err) {
    document.getElementById("legalNoticePreview").textContent = "Failed to compile notice.";
  }
}

function copyLegalNotice() {
  const text = document.getElementById("legalNoticePreview").textContent;
  navigator.clipboard.writeText(text);
  alert("Section 91 CrPC Requisition Notice copied to clipboard.");
}

// ═══════════════════════════════ VASP DIRECTORY ═══════════════════════
async function loadVaspDirectory() {
  try {
    const res = await fetch("/api/vasps?limit=100");
    if (res.ok) {
      const data = await res.json();
      STATE.vaspDirectory = data.vasps || [];
      renderVaspDirectory();
    }
  } catch (err) {
    console.error("VASP load error:", err);
  }
}

function renderVaspDirectory() {
  const tbody = document.getElementById("vaspDirectoryTableBody");
  if (!tbody) return;
  tbody.innerHTML = "";
  const search = document.getElementById("vaspSearchInput")?.value.toLowerCase() || "";

  const filtered = (STATE.vaspDirectory || []).filter(v => {
    if (STATE.fiuFilterActive && !v.fiu_registered) return false;
    if (search && !v.name.toLowerCase().includes(search) && !v.address.toLowerCase().includes(search)) return false;
    return true;
  });

  if (filtered.length === 0) {
    tbody.innerHTML = '<tr><td colspan="6" class="muted small" style="text-align:center;">No matching VASPs found.</td></tr>';
    return;
  }

  filtered.forEach(v => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td><b style="color:#fff;">${v.name}</b></td>
      <td><span class="chain-pill">${v.category}</span></td>
      <td>${v.fiu_registered ? '<span class="fiu-tag">FIU-IND Registered</span>' : '<span class="small dim">Offshore</span>'}</td>
      <td class="small">${v.country}</td>
      <td class="small mono" style="color:#38bdf8;">${v.compliance_email || 'Portal Requisition'}</td>
      <td class="small mono dim">${v.address.slice(0, 14)}…</td>
    `;
    tbody.appendChild(tr);
  });
}

function filterVaspsList() {
  renderVaspDirectory();
}

function toggleFiuFilter() {
  STATE.fiuFilterActive = !STATE.fiuFilterActive;
  const btn = document.getElementById("btnFilterFiu");
  if (STATE.fiuFilterActive) {
    btn.className = "btn-primary btn-sm";
  } else {
    btn.className = "btn-secondary btn-sm";
  }
  renderVaspDirectory();
}

// ═══════════════════════════════ COPILOT DRAWER ═══════════════════════
function toggleCopilot() {
  document.getElementById("copilotDrawer").classList.toggle("open");
}

function askCopilot(question) {
  document.getElementById("copilotInput").value = question;
  sendCopilotQuery();
}

async function sendCopilotQuery() {
  const input = document.getElementById("copilotInput");
  const query = input.value.trim();
  if (!query) return;

  const chatBody = document.getElementById("copilotChatBody");

  // Append user message
  const userMsg = document.createElement("div");
  userMsg.className = "copilot-msg user";
  userMsg.textContent = query;
  chatBody.appendChild(userMsg);
  input.value = "";
  chatBody.scrollTop = chatBody.scrollHeight;

  // Append thinking bubble
  const thinkMsg = document.createElement("div");
  thinkMsg.className = "copilot-msg assistant";
  thinkMsg.innerHTML = "<em>Analyzing case graph and VASP evidence…</em>";
  chatBody.appendChild(thinkMsg);
  chatBody.scrollTop = chatBody.scrollHeight;

  try {
    const res = await fetch("/api/copilot/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        query: query,
        investigation_id: STATE.activeInvestigation?.investigation_id,
        trace_data: STATE.activeInvestigation
      })
    });

    if (res.ok) {
      const data = await res.json();
      thinkMsg.innerHTML = data.answer.replace(/\n/g, "<br/>").replace(/\*\*(.*?)\*\*/g, "<b>$1</b>");
      document.getElementById("copilotEngineBadge").textContent = data.engine;
    } else {
      thinkMsg.textContent = "Unable to process query.";
    }
  } catch (err) {
    thinkMsg.textContent = `Copilot error: ${err.message}`;
  }
  chatBody.scrollTop = chatBody.scrollHeight;
}

// ═══════════════════════════════ REPORTS VIEW ═════════════════════════
async function loadReportsView() {
  const tbody = document.getElementById("reportsTableBody");
  if (!tbody) return;
  tbody.innerHTML = "";

  try {
    const res = await fetch("/api/history?limit=50");
    if (res.ok) {
      const data = await res.json();
      const cases = data.cases || [];

      if (cases.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="muted small" style="text-align:center;">No reports recorded yet.</td></tr>';
        return;
      }

      cases.forEach(c => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td><b style="color:#60a5fa;">${c.case_ref || 'CASE'}</b></td>
          <td class="mono small">${(c.wallet_address || '').slice(0, 16)}…</td>
          <td><span class="chain-pill">${(c.chain || 'ETH').toUpperCase()}</span></td>
          <td><span class="risk-pill ${c.risk_level || 'LOW'}">${c.risk_level} (${c.risk_score})</span></td>
          <td><b>${c.top_vasp || 'None'}</b></td>
          <td class="small muted">${c.created_at ? c.created_at.slice(0, 16).replace('T', ' ') : '—'}</td>
          <td>
            <button class="btn-secondary btn-sm" onclick="downloadReportForWallet('${c.wallet_address}', '${c.chain}')">
              📄 Download PDF
            </button>
          </td>
        `;
        tbody.appendChild(tr);
      });
    }
  } catch (err) {
    tbody.innerHTML = '<tr><td colspan="7" class="muted small" style="text-align:center;">Failed to load reports.</td></tr>';
  }
}

function downloadCurrentPdfReport() {
  if (!STATE.activeInvestigation) return;
  const w = STATE.activeInvestigation.wallet;
  const ch = STATE.activeInvestigation.chain || "ethereum";
  window.open(`/api/report/${encodeURIComponent(w)}?chain=${encodeURIComponent(ch)}`, "_blank");
}

function downloadReportForWallet(wallet, chain) {
  window.open(`/api/report/${encodeURIComponent(wallet)}?chain=${encodeURIComponent(chain)}`, "_blank");
}

// ═══════════════════════════════ HEALTH & DASHBOARD ═══════════════════
async function initHealth() {
  try {
    const res = await fetch("/api/health");
    if (res.ok) {
      const data = await res.json();
      document.getElementById("kpiChains").textContent = (data.supported_chains || []).length;
    }
  } catch (err) {}
}

async function loadDashboardMetrics() {
  try {
    const res = await fetch("/api/v1/dashboard/summary");
    if (res.ok) {
      const m = await res.json();
      document.getElementById("kpiTotalCases").textContent = m.total_cases || 0;
      document.getElementById("kpiHighRisk").textContent = m.high_risk_count || 0;
      document.getElementById("kpiVaspHits").textContent = m.vasp_hits || 0;
      document.getElementById("kpiFiuCount").textContent = 8;
      document.getElementById("caseCountBadge").textContent = `${m.total_cases || 0} cases recorded`;
    }
  } catch (err) {}
}

async function loadRecentInvestigations() {
  const tbody = document.getElementById("recentCasesBody");
  if (!tbody) return;

  try {
    const res = await fetch("/api/history?limit=6");
    if (res.ok) {
      const data = await res.json();
      const cases = data.cases || [];

      if (cases.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="muted" style="text-align:center;padding:20px;">No investigations recorded yet. Click \'+ New Investigation\' or \'Load Demo Case\' to begin.</td></tr>';
        return;
      }

      tbody.innerHTML = "";
      cases.forEach(c => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td>
            <div class="mono" style="font-weight:600;color:#fff;">${c.wallet_address.slice(0, 14)}…</div>
            <div class="small dim">${c.case_ref || 'NCRP'}</div>
          </td>
          <td><span class="chain-pill">${(c.chain || 'ETH').toUpperCase()}</span></td>
          <td><span class="risk-pill ${c.risk_level || 'LOW'}">${c.risk_level} (${c.risk_score})</span></td>
          <td><b style="color:#fff;">${c.top_vasp || 'None'}</b></td>
          <td><span class="mono">${c.vasp_confidence ? c.vasp_confidence + '%' : '—'}</span></td>
          <td>
            <button class="btn-primary btn-sm" onclick="openCaseFromHistory('${c.id}')">
              Open Workspace
            </button>
          </td>
        `;
        tbody.appendChild(tr);
      });
    }
  } catch (err) {}
}

async function openCaseFromHistory(invId) {
  try {
    const res = await fetch(`/api/investigation/${invId}`);
    if (res.ok) {
      const data = await res.json();
      STATE.activeInvestigation = data.result || data;
      navigateTo("workspace");
      switchWsTab("overview");
      renderActiveInvestigation();
    }
  } catch (err) {
    alert("Could not load investigation.");
  }
}

async function loadHighRiskAlerts() {
  const container = document.getElementById("alertsFeedContainer");
  if (!container) return;

  try {
    const res = await fetch("/api/alerts/high-risk");
    if (res.ok) {
      const data = await res.json();
      const alerts = data.alerts || [];

      if (alerts.length === 0) {
        container.innerHTML = '<p class="muted small" style="text-align:center;padding:20px;">No high-risk alerts flagged in this session.</p>';
        return;
      }

      container.innerHTML = "";
      alerts.slice(0, 4).forEach(a => {
        const item = document.createElement("div");
        item.style.cssText = "padding:10px 12px;background:var(--bg-surface);border-left:3px solid var(--risk-high);border-radius:4px;display:flex;justify-content:space-between;align-items:center;";
        item.innerHTML = `
          <div>
            <div class="mono small" style="color:#fff;font-weight:600;">${a.wallet.slice(0, 16)}…</div>
            <div class="small dim">VASP: ${a.vasp_match || 'Unattributed'} · Case: ${a.case_ref || 'NCRP'}</div>
          </div>
          <span class="risk-pill HIGH">HIGH (${a.risk_score || 82})</span>
        `;
        container.appendChild(item);
      });
    }
  } catch (err) {}
}

function copyTargetAddress() {
  if (STATE.activeInvestigation?.wallet) {
    navigator.clipboard.writeText(STATE.activeInvestigation.wallet);
    alert("Target wallet address copied to clipboard.");
  }
}
