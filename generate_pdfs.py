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


def create_deposition_mitchell():
    """Create James Mitchell deposition transcript"""
    filename = "Deposition_James_Mitchell_2023-03-15.pdf"

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
        textColor=colors.HexColor("#1a1a1a"),
        alignment=TA_CENTER,
        spaceAfter=12,
        fontName="Helvetica-Bold",
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontSize=10,
        textColor=colors.HexColor("#2c3e50"),
        spaceAfter=4,
        leading=12,
        fontName="Courier",
    )

    highlight_red = ParagraphStyle(
        "HighlightRed",
        parent=body_style,
        textColor=colors.HexColor("#c0392b"),
        fontName="Courier-Bold",
    )

    story = []

    # Header
    story.append(Paragraph("James Robert Mitchell", title_style))
    story.append(Paragraph("March 15, 2023", title_style))
    story.append(Paragraph("McGown, Lisa Ann Vs. Roberts, Sara Brooke", title_style))
    story.append(Spacer(1, 0.3 * inch))

    # Transcript content
    transcript_lines = [
        "1                  P R O C E E D I N G S",
        "2                       - - - - -",
        "3               VIDEOGRAPHER:  Good morning.  Today's",
        "4   date is March 15th, 2023.  The time on camera is",
        "5   approximately 10:12 a.m.  This will be the beginning",
        "6   of the video deposition of James Robert Mitchell.",
        "7",
        "8               MR. HALL:  Rick Hall, representing",
        "9   plaintiff Lisa McGown.",
        "10",
        "11              MR. NEUBAUER:  Michael Neubauer for",
        "12  defendant Sara Roberts.",
        "13",
        "14                 JAMES ROBERT MITCHELL,",
        "15  being first duly sworn, testified as follows:",
        "16",
        "17                      EXAMINATION",
        "18  BY MR. HALL:",
        "19         Q.   Good morning, Mr. Mitchell. Can you",
        "20  state your full name for the record?",
        "21         A.   James Robert Mitchell.",
        "22         Q.   And where do you live, sir?",
    ]

    for line in transcript_lines:
        story.append(Paragraph(line, body_style))

    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("...", body_style))
    story.append(Spacer(1, 0.2 * inch))

    # Key testimony section
    key_testimony = [
        "45         Q.   Now, Mr. Mitchell, I want to direct",
        "46  your attention to the afternoon of January 12th,",
        "47  2023. Do you recall that date?",
        "48         A.   Yes, I do. That was the day of the",
        "49  accident.",
        "50         Q.   Can you describe the weather conditions",
        "51  that afternoon?",
        "52         A.   It was overcast, kind of gloomy. There",
        "53  was a light drizzle, not heavy rain, but enough to",
        "54  make the roads wet.",
    ]

    for line in key_testimony:
        story.append(Paragraph(line, body_style))

    # Highlighted visibility section
    visibility_lines = [
        "55         Q.   What about visibility? Could you see",
        "56  clearly?",
        "57         A.   Visibility was poor. The drizzle and",
        "58  fog made it hard to see more than maybe 50 to 75",
        "59  feet ahead clearly. Everything beyond that was",
        "60  hazy.",
    ]

    for line in visibility_lines:
        story.append(Paragraph(line, highlight_red))

    more_testimony = [
        "61         Q.   Where were you positioned when you",
        "62  witnessed the collision?",
        "63         A.   I was standing at the corner of",
        "64  Elm Street and Park Avenue, waiting to cross.",
        "65         Q.   And what did you observe?",
    ]

    for line in more_testimony:
        story.append(Paragraph(line, body_style))

    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("...", body_style))
    story.append(Spacer(1, 0.2 * inch))

    # Speed testimony
    speed_testimony = [
        "78         Q.   Can you estimate the speed at which",
        "79  the defendant's vehicle was traveling?",
    ]

    for line in speed_testimony:
        story.append(Paragraph(line, body_style))

    speed_estimate = [
        "80         A.   I'd say she was going about 35 to 40",
        "81  miles per hour. The speed limit there is 25, so",
        "82  she was definitely speeding.",
    ]

    for line in speed_estimate:
        story.append(Paragraph(line, highlight_red))

    remaining_lines = [
        "83         Q.   How can you be certain about that",
        "84  speed estimate?",
        "85         A.   I've lived in that neighborhood for",
        "86  15 years. You get a sense of how fast cars should",
        "87  be going versus how fast they actually are. Her",
        "88  car came through that intersection faster than",
        "89  normal.",
        "90         Q.   Did you see the defendant's brake",
        "91  lights?",
        "92         A.   Not until it was too late. She",
        "93  slammed on the brakes right before impact, but",
        "94  there wasn't enough distance to stop.",
        "95         Q.   What happened immediately after the",
        "96  collision?",
        "97         A.   The plaintiff's car spun about 90",
        "98  degrees. I immediately called 911.",
    ]

    for line in remaining_lines:
        story.append(Paragraph(line, body_style))

    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("...", body_style))
    story.append(Spacer(1, 0.2 * inch))

    conclusion = [
        "134        Q.   Going back to visibility - you said",
        "135 it was poor. Could the defendant have seen the",
        "136 plaintiff's vehicle in time to stop?",
        "137        A.   If she'd been going the speed limit",
        "138 and paying attention, yes. But with the speed she",
        "139 was traveling and the conditions, she didn't have",
        "140 enough reaction time.",
        "141        Q.   Thank you, Mr. Mitchell.",
        "142               MR. HALL:  No further questions.",
    ]

    for line in conclusion:
        story.append(Paragraph(line, body_style))

    doc.build(story)
    print(f"✓ Created: {filename}")


