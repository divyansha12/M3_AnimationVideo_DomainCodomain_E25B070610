"""Builds Storyboard.pdf (6-scene storyboard). Run:  python make_storyboard.py"""
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from config import STUDENT_NAME, STUDENT_ID

OUT = "../Storyboard.pdf"
ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Title"], fontSize=20, spaceAfter=6)
H2 = ParagraphStyle("H2", parent=ss["Heading2"], fontSize=13, spaceBefore=8, spaceAfter=4)
B = ParagraphStyle("B", parent=ss["BodyText"], fontSize=9, leading=11.5)
S = ParagraphStyle("S", parent=B, fontSize=8, leading=9.8)
HD = ParagraphStyle("HD", parent=S, textColor=colors.white, fontName="Helvetica-Bold")

def P(t, st=S): return Paragraph(t, st)

doc = SimpleDocTemplate(OUT, pagesize=landscape(A4), leftMargin=14*mm, rightMargin=14*mm,
                        topMargin=9*mm, bottomMargin=9*mm,
                        title="M3 Animation Video - Storyboard", author=STUDENT_NAME)
st = []
st.append(P("M3 Animation Video: Storyboard", H1))
st.append(P(f"<b>Concept:</b> Domain, Codomain and Range (through mapping diagrams) &nbsp;|&nbsp; "
            f"<b>Student:</b> {STUDENT_NAME} ({STUDENT_ID}) &nbsp;|&nbsp; <b>Tool:</b> Manim Community Edition (Python) "
            f"&nbsp;|&nbsp; <b>Length:</b> about 5:05, 16:9, 1080p", B))
st.append(P("<b>Learning objective:</b> By the end of this video, the viewer will be able to identify the domain, "
            "codomain and range of a function from a mapping diagram, a formula in one variable and a formula in two "
            "variables, and explain how the three differ.", B))
st.append(P("<b>Colour code used in every scene:</b> domain = blue, codomain = green, range = orange, "
            "errors / not allowed = red.", B))
st.append(Spacer(1, 4))

