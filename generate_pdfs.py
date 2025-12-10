import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfgen import canvas


def create_property_management_agreement():
    """Create a 15-page Property Management Agreement with key excerpts on specific pages"""
    filename = "Shelter_Cove_District_Property_Management_Agreement_2024.pdf"
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        topMargin=1 * inch,
        bottomMargin=1 * inch,
        leftMargin=1 * inch,
        rightMargin=1 * inch,
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Heading1"],
        fontSize=16,
        textColor="black",
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
    )

    heading_style = ParagraphStyle(
        "CustomHeading",
        parent=styles["Heading2"],
        fontSize=12,
        textColor="black",
        spaceAfter=12,
        spaceBefore=12,
        fontName="Helvetica-Bold",
    )

    subheading_style = ParagraphStyle(
        "CustomSubHeading",
        parent=styles["Heading3"],
        fontSize=10,
        textColor="black",
        spaceAfter=8,
        spaceBefore=8,
        fontName="Helvetica-Bold",
    )

    body_style = ParagraphStyle(
        "CustomBody",
        parent=styles["BodyText"],
        fontSize=10,
        textColor="black",
        spaceAfter=6,
        alignment=TA_JUSTIFY,
        leading=14,
    )

    story = []

    # Page 1 - Title Page
    story.append(Spacer(1, 1 * inch))
    story.append(Paragraph("PROPERTY MANAGEMENT AGREEMENT", title_style))
    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph("<b>Date:</b> March 15, 2024", body_style))
    story.append(
        Paragraph(
            '<b>Between:</b> Shelter Cove District ("Owner") and Coastal Property Services LLC ("Manager")',
            body_style,
        )
    )
    story.append(
        Paragraph(
            "<b>Property:</b> Marios Marina, 533 Machi Road, Shelter Cove, California 95589",
            body_style,
        )
    )

    # Pages 2-3 - Blank
    story.append(PageBreak())
    story.append(Paragraph(" ", body_style))
    story.append(PageBreak())
    story.append(Paragraph(" ", body_style))

    # Page 4 - SECTION 5: MAINTENANCE AND REPAIRS
    story.append(PageBreak())
    story.append(Paragraph("SECTION 5: MAINTENANCE AND REPAIRS", heading_style))
    story.append(Spacer(1, 0.2 * inch))

    story.append(
        Paragraph("5.1 Manager's Maintenance Responsibilities", subheading_style)
    )
    story.append(Paragraph("Manager shall be responsible for:", body_style))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("• Routine inspections of all common areas", body_style))
    story.append(Paragraph("• Landscaping and grounds maintenance", body_style))
    story.append(
        Paragraph("• Exterior building maintenance including roofing", body_style)
    )
    story.append(
        Paragraph(
            "• <b>HVAC system maintenance, repair, and replacement for all building systems</b>",
            body_style,
        )
    )
    story.append(Paragraph("• Plumbing and electrical system oversight", body_style))
    story.append(
        Paragraph("• Emergency repairs up to $5,000 without prior approval", body_style)
    )
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("5.2 Maintenance Schedule", subheading_style))
    story.append(Paragraph("Manager agrees to:", body_style))
    story.append(Spacer(1, 0.1 * inch))
    story.append(
        Paragraph("• Conduct quarterly HVAC inspections and servicing", body_style)
    )
    story.append(
        Paragraph(
            "• Maintain service contracts with licensed HVAC contractors", body_style
        )
    )
    story.append(Paragraph("• Respond to HVAC emergencies within 4 hours", body_style))
    story.append(
        Paragraph("• Keep detailed maintenance logs for Owner review", body_style)
    )

    # Pages 5-8 - Blank
    for _ in range(4):
        story.append(PageBreak())
        story.append(Paragraph(" ", body_style))

    # Page 9 - SECTION 8: TENANT COORDINATION
    story.append(PageBreak())
    story.append(Paragraph("SECTION 8: TENANT COORDINATION", heading_style))
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("8.3 Tenant Maintenance Issues", subheading_style))
    story.append(
        Paragraph("When tenants report maintenance issues, Manager shall:", body_style)
    )
    story.append(Spacer(1, 0.1 * inch))
    story.append(
        Paragraph(
            "• Assess whether issue falls under tenant or landlord responsibility per lease terms",
            body_style,
        )
    )
    story.append(
        Paragraph(
            "• <b>For HVAC issues: Manager assumes responsibility regardless of lease terms to ensure property protection</b>",
            body_style,
        )
    )
    story.append(
        Paragraph("• Coordinate with tenants for access within 24-48 hours", body_style)
    )
    story.append(
        Paragraph(
            "• Document all maintenance activities in monthly reports", body_style
        )
    )

    # Pages 10-11 - Blank
    story.append(PageBreak())
    story.append(Paragraph(" ", body_style))
    story.append(PageBreak())
    story.append(Paragraph(" ", body_style))

    # Page 12 - SECTION 11: INSURANCE AND LIABILITY
    story.append(PageBreak())
    story.append(Paragraph("SECTION 11: INSURANCE AND LIABILITY", heading_style))
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("11.4 Equipment Coverage", subheading_style))
    story.append(Paragraph("Manager maintains insurance coverage for:", body_style))
    story.append(Spacer(1, 0.1 * inch))
    story.append(
        Paragraph("• All mechanical systems including HVAC equipment", body_style)
    )
    story.append(
        Paragraph(
            "• Manager assumes liability for mechanical system failures", body_style
        )
    )
    story.append(
        Paragraph("• Coverage includes emergency replacement costs", body_style)
    )
    story.append(Spacer(1, 0.1 * inch))
    story.append(
        Paragraph(
            "Owner acknowledges Manager's authority to make urgent repairs to preserve property value.",
            body_style,
        )
    )

    # Pages 13-15 - Blank
    for _ in range(3):
        story.append(PageBreak())
        story.append(Paragraph(" ", body_style))

    doc.build(story)
    print(f"Created: {filename}")


