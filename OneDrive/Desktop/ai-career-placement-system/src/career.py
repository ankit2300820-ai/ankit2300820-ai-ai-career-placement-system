"""Career / job-role recommendation: weighted skill coverage blended with cosine similarity (scikit-learn)."""
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

ROLES = {  # skill -> importance weight (1-3)
    "Software Developer": {"Data Structures": 3, "Algorithms": 3, "OOP": 3, "Java": 2, "Python": 2, "SQL": 2, "Git": 2, "Problem Solving": 3, "DBMS": 1, "Operating Systems": 1},
    "Backend Developer": {"Java": 3, "Python": 2, "SQL": 3, "REST APIs": 3, "DBMS": 2, "Git": 2, "Spring Boot": 2, "Node.js": 1, "Docker": 1, "Data Structures": 2},
    "Full Stack Developer": {"JavaScript": 3, "React": 3, "Node.js": 3, "HTML/CSS": 3, "SQL": 2, "MongoDB": 2, "REST APIs": 2, "Git": 2, "TypeScript": 1},
    "Data Analyst": {"SQL": 3, "Excel": 3, "Python": 2, "Statistics": 3, "Power BI": 2, "Tableau": 2, "Pandas": 3, "NumPy": 1},
    "Data Scientist": {"Python": 3, "Machine Learning": 3, "Statistics": 3, "Pandas": 3, "NumPy": 2, "Scikit-learn": 3, "SQL": 2, "Deep Learning": 1},
    "ML Engineer": {"Python": 3, "Machine Learning": 3, "Deep Learning": 3, "TensorFlow": 3, "Scikit-learn": 2, "NLP": 2, "Docker": 1, "Git": 1, "AWS": 1},
    "DevOps Engineer": {"Linux": 3, "Docker": 3, "Kubernetes": 2, "AWS": 3, "CI/CD": 3, "Git": 2, "Python": 1, "Computer Networks": 1},
    "Cybersecurity Analyst": {"Cybersecurity": 3, "Computer Networks": 3, "Linux": 3, "Operating Systems": 2, "Python": 1, "SQL": 1},
    "QA / Test Engineer": {"Selenium": 3, "Java": 2, "Python": 1, "SQL": 2, "Git": 1, "Problem Solving": 1, "OOP": 1},
}
_VOCAB = sorted({s for r in ROLES.values() for s in r})

def _vec(d):
    return np.array([d.get(s, 0) for s in _VOCAB], dtype=float)

def role_match(skills, role):
    """Return (match %, matched skills, missing skills sorted by importance)."""
    req, have = ROLES[role], set(skills)
    total = sum(req.values())
    got = sum(w for s, w in req.items() if s in have)
    matched = [s for s in req if s in have]
    missing = sorted((s for s in req if s not in have), key=lambda s: -req[s])
    return 100 * got / total, matched, missing

def recommend_roles(skills) -> pd.DataFrame:
    stu = _vec({s: 1 for s in skills}).reshape(1, -1)
    rows = []
    for role, req in ROLES.items():
        cov, matched, missing = role_match(skills, role)
        cos = float(cosine_similarity(stu, _vec(req).reshape(1, -1))[0, 0]) if stu.any() else 0.0
        rows.append(dict(role=role, match_pct=round(0.7 * cov + 0.3 * 100 * cos, 1), coverage_pct=round(cov, 1),
                         matched=", ".join(matched), missing=", ".join(missing)))
    return pd.DataFrame(rows).sort_values("match_pct", ascending=False).reset_index(drop=True)