rows = [[P(h, HD) for h in ["Scene", "Time", "Purpose", "Visual plan", "Narration (summary)", "Maths shown"]]]
data = [
 ("Opening frame", "0:00-0:07", "Title, concept, student name and ID.",
  "Title card with course name, student name and ID.", "Short introduction.", "None."),
 ("1. Hook", "0:07-0:40", "Spark curiosity with a real-life mapping.",
  "A vending machine drawn as two ovals: buttons A1, A2, A3 on the left, snacks Chips, Biscuit, Juice, Candy on the "
  "right. Arrows are drawn one at a time: A1 to Chips, A2 to Juice, A3 to Juice. Captions pose four questions: two "
  "buttons, same snack (allowed); a snack nobody gets (allowed); a button giving nothing or two snacks (not allowed).",
  "Every button gives exactly one snack. Buttons are the inputs, the shelf is where outputs may land.",
  "Informal idea of a function; no formulas yet."),
 ("2. Concept introduction", "0:40-1:08", "Define the concept and the learning goal.",
  "Text builds on screen: definition of a function f: A to B, then three coloured rows: Domain, Codomain, Range. "
  "A boxed learning objective appears at the bottom.",
  "Reads out the three definitions and the learning objective.",
  "f: A to B; Domain = A; Codomain = B; Range = f(A), a subset of B."),
 ("3. Visual intuition", "1:08-2:08", "Build geometric / visual understanding before algebra.",
  "Mapping diagram with A = {1,2,3}, B = {a,b,c,d}, arrows 1 to a, 2 to b, 3 to b. Left oval fills blue (domain), "
  "right oval fills green (codomain), then only a and b turn orange (range) while c and d fade to grey. Second part: "
  "two small diagrams showing what is NOT a function (one input with two arrows; one input with no arrow).",
  "Explains each highlight, then the rule: every input has exactly one arrow; outputs may have zero, one or many.",
  "f(1) = a, f(2) = b, f(3) = b; range = {a, b}."),
 ("4. Worked examples", "2:08-4:02", "Show why and how the maths works with three carefully chosen examples.",
  "Example 1: graph of y = x<super>2</super> with the x-axis (domain) in blue, the whole y-axis (codomain) in green and "
  "the part from 0 upward (range) in orange; red dot at -2 shows a codomain element that is never hit. "
  "Example 2: graph of y = sqrt(x - 2) starting at x = 2, with domain and range highlighted and a check at x = 6. "
  "Example 3: the xy-plane with the unit disk shaded (domain), test points (0,0), (0.6,0.8), (1,1), and a number line "
  "showing the range [0,1].",
  "Step by step: what is allowed as input, what is declared as codomain, what actually comes out.",
  "Ex 1: f(x) = x<super>2</super>, domain R, range [0, inf). Ex 2: f(x) = sqrt(x - 2), domain [2, inf), range [0, inf). "
  "Ex 3: f(x,y) = sqrt(1 - x<super>2</super> - y<super>2</super>), domain x<super>2</super> + y<super>2</super> <= 1, range [0, 1]."),
 ("5. Interpretation", "4:02-4:38", "Connect the algebra back to the visual meaning.",
  "Number line for f(x) = x<super>2</super>: green codomain R, orange range [0, inf). Then the codomain shrinks to "
  "[0, inf) and matches the range. Finally a three-row comparison and the rule Range is a subset of Codomain.",
  "Codomain is a choice, range is a result. Same rule, different codomain. Range equals codomain only when every "
  "element is hit.",
  "Range is a subset of Codomain."),
 ("6. Summary and credits", "4:38-5:05", "Reinforce takeaways and cite sources.",
  "Three takeaways on screen, then the closing frame: author, Manim credit, voice-over, music credit (or none) and "
  "AI-tool disclosure.", "Recaps the three takeaways; mentions tools used.", "Recap only."),
]
for r in data:
    rows.append([P(f"<b>{r[0]}</b>"), P(r[1]), P(r[2]), P(r[3]), P(r[4]), P(r[5])])
t = Table(rows, colWidths=[24*mm, 18*mm, 34*mm, 85*mm, 50*mm, 46*mm], repeatRows=1)
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f3a5f")),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f5fa")]),
    ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
]))
st.append(t)
st.append(PageBreak())

st.append(P("Verification and production notes", H1))
st.append(P("Mathematics checked", H2))
for line in [
    "Every example was recalculated by hand and by a Python script (<font face='Courier'>math_check.py</font>, included in the repository).",
    "Example 1: x<super>2</super> &gt;= 0 for all real x; every y &gt;= 0 is reached by x = sqrt(y); -2 is not reached because x<super>2</super> = -2 has no real solution.",
    "Example 2: x - 2 &gt;= 0 gives x &gt;= 2; for any y &gt;= 0 the input x = y<super>2</super> + 2 gives f(x) = y, so the range is [0, inf). Check: f(6) = sqrt(4) = 2.",
    "Example 3: 1 - x<super>2</super> - y<super>2</super> &gt;= 0 gives the closed unit disk; f(0,0) = 1; f(0.6,0.8) = sqrt(1 - 0.36 - 0.64) = 0; (1,1) gives sqrt(-1), not real, so it is outside the domain; the range is [0, 1].",
]:
    st.append(P("&bull; " + line, B))
st.append(P("Production plan", H2))
for line in [
    "Animation: Manim Community Edition scripts in the code folder (<font face='Courier'>domain_codomain.py</font>); no LaTeX needed, all labels use plain text.",
    "Narration: recorded by the student while watching the rendered video. No background music is planned; if added, it will be credited and kept low.",
    "Style rules followed: clean background, one idea per step, consistent colours, all sets and axes labelled, one step animated at a time.",
    "Disclosure: Claude (Anthropic) was used to help draft this storyboard, the narration script and the Manim code. The student checked the mathematics and is able to explain every step and line of code.",
]:
    st.append(P("&bull; " + line, B))
doc.build(st)
print("wrote", OUT)