def create_email_correspondence():
    """Create Email Correspondence Chain PDF"""
    filename = "Email_Thread_HVAC_Maintenance_Oct2024.pdf"
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
        "CustomTitle",
        parent=styles["Heading1"],
        fontSize=14,
        textColor="black",
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
    )

    email_header_style = ParagraphStyle(
        "EmailHeader",
        parent=styles["Normal"],
        fontSize=9,
        textColor="#333333",
        spaceAfter=4,
        fontName="Helvetica",
    )

    email_subject_style = ParagraphStyle(
        "EmailSubject",
        parent=styles["Normal"],
        fontSize=10,
        textColor="black",
        spaceAfter=10,
        fontName="Helvetica-Bold",
    )

    body_style = ParagraphStyle(
        "CustomBody",
        parent=styles["BodyText"],
        fontSize=10,
        textColor="black",
        spaceAfter=6,
        leading=14,
    )

    story = []

    # Title
    story.append(Paragraph("EMAIL THREAD: HVAC Maintenance Clarification", title_style))
    story.append(Spacer(1, 0.3 * inch))

    # Email 1
    story.append(Paragraph("Email 1 of 5", email_subject_style))
    story.append(
        Paragraph(
            "<b>From:</b> Mario Battaglia &lt;mario@mariosmarina.com&gt;",
            email_header_style,
        )
    )
    story.append(
        Paragraph(
            "<b>To:</b> Jennifer Wells &lt;jwells@coastalpropertyservices.com&gt;",
            email_header_style,
        )
    )
    story.append(Paragraph("<b>Date:</b> October 3, 2024, 9:42 AM", email_header_style))
    story.append(
        Paragraph(
            "<b>Subject:</b> HVAC Unit Making Noise - Marina Office",
            email_subject_style,
        )
    )
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("Hi Jennifer,", body_style))
    story.append(Spacer(1, 0.05 * inch))
    story.append(
        Paragraph(
            "The HVAC unit in the main marina office has been making a grinding noise for the past week. It's getting louder and I'm concerned it might fail completely.",
            body_style,
        )
    )
    story.append(Spacer(1, 0.05 * inch))
    story.append(
        Paragraph(
            "According to our lease agreement (Section 6, I believe), I think this might be my responsibility to handle, but I wanted to check with you first since it's a major building system. Can you advise on the proper procedure?",
            body_style,
        )
    )
    story.append(Spacer(1, 0.05 * inch))
    story.append(
        Paragraph(
            "The unit is still cooling, but the noise is disruptive to customers.",
            body_style,
        )
    )
    story.append(Spacer(1, 0.05 * inch))
    story.append(Paragraph("Thanks,<br/>Mario", body_style))
    story.append(Spacer(1, 0.3 * inch))

    # Email 2
    story.append(Paragraph("Email 2 of 5", email_subject_style))
    story.append(
        Paragraph(
            "<b>From:</b> Jennifer Wells &lt;jwells@coastalpropertyservices.com&gt;",
            email_header_style,
        )
    )
    story.append(
        Paragraph(
            "<b>To:</b> Mario Battaglia &lt;mario@mariosmarina.com&gt;",
            email_header_style,
        )
    )
    story.append(
        Paragraph("<b>Date:</b> October 3, 2024, 11:15 AM", email_header_style)
    )
    story.append(
        Paragraph(
            "<b>Subject:</b> RE: HVAC Unit Making Noise - Marina Office",
            email_subject_style,
        )
    )
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("Hi Mario,", body_style))
    story.append(Spacer(1, 0.05 * inch))
    story.append(
        Paragraph(
            "<b>Don't worry about this - HVAC is definitely our responsibility under the property management agreement.</b> I'll have our HVAC contractor (Redwood Climate Control) come out tomorrow to assess it.",
            body_style,
        )
    )
    story.append(Spacer(1, 0.05 * inch))
    story.append(
        Paragraph(
            "We handle all mechanical systems to protect the owner's investment. You shouldn't be paying for or arranging any HVAC work.",
            body_style,
        )
    )
    story.append(Spacer(1, 0.05 * inch))
    story.append(Paragraph("I'll keep you posted on what they find.", body_style))
    story.append(Spacer(1, 0.05 * inch))
    story.append(
        Paragraph(
            "Best,<br/>Jennifer Wells<br/>Property Manager<br/>Coastal Property Services LLC",
            body_style,
        )
    )
    story.append(Spacer(1, 0.3 * inch))

    # Email 3
    story.append(Paragraph("Email 3 of 5", email_subject_style))
    story.append(
        Paragraph(
            "<b>From:</b> Mario Battaglia &lt;mario@mariosmarina.com&gt;",
            email_header_style,
        )
    )
    story.append(
        Paragraph(
            "<b>To:</b> Jennifer Wells &lt;jwells@coastalpropertyservices.com&gt;",
            email_header_style,
        )
    )
    story.append(Paragraph("<b>Date:</b> October 3, 2024, 2:33 PM", email_header_style))
    story.append(
        Paragraph(
            "<b>Subject:</b> RE: HVAC Unit Making Noise - Marina Office",
            email_subject_style,
        )
    )
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("Jennifer,", body_style))
    story.append(Spacer(1, 0.05 * inch))
    story.append(
        Paragraph(
            'Thanks for the quick response. Just to clarify - I was reviewing my lease this morning and <b>Section 6(a), item 4 specifically mentions that I\'m responsible for "maintenance and repair of all improvements constructed by Lessee."</b>',
            body_style,
        )
    )
    story.append(Spacer(1, 0.05 * inch))
    story.append(
        Paragraph(
            "Since I made significant improvements to the office building including the HVAC upgrade in 2023, I want to make sure we're on the same page about who handles this.",
            body_style,
        )
    )
    story.append(Spacer(1, 0.05 * inch))
    story.append(
        Paragraph(
            "I'm fine either way, just want to avoid any confusion or billing issues later.",
            body_style,
        )
    )
    story.append(Spacer(1, 0.05 * inch))
    story.append(Paragraph("Mario", body_style))
    story.append(PageBreak())

    # Email 4
    story.append(Paragraph("Email 4 of 5", email_subject_style))
    story.append(
        Paragraph(
            "<b>From:</b> Jennifer Wells &lt;jwells@coastalpropertyservices.com&gt;",
            email_header_style,
        )
    )
    story.append(
        Paragraph(
            "<b>To:</b> David Chen &lt;dchen@coastalpropertyservices.com&gt;",
            email_header_style,
        )
    )
    story.append(
        Paragraph(
            "<b>Cc:</b> Mario Battaglia &lt;mario@mariosmarina.com&gt;",
            email_header_style,
        )
    )
    story.append(Paragraph("<b>Date:</b> October 3, 2024, 4:50 PM", email_header_style))
    story.append(
        Paragraph(
            "<b>Subject:</b> RE: HVAC Unit Making Noise - Marina Office",
            email_subject_style,
        )
    )
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("Looping in David from our legal team.", body_style))
    story.append(Spacer(1, 0.05 * inch))
    story.append(
        Paragraph(
            "Mario raises a good point. <b>There may be a conflict between the tenant lease and our management agreement regarding HVAC responsibility.</b> Our agreement with the District clearly puts all HVAC under our scope (Section 5.1), but Mario's lease may assign responsibility for improvements he made.",
            body_style,
        )
    )
    story.append(Spacer(1, 0.05 * inch))
    story.append(
        Paragraph(
            "David - can you review both documents and advise? The HVAC tech is scheduled for tomorrow at 10 AM.",
            body_style,
        )
    )
    story.append(Spacer(1, 0.05 * inch))
    story.append(Paragraph("Jennifer", body_style))
    story.append(Spacer(1, 0.3 * inch))

    # Email 5
    story.append(Paragraph("Email 5 of 5", email_subject_style))
    story.append(
        Paragraph(
            "<b>From:</b> David Chen &lt;dchen@coastalpropertyservices.com&gt;",
            email_header_style,
        )
    )
    story.append(
        Paragraph(
            "<b>To:</b> Jennifer Wells &lt;jwells@coastalpropertyservices.com&gt;",
            email_header_style,
        )
    )
    story.append(
        Paragraph(
            "<b>Cc:</b> Mario Battaglia &lt;mario@mariosmarina.com&gt;",
            email_header_style,
        )
    )
    story.append(Paragraph("<b>Date:</b> October 4, 2024, 8:20 AM", email_header_style))
    story.append(
        Paragraph(
            "<b>Subject:</b> RE: HVAC Unit Making Noise - Marina Office - URGENT CLARIFICATION NEEDED",
            email_subject_style,
        )
    )
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("Jennifer and Mario,", body_style))
    story.append(Spacer(1, 0.05 * inch))
    story.append(
        Paragraph(
            "After reviewing both documents, <b>we have a clear conflict:</b>",
            body_style,
        )
    )
    story.append(Spacer(1, 0.1 * inch))
    story.append(
        Paragraph(
            "<b>Tenant Lease (Section 6(a), item 4):</b> Tenant responsible for maintenance/repair of all improvements constructed by Lessee",
            body_style,
        )
    )
    story.append(Spacer(1, 0.05 * inch))
    story.append(
        Paragraph(
            "<b>Property Management Agreement (Section 5.1):</b> Manager responsible for all HVAC system maintenance and repair",
            body_style,
        )
    )
    story.append(Spacer(1, 0.1 * inch))
    story.append(
        Paragraph(
            "<b>Recommendation:</b> We need written clarification from Shelter Cove District on which document takes precedence. In the interim, I suggest:",
            body_style,
        )
    )
    story.append(Spacer(1, 0.05 * inch))
    story.append(
        Paragraph(
            "1. Manager proceeds with inspection/repair to prevent property damage",
            body_style,
        )
    )
    story.append(
        Paragraph("2. Hold invoicing pending District clarification", body_style)
    )
    story.append(
        Paragraph(
            "3. District should issue amendment to either lease or management agreement",
            body_style,
        )
    )
    story.append(Spacer(1, 0.1 * inch))
    story.append(
        Paragraph(
            "This affects not just this repair but ongoing maintenance protocol.",
            body_style,
        )
    )
    story.append(Spacer(1, 0.05 * inch))
    story.append(
        Paragraph(
            "David Chen, Legal Counsel<br/>Coastal Property Services LLC", body_style
        )
    )

    doc.build(story)
    print(f"Created: {filename}")


