import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from datetime import datetime


def create_offer_letter():
    """Create employment offer letter"""
    filename = "Mobility_Authority_Offer_Letter_Martinez_2022.pdf"
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        topMargin=1 * inch,
        bottomMargin=1 * inch,
        leftMargin=1 * inch,
        rightMargin=1 * inch,
    )

    styles = getSampleStyleSheet()

    header_style = ParagraphStyle(
        "Header",
        parent=styles["Normal"],
        fontSize=10,
        textColor="black",
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
        spaceAfter=20,
    )

    body_style = ParagraphStyle(
        "CustomBody",
        parent=styles["BodyText"],
        fontSize=11,
        textColor="black",
        spaceAfter=12,
        leading=16,
    )

    signature_style = ParagraphStyle(
        "Signature",
        parent=styles["Normal"],
        fontSize=11,
        textColor="black",
        spaceAfter=6,
    )

    story = []

    # Letterhead
    story.append(Paragraph("CENTRAL TEXAS MOBILITY AUTHORITY", header_style))
    story.append(Paragraph("3300 North IH-35, Suite 300", body_style))
    story.append(Paragraph("Austin, Texas 78705", body_style))
    story.append(Spacer(1, 0.3 * inch))

    # Date and address
    story.append(Paragraph("March 15, 2022", body_style))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("Jane Martinez", body_style))
    story.append(Paragraph("456 Oak Street", body_style))
    story.append(Paragraph("Austin, TX 78701", body_style))
    story.append(Spacer(1, 0.2 * inch))

    # Letter body
    story.append(Paragraph("Dear Ms. Martinez,", body_style))
    story.append(Spacer(1, 0.1 * inch))

    story.append(
        Paragraph(
            "We are pleased to offer you the position of <b>Chief Operating Officer</b> with the Central Texas Mobility Authority, reporting directly to the Executive Director.",
            body_style,
        )
    )

    story.append(Paragraph("<b>Position Details:</b>", body_style))
    story.append(Paragraph("• <b>Start Date:</b> April 18, 2022", body_style))
    story.append(Paragraph("• <b>Base Salary:</b> $185,000 annually", body_style))
    story.append(
        Paragraph(
            "• <b>Benefits:</b> Comprehensive health insurance, 401(k) with employer matching, 3 weeks paid time off",
            body_style,
        )
    )
    story.append(Paragraph("• <b>Status:</b> Full-time, exempt position", body_style))

    story.append(Spacer(1, 0.1 * inch))
    story.append(
        Paragraph(
            "This offer is contingent upon successful completion of a background check. Please sign and return this letter by March 22, 2022 to confirm your acceptance.",
            body_style,
        )
    )

    story.append(Spacer(1, 0.1 * inch))
    story.append(
        Paragraph(
            "We look forward to welcoming you to our leadership team!",
            body_style,
        )
    )

    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("Sincerely,", signature_style))
    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph("Robert Chen", signature_style))
    story.append(Paragraph("Executive Director", signature_style))
    story.append(Paragraph("Central Texas Mobility Authority", signature_style))

    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph("_" * 50, body_style))
    story.append(
        Paragraph(
            "I accept the above terms of employment:",
            body_style,
        )
    )
    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph("Signature: _________________________", body_style))
    story.append(Paragraph("Date: March 18, 2022", body_style))

    doc.build(story)
    print(f"Created: {filename}")


