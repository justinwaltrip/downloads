import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from datetime import datetime


def create_purchase_agreement():
    """Create Share Purchase Agreement excerpt"""
    filename = "Share_Purchase_Agreement_Prolife_2024.pdf"
    
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
        textColor="black",
        alignment=TA_CENTER,
        spaceAfter=20,
        fontName="Helvetica-Bold",
    )
    
    heading_style = ParagraphStyle(
        "Heading",
        parent=styles["Heading2"],
        fontSize=12,
        textColor="black",
        spaceAfter=10,
        fontName="Helvetica-Bold",
    )
    
    subheading_style = ParagraphStyle(
        "SubHeading",
        parent=styles["Heading3"],
        fontSize=11,
        textColor="black",
        spaceAfter=8,
        fontName="Helvetica-Bold",
    )
    
    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontSize=10,
        textColor="black",
        spaceAfter=8,
        leading=14,
    )
    
    story = []
    
    # Title
    story.append(Paragraph("SHARE PURCHASE AGREEMENT", title_style))
    story.append(Paragraph("(EXCERPT)", heading_style))
    story.append(Spacer(1, 0.3 * inch))
    
    # Date and parties
    story.append(Paragraph("This Agreement dated November 15, 2024, between:", body_style))
    story.append(Spacer(1, 0.1 * inch))
    
    story.append(Paragraph("<b>Seller:</b> Mr. Mahendra Patel and Mrs. Nita Patel (Promoters)", body_style))
    story.append(Paragraph("<b>Purchaser:</b> MedTech Global Holdings Ltd.", body_style))
    story.append(Paragraph("<b>Target Company:</b> Prolife Industries Limited", body_style))
    story.append(Spacer(1, 0.1 * inch))
    
    story.append(Paragraph("<b>Purchase Price:</b> INR 450 Crores (subject to adjustments)", body_style))
    story.append(Spacer(1, 0.3 * inch))
    
    # Article 4
    story.append(Paragraph("ARTICLE 4: REPRESENTATIONS AND WARRANTIES", heading_style))
    story.append(Spacer(1, 0.1 * inch))
    
    story.append(Paragraph("<b>4.1 Corporate Matters</b>", subheading_style))
    story.append(Paragraph("• The Company is duly incorporated and validly existing under the laws of India", body_style))
    story.append(Paragraph("• All corporate actions required for this transaction have been properly authorized", body_style))
    story.append(Spacer(1, 0.1 * inch))
    
    story.append(Paragraph("<b>4.2 Financial Statements</b>", subheading_style))
    story.append(Paragraph("• The audited financial statements for FY 2012-2015 prepared by M/s Mistry & Shah present fairly the financial position", body_style))
    story.append(Paragraph("• No material adverse changes since March 31, 2015", body_style))
    story.append(Spacer(1, 0.1 * inch))
    
    story.append(Paragraph("<b>4.3 Assets and Properties</b>", subheading_style))
    story.append(Paragraph("• The Company has good and marketable title to all manufacturing facilities in Ahmedabad", body_style))
    story.append(Paragraph("• All machinery and equipment are in good working condition", body_style))
    story.append(Spacer(1, 0.1 * inch))
    
    story.append(Paragraph("<b>4.4 Material Contracts</b>", subheading_style))
    story.append(Paragraph("• All customer and supplier agreements disclosed in Schedule 4.4 are valid and enforceable", body_style))
    story.append(Paragraph("• No customer represents more than 15% of annual revenue", body_style))
    story.append(Spacer(1, 0.1 * inch))
    
    story.append(Paragraph("<b>4.5 Compliance</b>", subheading_style))
    story.append(Paragraph("• Company is in compliance with all pharmaceutical manufacturing regulations", body_style))
    story.append(Paragraph("• All necessary licenses from regulatory authorities are current", body_style))
    story.append(Spacer(1, 0.3 * inch))
    
    # Article 7
    story.append(Paragraph("ARTICLE 7: INDEMNIFICATION", heading_style))
    story.append(Spacer(1, 0.1 * inch))
    
    story.append(Paragraph("<b>7.1 Indemnification by Seller</b>", subheading_style))
    story.append(Paragraph("Seller agrees to indemnify Purchaser for:", body_style))
    story.append(Paragraph("• Breach of representations and warranties (Cap: 30% of Purchase Price)", body_style))
    story.append(Paragraph("• Pre-closing tax liabilities", body_style))
    story.append(Paragraph("• Environmental liabilities existing prior to Closing Date", body_style))
    story.append(Paragraph("• Undisclosed litigation or claims", body_style))
    story.append(Spacer(1, 0.1 * inch))
    
    story.append(Paragraph("<b>7.2 Survival Period</b>", subheading_style))
    story.append(Paragraph("• General representations: 24 months post-closing", body_style))
    story.append(Paragraph("• Tax matters: 6 years", body_style))
    story.append(Paragraph("• Environmental: 7 years", body_style))
    story.append(Spacer(1, 0.1 * inch))
    
    story.append(Paragraph("<b>7.3 Basket and Cap</b>", subheading_style))
    story.append(Paragraph("• Basket (minimum claim): INR 50 Lakhs", body_style))
    story.append(Paragraph("• Cap (maximum liability): INR 135 Crores (30% of purchase price)", body_style))
    story.append(Spacer(1, 0.3 * inch))
    
    # Article 9
    story.append(Paragraph("ARTICLE 9: MATERIAL ADVERSE CHANGE", heading_style))
    story.append(Spacer(1, 0.1 * inch))
    
    story.append(Paragraph("<b>9.1 Definition</b>", subheading_style))
    story.append(Paragraph('"Material Adverse Change" means any event, change, or effect that has resulted in, or would reasonably be expected to result in:', body_style))
    story.append(Paragraph("• Decline in EBITDA exceeding 20% compared to prior year", body_style))
    story.append(Paragraph("• Loss of any customer representing more than 10% of revenue", body_style))
    story.append(Paragraph("• Regulatory action suspending manufacturing operations", body_style))
    story.append(Paragraph("• Litigation with potential liability exceeding INR 10 Crores", body_style))
    
    doc.build(story)
    print(f"Created: {filename}")


