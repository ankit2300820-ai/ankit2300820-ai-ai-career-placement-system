"""Company eligibility + compatibility (criteria in data/companies.csv are illustrative, not official)."""
import pandas as pd
from . import db

def check(profile: dict, skills, readiness_score: float) -> pd.DataFrame:
    comp, have, rows = db.query("SELECT * FROM companies"), {s.lower() for s in skills}, []
    for _, c in comp.iterrows():
        fails = []
        if profile["cgpa"] < c.min_cgpa: fails.append(f"CGPA below {c.min_cgpa}")
        if profile["backlogs"] > c.max_backlogs: fails.append(f"Backlogs above {c.max_backlogs}")
        if profile["tenth_pct"] < c.min_10th: fails.append(f"10th below {c.min_10th}%")
        if profile["twelfth_pct"] < c.min_12th: fails.append(f"12th below {c.min_12th}%")
        req = [s for s in c.required_skills.split(";") if s]
        miss = [s for s in req if s.lower() not in have]
        skill_match = 1 - len(miss) / len(req) if req else 1
        compat = 100 * (0.55 * skill_match + 0.25 * min(1, profile["cgpa"] / (c.min_cgpa + 1.5)) + 0.20 * readiness_score / 100)
        rows.append(dict(Company=c["name"], Tier=c.tier, Role=c.roles, Package_LPA=c.avg_package_lpa,
                         Eligible="Yes" if not fails else "No", Compatibility=round(compat, 1),
                         Skill_Match_pct=round(skill_match * 100), Missing_Skills=", ".join(miss) or "-",
                         Why_Not_Eligible="; ".join(fails) or "-"))
    return pd.DataFrame(rows).sort_values(["Eligible", "Compatibility"], ascending=[False, False]).reset_index(drop=True)