def create_performance_review_1():
    """Create first performance review (positive)"""
    filename = "Performance_Review_Martinez_Oct2022.pdf"
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

    story.append(Paragraph("EMPLOYEE PERFORMANCE REVIEW", title_style))
    story.append(Spacer(1, 0.2 * inch))

    # Employee info
    story.append(Paragraph("<b>Employee:</b> Jane Martinez", body_style))
    story.append(Paragraph("<b>Position:</b> Chief Operating Officer", body_style))
    story.append(
        Paragraph(
            "<b>Review Period:</b> April 18, 2022 - October 18, 2022",
            body_style,
        )
    )
    story.append(Paragraph("<b>Review Date:</b> October 25, 2022", body_style))
    story.append(
        Paragraph("<b>Reviewer:</b> Robert Chen, Executive Director", body_style)
    )
    story.append(Spacer(1, 0.2 * inch))

    # Rating
    story.append(
        Paragraph(
            "<b>OVERALL RATING: EXCEEDS EXPECTATIONS (4/5)</b>",
            heading_style,
        )
    )
    story.append(Spacer(1, 0.1 * inch))

    # Strengths
    story.append(Paragraph("STRENGTHS:", heading_style))
    story.append(
        Paragraph(
            "• Successfully restructured the operations division, improving efficiency by 15%",
            body_style,
        )
    )
    story.append(
        Paragraph(
            "• Reduced operational costs by 12% while maintaining service quality",
            body_style,
        )
    )
    story.append(
        Paragraph(
            "• Established strong relationships with key stakeholders and contractors",
            body_style,
        )
    )
    story.append(
        Paragraph(
            "• Implemented new safety protocols that resulted in zero workplace incidents",
            body_style,
        )
    )
    story.append(
        Paragraph(
            "• Excellent crisis management during August construction delays",
            body_style,
        )
    )
    story.append(Spacer(1, 0.1 * inch))

    # Areas for development
    story.append(Paragraph("AREAS FOR DEVELOPMENT:", heading_style))
    story.append(
        Paragraph(
            "• Continue building relationships with Board members",
            body_style,
        )
    )
    story.append(
        Paragraph(
            "• Enhance public speaking confidence for board presentations",
            body_style,
        )
    )
    story.append(Spacer(1, 0.1 * inch))

    # Comments
    story.append(Paragraph("REVIEWER COMMENTS:", heading_style))
    story.append(
        Paragraph(
            "Jane has been an exceptional addition to our leadership team. Her operational expertise and strategic thinking have already made a significant positive impact on the Authority. She demonstrates strong leadership qualities and has earned the respect of her team and peers. I look forward to her continued contributions.",
            body_style,
        )
    )
    story.append(Spacer(1, 0.3 * inch))

    # Signatures
    story.append(Paragraph("_" * 50, body_style))
    story.append(
        Paragraph("Employee Signature: _______________  Date: 10/25/22", body_style)
    )
    story.append(Spacer(1, 0.1 * inch))
    story.append(
        Paragraph("Supervisor Signature: _______________  Date: 10/25/22", body_style)
    )

    doc.build(story)
    print(f"Created: {filename}")


def create_performance_review_2():
    """Create second performance review (concerns)"""
    filename = "Performance_Review_Martinez_May2023.pdf"
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

    story.append(Paragraph("EMPLOYEE PERFORMANCE REVIEW", title_style))
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("<b>Employee:</b> Jane Martinez", body_style))
    story.append(Paragraph("<b>Position:</b> Chief Operating Officer", body_style))
    story.append(
        Paragraph(
            "<b>Review Period:</b> October 18, 2022 - April 18, 2023",
            body_style,
        )
    )
    story.append(Paragraph("<b>Review Date:</b> May 2, 2023", body_style))
    story.append(
        Paragraph("<b>Reviewer:</b> Robert Chen, Executive Director", body_style)
    )
    story.append(Spacer(1, 0.2 * inch))

    story.append(
        Paragraph("<b>OVERALL RATING: MEETS EXPECTATIONS (3/5)</b>", heading_style)
    )
    story.append(Spacer(1, 0.1 * inch))

    story.append(Paragraph("PERFORMANCE CONCERNS:", heading_style))
    story.append(
        Paragraph(
            "• Missed Q1 2023 budget submission deadline by 2 weeks, creating board meeting complications",
            body_style,
        )
    )
    story.append(
        Paragraph(
            "• Communication gaps with finance team noted by CFO",
            body_style,
        )
    )
    story.append(
        Paragraph(
            "• Board members expressed concerns about project timeline delays on toll lane expansion",
            body_style,
        )
    )
    story.append(
        Paragraph(
            "• Two instances of missing scheduled meetings without advance notice",
            body_style,
        )
    )
    story.append(Spacer(1, 0.1 * inch))

    story.append(Paragraph("POSITIVE NOTES:", heading_style))
    story.append(Paragraph("• Vendor relationships remain strong", body_style))
    story.append(Paragraph("• Safety record continues to be excellent", body_style))
    story.append(Paragraph("• Team morale in operations remains positive", body_style))
    story.append(Spacer(1, 0.1 * inch))

    story.append(Paragraph("ACTION PLAN:", heading_style))
    story.append(
        Paragraph(
            "Monthly one-on-one check-ins implemented starting June 2023 to address communication and deadline management. Employee is expected to demonstrate improvement in organizational and communication skills over the next review period.",
            body_style,
        )
    )
    story.append(Spacer(1, 0.3 * inch))

    story.append(Paragraph("_" * 50, body_style))
    story.append(
        Paragraph("Employee Signature: _______________  Date: 5/2/23", body_style)
    )
    story.append(Spacer(1, 0.1 * inch))
    story.append(
        Paragraph("Supervisor Signature: _______________  Date: 5/2/23", body_style)
    )

    doc.build(story)
    print(f"Created: {filename}")


