"""Skill-gap analysis and a week-by-week personalised learning roadmap."""
import math
import pandas as pd
from .career import ROLES, role_match

LEARNING = {  # skill -> (free resource, base weeks at 10 hrs/week)
    "Python": ("Python for Everybody (Coursera/freeCodeCamp) + 30 LeetCode easy", 3), "Java": ("Java Programming - Apna College / Telusko + practice OOP programs", 4),
    "SQL": ("SQLBolt + W3Schools SQL + 50 HackerRank SQL problems", 2), "Data Structures": ("Striver's / Love Babbar DSA sheet - arrays to graphs", 6),
    "Algorithms": ("NeetCode 150 - sorting, DP, greedy, binary search", 5), "OOP": ("Java/C++ OOP concepts + build 2 class-based mini projects", 2),
    "Git": ("Git & GitHub crash course; push all projects to GitHub", 1), "DBMS": ("Gate Smashers DBMS playlist - ER, normalization, transactions", 2),
    "Operating Systems": ("Neso Academy OS - processes, scheduling, memory, deadlocks", 3), "Computer Networks": ("Neso Academy CN - OSI/TCP-IP, HTTP, DNS", 3),
    "REST APIs": ("Build a CRUD API with Flask/Spring Boot, test with Postman", 2), "Spring Boot": ("Spring Boot official guides + build a REST app", 4),
    "JavaScript": ("javascript.info + 20 DOM mini-tasks", 4), "React": ("React official tutorial + build a todo/dashboard app", 3),
    "Node.js": ("Node + Express crash course, build an API", 3), "HTML/CSS": ("freeCodeCamp Responsive Web Design", 2), "TypeScript": ("TypeScript Handbook", 2),
    "MongoDB": ("MongoDB University M001", 2), "Pandas": ("Kaggle Pandas micro-course + clean a real dataset", 2), "NumPy": ("NumPy quickstart + 30 exercises", 1),
    "Statistics": ("Khan Academy Statistics - distributions, hypothesis tests", 3), "Excel": ("Excel pivot tables, VLOOKUP/XLOOKUP, dashboards", 2),
    "Power BI": ("Microsoft Learn Power BI - build one dashboard", 2), "Tableau": ("Tableau Public free training", 2),
    "Machine Learning": ("Andrew Ng ML Specialization + 3 Kaggle projects", 6), "Scikit-learn": ("Kaggle ML intro + scikit-learn user guide", 2),
    "Deep Learning": ("fast.ai / DeepLearning.AI course", 6), "TensorFlow": ("TensorFlow tutorials / PyTorch basics", 3), "NLP": ("HuggingFace NLP course", 4),
    "Linux": ("Linux Journey + OverTheWire Bandit", 2), "Docker": ("Docker official getting-started; containerise one project", 2),
    "Kubernetes": ("Kubernetes basics (kodekloud / official docs)", 3), "AWS": ("AWS Cloud Practitioner free training", 3), "CI/CD": ("GitHub Actions: automate tests for one repo", 2),
    "Cybersecurity": ("TryHackMe Pre-Security + Jr Penetration Tester path", 5), "Selenium": ("Selenium WebDriver tutorial + automate a website", 3),
    "Problem Solving": ("Solve 100 problems on LeetCode / CodeChef", 4),
}

def gap_analysis(skills, role):
    pct, matched, missing = role_match(skills, role)
    return pd.DataFrame([dict(Skill=s, Importance={3: "High", 2: "Medium", 1: "Low"}[ROLES[role][s]]) for s in missing]), pct

def build_roadmap(skills, role, hours_per_week=10):
    _, _, missing = role_match(skills, role)
    rows, week = [], 1
    for s in missing:
        res, base = LEARNING.get(s, ("Official docs + one mini project", 2))
        w = max(1, math.ceil(base * 10 / hours_per_week))
        rows.append(dict(Skill=s, Priority={3: "High", 2: "Medium", 1: "Low"}[ROLES[role][s]], Resource=res,
                         Weeks=w, Schedule=f"Week {week}-{week + w - 1}"))
        week += w
    return pd.DataFrame(rows), week - 1
