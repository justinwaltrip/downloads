import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from datetime import datetime


def create_saas_master_agreement():
    """Create SaaS Master Service Agreement with key sections highlighted"""
    filename = "SaaS_Master_Agreement_CloudTech_2024.pdf"

    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        topMargin=1 * inch,
        bottomMargin=1 * inch,
        leftMargin=1 * inch,
        rightMargin=1 * inch,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "Title",
        parent=styles["Heading1"],
        fontSize=16,
        textColor=colors.HexColor("#1a1a1a"),
        alignment=TA_CENTER,
        spaceAfter=20,
        fontName="Helvetica-Bold",
    )

    heading_style = ParagraphStyle(
        "Heading",
        parent=styles["Heading2"],
        fontSize=13,
        textColor=colors.HexColor("#2c3e50"),
        spaceAfter=12,
        spaceBefore=15,
        fontName="Helvetica-Bold",
    )

    subheading_style = ParagraphStyle(
        "SubHeading",
        parent=styles["Heading3"],
        fontSize=11,
        textColor=colors.HexColor("#34495e"),
        spaceAfter=8,
        spaceBefore=10,
        fontName="Helvetica-Bold",
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontSize=10,
        textColor=colors.HexColor("#2c3e50"),
        spaceAfter=8,
        leading=14,
        alignment=TA_JUSTIFY,
    )

    highlight_style = ParagraphStyle(
        "Highlight",
        parent=styles["BodyText"],
        fontSize=10,
        textColor=colors.HexColor("#c0392b"),
        spaceAfter=8,
        leading=14,
        fontName="Helvetica-Bold",
    )

    story = []

    # Title Page
    story.append(Spacer(1, 1.5 * inch))
    story.append(Paragraph("SOFTWARE AS A SERVICE", title_style))
    story.append(Paragraph("MASTER SERVICE AGREEMENT", title_style))
    story.append(Spacer(1, 0.5 * inch))

    story.append(Paragraph("<b>Between:</b>", body_style))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("<b>CloudTech Solutions Inc.</b>", body_style))
    story.append(Paragraph("1500 Technology Drive, Suite 300", body_style))
    story.append(Paragraph("San Francisco, CA 94105", body_style))
    story.append(Paragraph('("Provider" or "CloudTech")', body_style))
    story.append(Spacer(1, 0.3 * inch))

    story.append(Paragraph("<b>And:</b>", body_style))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("<b>Enterprise Customer Corp.</b>", body_style))
    story.append(Paragraph("2000 Business Plaza", body_style))
    story.append(Paragraph("New York, NY 10001", body_style))
    story.append(Paragraph('("Customer" or "Client")', body_style))
    story.append(Spacer(1, 0.5 * inch))

    story.append(Paragraph("<b>Effective Date:</b> January 1, 2024", body_style))
    story.append(Paragraph("<b>Initial Term:</b> 3 Years", body_style))
    story.append(Spacer(1, 0.3 * inch))

    story.append(
        Paragraph(
            'This Master Service Agreement ("Agreement") governs the provision of cloud-based software services by Provider to Customer.',
            body_style,
        )
    )

    story.append(PageBreak())

    # Table of Contents
    story.append(Paragraph("TABLE OF CONTENTS", heading_style))
    story.append(Spacer(1, 0.2 * inch))

    toc_data = [
        ["Section 1:", "Definitions and Interpretation"],
        ["Section 2:", "Grant of Rights and Service Provision"],
        ["Section 3:", "Fees and Payment Terms"],
        ["Section 4:", "Customer Obligations"],
        ["Section 5:", "Service Levels and Support"],
        ["Section 6:", "Data Protection and Security"],
        ["Section 7:", "Intellectual Property Rights"],
        ["Section 8:", "Warranties and Disclaimers"],
        ["Section 9:", "Indemnification"],
        ["Section 10:", "Termination and Suspension"],
        ["Section 11:", "Effect of Termination"],
        ["Section 12:", "IP Indemnity Provisions"],
        ["Section 13:", "Confidentiality"],
        ["Section 14:", "General Provisions"],
        ["Section 15:", "U.S. Government Users"],
        ["Section 16:", "Limitation of Liability"],
    ]

    toc_table = Table(toc_data, colWidths=[1.2 * inch, 4.8 * inch])
    toc_table.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    story.append(toc_table)
    story.append(PageBreak())

    # Sections 1-2 (Placeholder)
    story.append(Paragraph("SECTION 1: DEFINITIONS AND INTERPRETATION", heading_style))
    story.append(
        Paragraph(
            "[Standard definitions section - content omitted for brevity]", body_style
        )
    )
    story.append(Spacer(1, 0.5 * inch))

    story.append(
        Paragraph("SECTION 2: GRANT OF RIGHTS AND SERVICE PROVISION", heading_style)
    )
    story.append(
        Paragraph(
            "[Service description and license grant - content omitted for brevity]",
            body_style,
        )
    )
    story.append(PageBreak())

    # Section 3: Payment Terms
    story.append(Paragraph("SECTION 3: FEES AND PAYMENT TERMS", heading_style))
    story.append(Spacer(1, 0.1 * inch))

    story.append(Paragraph("<b>3.1 Subscription Fees</b>", subheading_style))
    story.append(
        Paragraph(
            "Customer shall pay Provider the subscription fees as set forth in the applicable Order Form. All fees are quoted and payable in U.S. Dollars unless otherwise specified.",
            body_style,
        )
    )
    story.append(Spacer(1, 0.1 * inch))

    story.append(Paragraph("<b>3.2 Payment Terms</b>", subheading_style))
    story.append(
        Paragraph(
            "<font color='#c0392b'><b>• Payment Due:</b></font> All invoices are due and payable within thirty (30) days of the invoice date.",
            highlight_style,
        )
    )
    story.append(
        Paragraph(
            "<font color='#c0392b'><b>• Late Payment:</b></font> Late payments shall accrue interest at the rate of 1.5% per month (or the maximum rate permitted by law, whichever is lower).",
            highlight_style,
        )
    )
    story.append(
        Paragraph(
            "<font color='#c0392b'><b>• Annual Prepayment:</b></font> Fees for annual subscriptions are due in advance of the subscription period.",
            highlight_style,
        )
    )
    story.append(Spacer(1, 0.1 * inch))

    story.append(Paragraph("<b>3.3 Fee Increases</b>", subheading_style))
    story.append(
        Paragraph(
            "Provider may increase fees upon renewal with at least ninety (90) days prior written notice. Fee increases shall not exceed 7% per annum unless mutually agreed.",
            body_style,
        )
    )
    story.append(Spacer(1, 0.1 * inch))

    story.append(Paragraph("<b>3.4 Taxes</b>", subheading_style))
    story.append(
        Paragraph(
            'All fees are exclusive of taxes, duties, levies, tariffs, and other governmental charges (collectively, "Taxes"). Customer is responsible for all Taxes except those based on Provider\'s net income.',
            body_style,
        )
    )
    story.append(Spacer(1, 0.1 * inch))

    story.append(Paragraph("<b>3.5 No Refunds</b>", subheading_style))
    story.append(
        Paragraph(
            "<font color='#c0392b'><b>Except as specifically provided in Section 10(d),</b></font> all fees paid are non-refundable and non-cancellable.",
            highlight_style,
        )
    )

    story.append(PageBreak())

    # Sections 4-9 (Placeholder)
    story.append(Paragraph("SECTIONS 4-9: [STANDARD PROVISIONS]", heading_style))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("SECTION 4: CUSTOMER OBLIGATIONS", subheading_style))
    story.append(
        Paragraph(
            "[Customer responsibilities - content omitted for brevity]", body_style
        )
    )
    story.append(Spacer(1, 0.3 * inch))

    story.append(Paragraph("SECTION 5: SERVICE LEVELS AND SUPPORT", subheading_style))
    story.append(
        Paragraph("[SLA commitments - content omitted for brevity]", body_style)
    )
    story.append(Spacer(1, 0.3 * inch))

    story.append(Paragraph("SECTION 6: DATA PROTECTION AND SECURITY", subheading_style))
    story.append(
        Paragraph(
            "[Data handling provisions - content omitted for brevity]", body_style
        )
    )
    story.append(Spacer(1, 0.3 * inch))

    story.append(Paragraph("SECTION 7: INTELLECTUAL PROPERTY RIGHTS", subheading_style))
    story.append(Paragraph("[IP ownership - content omitted for brevity]", body_style))
    story.append(Spacer(1, 0.3 * inch))

    story.append(Paragraph("SECTION 8: WARRANTIES AND DISCLAIMERS", subheading_style))
    story.append(
        Paragraph("[Warranty provisions - content omitted for brevity]", body_style)
    )
    story.append(Spacer(1, 0.3 * inch))

    story.append(Paragraph("SECTION 9: INDEMNIFICATION", subheading_style))
    story.append(
        Paragraph("[General indemnity - content omitted for brevity]", body_style)
    )

    story.append(PageBreak())

    # Section 10: Termination (HIGH PRIORITY)
    story.append(Paragraph("SECTION 10: TERMINATION AND SUSPENSION", heading_style))
    story.append(Spacer(1, 0.1 * inch))

    story.append(Paragraph("<b>10(a) Termination for Insolvency</b>", subheading_style))
    story.append(
        Paragraph(
            "<font color='#c0392b'><b>Either party may terminate this Agreement immediately upon written notice if the other party:</b></font>",
            highlight_style,
        )
    )
    story.append(Spacer(1, 0.05 * inch))

    termination_data = [
        ["(i)", "Becomes unable to pay its debts as they become due;"],
        ["(ii)", "Makes a general assignment for the benefit of creditors;"],
        [
            "(iii)",
            "Suffers or permits the appointment of a receiver for its business or assets;",
        ],
        [
            "(iv)",
            "Becomes subject to any bankruptcy, reorganization, liquidation, dissolution, or similar proceeding;",
        ],
        ["(v)", "Ceases to carry on business in the ordinary course; or"],
        [
            "(vi)",
            "Takes any corporate action to authorize or effect any of the foregoing.",
        ],
    ]

    termination_table = Table(termination_data, colWidths=[0.4 * inch, 5.6 * inch])
    termination_table.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (0, -1), "LEFT"),
                ("ALIGN", (1, 0), (1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#c0392b")),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    story.append(termination_table)
    story.append(Spacer(1, 0.2 * inch))

    story.append(
        Paragraph("<b>10(b) Termination for Material Breach</b>", subheading_style)
    )
    story.append(
        Paragraph(
            "Either party may terminate this Agreement upon thirty (30) days' written notice if the other party materially breaches this Agreement and fails to cure such breach within the notice period.",
            body_style,
        )
    )
    story.append(Spacer(1, 0.2 * inch))

    story.append(
        Paragraph("<b>10(c) Post-Termination Obligations</b>", subheading_style)
    )
    story.append(
        Paragraph(
            "<font color='#c0392b'><b>Upon termination or expiration of this Agreement:</b></font>",
            highlight_style,
        )
    )
    story.append(Spacer(1, 0.05 * inch))

    post_term_data = [
        [
            "(i)",
            "<font color='#c0392b'><b>Immediate Cessation:</b> Customer shall immediately cease all use of the Services and delete or destroy all copies of Provider's Confidential Information and software in Customer's possession or control;</font>",
        ],
        [
            "(ii)",
            "<font color='#c0392b'><b>Data Return:</b> Provider shall make Customer Data available for download by Customer for a period of ten (10) business days following termination, after which Provider may delete all Customer Data;</font>",
        ],
        [
            "(iii)",
            "<font color='#c0392b'><b>No Access:</b> All access credentials shall be deactivated immediately upon the effective date of termination;</font>",
        ],
        [
            "(iv)",
            "<font color='#c0392b'><b>Outstanding Fees:</b> Customer shall pay all outstanding fees and charges accrued prior to the effective date of termination.</font>",
        ],
    ]

    post_term_table = Table(post_term_data, colWidths=[0.4 * inch, 5.6 * inch])
    post_term_table.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (0, -1), "LEFT"),
                ("ALIGN", (1, 0), (1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#c0392b")),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    story.append(post_term_table)
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("<b>10(d) Refund of Prepaid Fees</b>", subheading_style))
    story.append(
        Paragraph(
            "<font color='#c0392b'><b>If Provider terminates this Agreement other than for Customer's breach, or if Customer terminates for Provider's material breach, Provider shall refund to Customer any prepaid fees for Services not yet rendered, calculated on a pro-rata basis.</b></font>",
            highlight_style,
        )
    )
    story.append(Spacer(1, 0.05 * inch))
    story.append(
        Paragraph(
            "<font color='#c0392b'><b>If Customer terminates for convenience or due to Customer's breach, no refund of prepaid fees shall be due.</b></font>",
            highlight_style,
        )
    )
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("<b>10(e) Suspension Rights</b>", subheading_style))
    story.append(
        Paragraph(
            "Provider may suspend Customer's access to the Services immediately without liability if: (i) Customer's account is more than thirty (30) days overdue; (ii) Customer's use poses a security risk; or (iii) Customer violates the Acceptable Use Policy.",
            body_style,
        )
    )

    story.append(PageBreak())

    # Section 11: Effect of Termination (Placeholder)
    story.append(Paragraph("SECTION 11: EFFECT OF TERMINATION", heading_style))
    story.append(
        Paragraph("[Survival provisions - content omitted for brevity]", body_style)
    )
    story.append(PageBreak())

    # Section 12: IP Indemnity
    story.append(
        Paragraph("SECTION 12: INTELLECTUAL PROPERTY INDEMNITY", heading_style)
    )
    story.append(Spacer(1, 0.1 * inch))

    story.append(Paragraph("<b>12.1 Indemnification by Provider</b>", subheading_style))
    story.append(
        Paragraph(
            "<font color='#2980b9'><b>Provider shall defend, indemnify, and hold harmless Customer from and against any claims, damages, losses, and expenses (including reasonable attorneys' fees) arising from any third-party claim that Customer's authorized use of the Services infringes or misappropriates such third party's intellectual property rights.</b></font>",
            ParagraphStyle(
                "IPHighlight",
                parent=body_style,
                textColor=colors.HexColor("#2980b9"),
                fontName="Helvetica-Bold",
            ),
        )
    )
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("<b>12.2 Exclusions</b>", subheading_style))
    story.append(
        Paragraph(
            "Provider's indemnification obligations shall not apply to claims arising from:",
            body_style,
        )
    )
    story.append(Paragraph("• Customer's modification of the Services;", body_style))
    story.append(
        Paragraph(
            "• Customer's combination of the Services with third-party products;",
            body_style,
        )
    )
    story.append(
        Paragraph(
            "• Customer's use of the Services in violation of this Agreement;",
            body_style,
        )
    )
    story.append(Paragraph("• Customer Data or third-party content.", body_style))
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("<b>12.3 Remedies</b>", subheading_style))
    story.append(
        Paragraph(
            "If the Services become, or in Provider's opinion are likely to become, the subject of an infringement claim, Provider may, at its option and expense:",
            body_style,
        )
    )
    story.append(
        Paragraph(
            "(a) Procure the right for Customer to continue using the Services;",
            body_style,
        )
    )
    story.append(
        Paragraph(
            "(b) Replace or modify the Services to make them non-infringing; or",
            body_style,
        )
    )
    story.append(
        Paragraph(
            "(c) Terminate the Agreement and refund prepaid fees on a pro-rata basis.",
            body_style,
        )
    )
    story.append(Spacer(1, 0.2 * inch))

    story.append(
        Paragraph(
            "<font color='#2980b9'><b>THIS SECTION 12 STATES PROVIDER'S ENTIRE LIABILITY AND CUSTOMER'S EXCLUSIVE REMEDY FOR INTELLECTUAL PROPERTY INFRINGEMENT CLAIMS.</b></font>",
            ParagraphStyle(
                "IPHighlight2",
                parent=body_style,
                textColor=colors.HexColor("#2980b9"),
                fontName="Helvetica-Bold",
                alignment=TA_CENTER,
            ),
        )
    )

    story.append(PageBreak())

    # Section 13: Confidentiality
    story.append(Paragraph("SECTION 13: CONFIDENTIALITY", heading_style))
    story.append(Spacer(1, 0.1 * inch))

    story.append(
        Paragraph(
            "<b>13.1 Definition of Confidential Information</b>", subheading_style
        )
    )
    story.append(
        Paragraph(
            '"Confidential Information" means all non-public information disclosed by one party ("Disclosing Party") to the other party ("Receiving Party"), whether orally or in writing, that is designated as confidential or that reasonably should be understood to be confidential given the nature of the information and the circumstances of disclosure.',
            body_style,
        )
    )
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("<b>13.2 Obligations</b>", subheading_style))
    story.append(
        Paragraph(
            "<font color='#27ae60'><b>The Receiving Party shall:</b></font>",
            ParagraphStyle(
                "ConfHighlight",
                parent=body_style,
                textColor=colors.HexColor("#27ae60"),
                fontName="Helvetica-Bold",
            ),
        )
    )
    story.append(Spacer(1, 0.05 * inch))

    conf_data = [
        [
            "(a)",
            "<font color='#27ae60'><b>Protect Confidential Information using the same degree of care it uses to protect its own confidential information, but in no event less than reasonable care;</b></font>",
        ],
        [
            "(b)",
            "<font color='#27ae60'><b>Not disclose Confidential Information to any third party except to employees, contractors, and advisors who have a legitimate need to know and are bound by confidentiality obligations at least as restrictive as those contained herein;</b></font>",
        ],
        [
            "(c)",
            "<font color='#27ae60'><b>Not use Confidential Information for any purpose other than performing its obligations or exercising its rights under this Agreement;</b></font>",
        ],
        [
            "(d)",
            "<font color='#27ae60'><b>Promptly notify the Disclosing Party of any unauthorized use or disclosure of Confidential Information.</b></font>",
        ],
    ]

    conf_table = Table(conf_data, colWidths=[0.4 * inch, 5.6 * inch])
    conf_table.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (0, -1), "LEFT"),
                ("ALIGN", (1, 0), (1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#27ae60")),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    story.append(conf_table)
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("<b>13.3 Exceptions</b>", subheading_style))
    story.append(
        Paragraph(
            "Confidential Information does not include information that:", body_style
        )
    )
    story.append(
        Paragraph(
            "• Is or becomes publicly available through no breach of this Agreement;",
            body_style,
        )
    )
    story.append(
        Paragraph(
            "• Was rightfully known to the Receiving Party prior to disclosure;",
            body_style,
        )
    )
    story.append(
        Paragraph(
            "• Is rightfully received from a third party without breach of confidentiality obligations;",
            body_style,
        )
    )
    story.append(
        Paragraph(
            "• Is independently developed without use of the Confidential Information.",
            body_style,
        )
    )
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("<b>13.4 Compelled Disclosure</b>", subheading_style))
    story.append(
        Paragraph(
            "If the Receiving Party is compelled by law to disclose Confidential Information, it shall provide prompt notice to the Disclosing Party (unless prohibited by law) and shall cooperate with the Disclosing Party's efforts to seek a protective order or other appropriate remedy.",
            body_style,
        )
    )
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("<b>13.5 Term</b>", subheading_style))
    story.append(
        Paragraph(
            "<font color='#27ae60'><b>The obligations under this Section 13 shall survive termination of this Agreement for a period of five (5) years, except that obligations with respect to trade secrets shall continue for as long as such information remains a trade secret under applicable law.</b></font>",
            ParagraphStyle(
                "ConfHighlight2",
                parent=body_style,
                textColor=colors.HexColor("#27ae60"),
                fontName="Helvetica-Bold",
            ),
        )
    )

    story.append(PageBreak())

    # Section 14: General Provisions (with Assignment)
    story.append(Paragraph("SECTION 14: GENERAL PROVISIONS", heading_style))
    story.append(Spacer(1, 0.1 * inch))

    story.append(Paragraph("<b>14(a) Governing Law</b>", subheading_style))
    story.append(
        Paragraph(
            "This Agreement shall be governed by and construed in accordance with the laws of the State of California, without regard to its conflict of laws principles.",
            body_style,
        )
    )
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("<b>14(b) Dispute Resolution</b>", subheading_style))
    story.append(
        Paragraph(
            "Any disputes arising under this Agreement shall be resolved through binding arbitration in San Francisco, California, in accordance with the Commercial Arbitration Rules of the American Arbitration Association.",
            body_style,
        )
    )
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("<b>14(c) Notices</b>", subheading_style))
    story.append(
        Paragraph(
            "All notices under this Agreement shall be in writing and delivered by email (with confirmation), courier, or certified mail to the addresses set forth in the preamble or as otherwise specified by a party in writing.",
            body_style,
        )
    )
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("<b>14(d) Entire Agreement</b>", subheading_style))
    story.append(
        Paragraph(
            "This Agreement, including all Order Forms and referenced policies, constitutes the entire agreement between the parties and supersedes all prior agreements and understandings, whether written or oral.",
            body_style,
        )
    )
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("<b>14(e) Assignment</b>", subheading_style))
    story.append(
        Paragraph(
            "<font color='#8e44ad'><b>ASSIGNMENT RESTRICTIONS:</b></font>",
            ParagraphStyle(
                "AssignHighlight",
                parent=body_style,
                textColor=colors.HexColor("#8e44ad"),
                fontName="Helvetica-Bold",
            ),
        )
    )
    story.append(Spacer(1, 0.1 * inch))

    assign_data = [
        [
            "1.",
            "<font color='#8e44ad'><b>Complete Assignment Required:</b> Neither party may assign any of its rights or delegate any of its obligations under this Agreement without the prior written consent of the other party. Any purported assignment in violation of this provision shall be void. For clarity, partial assignments of rights are expressly prohibited.</font>",
        ],
        [
            "2.",
            "<font color='#8e44ad'><b>Permitted Assignments:</b> Notwithstanding the foregoing, either party may assign this Agreement without consent:</font>",
        ],
        [
            "",
            "<font color='#8e44ad'>  (i) To an Affiliate, provided the assigning party remains liable for all obligations;</font>",
        ],
        [
            "",
            "<font color='#8e44ad'>  (ii) In connection with a merger, acquisition, corporate reorganization, or sale of all or substantially all of its assets or business to which this Agreement relates; provided that:</font>",
        ],
        [
            "",
            "<font color='#8e44ad'>      • The assignment is of ALL rights and obligations under this Agreement (not selective);</font>",
        ],
        [
            "",
            "<font color='#8e44ad'>      • The assignee is financially capable of performing the obligations hereunder;</font>",
        ],
        [
            "",
            "<font color='#8e44ad'>      • The assignee has the technical and operational capability to perform the Services (in the case of Provider assignment) or fulfill payment obligations (in the case of Customer assignment);</font>",
        ],
        [
            "",
            "<font color='#8e44ad'>      • The assigning party provides written notice to the other party at least thirty (30) days prior to the effective date of assignment.</font>",
        ],
        [
            "3.",
            "<font color='#8e44ad'><b>Objection Rights:</b> The non-assigning party may object to a proposed assignment to an Affiliate or in connection with a change of control if it can demonstrate, in good faith, that the proposed assignee lacks the financial or technical capability to perform the obligations under this Agreement.</font>",
        ],
        [
            "4.",
            "<font color='#8e44ad'><b>Effect of Assignment:</b> Any permitted assignment shall not relieve the assigning party of its obligations unless the non-assigning party provides written consent to such release.</font>",
        ],
    ]

    assign_table = Table(assign_data, colWidths=[0.4 * inch, 5.6 * inch])
    assign_table.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (0, -1), "LEFT"),
                ("ALIGN", (1, 0), (1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#8e44ad")),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    story.append(assign_table)
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("<b>14(f) Severability</b>", subheading_style))
    story.append(
        Paragraph(
            "If any provision of this Agreement is held to be invalid or unenforceable, the remaining provisions shall continue in full force and effect.",
            body_style,
        )
    )
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("<b>14(g) Waiver</b>", subheading_style))
    story.append(
        Paragraph(
            "No waiver of any provision of this Agreement shall be effective unless in writing and signed by the party against whom the waiver is sought to be enforced.",
            body_style,
        )
    )
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("<b>14(h) Force Majeure</b>", subheading_style))
    story.append(
        Paragraph(
            "Neither party shall be liable for any failure or delay in performance due to causes beyond its reasonable control, including acts of God, war, terrorism, labor disputes, or internet service provider failures.",
            body_style,
        )
    )
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("<b>14(i) Anti-Bribery Compliance</b>", subheading_style))
    story.append(
        Paragraph(
            "<font color='#d35400'><b>Each party represents and warrants that it shall comply with all applicable anti-bribery and anti-corruption laws, including the U.S. Foreign Corrupt Practices Act and the UK Bribery Act. Neither party shall, directly or indirectly, offer, promise, give, or authorize the giving of money or anything of value to any government official or any other person for the purpose of obtaining or retaining business or securing any improper advantage.</b></font>",
            ParagraphStyle(
                "BriberyHighlight",
                parent=body_style,
                textColor=colors.HexColor("#d35400"),
                fontName="Helvetica-Bold",
            ),
        )
    )

    story.append(PageBreak())

    # Section 15: U.S. Government Users
    story.append(Paragraph("SECTION 15: U.S. GOVERNMENT END USERS", heading_style))
    story.append(Spacer(1, 0.1 * inch))

    story.append(
        Paragraph("<b>15.1 Commercial Computer Software</b>", subheading_style)
    )
    story.append(
        Paragraph(
            "<font color='#16a085'><b>If Customer is a U.S. Government entity or the Services are being acquired by or on behalf of the U.S. Government, the following provisions apply:</b></font>",
            ParagraphStyle(
                "GovHighlight",
                parent=body_style,
                textColor=colors.HexColor("#16a085"),
                fontName="Helvetica-Bold",
            ),
        )
    )
    story.append(Spacer(1, 0.1 * inch))

    gov_data = [
        [
            "•",
            '<font color=\'#16a085\'><b>Commercial Item:</b> The Services constitute a "commercial item" as that term is defined at 48 C.F.R. § 2.101, consisting of "commercial computer software" and "commercial computer software documentation" as such terms are used in 48 C.F.R. § 12.212.</font>',
        ],
        [
            "•",
            "<font color='#16a085'><b>Limited Rights:</b> Pursuant to 48 C.F.R. § 12.212 or 48 C.F.R. § 227.7202-1 through 227.7202-4, as applicable, the Services are licensed to U.S. Government end users:</font>",
        ],
        ["", "<font color='#16a085'>  (i) Only as commercial items; and</font>"],
        [
            "",
            "<font color='#16a085'>  (ii) With only those rights as are granted to all other end users pursuant to the terms and conditions of this Agreement.</font>",
        ],
        [
            "•",
            "<font color='#16a085'><b>Unpublished Rights:</b> Use, duplication, or disclosure by the U.S. Government is subject to restrictions as set forth in this Agreement and as provided in DFARS 227.7202-1(a) and 227.7202-3(a) (1995), DFARS 252.227-7013(c)(1)(ii) (OCT 1988), FAR 12.212(a) (1995), FAR 52.227-19, or FAR 52.227-14 (ALT III), as applicable.</font>",
        ],
        [
            "•",
            "<font color='#16a085'><b>Manufacturer:</b> The manufacturer for purposes of this clause is CloudTech Solutions Inc., 1500 Technology Drive, Suite 300, San Francisco, CA 94105.</font>",
        ],
    ]

    gov_table = Table(gov_data, colWidths=[0.3 * inch, 5.7 * inch])
    gov_table.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (0, -1), "LEFT"),
                ("ALIGN", (1, 0), (1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#16a085")),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    story.append(gov_table)
    story.append(Spacer(1, 0.2 * inch))

    story.append(
        Paragraph(
            "<b>15.2 Federal Acquisition Regulation (FAR) Compliance</b>",
            subheading_style,
        )
    )
    story.append(
        Paragraph(
            "If Customer is subject to FAR regulations, Customer acknowledges that the Services and related documentation are not designed, manufactured, or intended for use in hazardous environments requiring fail-safe performance, including but not limited to the operation of nuclear facilities, aircraft navigation or communication systems, air traffic control, or weapons systems.",
            body_style,
        )
    )
    story.append(Spacer(1, 0.2 * inch))

    story.append(
        Paragraph(
            "<b>15.3 Additional Terms for Government Contracts</b>", subheading_style
        )
    )
    story.append(
        Paragraph(
            "To the extent required by applicable federal law, the following FAR clauses are incorporated by reference:",
            body_style,
        )
    )
    story.append(
        Paragraph("• FAR 52.227-19 (Commercial Computer Software License)", body_style)
    )
    story.append(
        Paragraph(
            "• FAR 52.204-25 (Prohibition on Contracting for Certain Telecommunications)",
            body_style,
        )
    )
    story.append(
        Paragraph(
            "• FAR 52.204-21 (Basic Safeguarding of Covered Contractor Information Systems)",
            body_style,
        )
    )

    story.append(PageBreak())

    # Section 16: Limitation of Liability (HIGH PRIORITY)
    story.append(Paragraph("SECTION 16: LIMITATION OF LIABILITY", heading_style))
    story.append(Spacer(1, 0.1 * inch))

    story.append(
        Paragraph("<b>16(a) Exceptions to Liability Limitations</b>", subheading_style)
    )
    story.append(
        Paragraph(
            "<font color='#c0392b'><b>THE LIMITATIONS OF LIABILITY SET FORTH IN THIS SECTION 16 SHALL NOT APPLY TO:</b></font>",
            ParagraphStyle(
                "LiabilityHighlight",
                parent=body_style,
                textColor=colors.HexColor("#c0392b"),
                fontName="Helvetica-Bold",
                alignment=TA_CENTER,
            ),
        )
    )
    story.append(Spacer(1, 0.1 * inch))

    liability_data = [
        [
            "(i)",
            "<font color='#c0392b'><b>Gross Negligence or Willful Misconduct:</b> Claims arising from a party's gross negligence, willful misconduct, or intentional breach of this Agreement;</font>",
        ],
        [
            "(ii)",
            "<font color='#c0392b'><b>Fraud:</b> Claims arising from fraud, fraudulent misrepresentation, or fraudulent inducement by either party;</font>",
        ],
        [
            "(iii)",
            "<font color='#c0392b'><b>Intellectual Property Indemnity:</b> Provider's indemnification obligations under Section 12 (IP Indemnity Provisions) for third-party intellectual property infringement claims;</font>",
        ],
        [
            "(iv)",
            "<font color='#c0392b'><b>Confidentiality Breaches:</b> Breaches of the confidentiality obligations set forth in Section 13, including unauthorized use or disclosure of Confidential Information;</font>",
        ],
        [
            "(v)",
            "<font color='#c0392b'><b>Data Security Breaches:</b> Breaches of data security obligations that result in unauthorized access to or disclosure of Customer Data due to Provider's failure to implement required security measures;</font>",
        ],
        [
            "(vi)",
            "<font color='#c0392b'><b>Payment Obligations:</b> Customer's obligation to pay all fees and charges due under this Agreement;</font>",
        ],
        [
            "(vii)",
            "<font color='#c0392b'><b>Violation of Law:</b> Claims arising from a party's violation of applicable laws or regulations, including but not limited to data protection laws, export control laws, and anti-bribery laws;</font>",
        ],
        [
            "(viii)",
            "<font color='#c0392b'><b>Bodily Injury or Property Damage:</b> Claims for bodily injury, death, or tangible property damage caused by a party's negligence;</font>",
        ],
        [
            "(ix)",
            "<font color='#c0392b'><b>Indemnification Obligations:</b> Either party's indemnification obligations under Section 9 of this Agreement.</font>",
        ],
    ]

    liability_table = Table(liability_data, colWidths=[0.5 * inch, 5.5 * inch])
    liability_table.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (0, -1), "LEFT"),
                ("ALIGN", (1, 0), (1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#c0392b")),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )

    story.append(liability_table)
    story.append(Spacer(1, 0.3 * inch))

    story.append(
        Paragraph("<b>16(b) General Limitation of Liability</b>", subheading_style)
    )
    story.append(
        Paragraph(
            "EXCEPT AS PROVIDED IN SECTION 16(a), IN NO EVENT SHALL EITHER PARTY'S AGGREGATE LIABILITY ARISING OUT OF OR RELATED TO THIS AGREEMENT EXCEED THE TOTAL AMOUNT PAID OR PAYABLE BY CUSTOMER TO PROVIDER IN THE TWELVE (12) MONTHS IMMEDIATELY PRECEDING THE EVENT GIVING RISE TO LIABILITY.",
            body_style,
        )
    )
    story.append(Spacer(1, 0.2 * inch))

    story.append(
        Paragraph("<b>16(c) Exclusion of Consequential Damages</b>", subheading_style)
    )
    story.append(
        Paragraph(
            "EXCEPT AS PROVIDED IN SECTION 16(a), IN NO EVENT SHALL EITHER PARTY BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES, INCLUDING BUT NOT LIMITED TO LOSS OF PROFITS, LOSS OF REVENUE, LOSS OF DATA, LOSS OF BUSINESS OPPORTUNITY, OR BUSINESS INTERRUPTION, HOWEVER CAUSED AND UNDER ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, TORT (INCLUDING NEGLIGENCE), STRICT LIABILITY, OR OTHERWISE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.",
            body_style,
        )
    )
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("<b>16(d) Allocation of Risk</b>", subheading_style))
    story.append(
        Paragraph(
            "The parties acknowledge that the limitations of liability set forth in this Section 16 are an essential element of the basis of the bargain between the parties and that Provider would not provide the Services or enter into this Agreement without these limitations.",
            body_style,
        )
    )
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("<b>16(e) Time Limitation on Claims</b>", subheading_style))
    story.append(
        Paragraph(
            "No action, regardless of form, arising out of this Agreement may be brought by either party more than two (2) years after the cause of action has accrued, except that claims for non-payment may be brought within the applicable statute of limitations.",
            body_style,
        )
    )

    story.append(PageBreak())

    # Signature Page
    story.append(Paragraph("SIGNATURE PAGE", heading_style))
    story.append(Spacer(1, 0.3 * inch))

    story.append(
        Paragraph(
            "IN WITNESS WHEREOF, the parties have executed this Software as a Service Master Service Agreement as of the Effective Date.",
            body_style,
        )
    )
    story.append(Spacer(1, 0.5 * inch))

    # Signature table
    sig_data = [
        ["CLOUDTECH SOLUTIONS INC.", "ENTERPRISE CUSTOMER CORP."],
        ["", ""],
        ["", ""],
        ["By: _________________________", "By: _________________________"],
        ["", ""],
        ["Name: Jennifer Martinez", "Name: Robert Chen"],
        ["", ""],
        ["Title: Chief Revenue Officer", "Title: Chief Procurement Officer"],
        ["", ""],
        ["Date: _______________________", "Date: _______________________"],
    ]

    sig_table = Table(sig_data, colWidths=[3 * inch, 3 * inch])
    sig_table.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ]
        )
    )

    story.append(sig_table)

    doc.build(story)
    print(f"✓ Created: {filename}")