def create_written_warning():
    """Create formal written warning"""
    filename = "Written_Warning_Martinez_Aug2023.pdf"
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
        spaceAfter=10,
        leading=14,
    )

    story = []

    story.append(Paragraph("CONFIDENTIAL MEMORANDUM", title_style))
    story.append(Spacer(1, 0.3 * inch))

    story.append(
        Paragraph("<b>TO:</b> Jane Martinez, Chief Operating Officer", body_style)
    )
    story.append(Paragraph("<b>FROM:</b> Robert Chen, Executive Director", body_style))
    story.append(Paragraph("<b>DATE:</b> August 14, 2023", body_style))
    story.append(Paragraph("<b>RE:</b> Performance Improvement Plan", body_style))
    story.append(Spacer(1, 0.2 * inch))

    story.append(
        Paragraph(
            "This memorandum serves as formal notice of serious performance concerns and outlines a mandatory Performance Improvement Plan (PIP).",
            body_style,
        )
    )
    story.append(Spacer(1, 0.1 * inch))

    story.append(Paragraph("SPECIFIC PERFORMANCE ISSUES:", heading_style))
    story.append(
        Paragraph(
            "<b>1. July 2023 Board Meeting:</b> Arrived 20 minutes late to Board of Directors meeting without prior notice or explanation, causing agenda delays and board member frustration.",
            body_style,
        )
    )
    story.append(
        Paragraph(
            "<b>2. Budget Variance:</b> Q2 2023 operational costs exceeded approved budget by 18% ($127,000), with insufficient documentation or justification provided to finance team.",
            body_style,
        )
    )
    story.append(
        Paragraph(
            "<b>3. Staff Complaints:</b> Three separate team members (names withheld) submitted written complaints regarding communication breakdowns and unclear direction from COO office.",
            body_style,
        )
    )
    story.append(Spacer(1, 0.1 * inch))

    story.append(Paragraph("REQUIRED ACTIONS (30-DAY PERIOD):", heading_style))
    story.append(
        Paragraph(
            "• Submit weekly written status reports every Friday by 5:00 PM",
            body_style,
        )
    )
    story.append(
        Paragraph(
            "• Attend all scheduled meetings punctually; provide 24-hour notice for any unavoidable conflicts",
            body_style,
        )
    )
    story.append(
        Paragraph(
            "• Complete management and communication skills training by September 15, 2023",
            body_style,
        )
    )
    story.append(
        Paragraph(
            "• Meet weekly with Executive Director for progress review",
            body_style,
        )
    )
    story.append(
        Paragraph(
            "• Develop and submit corrective budget plan by August 25, 2023",
            body_style,
        )
    )
    story.append(Spacer(1, 0.1 * inch))

    story.append(
        Paragraph(
            "<b>Please understand that failure to demonstrate immediate and sustained improvement may result in further disciplinary action up to and including termination of employment.</b>",
            body_style,
        )
    )
    story.append(Spacer(1, 0.1 * inch))

    story.append(
        Paragraph(
            "We will meet on September 15, 2023 to review your progress under this plan.",
            body_style,
        )
    )
    story.append(Spacer(1, 0.3 * inch))

    story.append(Paragraph("_" * 50, body_style))
    story.append(
        Paragraph(
            "Employee Acknowledgment (receipt only, not agreement): _______________  Date: ______",
            body_style,
        )
    )

    doc.build(story)
    print(f"Created: {filename}")