def create_employment_agreement_coo():
    """Create Employment Retention Agreement for COO"""
    filename = "Employment_Agreement_Kumar_COO_2024.pdf"
    
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
        fontSize=14,
        textColor="black",
        alignment=TA_CENTER,
        spaceAfter=20,
        fontName="Helvetica-Bold",
    )
    
    heading_style = ParagraphStyle(
        "Heading",
        parent=styles["Heading2"],
        fontSize=12,
        textColor="black",
        spaceAfter=10,
        fontName="Helvetica-Bold",
    )
    
    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontSize=10,
        textColor="black",
        spaceAfter=8,
        leading=14,
    )
    
    story = []
    
    story.append(Paragraph("EMPLOYMENT RETENTION AGREEMENT", title_style))
    story.append(Spacer(1, 0.3 * inch))
    
    story.append(Paragraph("<b>Employee:</b> Mr. Rajesh Kumar, Chief Operating Officer", body_style))
    story.append(Paragraph("<b>Effective Date:</b> Upon Transaction Closing", body_style))
    story.append(Paragraph("<b>Term:</b> 3 years", body_style))
    story.append(Spacer(1, 0.2 * inch))
    
    story.append(Paragraph("COMPENSATION PACKAGE:", heading_style))
    story.append(Paragraph("• <b>Base Salary:</b> INR 95 Lakhs per annum", body_style))
    story.append(Paragraph("• <b>Retention Bonus:</b> INR 1.2 Crores (paid 50% at 18 months, 50% at 36 months)", body_style))
    story.append(Paragraph("• <b>Annual Performance Bonus:</b> Up to 40% of base salary", body_style))
    story.append(Paragraph("• <b>Benefits:</b> Company car, health insurance, provident fund", body_style))
    story.append(Spacer(1, 0.2 * inch))
    
    story.append(Paragraph("KEY TERMS:", heading_style))
    story.append(Spacer(1, 0.1 * inch))
    
    story.append(Paragraph("<b>Change of Control Protection:</b>", body_style))
    story.append(Paragraph("If terminated without cause within 24 months post-closing, entitled to 18 months severance", body_style))
    story.append(Spacer(1, 0.1 * inch))
    
    story.append(Paragraph("<b>Non-Compete:</b>", body_style))
    story.append(Paragraph("2 years post-employment within pharmaceutical manufacturing sector in India", body_style))
    story.append(Spacer(1, 0.1 * inch))
    
    story.append(Paragraph("<b>Non-Solicitation:</b>", body_style))
    story.append(Paragraph("2 years for employees and customers", body_style))
    story.append(Spacer(1, 0.4 * inch))
    
    story.append(Paragraph("_" * 60, body_style))
    story.append(Paragraph("Employee Signature: _________________________  Date: __________", body_style))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("Company Representative: _____________________  Date: __________", body_style))
    
    doc.build(story)
    print(f"Created: {filename}")


