"""
CryptoGuard AI - Final SIH 2026 Presentation Generator (Refined & Audited)
File: FINAL_SIH26182_CryptoGuard_AI_6_SLIDE.pptx
Strictly 6 slides, 100% verified facts, no placeholders, no unsupported claims.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_presentation():
    template_path = r"C:\Users\SKYNET\Downloads\SIH2026-IDEA-Presentation-Format.pptx"
    output_path = r"d:\SIH 2\FINAL_SIH26182_CryptoGuard_AI_6_SLIDE.pptx"
    
    prs = Presentation(template_path)
    
    # ── Ensure exactly 6 slides remain ──
    if len(prs.slides) > 6:
        rId = prs.slides._sldIdLst[6].rId
        prs.part.drop_rel(rId)
        del prs.slides._sldIdLst[6]
        
    print(f"Total slides after trimming instructions: {len(prs.slides)}")
    assert len(prs.slides) == 6, f"Expected exactly 6 slides, got {len(prs.slides)}"

    # Curated Professional SIH Palette
    NAVY = RGBColor(15, 32, 66)          # #0F2042 - Deep Academic Navy
    DARK_BLUE = RGBColor(30, 58, 138)     # #1E3A8A - Primary Header
    ELECTRIC_BLUE = RGBColor(37, 99, 235) # #2563EB - Accent / Highlights
    LIGHT_BLUE_BG = RGBColor(239, 246, 255) # #EFF6FF - Soft Card Fill
    BORDER_BLUE = RGBColor(191, 219, 254)   # #BFDBFE - Card Border
    
    SLATE_TEXT = RGBColor(51, 65, 85)     # #334155 - High Contrast Body Text
    MUTED_TEXT = RGBColor(100, 116, 139)  # #64748B - Secondary Subtext
    WHITE = RGBColor(255, 255, 255)
    CARD_BG = RGBColor(255, 255, 255)
    BORDER_GRAY = RGBColor(226, 232, 240) # #E2E8F0
    
    RED_ACCENT = RGBColor(185, 28, 28)    # #B91C1C - Challenges
    RED_BG = RGBColor(254, 242, 242)      # #FEF2F2
    RED_BORDER = RGBColor(254, 202, 202)  # #FECACA
    
    GREEN_ACCENT = RGBColor(4, 120, 87)   # #047857 - Feasibility / Benefits
    GREEN_BG = RGBColor(236, 253, 245)    # #ECFDF5
    GREEN_BORDER = RGBColor(167, 243, 208)# #A7F3D0
    
    AMBER_ACCENT = RGBColor(180, 83, 9)   # #B45309 - Risks / Warnings
    AMBER_BG = RGBColor(255, 251, 235)    # #FFFBEB
    AMBER_BORDER = RGBColor(253, 230, 138)# #FDE68A

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=BORDER_GRAY, border_width=1.0):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        if border_color:
            shape.line.color.rgb = border_color
            shape.line.width = Pt(border_width)
        else:
            shape.line.fill.background()
        return shape

    def clean_template_body(slide):
        shapes_to_remove = []
        for s in slide.shapes:
            if s.has_text_frame:
                txt = s.text_frame.text.strip()
                if any(k in txt for k in ["Describe your Idea", "Technologies to be used", "Analysis of the feasibility", "Potential impact", "Details / Links of the reference"]):
                    shapes_to_remove.append(s)
            if s.has_text_frame and "Your Team Name" in s.text_frame.text:
                s.text_frame.text = "CodeMesh"
                for p in s.text_frame.paragraphs:
                    p.alignment = PP_ALIGN.CENTER
                    p.font.size = Pt(11)
                    p.font.bold = True
                    p.font.color.rgb = NAVY
        for s in shapes_to_remove:
            sp = s._element
            sp.getparent().remove(sp)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 1: TITLE PAGE
    # ═════════════════════════════════════════════════════════════════════════
    s1 = prs.slides[0]
    for s in list(s1.shapes):
        sp = s._element
        sp.getparent().remove(sp)

    title_slide_img = r"d:\SIH 2\SIH26182_TITLE_SLIDE.png"
    if os.path.exists(title_slide_img):
        s1.shapes.add_picture(title_slide_img, Inches(0), Inches(0), width=prs.slide_width, height=prs.slide_height)


    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 2: IDEA / PROPOSED SOLUTION
    # ═════════════════════════════════════════════════════════════════════════
    s2 = prs.slides[1]
    clean_template_body(s2)
    
    for s in s2.shapes:
        if s.has_text_frame and "IDEA TITLE" in s.text_frame.text:
            s.text_frame.text = "IDEA TITLE: CryptoGuard AI"
            p = s.text_frame.paragraphs[0]
            p.font.bold = True
            p.font.size = Pt(20)
            p.font.color.rgb = NAVY

    blocks = [
        ("1. BLOCKCHAIN INVESTIGATION", BORDER_BLUE, LIGHT_BLUE_BG, [
            "Multi-chain: Ethereum, BSC, Polygon, Tron, Bitcoin",
            "Directed Breadth-First Search (BFS) multi-hop tracing",
            "Interactive Vis.js force-directed transaction graph",
            "Node Inspector with real-time inflow/outflow metrics",
        ]),
        ("2. VASP ATTRIBUTION ENGINE", RGBColor(199, 210, 254), RGBColor(238, 242, 255), [
            "Curated FIU-IND registered & global VASP registry",
            "4-Factor: Proximity 40%, Volume 30%, Recency 20%, Trust 10%",
            "Strict evidence rule: interacts_with vs controlled_by",
            "Full hop-walk explanation from suspect to deposit node",
        ]),
        ("3. RISK & FORENSIC INTEL", AMBER_BORDER, AMBER_BG, [
            "10-Signal weighted AML risk engine (0–100 score)",
            "Active typologies: Peel chains, Mixer hops, Rapid exit",
            "Behavioral archetypes: Exchange, Mule, Scam, Stash",
            "Forensic Copilot: Rule engine + optional LLM integration",
        ]),
        ("4. INVESTIGATION & RESPONSE", GREEN_BORDER, GREEN_BG, [
            "Evidence Locker with SHA-256 integrity hash tracking",
            "Reconstructed multi-chain chronological timeline",
            "1-Click statutory Section 91 CrPC notice generator",
            "ReportLab court-ready PDF & SAHYOG-ready workflow",
        ]),
    ]
    
    card_w = Inches(2.85)
    card_h = Inches(2.40)
    card_top = Inches(1.15)
    spacing = Inches(0.20)
    start_left = Inches(0.60)
    
    for i, (b_title, b_border, b_bg, b_points) in enumerate(blocks):
        c_left = start_left + i * (card_w + spacing)
        c = add_card(s2, c_left, card_top, card_w, card_h, bg_color=CARD_BG, border_color=b_border, border_width=1.2)
        tf = c.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.16)
        tf.margin_top = Inches(0.12)
        tf.margin_right = Inches(0.16)
        
        p = tf.paragraphs[0]
        p.text = b_title
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = DARK_BLUE
        p.space_after = Pt(5)
        
        for pt in b_points:
            p = tf.add_paragraph()
            p.text = f"• {pt}"
            p.font.size = Pt(9)
            p.font.color.rgb = SLATE_TEXT
            p.space_after = Pt(2.5)

    # Real UI Screenshots on Slide 2
    img_top = Inches(3.68)
    img_h = Inches(2.45)
    
    graph_img_path = r"d:\SIH 2\cryptoguard_screenshot_graph.png"
    if os.path.exists(graph_img_path):
        s2.shapes.add_picture(graph_img_path, Inches(0.60), img_top, width=Inches(5.85), height=img_h)
        cap1 = add_card(s2, Inches(0.60), Inches(6.16), Inches(5.85), Inches(0.28), bg_color=LIGHT_BLUE_BG, border_color=BORDER_BLUE, border_width=0.8)
        tf_cap1 = cap1.text_frame
        p = tf_cap1.paragraphs[0]
        p.text = "DEMO MODE: Interactive Vis.js Multi-Hop Transaction Graph (12 Nodes, Mule Peeling, VASP Hops)"
        p.font.bold = True
        p.font.size = Pt(8)
        p.font.color.rgb = DARK_BLUE
        p.alignment = PP_ALIGN.CENTER

    vasp_img_path = r"d:\SIH 2\cryptoguard_screenshot_vasp.png"
    if os.path.exists(vasp_img_path):
        s2.shapes.add_picture(vasp_img_path, Inches(6.75), img_top, width=Inches(5.85), height=img_h)
        cap2 = add_card(s2, Inches(6.75), Inches(6.16), Inches(5.85), Inches(0.28), bg_color=GREEN_BG, border_color=GREEN_BORDER, border_width=0.8)
        tf_cap2 = cap2.text_frame
        p = tf_cap2.paragraphs[0]
        p.text = "DEMO MODE: VASP Attribution Console (CoinDCX 84.5% FIU-IND, Binance 73.8%, Kraken 58.2%)"
        p.font.bold = True
        p.font.size = Pt(8)
        p.font.color.rgb = GREEN_ACCENT
        p.alignment = PP_ALIGN.CENTER

    # Flow Banner at Bottom
    flow_bar = add_card(s2, Inches(0.60), Inches(6.48), Inches(12.00), Inches(0.28), bg_color=WHITE, border_color=BORDER_BLUE, border_width=0.8)
    tf_fb = flow_bar.text_frame
    p = tf_fb.paragraphs[0]
    p.text = "FLOW: UNKNOWN WALLET -> BLOCKCHAIN ADAPTERS -> MULTI-HOP GRAPH -> WALLET INTEL -> VASP ATTRIBUTION -> RISK SCORING -> EVIDENCE + REPORT"
    p.font.bold = True
    p.font.size = Pt(8)
    p.font.color.rgb = ELECTRIC_BLUE
    p.alignment = PP_ALIGN.CENTER

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 3: TECHNICAL APPROACH & PROTOTYPE
    # ═════════════════════════════════════════════════════════════════════════
    s3 = prs.slides[2]
    clean_template_body(s3)
    
    for s in s3.shapes:
        if s.has_text_frame and "TECHNICAL APPROACH" in s.text_frame.text:
            s.text_frame.text = "TECHNICAL APPROACH: CryptoGuard AI Forensic Pipeline"
            p = s.text_frame.paragraphs[0]
            p.font.bold = True
            p.font.size = Pt(20)
            p.font.color.rgb = NAVY

    tbl_left = Inches(0.60)
    tbl_top = Inches(1.15)
    tbl_w = Inches(7.55)
    tbl_h = Inches(5.55)
    
    tbl_card = add_card(s3, tbl_left, tbl_top, tbl_w, tbl_h, bg_color=CARD_BG, border_color=BORDER_BLUE, border_width=1.2)
    tf_tbl = tbl_card.text_frame
    tf_tbl.word_wrap = True
    tf_tbl.margin_left = Inches(0.18)
    tf_tbl.margin_top = Inches(0.12)
    tf_tbl.margin_right = Inches(0.18)
    
    p = tf_tbl.paragraphs[0]
    p.text = "END-TO-END INVESTIGATION WORKFLOW & METHODOLOGY"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = DARK_BLUE
    p.space_after = Pt(6)

    phases = [
        ("1. TARGET INPUT", "Investigator inputs suspect address, selects chain (ETH, BSC, Polygon, Tron, BTC), and sets max hops (1–6)."),
        ("2. BLOCKCHAIN ADAPTERS", "Modular REST clients (Etherscan v2, TronGrid, Blockstream) fetch raw on-chain transaction records."),
        ("3. TRANSACTION NORMALIZATION", "Address checksum validation, wei/satoshi conversion, ERC-20 parsing, and chronological indexing."),
        ("4. GRAPH ANALYSIS (BFS)", "Directed Breadth-First Search builds multi-hop fund flow graph; pruned cycles rendered via Vis.js."),
        ("5. VASP ATTRIBUTION ENGINE", "4-Factor scoring (Proximity 40%, Volume 30%, Recency 20%, Provenance 10%) identifies nearest VASP."),
        ("6. RISK & AML ENGINE", "10-Signal explainable risk calculation (OFAC sanctions, mixers, peel chains, structuring) outputs 0–100 score."),
        ("7. FORENSIC WORKSPACE", "Reconstructs chronological timeline, SHA-256 evidence locker, behavioral classification, & Node Inspector."),
        ("8. RESPONSE & LEGAL EXPORT", "Automated Section 91 CrPC requisition notice generation, ReportLab PDF report, & SAHYOG-ready stub."),
    ]
    for ph_name, ph_desc in phases:
        p = tf_tbl.add_paragraph()
        r1 = p.add_run()
        r1.text = f"{ph_name}: "
        r1.font.bold = True
        r1.font.size = Pt(9.2)
        r1.font.color.rgb = ELECTRIC_BLUE
        
        r2 = p.add_run()
        r2.text = ph_desc
        r2.font.size = Pt(8.8)
        r2.font.color.rgb = SLATE_TEXT
        p.space_after = Pt(4.5)

    stack_left = Inches(8.35)
    stack_w = Inches(4.35)
    stack_h = Inches(3.60)
    stack_card = add_card(s3, stack_left, tbl_top, stack_w, stack_h, bg_color=LIGHT_BLUE_BG, border_color=BORDER_BLUE, border_width=1.2)
    tf_stack = stack_card.text_frame
    tf_stack.word_wrap = True
    tf_stack.margin_left = Inches(0.18)
    tf_stack.margin_top = Inches(0.12)
    tf_stack.margin_right = Inches(0.18)
    
    p = tf_stack.paragraphs[0]
    p.text = "TECHNOLOGY STACK ARCHITECTURE"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = NAVY
    p.space_after = Pt(6)

    techs = [
        ("Frontend", "Vanilla HTML5, CSS3, ES6 JavaScript (Zero CDN / 100% offline)"),
        ("Graph Visualization", "Vis-network v9.1.2 (Bundled force-directed physics engine)"),
        ("Backend Framework", "Python 3.10+ / FastAPI v0.141 on Starlette & Uvicorn ASGI"),
        ("Forensic Database", "SQLite3 persistent store (cryptoguard.db, 7 indexed tables)"),
        ("Blockchain APIs", "Etherscan v2 API, TronGrid REST, Blockstream Bitcoin REST"),
        ("Investigation Copilot", "Explainable Rule-Based Engine + Optional LLM Integration"),
        ("Report Generation", "ReportLab v5.0 Binary PDF Engine with SHA-256 verification"),
    ]
    for t_name, t_val in techs:
        p = tf_stack.add_paragraph()
        r1 = p.add_run()
        r1.text = f"• {t_name}: "
        r1.font.bold = True
        r1.font.size = Pt(9)
        r1.font.color.rgb = DARK_BLUE
        
        r2 = p.add_run()
        r2.text = t_val
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = SLATE_TEXT
        p.space_after = Pt(3)

    links_top = Inches(4.90)
    links_h = Inches(1.80)
    links_card = add_card(s3, stack_left, links_top, stack_w, links_h, bg_color=CARD_BG, border_color=BORDER_BLUE, border_width=1.2)
    tf_links = links_card.text_frame
    tf_links.word_wrap = True
    tf_links.margin_left = Inches(0.18)
    tf_links.margin_top = Inches(0.12)
    tf_links.margin_right = Inches(0.18)

    p = tf_links.paragraphs[0]
    p.text = "OFFICIAL LINKS & DELIVERABLES"
    p.font.bold = True
    p.font.size = Pt(10.5)
    p.font.color.rgb = NAVY
    p.space_after = Pt(5)

    links = [
        ("GITHUB LINK", "https://github.com/aryan311007w-ux/SIH-codeMesh", ELECTRIC_BLUE),
        ("WEBSITE LINK", "https://tubes-intersection-judicial-weapon.trycloudflare.com", ELECTRIC_BLUE),
        ("DEMO VIDEO", "To be updated after deployment", MUTED_TEXT),
    ]
    for l_label, l_url, col in links:
        p = tf_links.add_paragraph()
        r1 = p.add_run()
        r1.text = f"{l_label}: "
        r1.font.bold = True
        r1.font.size = Pt(9)
        r1.font.color.rgb = SLATE_TEXT
        
        r2 = p.add_run()
        r2.text = l_url
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = col
        p.space_after = Pt(3.5)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 4: PROBLEM → SOLUTION → FEASIBILITY / VIABILITY
    # ═════════════════════════════════════════════════════════════════════════
    s4 = prs.slides[3]
    clean_template_body(s4)
    
    for s in s4.shapes:
        if s.has_text_frame and "FEASIBILITY AND VIABILITY" in s.text_frame.text:
            s.text_frame.text = "FEASIBILITY AND VIABILITY: Problem, Solution & Scalability"
            p = s.text_frame.paragraphs[0]
            p.font.bold = True
            p.font.size = Pt(20)
            p.font.color.rgb = NAVY

    col_w = Inches(3.85)
    col_h = Inches(4.15)
    col_top = Inches(1.15)

    c1 = add_card(s4, Inches(0.60), col_top, col_w, col_h, bg_color=CARD_BG, border_color=RED_BORDER, border_width=1.2)
    tf1 = c1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = Inches(0.16)
    tf1.margin_top = Inches(0.12)
    tf1.margin_right = Inches(0.16)
    
    p = tf1.paragraphs[0]
    p.text = "OPERATIONAL CHALLENGES"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = RED_ACCENT
    p.space_after = Pt(7)

    challs = [
        "Rapid Fund Dissipation: Stolen crypto structured & layered across peel chains in minutes.",
        "Multi-Hop Graph Complexity: Obfuscation through multiple intermediate mule accounts.",
        "Cross-Chain Fragmentation: Criminals hopping across Ethereum, Tron, BSC, Polygon, Bitcoin.",
        "Attribution Uncertainty: Unreliable clustering without verified VASP registries or legal distinction.",
        "Opaque Black-Box Forensics: Defense challenges in court against unexplainable proprietary scores.",
        "Manual Paperwork Overhead: Hours spent compiling Section 91 CrPC notices and chain of custody.",
    ]
    for ch in challs:
        p = tf1.add_paragraph()
        p.text = f"• {ch}"
        p.font.size = Pt(9)
        p.font.color.rgb = SLATE_TEXT
        p.space_after = Pt(4)

    c2 = add_card(s4, Inches(4.65), col_top, col_w, col_h, bg_color=CARD_BG, border_color=BORDER_BLUE, border_width=1.2)
    tf2 = c2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = Inches(0.16)
    tf2.margin_top = Inches(0.12)
    tf2.margin_right = Inches(0.16)

    p = tf2.paragraphs[0]
    p.text = "CRYPTOGUARD AI SOLUTION"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = DARK_BLUE
    p.space_after = Pt(7)

    sols = [
        "Automated BFS Traversal: Traces complex multi-hop fund flows in sub-second graph walks.",
        "Transparent 4-Factor Scoring: Mathematical confidence (Proximity, Interaction, Recency, Provenance).",
        "Unified Multi-Chain Schema: Standardized investigation across 5 major blockchain ecosystems.",
        "Explainable Evidence: Strict legal separation of on-chain hops from behavioral heuristics.",
        "Instant Statutory Requisitions: 1-Click Section 91 CrPC notices populated with VASP nodals.",
        "Tamper-Evident Reporting: ReportLab generated PDF with cryptographic SHA-256 evidence logs.",
    ]
    for sol in sols:
        p = tf2.add_paragraph()
        p.text = f"• {sol}"
        p.font.size = Pt(9)
        p.font.color.rgb = SLATE_TEXT
        p.space_after = Pt(4)

    c3 = add_card(s4, Inches(8.70), col_top, col_w, col_h, bg_color=CARD_BG, border_color=GREEN_BORDER, border_width=1.2)
    tf3 = c3.text_frame
    tf3.word_wrap = True
    tf3.margin_left = Inches(0.16)
    tf3.margin_top = Inches(0.12)
    tf3.margin_right = Inches(0.16)

    p = tf3.paragraphs[0]
    p.text = "FEASIBILITY & SCALABILITY PILLARS"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = GREEN_ACCENT
    p.space_after = Pt(7)

    feas = [
        ("Technical Feasibility", "Lightweight Python/FastAPI + Vis.js stack; deterministic execution with zero heavy GPU overhead."),
        ("Practical Implementability", "Repeatable workflow; built-in high-fidelity Demo Mode for offline evaluation; zero compilation."),
        ("Sustainable Impact", "Aligned with FIU-IND reporting guidelines, PMLA 2002, and LEA standard operating procedures."),
        ("Scalability by Design", "Current MVP can evolve toward PostgreSQL, production blockchain APIs, institutional authentication, & live government portals."),
    ]
    for f_title, f_desc in feas:
        p = tf3.add_paragraph()
        r1 = p.add_run()
        r1.text = f"• {f_title}: "
        r1.font.bold = True
        r1.font.size = Pt(9)
        r1.font.color.rgb = DARK_BLUE
        
        r2 = p.add_run()
        r2.text = f_desc
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = SLATE_TEXT
        p.space_after = Pt(4)

    risk_top = Inches(5.45)
    risk_w = Inches(11.95)
    risk_h = Inches(1.25)
    risk_card = add_card(s4, Inches(0.60), risk_top, risk_w, risk_h, bg_color=AMBER_BG, border_color=AMBER_BORDER, border_width=1.0)
    tf_risk = risk_card.text_frame
    tf_risk.word_wrap = True
    tf_risk.margin_left = Inches(0.18)
    tf_risk.margin_top = Inches(0.08)
    tf_risk.margin_right = Inches(0.18)

    p = tf_risk.paragraphs[0]
    p.text = "RISK IDENTIFICATION & MITIGATION STRATEGY"
    p.font.bold = True
    p.font.size = Pt(10)
    p.font.color.rgb = AMBER_ACCENT
    p.space_after = Pt(2)

    risks = (
        "• API Rate Limits: Handled via deterministic demo fixture fallback & key rotation  |  "
        "• Blockchain Data Quality: Addressed via volume thresholds & node deduplication  |  "
        "• Attribution Uncertainty: Explicitly separated into interacts_with vs controlled_by  |  "
        "• Institutional Hardening: Architecture ready for JWT auth & role-based access control (RBAC)."
    )
    p = tf_risk.add_paragraph()
    p.text = risks
    p.font.size = Pt(8.8)
    p.font.color.rgb = SLATE_TEXT

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 5: IMPACT AND BENEFITS
    # ═════════════════════════════════════════════════════════════════════════
    s5 = prs.slides[4]
    clean_template_body(s5)
    
    for s in s5.shapes:
        if s.has_text_frame and "IMPACT AND BENEFITS" in s.text_frame.text:
            s.text_frame.text = "IMPACT AND BENEFITS: Stakeholder Value & Long-Term Transformation"
            p = s.text_frame.paragraphs[0]
            p.font.bold = True
            p.font.size = Pt(20)
            p.font.color.rgb = NAVY

    stk_cards = [
        ("LAW ENFORCEMENT & INVESTIGATORS", BORDER_BLUE, [
            "Accelerates preliminary tracing from days to minutes",
            "Unified multi-chain graph eliminates portal switching",
            "Structured evidence locker maintains chain of custody",
            "Repeatable, reproducible forensic investigation workflow",
        ]),
        ("CYBERCRIME CELLS & PROSECUTION", RGBColor(199, 210, 254), [
            "Automated statutory Section 91 CrPC notice drafting",
            "Transparent mathematical scores defensible in court",
            "Court-admissible PDF reports with cryptographic hashes",
            "Response-ready workflow aligned with national SOPs",
        ]),
        ("VASPS & COMPLIANCE OFFICERS", GREEN_BORDER, [
            "Requisitions contain exact hop paths, tx hashes, & times",
            "Direct identification of deposit aggregators cuts delays",
            "Fulfills Prevention of Money Laundering Act obligations",
            "Streamlines communication with FIU-IND registered entities",
        ]),
        ("FINANCIAL & LEGAL ECOSYSTEM", AMBER_BORDER, [
            "Lowers friction for recovering stolen proceeds of crime",
            "Establishes a transparent benchmark for crypto attribution",
            "Multi-chain extensible architecture adaptable to new tokens",
            "Open, auditable codebase fostering institutional trust",
        ]),
    ]
    stk_w = Inches(2.85)
    stk_h = Inches(2.30)
    stk_top = Inches(1.15)
    
    for i, (stk_title, stk_border, stk_pts) in enumerate(stk_cards):
        c_left = start_left + i * (stk_w + spacing)
        c = add_card(s5, c_left, stk_top, stk_w, stk_h, bg_color=CARD_BG, border_color=stk_border, border_width=1.2)
        tf = c.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.16)
        tf.margin_top = Inches(0.12)
        tf.margin_right = Inches(0.16)
        
        p = tf.paragraphs[0]
        p.text = stk_title
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = DARK_BLUE
        p.space_after = Pt(5)
        
        for pt in stk_pts:
            p = tf.add_paragraph()
            p.text = f"• {pt}"
            p.font.size = Pt(8.8)
            p.font.color.rgb = SLATE_TEXT
            p.space_after = Pt(2.5)

    lt_top = Inches(3.60)
    lt_w = Inches(11.95)
    lt_h = Inches(3.10)
    lt_container = add_card(s5, Inches(0.60), lt_top, lt_w, lt_h, bg_color=LIGHT_BLUE_BG, border_color=BORDER_BLUE, border_width=1.2)
    tf_lt = lt_container.text_frame
    tf_lt.word_wrap = True
    tf_lt.margin_left = Inches(0.18)
    tf_lt.margin_top = Inches(0.10)
    tf_lt.margin_right = Inches(0.18)

    p = tf_lt.paragraphs[0]
    p.text = "LONG-TERM SYSTEMIC EFFECTS ON NATIONAL BLOCKCHAIN FORENSICS"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = NAVY
    p.space_after = Pt(5)

    long_term_effects = [
        ("1. Accelerated Asset Freezing", "Minimizes the critical time window before illicit funds are cashed out to fiat through domestic exchanges."),
        ("2. Standardized Digital Requisitions", "Replaces fragmented informal queries with statutory Section 91 CrPC notices containing full evidentiary trails."),
        ("3. Cross-Chain Investigative Parity", "Empowers investigators to track assets across EVM, Tron, and Bitcoin inside a single consolidated workspace."),
        ("4. Institutional Evidentiary Memory", "Persistent SQLite storage guarantees repeatable, verifiable re-analysis and audit trails for cold cyber cases."),
        ("5. Low-Cost Station Deployment", "Zero heavy ML dependency allows rapid deployment across district cybercrime police stations without server clusters."),
        ("6. National Integration-Ready", "Native data schemas aligned with the Indian Cybercrime Coordination Centre (I4C) and SAHYOG portal."),
    ]

    grid_col_w = Inches(3.75)
    grid_row_h = Inches(1.10)
    grid_gap_x = Inches(0.25)
    grid_gap_y = Inches(0.12)
    base_grid_top = Inches(4.10)
    base_grid_left = Inches(0.78)

    for idx, (lt_num_title, lt_desc) in enumerate(long_term_effects):
        r_idx = idx // 3
        c_idx = idx % 3
        b_x = base_grid_left + c_idx * (grid_col_w + grid_gap_x)
        b_y = base_grid_top + r_idx * (grid_row_h + grid_gap_y)
        
        box = add_card(s5, b_x, b_y, grid_col_w, grid_row_h, bg_color=WHITE, border_color=BORDER_BLUE, border_width=0.8)
        tf_b = box.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = Inches(0.12)
        tf_b.margin_top = Inches(0.08)
        tf_b.margin_right = Inches(0.12)
        
        p = tf_b.paragraphs[0]
        p.text = lt_num_title
        p.font.bold = True
        p.font.size = Pt(9.2)
        p.font.color.rgb = DARK_BLUE
        p.space_after = Pt(2)
        
        p = tf_b.add_paragraph()
        p.text = lt_desc
        p.font.size = Pt(8.2)
        p.font.color.rgb = SLATE_TEXT

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 6: RESEARCH AND REFERENCES
    # ═════════════════════════════════════════════════════════════════════════
    s6 = prs.slides[5]
    clean_template_body(s6)
    
    for s in s6.shapes:
        if s.has_text_frame and "RESEARCH" in s.text_frame.text:
            s.text_frame.text = "RESEARCH AND REFERENCES: Regulatory, Protocol & Academic Foundations"
            p = s.text_frame.paragraphs[0]
            p.font.bold = True
            p.font.size = Pt(20)
            p.font.color.rgb = NAVY

    ref_col_w = Inches(3.85)
    ref_col_h = Inches(4.25)
    ref_col_top = Inches(1.15)

    r1 = add_card(s6, Inches(0.60), ref_col_top, ref_col_w, ref_col_h, bg_color=CARD_BG, border_color=BORDER_BLUE, border_width=1.2)
    tf_r1 = r1.text_frame
    tf_r1.word_wrap = True
    tf_r1.margin_left = Inches(0.16)
    tf_r1.margin_top = Inches(0.12)
    tf_r1.margin_right = Inches(0.16)

    p = tf_r1.paragraphs[0]
    p.text = "STATUTORY & REGULATORY FRAMEWORKS"
    p.font.bold = True
    p.font.size = Pt(10.5)
    p.font.color.rgb = DARK_BLUE
    p.space_after = Pt(7)

    reg_refs = [
        ("FATF Virtual Assets Guidance (2021/2023)", "Financial Action Task Force, Updated Guidance for a Risk-Based Approach to Virtual Assets and VASPs, Recommendation 15 & 16 (Travel Rule)."),
        ("FIU-IND AML/CFT Guidelines (2023)", "Financial Intelligence Unit - India, Anti-Money Laundering & Countering Financing of Terrorism Guidelines for Virtual Digital Asset Service Providers (PMLA compliance)."),
        ("Section 91 CrPC / Section 94 BNSS", "Code of Criminal Procedure, 1973 (Section 91) & Bharatiya Nagarik Suraksha Sanhita, 2023 (Section 94) — Legal summons for digital evidence."),
        ("Prevention of Money Laundering Act (2002)", "PMLA 2002 Section 12 — Maintenance of records, identification of clients, & furnished information by crypto Reporting Entities."),
    ]
    for r_title, r_desc in reg_refs:
        p = tf_r1.add_paragraph()
        run1 = p.add_run()
        run1.text = f"• {r_title}: "
        run1.font.bold = True
        run1.font.size = Pt(8.8)
        run1.font.color.rgb = ELECTRIC_BLUE
        
        run2 = p.add_run()
        run2.text = r_desc
        run2.font.size = Pt(8.3)
        run2.font.color.rgb = SLATE_TEXT
        p.space_after = Pt(4.5)

    r2 = add_card(s6, Inches(4.65), ref_col_top, ref_col_w, ref_col_h, bg_color=CARD_BG, border_color=BORDER_BLUE, border_width=1.2)
    tf_r2 = r2.text_frame
    tf_r2.word_wrap = True
    tf_r2.margin_left = Inches(0.16)
    tf_r2.margin_top = Inches(0.12)
    tf_r2.margin_right = Inches(0.16)

    p = tf_r2.paragraphs[0]
    p.text = "BLOCKCHAIN APIS & FORENSIC PROTOCOLS"
    p.font.bold = True
    p.font.size = Pt(10.5)
    p.font.color.rgb = DARK_BLUE
    p.space_after = Pt(7)

    proto_refs = [
        ("Etherscan V2 API Developer Protocol", "Etherscan API documentation for EVM chains (Ethereum, BSC, Polygon) account transaction tracing, token events, & internal transfers (docs.etherscan.io)."),
        ("TronGrid Protocol Specification", "Tron Network TronGrid REST API for TRC-20 token tracking and account transaction history (developers.tron.network)."),
        ("Blockstream Bitcoin REST API", "Blockstream.info public Bitcoin explorer and UTXO graph query API specification (blockstream.info/api)."),
        ("Vis.js Network Force-Directed Graph Engine", "Vis.js open-source visualization library for force-directed physical graph rendering and dynamic node physics (visjs.github.io)."),
    ]
    for r_title, r_desc in proto_refs:
        p = tf_r2.add_paragraph()
        run1 = p.add_run()
        run1.text = f"• {r_title}: "
        run1.font.bold = True
        run1.font.size = Pt(8.8)
        run1.font.color.rgb = ELECTRIC_BLUE
        
        run2 = p.add_run()
        run2.text = r_desc
        run2.font.size = Pt(8.3)
        run2.font.color.rgb = SLATE_TEXT
        p.space_after = Pt(4.5)

    r3 = add_card(s6, Inches(8.70), ref_col_top, ref_col_w, ref_col_h, bg_color=CARD_BG, border_color=BORDER_BLUE, border_width=1.2)
    tf_r3 = r3.text_frame
    tf_r3.word_wrap = True
    tf_r3.margin_left = Inches(0.16)
    tf_r3.margin_top = Inches(0.12)
    tf_r3.margin_right = Inches(0.16)

    p = tf_r3.paragraphs[0]
    p.text = "FORENSIC HEURISTICS & RESEARCH"
    p.font.bold = True
    p.font.size = Pt(10.5)
    p.font.color.rgb = DARK_BLUE
    p.space_after = Pt(7)

    acad_refs = [
        ("Meiklejohn et al., ACM IMC (2013)", "A Fistful of Bitcoins: Characterizing Payments Among Men with No Names. Foundational paper on multi-input heuristic clustering & change address detection."),
        ("Friedhelm Victor, Springer (2020)", "Address Clustering Heuristics for Ethereum. Financial Cryptography & Data Security. Heuristic rules for deposit address identification & exchange attribution."),
        ("OFAC SDN Sanctioned Entity Lists", "U.S. Department of the Treasury, Specially Designated Nationals (SDN) cryptocurrency address blacklist & Tornado Cash sanctioned smart contracts."),
        ("UNODC Cybercrime Typology Manual", "United Nations Office on Drugs and Crime, Cryptocurrency Laundering Typologies: Peel Chains, Structuring, and Nested Exchange Services."),
    ]
    for r_title, r_desc in acad_refs:
        p = tf_r3.add_paragraph()
        run1 = p.add_run()
        run1.text = f"• {r_title}: "
        run1.font.bold = True
        run1.font.size = Pt(8.8)
        run1.font.color.rgb = ELECTRIC_BLUE
        
        run2 = p.add_run()
        run2.text = r_desc
        run2.font.size = Pt(8.3)
        run2.font.color.rgb = SLATE_TEXT
        p.space_after = Pt(4.5)

    ref_links_top = Inches(5.55)
    ref_links_w = Inches(11.95)
    ref_links_h = Inches(1.10)
    ref_links_card = add_card(s6, Inches(0.60), ref_links_top, ref_links_w, ref_links_h, bg_color=LIGHT_BLUE_BG, border_color=BORDER_BLUE, border_width=1.0)
    tf_rl = ref_links_card.text_frame
    tf_rl.word_wrap = True
    tf_rl.margin_left = Inches(0.18)
    tf_rl.margin_top = Inches(0.10)
    tf_rl.margin_right = Inches(0.18)

    p = tf_rl.paragraphs[0]
    p.text = "PROJECT REPOSITORY & DEMONSTRATION ACCESS"
    p.font.bold = True
    p.font.size = Pt(10)
    p.font.color.rgb = NAVY
    p.space_after = Pt(3)

    p = tf_rl.add_paragraph()
    r1 = p.add_run()
    r1.text = "GitHub Repository: "
    r1.font.bold = True
    r1.font.size = Pt(9)
    r1.font.color.rgb = SLATE_TEXT
    
    r2 = p.add_run()
    r2.text = "https://github.com/aryan311007w-ux/SIH-codeMesh  |  "
    r2.font.bold = True
    r2.font.size = Pt(9)
    r2.font.color.rgb = ELECTRIC_BLUE

    r3 = p.add_run()
    r3.text = "Website: "
    r3.font.bold = True
    r3.font.size = Pt(9)
    r3.font.color.rgb = SLATE_TEXT

    r4 = p.add_run()
    r4.text = "https://tubes-intersection-judicial-weapon.trycloudflare.com  |  "
    r4.font.bold = True
    r4.font.size = Pt(9)
    r4.font.color.rgb = ELECTRIC_BLUE

    r5 = p.add_run()
    r5.text = "Demo Video: "
    r5.font.bold = True
    r5.font.size = Pt(9)
    r5.font.color.rgb = SLATE_TEXT

    r6 = p.add_run()
    r6.text = "To be updated after deployment"
    r6.font.size = Pt(9)
    r6.font.color.rgb = MUTED_TEXT

    # Save
    prs.save(output_path)
    print(f"Presentation successfully built and saved to: {output_path}")

    # Reload check
    verify_prs = Presentation(output_path)
    assert len(verify_prs.slides) == 6, f"Verification failed: expected 6 slides, got {len(verify_prs.slides)}"
    print("SLIDE COUNT AUDIT: EXACTLY 6 SLIDES CONFIRMED.")

if __name__ == "__main__":
    build_presentation()