def create_termination_letter():
    """Create termination letter"""
    filename = "Termination_Letter_Martinez_Sept2023.pdf"
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        topMargin=1 * inch,
        bottomMargin=1 * inch,
        leftMargin=1 * inch,
        rightMargin=1 * inch,
    )

    styles = getSampleStyleSheet()

    header_style = ParagraphStyle(
        "Header",
        parent=styles["Normal"],
        fontSize=10,
        textColor="black",
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
        spaceAfter=20,
    )

    title_style = ParagraphStyle(
        "Title",
        parent=styles["Heading1"],
        fontSize=12,
        textColor="black",
        spaceAfter=20,
        fontName="Helvetica-Bold",
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontSize=11,
        textColor="black",
        spaceAfter=12,
        leading=16,
    )

    story = []

    story.append(Paragraph("CONFIDENTIAL", title_style))
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("CENTRAL TEXAS MOBILITY AUTHORITY", header_style))
    story.append(Paragraph("3300 North IH-35, Suite 300", body_style))
    story.append(Paragraph("Austin, Texas 78705", body_style))
    story.append(Spacer(1, 0.3 * inch))

    story.append(Paragraph("September 28, 2023", body_style))
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("Jane Martinez", body_style))
    story.append(Paragraph("456 Oak Street", body_style))
    story.append(Paragraph("Austin, TX 78701", body_style))
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("Dear Ms. Martinez,", body_style))
    story.append(Spacer(1, 0.1 * inch))

    story.append(
        Paragraph(
            "This letter confirms our conversation earlier today regarding the termination of your employment as Chief Operating Officer with the Central Texas Mobility Authority, <b>effective immediately (September 28, 2023)</b>.",
            body_style,
        )
    )

    story.append(
        Paragraph(
            "<b>Reason for Termination:</b> Performance-based termination due to failure to meet performance objectives outlined in the Performance Improvement Plan dated August 14, 2023.",
            body_style,
        )
    )

    story.append(Paragraph("<b>Final Compensation:</b>", body_style))
    story.append(Paragraph("• Salary through September 28, 2023", body_style))
    story.append(Paragraph("• Accrued paid time off: 8 days ($5,692.31)", body_style))
    story.append(
        Paragraph("• Final paycheck to be issued: October 6, 2023", body_style)
    )
    story.append(Spacer(1, 0.1 * inch))

    story.append(
        Paragraph(
            "<b>Benefits:</b> Your health insurance coverage will continue through October 31, 2023. COBRA continuation information is enclosed.",
            body_style,
        )
    )

    story.append(
        Paragraph(
            "<b>Return of Property:</b> Please return all Authority property including laptop, access cards, keys, and files by October 2, 2023 to Human Resources.",
            body_style,
        )
    )

    story.append(Spacer(1, 0.1 * inch))
    story.append(
        Paragraph(
            "If you have questions regarding final compensation or benefits, please contact HR at (512) 555-0100.",
            body_style,
        )
    )

    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("Sincerely,", body_style))
    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph("Robert Chen", body_style))
    story.append(Paragraph("Executive Director", body_style))
    story.append(Paragraph("Central Texas Mobility Authority", body_style))

    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("cc: Human Resources File", body_style))

    doc.build(story)
    print(f"Created: {filename}")


def main():
    print("Generating Employment Timeline Demo Documents...")
    print("-" * 60)

    create_offer_letter()
    create_performance_review_1()
    create_performance_review_2()
    create_written_warning()
    create_termination_letter()

    print("-" * 60)
    print("All documents generated successfully!")
    print("\nGenerated files:")
    print("1. Mobility_Authority_Offer_Letter_Martinez_2022.pdf")
    print("2. Performance_Review_Martinez_Oct2022.pdf (Exceeds Expectations)")
    print("3. Performance_Review_Martinez_May2023.pdf (Meets Expectations)")
    print("4. Written_Warning_Martinez_Aug2023.pdf (PIP)")
    print("5. Termination_Letter_Martinez_Sept2023.pdf")
    print("\n" + "=" * 60)
    print("KEY TIMELINE:")
    print("  3/15/22  - Offer letter")
    print("  4/18/22  - Start date")
    print("  10/25/22 - First review: EXCEEDS (4/5)")
    print("  5/2/23   - Second review: MEETS (3/5) - performance concerns")
    print("  8/14/23  - Written warning & 30-day PIP")
    print("  9/28/23  - TERMINATED")
    print("  Total employment: 17 months")
    print("=" * 60)


if __name__ == "__main__":
    main()
