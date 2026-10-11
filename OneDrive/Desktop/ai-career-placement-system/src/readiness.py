"""Rule-based Placement Readiness Score (0-100) with a transparent breakdown."""
from .career import role_match

MAXES = {"Academics": 25, "Skills Match": 30, "Experience": 20, "Coding & Aptitude": 15, "Communication": 10}

def compute(p: dict, skills, role: str):
    cov, _, _ = role_match(skills, role)
    acad = p["cgpa"] / 10 * 20 + (p["tenth_pct"] + p["twelfth_pct"]) / 200 * 5 - 3 * p["backlogs"]
    parts = {
        "Academics": max(0, acad),
        "Skills Match": cov / 100 * 30,
        "Experience": min(p["internships"], 2) / 2 * 10 + min(p["projects"], 4) / 4 * 7 + min(p["certifications"], 3) / 3 * 3,
        "Coding & Aptitude": p["coding_score"] / 100 * 8 + p["aptitude"] / 100 * 7,
        "Communication": p["communication"] / 10 * 10,
    }
    parts = {k: round(min(v, MAXES[k]), 1) for k, v in parts.items()}
    total = round(sum(parts.values()), 1)
    band = "Excellent" if total >= 80 else "Good" if total >= 65 else "Average" if total >= 50 else "Needs Improvement"
    return total, parts, band