def create_deposition_chen():
    """Create Patricia Chen deposition transcript"""
    filename = "Deposition_Patricia_Chen_2023-03-22.pdf"

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
        textColor=colors.HexColor("#1a1a1a"),
        alignment=TA_CENTER,
        spaceAfter=12,
        fontName="Helvetica-Bold",
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontSize=10,
        textColor=colors.HexColor("#2c3e50"),
        spaceAfter=4,
        leading=12,
        fontName="Courier",
    )

    highlight_blue = ParagraphStyle(
        "HighlightBlue",
        parent=body_style,
        textColor=colors.HexColor("#2980b9"),
        fontName="Courier-Bold",
    )

    story = []

    # Header
    story.append(Paragraph("Patricia Lynn Chen", title_style))
    story.append(Paragraph("March 22, 2023", title_style))
    story.append(Paragraph("McGown, Lisa Ann Vs. Roberts, Sara Brooke", title_style))
    story.append(Spacer(1, 0.3 * inch))

    # Opening
    opening = [
        "1                  P R O C E E D I N G S",
        "2                       - - - - -",
        "3               VIDEOGRAPHER:  Good afternoon.  Today's",
        "4   date is March 22nd, 2023.  The time on camera is",
        "5   approximately 2:34 p.m.  This will be the beginning",
        "6   of the video deposition of Patricia Lynn Chen.",
        "7",
        "8               MR. HALL:  Rick Hall for the plaintiff.",
        "9",
        "10              MR. NEUBAUER:  Michael Neubauer,",
        "11  representing defendant Sara Roberts.",
        "12",
        "13                 PATRICIA LYNN CHEN,",
        "14  being first duly sworn, testified as follows:",
        "15",
        "16                      EXAMINATION",
        "17  BY MR. HALL:",
        "18         Q.   Please state your name for the record.",
        "19         A.   Patricia Lynn Chen.",
        "20         Q.   Ms. Chen, you were driving near the",
        "21  scene of the accident on January 12th, correct?",
        "22         A.   Yes, that's correct.",
    ]

    for line in opening:
        story.append(Paragraph(line, body_style))

    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("...", body_style))
    story.append(Spacer(1, 0.2 * inch))

    # Weather testimony
    weather = [
        "56         Q.   Can you describe the weather and road",
        "57  conditions that day?",
        "58         A.   Honestly, it wasn't that bad. There",
        "59  was a little bit of mist in the air, but I could",
        "60  see fine. The roads were slightly damp but not",
        "61  slippery.",
        "62         Q.   What about visibility specifically?",
    ]

    for line in weather:
        story.append(Paragraph(line, body_style))

    # Contradictory visibility testimony
    visibility = [
        "63         A.   Visibility was adequate. I mean, it",
        "64  wasn't a bright sunny day, but I could see other",
        "65  vehicles clearly. I'd say visibility was good for",
        "66  at least 150 to 200 feet.",
    ]

    for line in visibility:
        story.append(Paragraph(line, highlight_blue))

    more_q = [
        "67         Q.   That contradicts another witness who",
        "68  said visibility was only 50 to 75 feet.",
        "69         A.   I can only tell you what I experienced.",
        "70  My headlights were on, and I had no trouble seeing",
        "71  the road ahead or other vehicles.",
        "72         Q.   Where was your vehicle positioned?",
        "73         A.   I was traveling southbound on Park",
        "74  Avenue, about two car lengths behind the defendant's",
        "75  vehicle.",
    ]

    for line in more_q:
        story.append(Paragraph(line, body_style))

    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("...", body_style))
    story.append(Spacer(1, 0.2 * inch))

    # Speed testimony
    speed_q = [
        "89         Q.   How fast was the defendant traveling?",
    ]

    for line in speed_q:
        story.append(Paragraph(line, body_style))

    speed_answer = [
        "90         A.   She was going approximately 25 miles",
        "91  per hour, maybe 27 or 28 at most. She was driving",
        "92  at a reasonable speed for the conditions.",
    ]

    for line in speed_answer:
        story.append(Paragraph(line, highlight_blue))

    speed_followup = [
        "93         Q.   Are you certain about that speed?",
        "94         A.   Yes. I was maintaining the same speed",
        "95  behind her, and I checked my speedometer. I was",
        "96  going 25, and she wasn't pulling away from me.",
        "97         Q.   Another witness estimated her speed at",
        "98  35 to 40 miles per hour.",
        "99         A.   Then that witness is mistaken. I was",
        "100 directly behind her. She wasn't speeding.",
        "101        Q.   What did you observe about the",
        "102 plaintiff's vehicle?",
        "103        A.   The plaintiff pulled out from Elm",
        "104 Street without fully stopping. She didn't yield",
        "105 the right of way.",
        "106        Q.   Did the defendant have time to react?",
        "107        A.   Barely. The plaintiff's vehicle",
        "108 entered the intersection suddenly. Ms. Roberts",
        "109 braked immediately, but there wasn't sufficient",
        "110 time to avoid the collision.",
    ]

    for line in speed_followup:
        story.append(Paragraph(line, body_style))

    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("...", body_style))
    story.append(Spacer(1, 0.2 * inch))

    closing = [
        "145        Q.   In your opinion, could this accident",
        "146 have been prevented?",
        "147        A.   If the plaintiff had come to a",
        "148 complete stop and yielded as required, yes. The",
        "149 defendant was driving properly given the conditions.",
        "150        Q.   Thank you, Ms. Chen.",
        "151               MR. HALL:  Nothing further.",
    ]

    for line in closing:
        story.append(Paragraph(line, body_style))

    doc.build(story)
    print(f"✓ Created: {filename}")