def main():
    print("\n" + "=" * 70)
    print("GENERATING SaaS MASTER SERVICE AGREEMENT")
    print("=" * 70)
    print("\nThis document includes highlighted sections for:")
    print("  🔴 Termination Clauses (Section 10)")
    print("  🔵 Assignment Restrictions (Section 14e)")
    print("  🟢 Confidentiality (Section 13)")
    print("  🟡 Payment Terms (Section 3)")
    print("  🟣 IP Indemnity (Section 12)")
    print("  🟠 U.S. Government Users (Section 15)")
    print("  🔴 Liability Limitations & Exceptions (Section 16)")
    print("\n" + "-" * 70)

    create_saas_master_agreement()

    print("-" * 70)
    print("✓ Document generated successfully!")
    print("\nGenerated file:")
    print("  • SaaS_Master_Agreement_CloudTech_2024.pdf")

    print("\n" + "=" * 70)
    print("KEY HIGHLIGHTED PROVISIONS SUMMARY:")
    print("=" * 70)

    print("\n📋 TERMINATION (Section 10):")
    print("  • Immediate termination for insolvency/bankruptcy")
    print("  • 10-day data retrieval window post-termination")
    print("  • Pro-rata refunds only if Provider breaches")
    print("  • No refunds for Customer convenience termination")

    print("\n📋 ASSIGNMENT (Section 14e):")
    print("  • Must assign ALL rights (no partial assignments)")
    print("  • Permitted: to affiliates or in M&A transactions")
    print("  • Assignee must be financially/technically capable")
    print("  • 30-day advance written notice required")

    print("\n📋 LIABILITY EXCEPTIONS (Section 16a):")
    print("  • Gross negligence & willful misconduct")
    print("  • Fraud & fraudulent misrepresentation")
    print("  • IP indemnity breaches (Section 12)")
    print("  • Confidentiality violations (Section 13)")
    print("  • Data security breaches")
    print("  • Payment obligations")
    print("  • Violations of law (including anti-bribery)")

    print("\n📋 PAYMENT TERMS (Section 3):")
    print("  • 30-day payment terms")
    print("  • 1.5% monthly late payment interest")
    print("  • Annual prepayment required")
    print("  • Non-refundable (except Section 10d)")

    print("\n📋 CONFIDENTIALITY (Section 13):")
    print("  • 5-year survival post-termination")
    print("  • Trade secrets protected indefinitely")
    print("  • Need-to-know disclosure only")
    print("  • Prompt breach notification required")

    print("\n📋 IP INDEMNITY (Section 12):")
    print("  • Provider defends infringement claims")
    print("  • Exclusive remedy for IP disputes")
    print("  • Exceptions for Customer modifications")

    print("\n📋 U.S. GOVERNMENT (Section 15):")
    print("  • Commercial item designation")
    print("  • Limited rights per FAR 12.212")
    print("  • FAR clause incorporations")

    print("\n📋 ANTI-BRIBERY (Section 14i):")
    print("  • FCPA & UK Bribery Act compliance")
    print("  • No payments to government officials")

    print("\n" + "=" * 70)
    print("Document ready for AI contract review demo!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
