"""
PDF investigation report generator.

Includes: VASP attribution (with relationship type + evidence quality),
risk assessment, laundering typologies, wallet classification,
wallet behavioural feature vector, and SAHYOG routing recommendation.

Language note
-------------
This report deliberately distinguishes between *interaction* and *ownership*.
The system traces fund flows and identifies VASP attribution candidates —
it does NOT claim ownership of wallets by VASPs unless explicit evidence
(controlled_by relationship with high evidence quality) supports that claim.
"""

import io
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER


# Colour palette matching the UI
_DARK    = colors.HexColor("#0f1420")
_PANEL   = colors.HexColor("#161d2e")
_BORDER  = colors.HexColor("#2a3448")
_ACCENT  = colors.HexColor("#4f8cff")
_GREEN   = colors.HexColor("#22c55e")
_YELLOW  = colors.HexColor("#eab308")
_RED     = colors.HexColor("#ef4444")
_MUTED   = colors.HexColor("#8b93a7")
_WHITE   = colors.white
_LIGHT   = colors.HexColor("#f3f4f6")


def _risk_colour(level: str) -> colors.Color:
    return {"HIGH": _RED, "MEDIUM": _YELLOW, "LOW": _GREEN}.get(level, _MUTED)


def _rel_label(rel: str) -> str:
    """Human-readable relationship type label."""
    return {
        "interacts_with":    "Fund flow interaction",
        "controlled_by":     "Attributed deposit/operational wallet",
        "laundered_through": "Funds laundered through",
    }.get(rel, rel)


def _evidence_label(eq: str) -> str:
    return {
        "high":   "High — Verified authoritative source",
        "medium": "Medium — Community-labelled dataset",
        "low":    "Low — Single unverified source",
    }.get(eq, eq)