def create_employment_agreement_qa():
    """Create Employment Retention Agreement for QA Head"""
    filename = "Employment_Agreement_Desai_QA_2024.pdf"
    
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
        fontSize=14,
        textColor="black",
        alignment=TA_CENTER,
        spaceAfter=20,
        fontName="Helvetica-Bold",
    )
    
    heading_style = ParagraphStyle(
        "Heading",
        parent=styles["Heading2"],
        fontSize=12,
        textColor="black",
        spaceAfter=10,
        fontName="Helvetica-Bold",
    )
    
    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontSize=10,
        textColor="black",
        spaceAfter=8,
        leading=14,
    )
    
    story = []
    
    story.append(Paragraph("EMPLOYMENT RETENTION AGREEMENT", title_style))
    story.append(Spacer(1, 0.3 * inch))
    
    story.append(Paragraph("<b>Employee:</b> Ms. Priya Desai, Head of Quality Assurance", body_style))
    story.append(Paragraph("<b>Effective Date:</b> Upon Transaction Closing", body_style))
    story.append(Paragraph("<b>Term:</b> 3 years", body_style))
    story.append(Spacer(1, 0.2 * inch))
    
    story.append(Paragraph("COMPENSATION PACKAGE:", heading_style))
    story.append(Paragraph("• <b>Base Salary:</b> INR 72 Lakhs per annum", body_style))
    story.append(Paragraph("• <b>Retention Bonus:</b> INR 90 Lakhs (paid 50% at 18 months, 50% at 36 months)", body_style))
    story.append(Paragraph("• <b>Annual Performance Bonus:</b> Up to 35% of base salary", body_style))
    story.append(Paragraph("• <b>Stock Options:</b> 25,000 options in parent company vesting over 4 years", body_style))
    story.append(Spacer(1, 0.2 * inch))
    
    story.append(Paragraph("KEY TERMS:", heading_style))
    story.append(Spacer(1, 0.1 * inch))
    
    story.append(Paragraph("<b>Change of Control Protection:</b>", body_style))
    story.append(Paragraph("If terminated without cause within 24 months, entitled to 12 months severance", body_style))
    story.append(Spacer(1, 0.1 * inch))
    
    story.append(Paragraph("<b>Non-Compete:</b>", body_style))
    story.append(Paragraph("18 months within pharmaceutical quality/regulatory roles in India", body_style))
    story.append(Spacer(1, 0.1 * inch))
    
    story.append(Paragraph("<b>Relocation:</b>", body_style))
    story.append(Paragraph("Company will cover relocation if required to move to Mumbai headquarters", body_style))
    story.append(Spacer(1, 0.4 * inch))
    
    story.append(Paragraph("_" * 60, body_style))
    story.append(Paragraph("Employee Signature: _________________________  Date: __________", body_style))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("Company Representative: _____________________  Date: __________", body_style))
    
    doc.build(story)
    print(f"Created: {filename}")