def create_deposition_yamamoto():
    """Create Dr. Yamamoto expert deposition transcript"""
    filename = "Deposition_Dr_Robert_Yamamoto_2023-04-05.pdf"

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
        textColor=colors.HexColor("#1a1a1a"),
        alignment=TA_CENTER,
        spaceAfter=12,
        fontName="Helvetica-Bold",
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontSize=10,
        textColor=colors.HexColor("#2c3e50"),
        spaceAfter=4,
        leading=12,
        fontName="Courier",
    )

    highlight_green = ParagraphStyle(
        "HighlightGreen",
        parent=body_style,
        textColor=colors.HexColor("#27ae60"),
        fontName="Courier-Bold",
    )

    story = []

    # Header
    story.append(Paragraph("Dr. Robert Yamamoto, Ph.D.", title_style))
    story.append(Paragraph("April 5, 2023", title_style))
    story.append(Paragraph("McGown, Lisa Ann Vs. Roberts, Sara Brooke", title_style))
    story.append(Spacer(1, 0.3 * inch))

    # Opening
    opening = [
        "1                  P R O C E E D I N G S",
        "2                       - - - - -",
        "3               VIDEOGRAPHER:  Good morning.  Today's",
        "4   date is April 5th, 2023.  The time on camera is",
        "5   approximately 9:45 a.m.  This will be the deposition",
        "6   of Dr. Robert Yamamoto, accident reconstruction expert.",
        "7",
        "8               MR. NEUBAUER:  Michael Neubauer for",
        "9   defendant Sara Roberts.",
        "10",
        "11              MR. HALL:  Rick Hall, plaintiff's counsel.",
        "12",
        "13                 DR. ROBERT YAMAMOTO,",
        "14  being first duly sworn, testified as follows:",
        "15",
        "16                      EXAMINATION",
        "17  BY MR. NEUBAUER:",
        "18         Q.   Dr. Yamamoto, please state your",
        "19  qualifications.",
        "20         A.   I have a Ph.D. in Mechanical Engineering",
        "21  from MIT. I've been performing accident reconstruction",
        "22  for 22 years and have testified in over 200 cases.",
    ]

    for line in opening:
        story.append(Paragraph(line, body_style))

    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("...", body_style))
    story.append(Spacer(1, 0.2 * inch))

    # Visibility analysis
    vis_q = [
        "67         Q.   Based on your analysis, what were the",
        "68  visibility conditions at the time of the accident?",
    ]

    for line in vis_q:
        story.append(Paragraph(line, body_style))

    vis_answer = [
        "69         A.   According to meteorological data from",
        "70  the National Weather Service, there was light",
        "71  precipitation with fog. Visibility was recorded at",
        "72  approximately 0.25 miles, or roughly 1,300 feet.",
    ]

    for line in vis_answer:
        story.append(Paragraph(line, highlight_green))

    vis_comparison = [
        "73         Q.   How does that compare to witness",
        "74  statements?",
        "75         A.   It's significantly better than what",
        "76  Mr. Mitchell reported - he said 50 to 75 feet,",
        "77  which would be dense fog conditions. The data",
        "78  doesn't support that. Ms. Chen's estimate of 150",
        "79  to 200 feet is more consistent with light fog",
        "80  conditions.",
        "81         Q.   What about the speed of the defendant's",
        "82  vehicle?",
    ]

    for line in vis_comparison:
        story.append(Paragraph(line, body_style))

    # Speed analysis
    speed_analysis = [
        "83         A.   Based on skid mark analysis, impact",
        "84  damage patterns, and vehicle weight, I calculated",
        "85  the defendant's speed at impact to be approximately",
        "86  28 to 32 miles per hour.",
    ]

    for line in speed_analysis:
        story.append(Paragraph(line, highlight_green))

    speed_comparison = [
        "87         Q.   Is that consistent with any witness",
        "88  testimony?",
        "89         A.   Yes, Ms. Chen's testimony that the",
        "90  defendant was traveling at approximately 25 to 27",
        "91  miles per hour prior to braking is consistent with",
        "92  my findings. Mr. Mitchell's estimate of 35 to 40",
        "93  miles per hour is not supported by the physical",
        "94  evidence.",
    ]

    for line in speed_comparison:
        story.append(Paragraph(line, body_style))

    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("...", body_style))
    story.append(Spacer(1, 0.2 * inch))

    conclusion = [
        "112        Q.   In your expert opinion, was the",
        "113 defendant speeding?",
        "114        A.   The speed limit is 25 miles per hour.",
        "115 My analysis shows she was traveling at or slightly",
        "116 above that limit - within a reasonable margin. She",
        "117 was not excessively speeding.",
        "118        Q.   Could the defendant have avoided the",
        "119 collision?",
        "120        A.   Given the plaintiff's sudden entry into",
        "121 the intersection and the defendant's reaction time,",
        "122 no. The defendant braked appropriately. The physical",
        "123 evidence shows she attempted to avoid the collision.",
        "124        Q.   Thank you, Dr. Yamamoto.",
        "125               MR. NEUBAUER:  No further questions.",
    ]

    for line in conclusion:
        story.append(Paragraph(line, body_style))

    doc.build(story)
    print(f"✓ Created: {filename}")


