"""
CryptoGuard AI - Forensic PDF Investigation Report Generator
Generates comprehensive law-enforcement grade investigation reports using ReportLab.

Distinguishes clearly between:
- Observed Evidence (verifiable on-chain data)
- Derived Analysis (heuristics, behavioral classification, risk scoring)
- Investigator Notes
- Statutory Recommendations (Section 91 CrPC / Section 94 BNSS Requisition)
"""

import io
from datetime import datetime, timezone
from typing import Dict, Any

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

# Palette matching CryptoGuard AI
_PRIMARY   = colors.HexColor("#0f172a") # Slate 900
_SECONDARY = colors.HexColor("#1e293b") # Slate 800
_ACCENT    = colors.HexColor("#2563eb") # Royal Blue
_BORDER    = colors.HexColor("#cbd5e1") # Slate 300
_GREEN     = colors.HexColor("#16a34a")
_AMBER     = colors.HexColor("#d97706")
_RED       = colors.HexColor("#dc2626")
_MUTED     = colors.HexColor("#64748b")
_LIGHT_BG  = colors.HexColor("#f8fafc")
_WHITE     = colors.white


def _risk_color(level: str) -> colors.Color:
    return {"HIGH": _RED, "MEDIUM": _AMBER, "LOW": _GREEN}.get(level.upper(), _MUTED)


