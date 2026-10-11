"""Generates SYNTHETIC placement data (NOT real students). Run: python data/generate_data.py"""
from pathlib import Path
import numpy as np
import pandas as pd

def generate(n=3000, seed=42):
    rng = np.random.default_rng(seed)
    cgpa = np.clip(rng.normal(7.4, 1.0, n), 5, 10).round(2)
    tenth = np.clip(rng.normal(76, 9, n), 50, 99).round(1)
    twelfth = np.clip(rng.normal(74, 9, n), 50, 99).round(1)
    backlogs = rng.choice([0, 1, 2, 3], n, p=[.72, .17, .08, .03])
    internships = rng.choice([0, 1, 2, 3], n, p=[.45, .35, .15, .05])
    projects = np.clip(rng.poisson(2.5, n), 0, 8)
    certs = np.clip(rng.poisson(1.5, n), 0, 6)
    coding = np.clip(rng.normal(55, 18, n), 5, 100).round(0)
    comm = np.clip(rng.normal(6, 1.8, n), 1, 10).round(1)
    apt = np.clip(rng.normal(55, 16, n), 5, 100).round(0)
    hack = rng.choice([0, 1, 2, 3], n, p=[.5, .3, .15, .05])
    nskills = np.clip(rng.poisson(5 + projects * 1.2 + certs * .5), 1, 25)
    z = (-9.05 + .55 * cgpa + .02 * coding + .015 * apt + .12 * comm + .5 * internships
         + .25 * projects + .15 * certs + .1 * hack - .9 * backlogs
         + .01 * (tenth + twelfth) / 2 + .12 * nskills + rng.normal(0, .7, n))
    placed = (rng.random(n) < 1 / (1 + np.exp(-z))).astype(int)
    return pd.DataFrame(dict(cgpa=cgpa, tenth_pct=tenth, twelfth_pct=twelfth, backlogs=backlogs,
        internships=internships, projects=projects, certifications=certs, coding_score=coding,
        communication=comm, aptitude=apt, hackathons=hack, num_skills=nskills, placed=placed))

if __name__ == "__main__":
    out = Path(__file__).parent / "synthetic_students.csv"
    df = generate(); df.to_csv(out, index=False)
    print(f"Saved {len(df)} rows to {out} | placement rate = {df.placed.mean():.1%}")
