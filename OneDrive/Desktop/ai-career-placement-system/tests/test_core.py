import pytest
from src import career, companies, db, interview, ml_model as ml, readiness, roadmap, skills_extractor as sx

PROFILE = dict(cgpa=8.2, tenth_pct=85, twelfth_pct=82, backlogs=0, internships=1, projects=3,
               certifications=2, coding_score=70, communication=7, aptitude=65, hackathons=1)

@pytest.fixture(scope="module", autouse=True)
def setup():
    db.init_db()

def test_skill_extraction():
    text = "Skills: Python, C++, MySQL, scikit-learn, React.js, Git/GitHub. CGPA: 8.4. Completed 2 internships."
    found = sx.extract_skills(text)
    for s in ["Python", "C++", "SQL", "Scikit-learn", "React", "Git"]: assert s in found
    assert "Java" not in found and sx.extract_meta(text)["cgpa"] == 8.4

def test_registration_login_profile_skills():
    sid = db.create_student("Test User", "t@x.com", "secret123")
    with pytest.raises(ValueError): db.create_student("Dup", "t@x.com", "secret123")
    assert db.login("t@x.com", "secret123") == sid and db.login("t@x.com", "wrong") is None
    db.update_profile(sid, cgpa=8.5, target_role="Data Analyst")
    assert db.get_student(sid)["cgpa"] == 8.5
    db.set_skills(sid, ["Python", "SQL"], "manual"); db.set_skills(sid, ["SQL", "Git"], "resume")
    assert db.get_skills(sid) == ["Git", "Python", "SQL"]
    db.save_prediction(sid, 0.7, 70, "Data Analyst")
    assert len(db.prediction_history(sid)) == 1

def test_role_recommendation_and_readiness():
    rec = career.recommend_roles(["Python", "Pandas", "Statistics", "SQL", "Excel", "Power BI"])
    assert rec.iloc[0]["role"] == "Data Analyst"
    total, parts, _ = readiness.compute(PROFILE, ["Python", "SQL"], "Data Analyst")
    assert 0 <= total <= 100 and set(parts) == set(readiness.MAXES)

def test_ml_model_is_real_and_monotonic():
    b = ml.train()
    assert b["metrics"]["roc_auc"] > 0.70
    strong, weak = dict(PROFILE), dict(PROFILE, cgpa=5.5, backlogs=3, internships=0, projects=0, coding_score=20)
    assert ml.predict_proba(strong, 10) > ml.predict_proba(weak, 2)
    assert not ml.what_if(PROFILE, 6).empty

def test_companies_roadmap_interview():
    df = companies.check(PROFILE, ["Java", "SQL", "Data Structures", "OOP"], 70)
    assert df[df.Company == "TCS"].iloc[0].Eligible == "Yes"
    assert companies.check(dict(PROFILE, cgpa=5.0), [], 40).Eligible.eq("No").any()
    road, weeks = roadmap.build_roadmap(["Python"], "Data Scientist", 10)
    assert weeks > 0 and "Machine Learning" in road.Skill.values
    tech, hr = interview.questions("Backend Developer", ["Java", "SQL"])
    assert tech and hr

def test_pdf_report():
    pytest.importorskip("fpdf")
    from src import report
    rec = career.recommend_roles(["Python"]); comp = companies.check(PROFILE, ["Python"], 60)
    road, w = roadmap.build_roadmap(["Python"], "Data Analyst")
    s = dict(name="T", email="t@x.com", branch="CSE", **{k: PROFILE[k] for k in ["cgpa", "tenth_pct", "twelfth_pct", "backlogs", "internships", "projects", "certifications"]})
    pdf = report.build_pdf(s, "Data Analyst", 70, {"Academics": 20}, "Good", 0.7, rec, comp, road, w)
    assert pdf[:4] == b"%PDF"