def create_lease_excerpt():
    """Create Lease Agreement Excerpt (Page 4 only)"""
    filename = "Marios_Marina_Lease_Agreement_Excerpt_Section6.pdf"
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        topMargin=1 * inch,
        bottomMargin=1 * inch,
        leftMargin=1 * inch,
        rightMargin=1 * inch,
    )

    styles = getSampleStyleSheet()

    heading_style = ParagraphStyle(
        "CustomHeading",
        parent=styles["Heading2"],
        fontSize=12,
        textColor="black",
        spaceAfter=12,
        spaceBefore=12,
        fontName="Helvetica-Bold",
    )

    body_style = ParagraphStyle(
        "CustomBody",
        parent=styles["BodyText"],
        fontSize=10,
        textColor="black",
        spaceAfter=6,
        alignment=TA_JUSTIFY,
        leading=14,
    )

    story = []

    story.append(Paragraph("LEASE AGREEMENT - Page 4", heading_style))
    story.append(Spacer(1, 0.3 * inch))

    story.append(
        Paragraph("SECTION 6: LESSEE'S IMPROVEMENTS AND OBLIGATIONS", heading_style)
    )
    story.append(Spacer(1, 0.1 * inch))

    story.append(
        Paragraph("(a) Lessee shall, at its sole cost and expense:", body_style)
    )
    story.append(Spacer(1, 0.1 * inch))

    story.append(
        Paragraph(
            "1. Maintain liability insurance as specified in Section 14", body_style
        )
    )
    story.append(Spacer(1, 0.05 * inch))
    story.append(Paragraph("2. Pay all utilities for the Premises", body_style))
    story.append(Spacer(1, 0.05 * inch))
    story.append(
        Paragraph("3. Comply with all applicable laws and regulations", body_style)
    )
    story.append(Spacer(1, 0.05 * inch))
    story.append(
        Paragraph(
            "4. <b>Perform all maintenance and repair of all improvements, structures, and fixtures constructed, installed, or placed on the Premises by Lessee, including but not limited to buildings, docks, utilities, HVAC systems, and landscaping</b>",
            body_style,
        )
    )
    story.append(Spacer(1, 0.05 * inch))
    story.append(
        Paragraph("5. Maintain the Premises in good condition and repair", body_style)
    )

    doc.build(story)
    print(f"Created: {filename}")


def main():
    print("Generating synthetic PDF documents...")
    print("-" * 50)

    create_property_management_agreement()
    create_email_correspondence()
    create_lease_excerpt()

    print("-" * 50)
    print("All documents generated successfully!")
    print("\nGenerated files:")
    print("1. Shelter_Cove_District_Property_Management_Agreement_2024.pdf (15 pages)")
    print("2. Email_Thread_HVAC_Maintenance_Oct2024.pdf")
    print("3. Marios_Marina_Lease_Agreement_Excerpt_Section6.pdf")


if __name__ == "__main__":
    main()
