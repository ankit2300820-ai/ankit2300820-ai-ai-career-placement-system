"""Downloadable PDF student report (fpdf2)."""
from datetime import date
from fpdf import FPDF

def _t(x):
    return str(x).encode("latin-1", "replace").decode("latin-1")

def build_pdf(student, role, ready, parts, band, prob, roles_df, comp_df, road_df, weeks) -> bytes:
    pdf = FPDF(); pdf.set_auto_page_break(True, 15); pdf.add_page()
    def h(txt):
        pdf.ln(3); pdf.set_font("Helvetica", "B", 13); pdf.set_text_color(79, 70, 229); pdf.cell(0, 8, _t(txt), new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(0, 0, 0); pdf.set_font("Helvetica", "", 10)
    def line(txt):
        pdf.multi_cell(0, 6, _t(txt), new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "B", 18); pdf.cell(0, 10, "AI Career & Placement Report", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10); line(f"Generated on {date.today():%d %b %Y}")
    h("Student Profile")
    line(f"Name: {student['name']}   Email: {student['email']}   Branch: {student['branch']}")
    line(f"CGPA: {student['cgpa']}  10th: {student['tenth_pct']}%  12th: {student['twelfth_pct']}%  Backlogs: {student['backlogs']}")
    line(f"Internships: {student['internships']}  Projects: {student['projects']}  Certifications: {student['certifications']}  Target role: {role}")
    h("Placement Readiness")
    line(f"Readiness score: {ready}/100 ({band})")
    for k, v in parts.items(): line(f"  - {k}: {v}")
    line(f"ML placement probability: {prob*100:.1f}% (model trained on SYNTHETIC data - indicative only)")
    h("Top Career Matches")
    for _, r in roles_df.head(3).iterrows(): line(f"  - {r.role}: {r.match_pct}% match | missing: {r.missing or 'none'}")
    h("Best Company Matches (eligible)")
    el = comp_df[comp_df.Eligible == "Yes"].head(5)
    if el.empty: line("No eligible companies with current profile.")
    for _, r in el.iterrows(): line(f"  - {r.Company} ({r.Tier}) - compatibility {r.Compatibility}%, ~{r.Package_LPA} LPA")
    h(f"Learning Roadmap ({weeks} weeks)")
    if road_df.empty: line("No skill gaps for the target role. Focus on interview practice.")
    for _, r in road_df.iterrows(): line(f"  - {r.Schedule}: {r.Skill} [{r.Priority}] - {r.Resource}")
    return bytes(pdf.output())