def main():
    print("\n" + "=" * 70)
    print("GENERATING DEPOSITION TRANSCRIPTS")
    print("McGown v. Roberts Case")
    print("=" * 70)
    print("\nCreating depositions with contradictory testimony:")
    print("  🔴 James Mitchell - Witness (poor visibility, high speed)")
    print("  🔵 Patricia Chen - Witness (good visibility, normal speed)")
    print("  🟢 Dr. Yamamoto - Expert (data-based analysis)")
    print("\n" + "-" * 70)

    create_deposition_mitchell()
    create_deposition_chen()
    create_deposition_yamamoto()

    print("-" * 70)
    print("✓ All depositions generated successfully!")
    print("\nGenerated files:")
    print("  • Deposition_James_Mitchell_2023-03-15.pdf")
    print("  • Deposition_Patricia_Chen_2023-03-22.pdf")
    print("  • Deposition_Dr_Robert_Yamamoto_2023-04-05.pdf")

    print("\n" + "=" * 70)
    print("KEY CONTRADICTIONS:")
    print("=" * 70)

    print("\n📋 VISIBILITY CONDITIONS:")
    print("  • Mitchell: 50-75 feet (poor)")
    print("  • Chen: 150-200 feet (adequate)")
    print("  • Yamamoto: ~1,300 feet per weather data (good)")

    print("\n📋 SPEED ESTIMATES:")
    print("  • Mitchell: 35-40 mph (speeding)")
    print("  • Chen: 25-27 mph (at limit)")
    print("  • Yamamoto: 28-32 mph at impact (slightly above)")

    print("\n" + "=" * 70)
    print("Documents ready for collaboration demo!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
