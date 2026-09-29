"""
CryptoGuard AI - SIH 2026 Submission Presentation Generator
Generates: FINAL_SIH26182_CryptoGuard_AI_SIH_SUBMISSION.pptx
Strictly 6 slides, high-impact visuals from Nano Banana, compact cards, 100% verified facts.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_submission_presentation():
    template_path = r"C:\Users\SKYNET\Downloads\SIH2026-IDEA-Presentation-Format.pptx"
    output_path = r"d:\SIH 2\FINAL_SIH26182_CryptoGuard_AI_SIH_SUBMISSION.pptx"
    visuals_dir = r"d:\SIH 2\visuals"
    
    prs = Presentation(template_path)
    
    # ── Ensure exactly 6 slides remain ──
    if len(prs.slides) > 6:
        rId = prs.slides._sldIdLst[6].rId
        prs.part.drop_rel(rId)
        del prs.slides._sldIdLst[6]
        
    print(f"Total slides after trimming instructions: {len(prs.slides)}")
    assert len(prs.slides) == 6, f"Expected exactly 6 slides, got {len(prs.slides)}"

    # Curated Professional SIH Palette
    NAVY = RGBColor(15, 32, 66)            # #0F2042 - Deep Academic Navy
    DARK_BLUE = RGBColor(30, 58, 138)       # #1E3A8A - Primary Header
    ELECTRIC_BLUE = RGBColor(37, 99, 235)   # #2563EB - Accent / Highlights
    CYAN_ACCENT = RGBColor(6, 182, 212)     # #06B6D4 - Data / Tech
    LIGHT_BLUE_BG = RGBColor(239, 246, 255) # #EFF6FF - Soft Card Fill
    BORDER_BLUE = RGBColor(191, 219, 254)   # #BFDBFE - Card Border
    
    SLATE_TEXT = RGBColor(51, 65, 85)       # #334155 - High Contrast Body Text
    MUTED_TEXT = RGBColor(100, 116, 139)    # #64748B - Secondary Subtext
    WHITE = RGBColor(255, 255, 255)
    CARD_BG = RGBColor(255, 255, 255)
    BORDER_GRAY = RGBColor(226, 232, 240)   # #E2E8F0
    
    RED_ACCENT = RGBColor(185, 28, 28)      # #B91C1C - Challenges / Risk
    RED_BG = RGBColor(254, 242, 242)        # #FEF2F2
    RED_BORDER = RGBColor(254, 202, 202)    # #FECACA
    
    GREEN_ACCENT = RGBColor(4, 120, 87)     # #047857 - Feasibility / Benefits
    GREEN_BG = RGBColor(236, 253, 245)      # #ECFDF5
    GREEN_BORDER = RGBColor(167, 243, 208)  # #A7F3D0
    
    PURPLE_ACCENT = RGBColor(109, 40, 217)  # #6D28D9 - Intelligence / AI
    PURPLE_BG = RGBColor(245, 243, 255)     # #F5F3FF
    PURPLE_BORDER = RGBColor(221, 214, 254) # #DDD6FE

    AMBER_ACCENT = RGBColor(180, 83, 9)     # #B45309 - Warning / Attention
    AMBER_BG = RGBColor(255, 251, 235)      # #FFFBEB
    AMBER_BORDER = RGBColor(253, 230, 138)  # #FDE68A

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
    
    shapes_to_remove_s1 = []
    for s in s1.shapes:
        if s.name in ["Picture 4", "Freeform: Shape 26", "Rectangle 24"]:
            shapes_to_remove_s1.append(s)
        elif s.has_text_frame and ("Problem Statement ID" in s.text_frame.text or "TITLE PAGE" in s.text_frame.text):
            shapes_to_remove_s1.append(s)
    for s in shapes_to_remove_s1:
        sp = s._element
        sp.getparent().remove(sp)

    ministry_logo = r"C:\Users\SKYNET\.gemini\antigravity-ide\brain\d9effeed-c96c-49a0-8dec-5dda1b8f6577\scratch\ref_images\page_1_img_1_X5.png"
    if os.path.exists(ministry_logo):
        s1.shapes.add_picture(ministry_logo, Inches(0.60), Inches(0.12), width=Inches(2.40), height=Inches(1.05))

    for s in s1.shapes:
        if s.has_text_frame and "SMART INDIA HACKATHON" in s.text_frame.text:
            s.text_frame.text = "SMART INDIA HACKATHON 2026"
            p = s.text_frame.paragraphs[0]
            p.font.bold = True
            p.font.size = Pt(24)
            p.font.color.rgb = NAVY

    # Left: Administrative & Problem Identification Card
    s1_left = Inches(0.60)
    s1_top = Inches(1.50)
    s1_w = Inches(7.40)
    s1_h = Inches(5.15)
    card_info = add_card(s1, s1_left, s1_top, s1_w, s1_h, bg_color=CARD_BG, border_color=BORDER_BLUE, border_width=1.5)
    tf_info = card_info.text_frame
    tf_info.word_wrap = True
    tf_info.margin_left = Inches(0.28)
    tf_info.margin_top = Inches(0.22)
    tf_info.margin_right = Inches(0.28)

    p = tf_info.paragraphs[0]
    p.text = "Problem Statement ID: SIH26182"
    p.font.bold = True
    p.font.size = Pt(15)
    p.font.color.rgb = ELECTRIC_BLUE
    p.space_after = Pt(6)

    p = tf_info.add_paragraph()
    p.text = "Problem Statement Title:"
    p.font.bold = True
    p.font.size = Pt(10.5)
    p.font.color.rgb = SLATE_TEXT

    p = tf_info.add_paragraph()
    p.text = "Automated Attribution of Unknown Cryptocurrency Wallets to Nearest Virtual Asset Service Providers (VASPs) through Blockchain Intelligence APIs"
    p.font.bold = True
    p.font.size = Pt(12.5)
    p.font.color.rgb = NAVY
    p.space_after = Pt(12)

    fields = [
        ("Theme", "Blockchain & Cybersecurity"),
        ("PS Category", "Software"),
        ("Team ID", "To be finalized on SIH Portal"),
        ("Team Name (Registered)", "CodeMesh"),
        ("Project / Solution", "CryptoGuard AI"),
    ]
    for label, val in fields:
        p = tf_info.add_paragraph()
        r1 = p.add_run()
        r1.text = f"{label}: "
        r1.font.bold = True
        r1.font.size = Pt(11.5)
        r1.font.color.rgb = SLATE_TEXT
        
        r2 = p.add_run()
        r2.text = val
        r2.font.bold = (label in ["Project / Solution", "Team Name (Registered)"])
        r2.font.size = Pt(13 if label == "Project / Solution" else 11.5)
        r2.font.color.rgb = ELECTRIC_BLUE if label == "Project / Solution" else NAVY
        p.space_after = Pt(5.5)

    p = tf_info.add_paragraph()
    r_tag = p.add_run()
    r_tag.text = "CORE PILLARS: Multi-Chain Tracing | 4-Factor VASP Scoring | 10-Signal AML Engine | Section 91 CrPC Notice"
    r_tag.font.bold = True
    r_tag.font.size = Pt(9)
    r_tag.font.color.rgb = CYAN_ACCENT

    # Right: Hero Visual Emblem & Executive Brief Card
    s1_r_left = Inches(8.25)
    s1_r_w = Inches(4.50)
    
    # Embed the Nano Banana Hero Brand Emblem
    emblem_path = os.path.join(visuals_dir, "visual_slide1_hero_emblem.jpg")
    if os.path.exists(emblem_path):
        s1.shapes.add_picture(emblem_path, s1_r_left + Inches(0.75), s1_top, width=Inches(3.00), height=Inches(3.00))

    # Brief box below emblem
    card_sc = add_card(s1, s1_r_left, s1_top + Inches(3.10), s1_r_w, Inches(2.05), bg_color=LIGHT_BLUE_BG, border_color=BORDER_BLUE, border_width=1.2)
    tf_sc = card_sc.text_frame
    tf_sc.word_wrap = True
    tf_sc.margin_left = Inches(0.20)
    tf_sc.margin_top = Inches(0.12)
    tf_sc.margin_right = Inches(0.20)

    p = tf_sc.paragraphs[0]
    p.text = "CRYPTOGUARD AI — SOLUTION BRIEF"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = NAVY
    p.space_after = Pt(4)

    brief_bullets = [
        "Primary Goal: Automatically attribute unknown crypto wallets to nearest VASPs.",
        "Target Users: Indian LEAs, State Cyber Cells, I4C, and FIU-IND compliance units.",
        "Regulatory Scope: PMLA 2002 Reporting Entities & Section 91 CrPC requisitions.",
        "Repository: github.com/aryan311007w-ux/SIH-codeMesh",
    ]
    for b in brief_bullets:
        p = tf_sc.add_paragraph()
        p.text = f"• {b}"
        p.font.size = Pt(9)
        p.font.color.rgb = SLATE_TEXT
        p.space_after = Pt(2)

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 2: IDEA / PROPOSED SOLUTION (HERO VISUAL SLIDE)
    # ═════════════════════════════════════════════════════════════════════════
    s2 = prs.slides[1]
    clean_template_body(s2)
    
    for s in s2.shapes:
        if s.has_text_frame and "IDEA TITLE" in s.text_frame.text:
            s.text_frame.text = "IDEA TITLE: CryptoGuard AI — Solution Overview"
            p = s.text_frame.paragraphs[0]
            p.font.bold = True
            p.font.size = Pt(20)
            p.font.color.rgb = NAVY

    # Top Section: Problem vs Solution Cards (Top: 1.15 in, Height: 1.95 in)
    # Left: The Problem & Gap
    c_prob = add_card(s2, Inches(0.60), Inches(1.15), Inches(4.50), Inches(1.95), bg_color=RED_BG, border_color=RED_BORDER, border_width=1.2)
    tf_prob = c_prob.text_frame
    tf_prob.word_wrap = True
    tf_prob.margin_left = Inches(0.18)
    tf_prob.margin_top = Inches(0.12)
    tf_prob.margin_right = Inches(0.18)
    
    p = tf_prob.paragraphs[0]
    p.text = "THE FORENSIC CHALLENGE"
    p.font.bold = True
    p.font.size = Pt(10.5)
    p.font.color.rgb = RED_ACCENT
    p.space_after = Pt(4)

    prob_pts = [
        "Rapid Fund Dissipation: Stolen crypto structured across peel chains & mixers in minutes.",
        "Opaque Attribution: Lack of explainable VASP matching leads to legal dismissal.",
        "Manual Delays: Slow notice preparation allows suspects to cashout to fiat unhindered.",
    ]
    for pt in prob_pts:
        p = tf_prob.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(8.8)
        p.font.color.rgb = SLATE_TEXT
        p.space_after = Pt(2.5)

    # Right: 4 Solution Pillars (2x2 grid in width: 7.30 in)
    pillars = [
        ("1. Multi-Chain Tracing", "Directed BFS graph walk across Ethereum, BSC, Polygon, Tron, Bitcoin.", BORDER_BLUE, LIGHT_BLUE_BG),
        ("2. 4-Factor VASP Scoring", "Proximity 40%, Volume 30%, Recency 20%, Registry Trust 10%.", PURPLE_BORDER, PURPLE_BG),
        ("3. 10-Signal AML Engine", "Sanctions, mixers, peel chains, rapid exit, structuring typologies.", AMBER_BORDER, AMBER_BG),
        ("4. Legal Response Export", "Section 91 CrPC notice generator, SHA-256 evidence, PDF report.", GREEN_BORDER, GREEN_BG),
    ]
    p_w = Inches(3.55)
    p_h = Inches(0.92)
    for idx, (p_title, p_desc, p_border, p_bg) in enumerate(pillars):
        r_i = idx // 2
        c_i = idx % 2
        px = Inches(5.30) + c_i * (p_w + Inches(0.20))
        py = Inches(1.15) + r_i * (p_h + Inches(0.11))
        
        p_card = add_card(s2, px, py, p_w, p_h, bg_color=CARD_BG, border_color=p_border, border_width=1.0)
        tf_p = p_card.text_frame
        tf_p.word_wrap = True
        tf_p.margin_left = Inches(0.12)
        tf_p.margin_top = Inches(0.06)
        tf_p.margin_right = Inches(0.12)
        
        p = tf_p.paragraphs[0]
        p.text = p_title
        p.font.bold = True
        p.font.size = Pt(9.5)
        p.font.color.rgb = DARK_BLUE
        p.space_after = Pt(1.5)
        
        p = tf_p.add_paragraph()
        p.text = p_desc
        p.font.size = Pt(8.3)
        p.font.color.rgb = SLATE_TEXT

    # Main Centerpiece: Visual 1 — Main Crypto Investigation Flowchart
    flowchart_path = os.path.join(visuals_dir, "visual_1_investigation_flowchart.jpg")
    if os.path.exists(flowchart_path):
        s2.shapes.add_picture(flowchart_path, Inches(0.60), Inches(3.22), width=Inches(12.00), height=Inches(3.18))

    # Bottom Banner
    banner2 = add_card(s2, Inches(0.60), Inches(6.46), Inches(12.00), Inches(0.28), bg_color=LIGHT_BLUE_BG, border_color=BORDER_BLUE, border_width=0.8)
    tf_b2 = banner2.text_frame
    p = tf_b2.paragraphs[0]
    p.text = "CORE ARCHITECTURE: UNKNOWN WALLET -> NORMALIZATION -> MULTI-HOP BFS GRAPH -> VASP ATTRIBUTION -> RISK ENGINE -> SECTION 91 NOTICE"
    p.font.bold = True
    p.font.size = Pt(8)
    p.font.color.rgb = ELECTRIC_BLUE
    p.alignment = PP_ALIGN.CENTER

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 3: TECHNICAL APPROACH / PROTOTYPE
    # ═════════════════════════════════════════════════════════════════════════
    s3 = prs.slides[2]
    clean_template_body(s3)
    
    for s in s3.shapes:
        if s.has_text_frame and "TECHNICAL APPROACH" in s.text_frame.text:
            s.text_frame.text = "TECHNICAL APPROACH: Architecture & Investigation Prototype"
            p = s.text_frame.paragraphs[0]
            p.font.bold = True
            p.font.size = Pt(20)
            p.font.color.rgb = NAVY

    # Left: Visual 3 — System Architecture
    arch_path = os.path.join(visuals_dir, "visual_3_system_architecture.jpg")
    if os.path.exists(arch_path):
        s3.shapes.add_picture(arch_path, Inches(0.60), Inches(1.15), width=Inches(5.90), height=Inches(4.15))
        cap_arch = add_card(s3, Inches(0.60), Inches(5.35), Inches(5.90), Inches(0.28), bg_color=LIGHT_BLUE_BG, border_color=BORDER_BLUE, border_width=0.8)
        tf_ca = cap_arch.text_frame
        p = tf_ca.paragraphs[0]
        p.text = "SYSTEM ARCHITECTURE: 4-Tier Forensic Stack with SQLite Persistence & Configurable Integrations"
        p.font.bold = True
        p.font.size = Pt(8)
        p.font.color.rgb = DARK_BLUE
        p.alignment = PP_ALIGN.CENTER

    # Right: Visual 2 — Transaction Graph Prototype
    graph_path = os.path.join(visuals_dir, "visual_2_transaction_graph.jpg")
    if os.path.exists(graph_path):
        s3.shapes.add_picture(graph_path, Inches(6.70), Inches(1.15), width=Inches(5.90), height=Inches(4.15))
        cap_grp = add_card(s3, Inches(6.70), Inches(5.35), Inches(5.90), Inches(0.28), bg_color=GREEN_BG, border_color=GREEN_BORDER, border_width=0.8)
        tf_cg = cap_grp.text_frame
        p = tf_cg.paragraphs[0]
        p.text = "PROTOTYPE GRAPH: Directed BFS Walk Traversal (1–6 Hops) with Mule Peeling & VASP Attribution"
        p.font.bold = True
        p.font.size = Pt(8)
        p.font.color.rgb = GREEN_ACCENT
        p.alignment = PP_ALIGN.CENTER

    # Bottom: Compact Tech Stack Chips
    tech_chips = [
        ("Frontend Engine", "Vanilla HTML5 / CSS3 / ES6 JS / Vis-network v9.1.2 (100% Offline / Zero CDN)", BORDER_BLUE, LIGHT_BLUE_BG),
        ("Backend ASGI", "Python 3.10+ / FastAPI v0.141 / Uvicorn ASGI Server with Pydantic validation", PURPLE_BORDER, PURPLE_BG),
        ("Forensic Store", "Persistent SQLite3 (cryptoguard.db - 7 indexed relational tables)", GREEN_BORDER, GREEN_BG),
        ("Live Deployment", "Web: https://tubes-intersection-judicial-weapon.trycloudflare.com | Code: github.com/aryan311007w-ux/SIH-codeMesh", AMBER_BORDER, AMBER_BG),
    ]
    chip_w = Inches(2.85)
    chip_h = Inches(0.95)
    for idx, (c_label, c_desc, c_border, c_bg) in enumerate(tech_chips):
        cx = Inches(0.60) + idx * (chip_w + Inches(0.20))
        cy = Inches(5.72)
        c_box = add_card(s3, cx, cy, chip_w, chip_h, bg_color=CARD_BG, border_color=c_border, border_width=1.0)
        tf_c = c_box.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = Inches(0.12)
        tf_c.margin_top = Inches(0.06)
        tf_c.margin_right = Inches(0.12)
        
        p = tf_c.paragraphs[0]
        p.text = c_label
        p.font.bold = True
        p.font.size = Pt(9.2)
        p.font.color.rgb = DARK_BLUE
        p.space_after = Pt(2)
        
        p = tf_c.add_paragraph()
        p.text = c_desc
        p.font.size = Pt(8.2)
        p.font.color.rgb = SLATE_TEXT

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 4: FEASIBILITY AND VIABILITY
    # ═════════════════════════════════════════════════════════════════════════
    s4 = prs.slides[3]
    clean_template_body(s4)
    
    for s in s4.shapes:
        if s.has_text_frame and "FEASIBILITY AND VIABILITY" in s.text_frame.text:
            s.text_frame.text = "FEASIBILITY AND VIABILITY: Operational Analysis & Engine Validation"
            p = s.text_frame.paragraphs[0]
            p.font.bold = True
            p.font.size = Pt(20)
            p.font.color.rgb = NAVY

    # Top Section: 3 Compact Cards (Top: 1.15 in, Height: 2.15 in)
    feas_blocks = [
        ("OPERATIONAL CHALLENGES", RED_BORDER, CARD_BG, RED_ACCENT, [
            "Rapid Fund Layering: Illicit structuring across peel chains in <15 minutes.",
            "Cross-Chain Fragmentation: Obfuscation spanning EVM, Tron, and Bitcoin.",
            "Opaque Black Boxes: Unexplainable scores fail legal defense scrutiny in court.",
            "Manual Paperwork: Hours lost manually drafting Section 91 notices.",
        ]),
        ("CRYPTOGUARD AI SOLUTIONS", BORDER_BLUE, CARD_BG, DARK_BLUE, [
            "Automated BFS Traversal: Traces multi-hop fund flows in sub-second walks.",
            "Unified Data Schema: Normalized schema across 5 major blockchains.",
            "Transparent 4-Factor Scoring: Mathematical confidence across 4 dimensions.",
            "1-Click Section 91 Notices: Pre-populated with verified VASP compliance nodals.",
        ]),
        ("FEASIBILITY & SCALABILITY", GREEN_BORDER, CARD_BG, GREEN_ACCENT, [
            "Technical Feasibility: Lightweight Python/FastAPI runs on standard laptops.",
            "Practical Implementability: Built-in Demo Mode runs 100% offline without API keys.",
            "Production Scalability: SQLite schema is 1-to-1 portable to PostgreSQL.",
            "Security Hardening: Architecture ready for JWT auth and role-based access control.",
        ]),
    ]
    fb_w = Inches(3.85)
    fb_h = Inches(2.15)
    for idx, (fb_title, fb_border, fb_bg, fb_col, fb_pts) in enumerate(feas_blocks):
        fb_x = Inches(0.60) + idx * (fb_w + Inches(0.22))
        fb_card = add_card(s4, fb_x, Inches(1.15), fb_w, fb_h, bg_color=fb_bg, border_color=fb_border, border_width=1.2)
        tf_fb = fb_card.text_frame
        tf_fb.word_wrap = True
        tf_fb.margin_left = Inches(0.16)
        tf_fb.margin_top = Inches(0.10)
        tf_fb.margin_right = Inches(0.16)
        
        p = tf_fb.paragraphs[0]
        p.text = fb_title
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = fb_col
        p.space_after = Pt(4)
        
        for pt in fb_pts:
            p = tf_fb.add_paragraph()
            p.text = f"• {pt}"
            p.font.size = Pt(8.8)
            p.font.color.rgb = SLATE_TEXT
            p.space_after = Pt(2.5)

    # Bottom Section: Visual 4 (VASP Attribution) + Visual 5 (Risk Engine)
    v4_path = os.path.join(visuals_dir, "visual_4_vasp_attribution.jpg")
    if os.path.exists(v4_path):
        s4.shapes.add_picture(v4_path, Inches(0.60), Inches(3.40), width=Inches(5.90), height=Inches(3.25))

    v5_path = os.path.join(visuals_dir, "visual_5_risk_engine.jpg")
    if os.path.exists(v5_path):
        s4.shapes.add_picture(v5_path, Inches(6.70), Inches(3.40), width=Inches(5.90), height=Inches(3.25))

    # ═════════════════════════════════════════════════════════════════════════
    # SLIDE 5: IMPACT AND BENEFITS
    # ═════════════════════════════════════════════════════════════════════════
    s5 = prs.slides[4]
    clean_template_body(s5)
    
    for s in s5.shapes:
        if s.has_text_frame and "IMPACT AND BENEFITS" in s.text_frame.text:
            s.text_frame.text = "IMPACT AND BENEFITS: Stakeholder Value & National Transformation"
            p = s.text_frame.paragraphs[0]
            p.font.bold = True
            p.font.size = Pt(20)
            p.font.color.rgb = NAVY

    # Left Summary Card
    c_s5_l = add_card(s5, Inches(0.60), Inches(1.15), Inches(2.65), Inches(3.60), bg_color=CARD_BG, border_color=BORDER_BLUE, border_width=1.2)
    tf_s5l = c_s5_l.text_frame
    tf_s5l.word_wrap = True
    tf_s5l.margin_left = Inches(0.14)
    tf_s5l.margin_top = Inches(0.12)
    tf_s5l.margin_right = Inches(0.14)

    p = tf_s5l.paragraphs[0]
    p.text = "FOR INVESTIGATORS & LEAs"
    p.font.bold = True
    p.font.size = Pt(10)
    p.font.color.rgb = DARK_BLUE
    p.space_after = Pt(5)

    s5l_pts = [
        "Tracing in minutes vs days across complex multi-hop peel chains.",
        "Unified multi-chain view eliminates portal switching overhead.",
        "Cryptographic SHA-256 evidence maintains unblemished chain of custody.",
        "Standardized Section 91 notices ready for judicial summons.",
    ]
    for pt in s5l_pts:
        p = tf_s5l.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(8.8)
        p.font.color.rgb = SLATE_TEXT
        p.space_after = Pt(4)

    # Center: Visual — Stakeholder Impact Hub
    hub_path = os.path.join(visuals_dir, "visual_slide5_impact_hub.jpg")
    if os.path.exists(hub_path):
        s5.shapes.add_picture(hub_path, Inches(3.40), Inches(1.15), width=Inches(6.30), height=Inches(3.60))

    # Right Summary Card
    c_s5_r = add_card(s5, Inches(9.85), Inches(1.15), Inches(2.75), Inches(3.60), bg_color=CARD_BG, border_color=GREEN_BORDER, border_width=1.2)
    tf_s5r = c_s5_r.text_frame
    tf_s5r.word_wrap = True
    tf_s5r.margin_left = Inches(0.14)
    tf_s5r.margin_top = Inches(0.12)
    tf_s5r.margin_right = Inches(0.14)

    p = tf_s5r.paragraphs[0]
    p.text = "FOR VASPs & REGULATORS"
    p.font.bold = True
    p.font.size = Pt(10)
    p.font.color.rgb = GREEN_ACCENT
    p.space_after = Pt(5)

    s5r_pts = [
        "Requisitions contain precise hop walks, tx hashes, & timestamps.",
        "Direct identification of deposit aggregators cuts verification delays.",
        "Fulfills Prevention of Money Laundering Act (PMLA) obligations.",
        "Schema natively aligned with national cybercrime reporting portals.",
    ]
    for pt in s5r_pts:
        p = tf_s5r.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(8.8)
        p.font.color.rgb = SLATE_TEXT
        p.space_after = Pt(4)

    # Bottom: 6 Numbered Long-Term Effects Cards
    lt_effects = [
        ("1. Accelerated Asset Freezing", "Minimizes the critical time window before illicit funds are cashed out to fiat through exchanges."),
        ("2. Standardized Requisitions", "Replaces informal queries with statutory Section 91 CrPC notices containing full evidentiary trails."),
        ("3. Cross-Chain Investigative Parity", "Empowers investigators to track assets across EVM, Tron, and Bitcoin inside a single consolidated workspace."),
        ("4. Institutional Evidentiary Memory", "Persistent SQLite storage guarantees repeatable, verifiable re-analysis and audit trails for cold cyber cases."),
        ("5. Low-Cost Station Deployment", "Zero heavy ML dependency allows rapid deployment across district cybercrime police stations without server clusters."),
        ("6. National Integration-Ready", "Native data schemas aligned with the Indian Cybercrime Coordination Centre (I4C) and SAHYOG portal."),
    ]
    grid_w = Inches(3.85)
    grid_h = Inches(0.88)
    for idx, (lt_title, lt_desc) in enumerate(lt_effects):
        r_i = idx // 3
        c_i = idx % 3
        gx = Inches(0.60) + c_i * (grid_w + Inches(0.22))
        gy = Inches(4.88) + r_i * (grid_h + Inches(0.10))
        
        g_box = add_card(s5, gx, gy, grid_w, grid_h, bg_color=WHITE, border_color=BORDER_BLUE, border_width=0.8)
        tf_g = g_box.text_frame
        tf_g.word_wrap = True
        tf_g.margin_left = Inches(0.12)
        tf_g.margin_top = Inches(0.06)
        tf_g.margin_right = Inches(0.12)
        
        p = tf_g.paragraphs[0]
        p.text = lt_title
        p.font.bold = True
        p.font.size = Pt(9)
        p.font.color.rgb = DARK_BLUE
        p.space_after = Pt(1.5)
        
        p = tf_g.add_paragraph()
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
    ref_col_h = Inches(3.70)
    ref_col_top = Inches(1.15)

    # Column 1: Regulatory Frameworks
    r1 = add_card(s6, Inches(0.60), ref_col_top, ref_col_w, ref_col_h, bg_color=CARD_BG, border_color=BORDER_BLUE, border_width=1.2)
    tf_r1 = r1.text_frame
    tf_r1.word_wrap = True
    tf_r1.margin_left = Inches(0.16)
    tf_r1.margin_top = Inches(0.10)
    tf_r1.margin_right = Inches(0.16)

    p = tf_r1.paragraphs[0]
    p.text = "STATUTORY & REGULATORY FRAMEWORKS"
    p.font.bold = True
    p.font.size = Pt(10)
    p.font.color.rgb = DARK_BLUE
    p.space_after = Pt(6)

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
        run2.font.size = Pt(8.2)
        run2.font.color.rgb = SLATE_TEXT
        p.space_after = Pt(4)

    # Column 2: Protocols & APIs
    r2 = add_card(s6, Inches(4.65), ref_col_top, ref_col_w, ref_col_h, bg_color=CARD_BG, border_color=BORDER_BLUE, border_width=1.2)
    tf_r2 = r2.text_frame
    tf_r2.word_wrap = True
    tf_r2.margin_left = Inches(0.16)
    tf_r2.margin_top = Inches(0.10)
    tf_r2.margin_right = Inches(0.16)

    p = tf_r2.paragraphs[0]
    p.text = "BLOCKCHAIN APIS & FORENSIC PROTOCOLS"
    p.font.bold = True
    p.font.size = Pt(10)
    p.font.color.rgb = DARK_BLUE
    p.space_after = Pt(6)

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
        run2.font.size = Pt(8.2)
        run2.font.color.rgb = SLATE_TEXT
        p.space_after = Pt(4)

    # Column 3: Forensic Research
    r3 = add_card(s6, Inches(8.70), ref_col_top, ref_col_w, ref_col_h, bg_color=CARD_BG, border_color=BORDER_BLUE, border_width=1.2)
    tf_r3 = r3.text_frame
    tf_r3.word_wrap = True
    tf_r3.margin_left = Inches(0.16)
    tf_r3.margin_top = Inches(0.10)
    tf_r3.margin_right = Inches(0.16)

    p = tf_r3.paragraphs[0]
    p.text = "FORENSIC HEURISTICS & RESEARCH"
    p.font.bold = True
    p.font.size = Pt(10)
    p.font.color.rgb = DARK_BLUE
    p.space_after = Pt(6)

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
        run2.font.size = Pt(8.2)
        run2.font.color.rgb = SLATE_TEXT
        p.space_after = Pt(4)

    # Middle Box: Scalability & Future Roadmap
    road_top = Inches(4.98)
    road_card = add_card(s6, Inches(0.60), road_top, Inches(11.95), Inches(1.02), bg_color=LIGHT_BLUE_BG, border_color=BORDER_BLUE, border_width=1.0)
    tf_road = road_card.text_frame
    tf_road.word_wrap = True
    tf_road.margin_left = Inches(0.18)
    tf_road.margin_top = Inches(0.08)
    tf_road.margin_right = Inches(0.18)

    p = tf_road.paragraphs[0]
    p.text = "DEPLOYMENT MATURITY: CURRENT MVP -> ENTERPRISE SCALE ROADMAP"
    p.font.bold = True
    p.font.size = Pt(9.5)
    p.font.color.rgb = NAVY
    p.space_after = Pt(3)

    steps = [
        ("Current Tested MVP", "Offline Vis.js UI + FastAPI + SQLite + 4-Factor VASP Scoring + Section 91 CrPC Notice + Deterministic Demo Dataset."),
        ("Near-Term Scale", "PostgreSQL migration + multi-tenant police station hierarchy + JWT/RBAC authentication hardening."),
        ("Institutional Production", "Direct secure webhook integration with Indian Cybercrime Coordination Centre (I4C) & national SAHYOG portal."),
    ]
    for st_title, st_desc in steps:
        p = tf_road.add_paragraph()
        r1 = p.add_run()
        r1.text = f"[{st_title}] "
        r1.font.bold = True
        r1.font.size = Pt(8.5)
        r1.font.color.rgb = DARK_BLUE
        
        r2 = p.add_run()
        r2.text = f"{st_desc}  "
        r2.font.size = Pt(8.2)
        r2.font.color.rgb = SLATE_TEXT

    # Bottom Links Bar
    link_top = Inches(6.12)
    link_card = add_card(s6, Inches(0.60), link_top, Inches(11.95), Inches(0.55), bg_color=WHITE, border_color=BORDER_BLUE, border_width=1.0)
    tf_l = link_card.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = Inches(0.18)
    tf_l.margin_top = Inches(0.08)
    tf_l.margin_right = Inches(0.18)

    p = tf_l.paragraphs[0]
    r1 = p.add_run()
    r1.text = "OFFICIAL REPOSITORY: "
    r1.font.bold = True
    r1.font.size = Pt(9)
    r1.font.color.rgb = SLATE_TEXT

    r2 = p.add_run()
    r2.text = "https://github.com/aryan311007w-ux/SIH-codeMesh   |   "
    r2.font.bold = True
    r2.font.size = Pt(9)
    r2.font.color.rgb = ELECTRIC_BLUE

    r3 = p.add_run()
    r3.text = "WEBSITE: "
    r3.font.bold = True
    r3.font.size = Pt(9)
    r3.font.color.rgb = SLATE_TEXT

    r4 = p.add_run()
    r4.text = "https://tubes-intersection-judicial-weapon.trycloudflare.com   |   "
    r4.font.bold = True
    r4.font.size = Pt(9)
    r4.font.color.rgb = ELECTRIC_BLUE

    r5 = p.add_run()
    r5.text = "DEMO VIDEO: "
    r5.font.bold = True
    r5.font.size = Pt(9)
    r5.font.color.rgb = SLATE_TEXT

    r6 = p.add_run()
    r6.text = "To be updated after deployment"
    r6.font.size = Pt(9)
    r6.font.color.rgb = MUTED_TEXT

    # Save upgraded presentation
    prs.save(output_path)
    print(f"Upgraded presentation successfully generated at: {output_path}")

    # Verify slide count
    v_prs = Presentation(output_path)
    assert len(v_prs.slides) == 6, f"Slide count verification failed! Expected 6, got {len(v_prs.slides)}"
    print("SLIDE COUNT VERIFICATION: EXACTLY 6 SLIDES CONFIRMED.")

if __name__ == "__main__":
    build_submission_presentation()