def create_financial_statements():
    """Create Financial Statements summary"""
    filename = "Financial_Statements_Prolife_FY2013-2015.pdf"
    
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
        fontSize=14,
        textColor="black",
        alignment=TA_CENTER,
        spaceAfter=20,
        fontName="Helvetica-Bold",
    )
    
    heading_style = ParagraphStyle(
        "Heading",
        parent=styles["Heading2"],
        fontSize=12,
        textColor="black",
        spaceAfter=10,
        fontName="Helvetica-Bold",
    )
    
    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontSize=10,
        textColor="black",
        spaceAfter=8,
        leading=14,
    )
    
    story = []
    
    story.append(Paragraph("PROLIFE INDUSTRIES LIMITED", title_style))
    story.append(Paragraph("Consolidated Statement of Profit & Loss", heading_style))
    story.append(Paragraph("(All figures in INR Crores)", body_style))
    story.append(Spacer(1, 0.2 * inch))
    
    # P&L Table
    pl_data = [
        ["", "FY 2015", "FY 2014", "FY 2013"],
        ["Revenue from Operations", "285.4", "242.8", "198.5"],
        ["Cost of Materials", "142.7", "121.4", "99.2"],
        ["Employee Benefits", "45.2", "38.6", "31.8"],
        ["EBITDA", "52.8", "44.3", "35.7"],
        ["EBITDA Margin", "18.5%", "18.2%", "18.0%"],
        ["Depreciation", "8.4", "7.2", "6.1"],
        ["Interest", "12.3", "10.8", "9.4"],
        ["Profit Before Tax", "32.1", "26.3", "20.2"],
        ["Tax", "10.9", "8.9", "6.9"],
        ["Profit After Tax", "21.2", "17.4", "13.3"],
    ]
    
    pl_table = Table(pl_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    pl_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 4), (-1, 4), 'Helvetica-Bold'),
        ('FONTNAME', (0, 9), (-1, 9), 'Helvetica-Bold'),
    ]))
    
    story.append(pl_table)
    story.append(Spacer(1, 0.3 * inch))
    
    # Balance Sheet
    story.append(Paragraph("Key Balance Sheet Items (as of March 31, 2015)", heading_style))
    story.append(Spacer(1, 0.1 * inch))
    
    story.append(Paragraph("• <b>Total Assets:</b> INR 385 Crores", body_style))
    story.append(Paragraph("• <b>Net Fixed Assets:</b> INR 145 Crores", body_style))
    story.append(Paragraph("• <b>Current Assets:</b> INR 198 Crores", body_style))
    story.append(Paragraph("• <b>Total Debt:</b> INR 142 Crores", body_style))
    story.append(Paragraph("• <b>Net Worth:</b> INR 168 Crores", body_style))
    story.append(Spacer(1, 0.3 * inch))
    
    story.append(Paragraph("_" * 70, body_style))
    story.append(Paragraph("Audited by: M/s Mistry & Shah, Chartered Accountants", body_style))
    story.append(Paragraph("Date: May 15, 2015", body_style))
    
    doc.build(story)
    print(f"Created: {filename}")