def build_pdf_report(trace_result: dict) -> io.BytesIO:
    buffer = io.BytesIO()
    doc    = SimpleDocTemplate(
        buffer, pagesize=A4,
        topMargin=2*cm, bottomMargin=2*cm,
        leftMargin=2*cm, rightMargin=2*cm,
    )
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "Title2", parent=styles["Title"], fontSize=18, textColor=_DARK, spaceAfter=4
    )
    section_style = ParagraphStyle(
        "Section", parent=styles["Heading2"], fontSize=12,
        textColor=_ACCENT, spaceBefore=10, spaceAfter=4
    )
    sub_style = ParagraphStyle(
        "Sub", parent=styles["Heading3"], fontSize=10,
        textColor=_DARK, spaceBefore=6, spaceAfter=2
    )
    body_style  = styles["Normal"]
    small_style = ParagraphStyle("Small", parent=styles["Normal"], fontSize=9)

    story = []

    # ── Header ────────────────────────────────────────────────────────────
    story.append(Paragraph("SIH-26182 INVESTIGATION REPORT", title_style))
    story.append(Paragraph(
        "Wallet-to-VASP Attribution System · I4C / Ministry of Home Affairs",
        small_style
    ))
    story.append(Spacer(1, 0.2*cm))
    story.append(HRFlowable(width="100%", thickness=1, color=_BORDER))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        f"<b>Generated:</b> {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}",
        small_style
    ))
    story.append(Spacer(1, 0.5*cm))

    # ── Case Summary ──────────────────────────────────────────────────────
    story.append(Paragraph("CASE SUMMARY", section_style))
    chain_meta = trace_result.get("chain", "ethereum").upper()
    summary_data = [
        ["Field", "Value"],
        ["Traced Wallet",        trace_result.get("wallet", "—")],
        ["Blockchain",           chain_meta],
        ["Transactions Scanned", str(trace_result.get("total_transactions_scanned", 0))],
        ["Hop Depth Searched",   str(trace_result.get("hops_searched", "—"))],
        ["Wallet Type",          trace_result.get("wallet_classification", {}).get("label", "Unknown")],
    ]
    t = _table(summary_data, col_widths=[4*cm, 12.5*cm])
    story.append(t)
    story.append(Spacer(1, 0.5*cm))

    # ── Risk Assessment ───────────────────────────────────────────────────
    story.append(Paragraph("RISK ASSESSMENT", section_style))
    risk       = trace_result.get("risk", {})
    risk_level = risk.get("risk_level", "LOW")
    risk_score = risk.get("risk_score", 0)
    typologies = risk.get("typologies", [])
    flags      = risk.get("flags", [])

    risk_colour = _risk_colour(risk_level)
    story.append(Paragraph(
        f"<b>Risk Level: <font color='#{risk_colour.hexval()[2:]}'>{risk_level}</font></b>"
        f"  ·  Risk Score: <b>{risk_score}/100</b>",
        body_style
    ))
    story.append(Spacer(1, 0.2*cm))

    if typologies:
        story.append(Paragraph("<b>Laundering Typologies Detected:</b>", body_style))
        for typo in typologies:
            story.append(Paragraph(f"• {typo}", small_style))
    else:
        story.append(Paragraph("No laundering typologies detected.", small_style))

    if flags:
        story.append(Spacer(1, 0.2*cm))
        story.append(Paragraph(
            f"<b>Active Risk Signals:</b> {', '.join(flags)}", small_style
        ))
    story.append(Spacer(1, 0.5*cm))

    # ── Score Breakdown ───────────────────────────────────────────────────
    details = risk.get("details", {})
    if details:
        story.append(Paragraph("SCORE BREAKDOWN", section_style))
        story.append(Paragraph(
            f"<b>{risk_score}/100</b> — derived from {len(flags)} active risk signals with weighted aggregation.",
            small_style
        ))
        story.append(Spacer(1, 0.1*cm))

        SIG_W = {
            "self_is_high_risk":  1.00, "sanctions_link": 0.95,
            "ransomware_link":    0.90, "darknet_link":    0.85,
            "fraud_link":         0.70, "mixer_interaction": 0.75,
            "structuring":        0.50, "peel_chain":     0.40,
            "cross_chain_bridge": 0.30, "high_velocity":   0.25,
        }
        SIG_LABEL = {
            "self_is_high_risk":  "High-Risk Address",
            "sanctions_link":     "Sanctions Proximity",
            "ransomware_link":    "Ransomware Link",
            "darknet_link":       "Darknet Market",
            "fraud_link":         "Fraud Connection",
            "mixer_interaction":  "Mixer Interaction",
            "cross_chain_bridge": "Cross-Chain Bridge",
            "high_velocity":      "High Velocity",
            "structuring":        "Structuring / Smurfing",
            "peel_chain":         "Peel Chain Pattern",
        }

        # Build a table of signal contributions
        sig_data = [["Signal", "Raw Score", "Weight", "Contribution", "Detection Reason"]]
        total_c = 0
        for sig in flags:
            raw = details.get(sig, 0)
            w   = SIG_W.get(sig, 0.5)
            c   = round(raw * w)
            total_c += c
            label = SIG_LABEL.get(sig, sig)
            sig_data.append([
                label, str(raw), f"{int(w*100)}%", f"+{c}",
                SIG_W.get(sig, "0.5") > 0.5 and "Direct link" or "Behavioral"
            ])
        boost = min(20, (len(flags) - 1) * 5)
        sig_data.append(["", "", "", f"<b>Sum: {total_c} + Boost: +{boost}</b>", ""])
        sig_data.append(["", "", "", f"<b>Final: {risk_score}/100</b>", ""])

        t2 = _table(sig_data, col_widths=[3.5*cm, 2*cm, 1.5*cm, 2.5*cm, 7.5*cm])
        story.append(t2)
        story.append(Spacer(1, 0.5*cm))

    # ── VASP Attribution ──────────────────────────────────────────────────
    story.append(Paragraph("VASP ATTRIBUTION RESULTS", section_style))
    story.append(Paragraph(
        "<i>Attribution identifies which Virtual Asset Service Providers (VASPs) "
        "are linked to fund flows from the traced wallet. A 'Fund flow interaction' "
        "means a transaction path was observed — it does NOT assert ownership of the "
        "wallet by the VASP. 'Attributed deposit/operational wallet' requires "
        "substantially stronger structural evidence and is stated only when warranted.</i>",
        small_style
    ))
    story.append(Spacer(1, 0.3*cm))

    matches = trace_result.get("matches", [])
    if not matches:
        story.append(Paragraph(
            trace_result.get("note", "No known VASP match found within the search depth."),
            small_style
        ))
    else:
        table_data = [[
            "VASP / Exchange", "Confidence", "Relationship", "Evidence", "Hops"
        ]]
        for m in matches[:10]:
            table_data.append([
                m.get("vasp_name", "—"),
                f"{m.get('confidence', 0)}%",
                _rel_label(m.get("relationship_type", "interacts_with")),
                m.get("evidence_quality", "medium").capitalize(),
                str(m.get("hops", "—")),
            ])
        t = _table(table_data, col_widths=[4*cm, 2*cm, 4.5*cm, 2.5*cm, 1.5*cm])
        story.append(t)

        # Component score breakdown for top match
        top = matches[0]
        story.append(Spacer(1, 0.4*cm))
        story.append(Paragraph("<b>Top Match — Score Breakdown (Explainability)</b>", sub_style))
        score_data = [
            ["Component", "Score", "Weight", "Contribution"],
            ["Graph Proximity",
             f"{top.get('graph_proximity_score', 0):.1f}/100",      "40%",
             f"{top.get('graph_proximity_score', 0) * 0.40:.1f}"],
            ["Interaction Strength",
             f"{top.get('interaction_strength_score', 0):.1f}/100", "30%",
             f"{top.get('interaction_strength_score', 0) * 0.30:.1f}"],
            ["Temporal Recency",
             f"{top.get('temporal_recency_score', 0):.1f}/100",     "20%",
             f"{top.get('temporal_recency_score', 0) * 0.20:.1f}"],
            ["Evidence Quality",
             _evidence_label(top.get("evidence_quality", "medium")),  "10%", "—"],
            ["Final Confidence", f"{top.get('confidence', 0)}%", "", ""],
        ]
        t2 = _table(score_data, col_widths=[4.5*cm, 5*cm, 1.5*cm, 2.5*cm])
        story.append(t2)

        story.append(Spacer(1, 0.4*cm))
        story.append(Paragraph("<b>Top Match — Fund Flow Path</b>", sub_style))
        path_str = " → ".join(top.get("path", []))
        story.append(Paragraph(path_str, ParagraphStyle(
            "Path", parent=small_style, fontName="Courier", fontSize=8, wordWrap="CJK"
        )))

    story.append(Spacer(1, 0.5*cm))

    # ── Wallet Behavioural Features ───────────────────────────────────────
    features = trace_result.get("wallet_features")
    if features:
        story.append(Paragraph("WALLET BEHAVIOURAL FEATURE VECTOR", section_style))
        story.append(Paragraph(
            "<i>These features describe the wallet's on-chain behaviour and are "
            "the input to the multi-dimensional attribution scorer. They form the "
            "foundation for future ML-based ranking (Level 3 of the roadmap).</i>",
            small_style
        ))
        story.append(Spacer(1, 0.2*cm))

        feat_data = [
            ["Feature Group", "Feature", "Value"],
            ["Graph",       "Unique counterparties",    str(features.get("unique_counterparties", 0))],
            ["Graph",       "Transaction count",         str(features.get("tx_count", 0))],
            ["Graph",       "Unique senders",            str(features.get("unique_senders", 0))],
            ["Graph",       "Unique receivers",          str(features.get("unique_receivers", 0))],
            ["Value",       "Total volume (ETH)",        f"{features.get('total_value_eth', 0):.4f}"],
            ["Value",       "Avg tx value (ETH)",        f"{features.get('avg_value_eth', 0):.4f}"],
            ["Value",       "In/out ratio",              f"{features.get('in_out_ratio', 0):.3f}"],
            ["Value",       "Value concentration",       f"{features.get('value_concentration', 0):.3f}"],
            ["Temporal",    "Tx per day (velocity)",     f"{features.get('tx_per_day', 0):.2f}"],
            ["Temporal",    "Burst score",               f"{features.get('burst_score', 1):.2f}"],
            ["Temporal",    "Recency (days)",            f"{features.get('recency_days', 0):.1f}"],
            ["Temporal",    "Activity span (days)",      f"{features.get('activity_span_days', 0):.1f}"],
            ["Exposure",    "Mixer exposure",            f"{features.get('mixer_exposure', 0):.3f}"],
            ["Exposure",    "Bridge exposure",           f"{features.get('bridge_exposure', 0):.3f}"],
            ["Exposure",    "VASP exposure",             f"{features.get('vasp_exposure', 0):.3f}"],
            ["Structuring", "Structuring ratio",         f"{features.get('structuring_ratio', 0):.3f}"],
            ["Structuring", "Peel chain score",          f"{features.get('peel_chain_score', 0):.1f}"],
        ]
        t3 = _table(feat_data, col_widths=[3*cm, 6*cm, 4.5*cm])
        story.append(t3)
        story.append(Spacer(1, 0.5*cm))

    # ── SAHYOG Routing ────────────────────────────────────────────────────
    story.append(Paragraph("SAHYOG PORTAL ROUTING RECOMMENDATION", section_style))
    routing = trace_result.get("sahyog_routing", {})
    story.append(Paragraph(f"<b>Recommended Action:</b> {routing.get('action', '—')}", body_style))
    story.append(Spacer(1, 0.15*cm))
    story.append(Paragraph(routing.get("disclosure_note", ""), small_style))
    if routing.get("vasp_name"):
        story.append(Spacer(1, 0.15*cm))
        story.append(Paragraph(
            f"<b>Target VASP:</b> {routing.get('vasp_name')}  |  "
            f"<b>Address:</b> {routing.get('vasp_address', '—')}",
            small_style,
        ))
    story.append(Spacer(1, 0.5*cm))

    # ── Wallet Classification ─────────────────────────────────────────────
    story.append(Paragraph("WALLET CLASSIFICATION", section_style))
    classification = trace_result.get("wallet_classification", {})
    story.append(Paragraph(f"<b>Type:</b> {classification.get('label', 'Unknown')}", body_style))
    story.append(Paragraph(f"<b>Reason:</b> {classification.get('reason', '—')}", small_style))
    story.append(Spacer(1, 0.5*cm))

    # ── Legal Disclaimer ──────────────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=0.5, color=_BORDER))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        "<i>DISCLAIMER: This report is generated by an automated prototype (SIH-26182) "
        "for investigative lead purposes only. Confidence scores are multi-dimensional "
        "heuristics and must be corroborated with formal legal process before any "
        "enforcement action. VASP attribution identifies fund flow relationships — it "
        "does NOT establish legal ownership unless explicitly stated as 'Attributed "
        "deposit/operational wallet' with High evidence quality. Attribution data is "
        "based on publicly available blockchain labels and known-address intelligence "
        "datasets. This report does not constitute legal evidence.</i>",
        small_style,
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer


def _table(data: list, col_widths: list) -> Table:
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("BACKGROUND",     (0, 0), (-1, 0),  _DARK),
        ("TEXTCOLOR",      (0, 0), (-1, 0),  _WHITE),
        ("FONTSIZE",       (0, 0), (-1, -1), 9),
        ("FONTNAME",       (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("GRID",           (0, 0), (-1, -1), 0.4, _BORDER),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [_WHITE, _LIGHT]),
        ("VALIGN",         (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING",    (0, 0), (-1, -1), 6),
        ("RIGHTPADDING",   (0, 0), (-1, -1), 6),
        ("TOPPADDING",     (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",  (0, 0), (-1, -1), 4),
    ]))
    return t