def build_pdf_report(trace_result: Dict[str, Any]) -> io.BytesIO:
    """Builds a multi-page PDF forensic report."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
        leftMargin=1.8 * cm,
        rightMargin=1.8 * cm,
    )

    styles = getSampleStyleSheet()

    # Custom styles
    header_style = ParagraphStyle(
        "HeaderStyle", parent=styles["Title"],
        fontSize=18, leading=22, textColor=_PRIMARY, alignment=TA_LEFT
    )
    tagline_style = ParagraphStyle(
        "TaglineStyle", parent=styles["Normal"],
        fontSize=9, leading=12, textColor=_ACCENT, fontName="Helvetica-Bold"
    )
    confidential_style = ParagraphStyle(
        "ConfStyle", parent=styles["Normal"],
        fontSize=8, leading=10, textColor=_RED, fontName="Helvetica-Bold", alignment=TA_RIGHT
    )
    section_style = ParagraphStyle(
        "SectionStyle", parent=styles["Heading2"],
        fontSize=12, leading=16, textColor=_PRIMARY, fontName="Helvetica-Bold",
        spaceBefore=12, spaceAfter=6
    )
    sub_style = ParagraphStyle(
        "SubStyle", parent=styles["Heading3"],
        fontSize=10, leading=14, textColor=_SECONDARY, fontName="Helvetica-Bold",
        spaceBefore=6, spaceAfter=3
    )
    body_style = ParagraphStyle(
        "BodyStyle", parent=styles["Normal"],
        fontSize=8.5, leading=12, textColor=_SECONDARY
    )
    table_cell = ParagraphStyle(
        "Cell", parent=styles["Normal"],
        fontSize=8, leading=10, textColor=_PRIMARY
    )
    table_cell_bold = ParagraphStyle(
        "CellBold", parent=styles["Normal"],
        fontSize=8, leading=10, textColor=_PRIMARY, fontName="Helvetica-Bold"
    )

    story = []

    # ── 1. Document Header ──────────────────────────────────────────────────
    header_table_data = [
        [
            Paragraph("<b>CRYPTOGUARD AI</b>", header_style),
            Paragraph("CONFIDENTIAL // LAW ENFORCEMENT SENSITIVE<br/>FOR OFFICIAL USE ONLY", confidential_style)
        ],
        [
            Paragraph("AI-Powered Blockchain Investigation & VASP Attribution Platform", tagline_style),
            Paragraph(f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}", ParagraphStyle("TS", parent=styles["Normal"], fontSize=8, alignment=TA_RIGHT, textColor=_MUTED))
        ]
    ]
    t_head = Table(header_table_data, colWidths=[10 * cm, 7.4 * cm])
    t_head.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_head)
    story.append(Spacer(1, 0.2 * cm))
    story.append(HRFlowable(width="100%", thickness=1.5, color=_ACCENT, spaceBefore=4, spaceAfter=10))

    # ── 2. Case & Target Metadata ───────────────────────────────────────────
    wallet = trace_result.get("wallet", "N/A")
    chain = trace_result.get("chain", "ethereum").upper()
    case_ref = trace_result.get("case_ref") or "NCRP-CYBER-2026-CASE"
    risk = trace_result.get("risk", {})
    risk_level = risk.get("risk_level", "LOW")
    risk_score = risk.get("risk_score", 0)
    classification = trace_result.get("wallet_classification", {})

    meta_data = [
        [Paragraph("<b>Target Wallet:</b>", table_cell_bold), Paragraph(f"<font name='Courier'>{wallet}</font>", table_cell),
         Paragraph("<b>Blockchain:</b>", table_cell_bold), Paragraph(chain, table_cell)],
        [Paragraph("<b>Case Reference:</b>", table_cell_bold), Paragraph(case_ref, table_cell),
         Paragraph("<b>Hops Scanned:</b>", table_cell_bold), Paragraph(str(trace_result.get("hops_searched", 3)), table_cell)],
        [Paragraph("<b>Risk Assessment:</b>", table_cell_bold), Paragraph(f"<font color='{_risk_color(risk_level).hexval()}'><b>{risk_score}/100 ({risk_level})</b></font>", table_cell),
         Paragraph("<b>Classification:</b>", table_cell_bold), Paragraph(classification.get("label", "Unknown"), table_cell)]
    ]
    t_meta = Table(meta_data, colWidths=[3.2 * cm, 6.5 * cm, 3.2 * cm, 4.5 * cm])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), _LIGHT_BG),
        ('GRID', (0,0), (-1,-1), 0.5, _BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 0.4 * cm))

    # ── 3. Executive Summary ────────────────────────────────────────────────
    story.append(Paragraph("1. Executive Summary", section_style))
    top_match = trace_result.get("top_match") or {}
    vasp_name = top_match.get("vasp_name", "Unattributed")
    vasp_conf = top_match.get("confidence", 0)

    exec_text = (
        f"This investigative report details the automated blockchain intelligence walk conducted for wallet "
        f"<b>{wallet}</b> on the {chain} network. Outward graph traversal identified direct and intermediary "
        f"transaction paths terminating at <b>{vasp_name}</b> with an attribution confidence of <b>{vasp_conf}%</b>. "
        f"Risk scoring evaluated the address at <b>{risk_score}/100 ({risk_level} RISK)</b> due to observed forensic indicators: "
        f"{', '.join(risk.get('typologies', ['Standard activity']))}. "
        f"Immediate legal requisition under Section 91 CrPC / Section 94 BNSS is recommended for KYC disclosure."
    )
    story.append(Paragraph(exec_text, body_style))
    story.append(Spacer(1, 0.3 * cm))

    # ── 4. Distinction: Observed Evidence vs Derived Analysis ───────────────
    story.append(Paragraph("2. Forensic Methodology: Observed vs. Derived", section_style))
    method_data = [
        [
            Paragraph("<b>OBSERVED EVIDENCE (On-Chain Facts)</b>", table_cell_bold),
            Paragraph("<b>DERIVED ANALYSIS (Forensic Inference)</b>", table_cell_bold)
        ],
        [
            Paragraph(
                "• Cryptographically validated transactions from blockchain ledgers.<br/>"
                "• Immutable timestamps, block heights, and transfer values.<br/>"
                "• Directed edges between sending and receiving public keys.<br/>"
                "• Direct interactions with verified smart contracts.",
                table_cell
            ),
            Paragraph(
                "• Attribution confidence scores computed via multi-dimensional proximity.<br/>"
                "• Laundering typology pattern matches (peel chains, rapid dispersal).<br/>"
                "• Behavioral heuristics distinguishing hot wallets, deposit hubs, and mules.<br/>"
                "• Forensic claim: <i>interacts_with</i> (does not assert ownership).",
                table_cell
            )
        ]
    ]
    t_method = Table(method_data, colWidths=[8.7 * cm, 8.7 * cm])
    t_method.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e2e8f0")),
        ('BACKGROUND', (0,1), (-1,-1), _LIGHT_BG),
        ('GRID', (0,0), (-1,-1), 0.5, _BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_method)
    story.append(Spacer(1, 0.4 * cm))

    # ── 5. VASP Attribution Candidates ──────────────────────────────────────
    story.append(Paragraph("3. VASP Attribution Findings", section_style))
    matches = trace_result.get("matches", [])
    if matches:
        vasp_rows = [
            [Paragraph("<b>VASP / Entity</b>", table_cell_bold),
             Paragraph("<b>Hops</b>", table_cell_bold),
             Paragraph("<b>Confidence</b>", table_cell_bold),
             Paragraph("<b>Flow Volume</b>", table_cell_bold),
             Paragraph("<b>FIU-IND Status</b>", table_cell_bold),
             Paragraph("<b>Attribution Path</b>", table_cell_bold)]
        ]
        for m in matches[:5]:
            path_short = " → ".join([p[:6] + ".." for p in m.get("path", [])])
            fiu_str = "Registered" if m.get("fiu_registered") else "Offshore/Non-Reg"
            vasp_rows.append([
                Paragraph(m.get("vasp_name", "VASP"), table_cell_bold),
                Paragraph(str(m.get("hops", "-")), table_cell),
                Paragraph(f"<b>{m.get('confidence', 0)}%</b>", table_cell),
                Paragraph(f"{m.get('volume_eth', 0)} ETH", table_cell),
                Paragraph(fiu_str, table_cell),
                Paragraph(f"<font name='Courier'>{path_short}</font>", table_cell)
            ])
        t_vasp = Table(vasp_rows, colWidths=[4.2 * cm, 1.2 * cm, 2.2 * cm, 2.2 * cm, 3.0 * cm, 4.6 * cm])
        t_vasp.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e2e8f0")),
            ('GRID', (0,0), (-1,-1), 0.5, _BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(t_vasp)
    else:
        story.append(Paragraph("No direct or intermediary VASP interactions identified within the hop threshold.", body_style))
    story.append(Spacer(1, 0.4 * cm))

    # ── 6. Hop-by-Hop Explanation ───────────────────────────────────────────
    if top_match and top_match.get("explanation"):
        story.append(Paragraph("4. Attribution Rationale & Hop Walk", section_style))
        story.append(Paragraph(f"<b>Primary Match: {top_match.get('vasp_name')}</b>", sub_style))
        story.append(Paragraph(top_match.get("explanation"), body_style))
        story.append(Spacer(1, 0.3 * cm))

    # ── 7. Chronological Investigation Timeline ─────────────────────────────
    timeline = trace_result.get("timeline", [])
    if timeline:
        story.append(Paragraph("5. Investigation Timeline (Fund Flow Sequence)", section_style))
        time_rows = [
            [Paragraph("<b>Timestamp (UTC)</b>", table_cell_bold),
             Paragraph("<b>Event Type</b>", table_cell_bold),
             Paragraph("<b>Description</b>", table_cell_bold),
             Paragraph("<b>Amount</b>", table_cell_bold)]
        ]
        for te in timeline[:8]:
            t_str = te.get("time", "").replace("T", " ").replace("Z", "")
            time_rows.append([
                Paragraph(t_str, table_cell),
                Paragraph(te.get("type", "transfer").upper(), table_cell_bold),
                Paragraph(te.get("desc", ""), table_cell),
                Paragraph(f"{te.get('amount', 0)} ETH", table_cell)
            ])
        t_time = Table(time_rows, colWidths=[3.5 * cm, 2.8 * cm, 9.0 * cm, 2.1 * cm])
        t_time.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e2e8f0")),
            ('GRID', (0,0), (-1,-1), 0.5, _BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(t_time)
        story.append(Spacer(1, 0.4 * cm))

    # ── 8. Statutory Requisition / Recommended Next Steps ────────────────────
    story.append(Paragraph("6. Recommended Law Enforcement Action", section_style))
    sahyog = trace_result.get("sahyog_routing", {})
    action_text = sahyog.get("action", "Initiate standard preliminary inquiry.")
    disclosure_note = sahyog.get("disclosure_note", "")

    rec_box = [
        [Paragraph("<b>RECOMMENDED STATUTORY NOTICE:</b>", table_cell_bold)],
        [Paragraph(f"<b>{action_text}</b>", ParagraphStyle("Act", parent=styles["Normal"], fontSize=9, textColor=_RED, fontName="Helvetica-Bold"))],
        [Paragraph(disclosure_note, body_style)],
        [Paragraph("<b>Target Entity Contact:</b> " + (sahyog.get("primary_email") or "compliance@vasp.com") +
                   f" | <b>Reporting ID:</b> {sahyog.get('primary_fiu_id', 'N/A')}", table_cell)]
    ]
    t_rec = Table(rec_box, colWidths=[17.4 * cm])
    t_rec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#fef2f2")),
        ('BOX', (0,0), (-1,-1), 1, _RED),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_rec)
    story.append(Spacer(1, 0.4 * cm))

    # ── 9. Disclaimers & Technical Limitations ──────────────────────────────
    story.append(Paragraph("7. Limitations & Forensic Disclaimers", section_style))
    disclaimer = (
        "1. Blockchain analytics provides probabilistic intelligence based on public ledger state and labeled counterparty registries.<br/>"
        "2. Attribution of an intermediary hop to a VASP deposit wallet indicates observed fund flow (interacts_with) and does not automatically prove direct ownership or culpability without corroborated exchange KYC disclosure.<br/>"
        "3. This document constitutes preliminary investigative intelligence under the Information Technology Act (2000) and Bharatiya Sakshya Adhiniyam (BSA) 2023. Final evidentiary submission requires formal production orders under Section 91 CrPC / Section 94 BNSS."
    )
    story.append(Paragraph(disclaimer, ParagraphStyle("Disc", parent=styles["Normal"], fontSize=7.5, leading=10, textColor=_MUTED)))

    doc.build(story)
    buffer.seek(0)
    return buffer