def create_indemnification_schedule():
    """Create Indemnification Claims Schedule"""
    filename = "Indemnification_Claims_Schedule_Prolife_2024.pdf"
    
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
        fontSize=14,
        textColor="black",
        alignment=TA_CENTER,
        spaceAfter=20,
        fontName="Helvetica-Bold",
    )
    
    heading_style = ParagraphStyle(
        "Heading",
        parent=styles["Heading2"],
        fontSize=12,
        textColor="black",
        spaceAfter=10,
        fontName="Helvetica-Bold",
    )
    
    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontSize=10,
        textColor="black",
        spaceAfter=8,
        leading=14,
    )
    
    story = []
    
    story.append(Paragraph("INDEMNIFICATION CLAIMS SCHEDULE", title_style))
    story.append(Paragraph("Schedule 7.1(a) - Known Indemnification Matters", heading_style))
    story.append(Spacer(1, 0.2 * inch))
    
    story.append(Paragraph("As of November 15, 2024", body_style))
    story.append(Spacer(1, 0.2 * inch))
    
    # Claims Table
    claims_data = [
        ["Item", "Description", "Estimated Liability", "Status"],
        ["A", "Pending GST audit for FY 2013-14", "INR 2.5 Cr", "Under review"],
        ["B", "Employee dispute - wrongful\ntermination claim", "INR 0.8 Cr", "In arbitration"],
        ["C", "Customer warranty claim -\nProduct batch QC issue", "INR 1.2 Cr", "Negotiating\nsettlement"],
    ]
    
    claims_table = Table(claims_data, colWidths=[0.5*inch, 3*inch, 1.5*inch, 1.5*inch])
    claims_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    story.append(claims_table)
    story.append(Spacer(1, 0.3 * inch))
    
    story.append(Paragraph("<b>Total Reserved Indemnity Amount: INR 4.5 Crores</b>", heading_style))
    story.append(Paragraph("(held in escrow)", body_style))
    story.append(Spacer(1, 0.3 * inch))
    
    story.append(Paragraph("NOTES:", heading_style))
    story.append(Paragraph("• All amounts are estimates and subject to final resolution", body_style))
    story.append(Paragraph("• Escrow amount will be released per the terms of the Escrow Agreement", body_style))
    story.append(Paragraph("• Additional claims may be made subject to the survival periods outlined in Article 7.2", body_style))
    
    doc.build(story)
    print(f"Created: {filename}")


def main():
    print("Generating M&A Transaction Documents for Prolife Industries...")
    print("-" * 70)
    
    create_purchase_agreement()
    create_employment_agreement_coo()
    create_employment_agreement_qa()
    create_financial_statements()
    create_indemnification_schedule()
    
    print("-" * 70)
    print("All documents generated successfully!")
    print("\nGenerated files:")
    print("1. Share_Purchase_Agreement_Prolife_2024.pdf")
    print("2. Employment_Agreement_Kumar_COO_2024.pdf")
    print("3. Employment_Agreement_Desai_QA_2024.pdf")
    print("4. Financial_Statements_Prolife_FY2013-2015.pdf")
    print("5. Indemnification_Claims_Schedule_Prolife_2024.pdf")
    
    print("\n" + "=" * 70)
    print("TRANSACTION SUMMARY:")
    print("  Target: Prolife Industries Limited")
    print("  Seller: Mahendra & Nita Patel (Promoters)")
    print("  Buyer: MedTech Global Holdings Ltd.")
    print("  Deal Value: INR 450 Crores")
    print("  Date: November 15, 2024")
    print("\nKEY TERMS:")
    print("  • Indemnity Cap: INR 135 Crores (30% of price)")
    print("  • Basket: INR 50 Lakhs")
    print("  • Escrow: INR 4.5 Crores (known claims)")
    print("  • R&W Survival: 24 months (general), 6 years (tax), 7 years (environmental)")
    print("\nKEY EMPLOYEES:")
    print("  • Rajesh Kumar (COO): INR 1.2 Cr retention, 18-month severance, 2-year non-compete")
    print("  • Priya Desai (QA Head): INR 90 Lakhs retention, 12-month severance, 18-month non-compete")
    print("\nFINANCIAL HIGHLIGHTS (FY 2015):")
    print("  • Revenue: INR 285.4 Crores")
    print("  • EBITDA: INR 52.8 Crores (18.5% margin)")
    print("  • PAT: INR 21.2 Crores")
    print("  • Total Assets: INR 385 Crores")
    print("=" * 70)


if __name__ == "__main__":
    main()