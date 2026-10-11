"""AI Career & Placement System - Streamlit app. Run: streamlit run app.py"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src import career, companies as co, db, interview as iv, ml_model as ml, readiness as rd, report as rp
from src import roadmap as rm, skills_extractor as sx
from src import config, ui

st.set_page_config(page_title="AI Career & Placement System", page_icon="🎓", layout="wide")
ui.inject_css()

@st.cache_resource
def boot():
    db.init_db()
    return ml.load_model()
bundle = boot()

# ------------------------------------------------------------------ auth
if "sid" not in st.session_state:
    st.markdown(ui.hero("🎓 AI Career & Placement System", "Skills analysis, placement prediction, company matching and a personal roadmap.", typing=True)
                + ui.author_strip(config.AUTHOR), unsafe_allow_html=True)
    t1, t2 = st.tabs(["Login", "Register"])
    with t1, st.form("login"):
        e, p = st.text_input("Email"), st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            sid = db.login(e, p)
            if sid: st.session_state.sid = sid; st.rerun()
            else: st.error("Invalid email or password.")
    with t2, st.form("reg"):
        n, e2 = st.text_input("Full name"), st.text_input("Email ")
        p2, br = st.text_input("Password (min 6 chars)", type="password"), st.selectbox("Branch", ["CSE", "IT", "ECE", "EEE", "ME", "Other"])
        if st.form_submit_button("Create account"):
            try:
                st.session_state.sid = db.create_student(n, e2, p2, br); st.rerun()
            except ValueError as ex:
                st.error(str(ex))
    st.stop()

sid = st.session_state.sid
S = db.get_student(sid)
skills = db.get_skills(sid)
P = {f: float(S[f]) for f in ml.FEATURES if f != "num_skills"}
role = S["target_role"] if S["target_role"] in career.ROLES else career.recommend_roles(skills).iloc[0]["role"]
ready, parts, band = rd.compute(P, skills, role)
prob = ml.predict_proba(P, len(skills))

st.sidebar.title(f"👋 {S['name'].split()[0]}")
page = st.sidebar.radio("Navigate", ["📊 Dashboard", "👤 Profile", "📄 Resume & Skills", "💼 Career Match",
                                     "🎯 Readiness & Prediction", "🏢 Companies", "🛣️ Skill Gap & Roadmap",
                                     "🎤 Interview Prep", "📥 Report", "ℹ️ About"])
if st.sidebar.button("Logout"):
    st.session_state.clear(); st.rerun()
st.sidebar.caption(f"Target role: **{role}**")
st.sidebar.caption(f"Made with ❤️ by **{config.AUTHOR['name']}**")
st.markdown(ui.hero(page, f"Student: {S['name']} · {S['branch']} · CGPA {S['cgpa']}"), unsafe_allow_html=True)

# ------------------------------------------------------------------ dashboard
if page == "📊 Dashboard":
    c = st.columns(4)
    c[0].markdown(ui.kpi("Readiness Score", ready, "/100", band, 0.0), unsafe_allow_html=True)
    c[1].markdown(ui.kpi("Placement Probability", prob * 100, "%", "ML model (synthetic data)", 0.1), unsafe_allow_html=True)
    c[2].markdown(ui.kpi("Skills Detected", len(skills), "", "from resume + profile", 0.2), unsafe_allow_html=True)
    c[3].markdown(ui.kpi_text("Target Role", role, "change in Profile", 0.3), unsafe_allow_html=True)
    l, r = st.columns(2)
    cats = list(parts)
    fig = go.Figure(go.Scatterpolar(r=[parts[k] / rd.MAXES[k] * 100 for k in cats] + [parts[cats[0]] / rd.MAXES[cats[0]] * 100],
                                    theta=cats + [cats[0]], fill="toself", line_color="#7c3aed"))
    fig.update_layout(title="Readiness profile (% of max)", polar=dict(radialaxis=dict(range=[0, 100])), showlegend=False)
    l.plotly_chart(fig, use_container_width=True)
    hist = db.prediction_history(sid)
    if len(hist) > 1:
        r.plotly_chart(px.line(hist, y=["probability", "readiness"], markers=True, title="Your progress (saved predictions)"), use_container_width=True)
    else:
        r.info("Save predictions on the 'Readiness & Prediction' page to see your progress over time.")
    st.subheader("Cohort analytics (synthetic training data)")
    syn = ml.load_data(); syn["CGPA band"] = pd.cut(syn.cgpa, [0, 6, 7, 8, 9, 10]).astype(str)
    a, b = st.columns(2)
    a.plotly_chart(px.bar(syn.groupby("CGPA band").placed.mean().mul(100).reset_index(), x="CGPA band", y="placed", title="Placement rate % by CGPA band", labels={"placed": "Placed %"}), use_container_width=True)
    b.plotly_chart(px.bar(syn.groupby("internships").placed.mean().mul(100).reset_index(), x="internships", y="placed", title="Placement rate % by internships", labels={"placed": "Placed %"}), use_container_width=True)
    pop = db.query("SELECT skill, COUNT(*) AS students FROM student_skills GROUP BY skill ORDER BY students DESC LIMIT 10")
    reg = db.query("SELECT COUNT(*) AS n FROM students").iloc[0, 0]
    st.caption(f"Registered students on this platform: {reg}")
    if not pop.empty: st.plotly_chart(px.bar(pop, x="skill", y="students", title="Most common skills among registered students (live DB)"), use_container_width=True)

# ------------------------------------------------------------------ profile
elif page == "👤 Profile":
    with st.form("profile"):
        c1, c2, c3 = st.columns(3)
        cg = c1.number_input("CGPA", 0.0, 10.0, P["cgpa"], 0.01)
        t10 = c2.number_input("10th %", 0.0, 100.0, P["tenth_pct"]); t12 = c3.number_input("12th %", 0.0, 100.0, P["twelfth_pct"])
        bk = c1.number_input("Backlogs", 0, 20, int(P["backlogs"])); it = c2.number_input("Internships", 0, 10, int(P["internships"]))
        pr = c3.number_input("Projects", 0, 20, int(P["projects"])); ce = c1.number_input("Certifications", 0, 20, int(P["certifications"]))
        hk = c2.number_input("Hackathons", 0, 20, int(P["hackathons"]))
        cs = c3.slider("Coding score (LeetCode/HackerRank level, 0-100)", 0, 100, int(P["coding_score"]))
        ap = c1.slider("Aptitude score (0-100)", 0, 100, int(P["aptitude"])); cm = c2.slider("Communication (1-10)", 1, 10, int(P["communication"]))
        tr = c3.selectbox("Target role", list(career.ROLES), index=list(career.ROLES).index(role))
        manual = st.multiselect("Skills you know", sx.ALL_SKILLS, default=db.skills_by_source(sid, "manual"))
        if st.form_submit_button("💾 Save profile"):
            db.update_profile(sid, cgpa=cg, tenth_pct=t10, twelfth_pct=t12, backlogs=bk, internships=it, projects=pr, certifications=ce,
                              hackathons=hk, coding_score=cs, aptitude=ap, communication=cm, target_role=tr)
            db.set_skills(sid, manual, "manual"); st.success("Profile saved."); st.rerun()

# ------------------------------------------------------------------ resume
elif page == "📄 Resume & Skills":
    up = st.file_uploader("Upload resume (PDF, DOCX or TXT)", type=["pdf", "docx", "txt"])
    if up:
        text = sx.extract_text(up.getvalue(), up.name)
        found, meta = sx.extract_skills(text), sx.extract_meta(text)
        if not text.strip(): st.warning("No text found (scanned PDF?). Try a text-based PDF or DOCX.")
        st.success(f"Extracted {len(found)} skills from {up.name}")
        st.write(" ".join(f"`{s}`" for s in found) or "None found")
        st.json(meta)
        with st.expander("Extracted text"): st.text(text[:3000])
        if st.button("✅ Save skills to my profile"):
            db.save_resume(sid, up.name, text); db.set_skills(sid, found, "resume"); st.success("Saved!"); st.rerun()
    st.subheader("Current skills in your profile")
    st.write(" ".join(f"`{s}`" for s in skills) or "No skills yet.")

# ------------------------------------------------------------------ career
elif page == "💼 Career Match":
    rec = career.recommend_roles(skills)
    st.plotly_chart(px.bar(rec, x="match_pct", y="role", orientation="h", title="Job-role compatibility %", color="match_pct", color_continuous_scale="Viridis").update_yaxes(autorange="reversed"), use_container_width=True)
    st.dataframe(rec.rename(columns={"match_pct": "Match %", "coverage_pct": "Skill coverage %", "matched": "You have", "missing": "You need"}), use_container_width=True)
    st.success(f"Best fit right now: **{rec.iloc[0]['role']}** ({rec.iloc[0]['match_pct']}%). Set it as target on the Profile page.")

# ------------------------------------------------------------------ readiness + ML
elif page == "🎯 Readiness & Prediction":
    a, b = st.columns(2)
    g = go.Figure(go.Indicator(mode="gauge+number", value=ready, title={"text": f"Readiness ({band})"}, gauge={"axis": {"range": [0, 100]}, "bar": {"color": "#7c3aed"}}))
    a.plotly_chart(g, use_container_width=True)
    g2 = go.Figure(go.Indicator(mode="gauge+number", value=prob * 100, number={"suffix": "%"}, title={"text": "ML placement probability"}, gauge={"axis": {"range": [0, 100]}, "bar": {"color": "#db2777"}}))
    b.plotly_chart(g2, use_container_width=True)
    st.dataframe(pd.DataFrame({"Component": list(parts), "Score": list(parts.values()), "Max": [rd.MAXES[k] for k in parts]}), use_container_width=True, hide_index=True)
    if st.button("💾 Save this prediction to my history"):
        db.save_prediction(sid, prob, ready, role); st.success("Saved.")
    st.subheader("What should I improve? (what-if analysis using the ML model)")
    st.dataframe(ml.what_if(P, len(skills)), use_container_width=True, hide_index=True)
    st.subheader("Model details")
    m = bundle["metrics"]
    st.warning("⚠️ The model is trained on clearly SYNTHETIC data (data/generate_data.py). Results are indicative, not a real-world guarantee.")
    k = st.columns(5)
    for col, n in zip(k, ["accuracy", "precision", "recall", "f1", "roc_auc"]): col.metric(n.upper(), f"{m[n]:.3f}")
    st.caption(f"Selected model: **{bundle['best_model']}** (5-fold CV ROC-AUC: " + ", ".join(f"{n} {v:.3f}" for n, v in bundle["cv_auc"].items()) + ")")
    imp = pd.DataFrame({"Feature": list(bundle["importances"]), "Importance": list(bundle["importances"].values())}).sort_values("Importance")
    c1, c2 = st.columns(2)
    c1.plotly_chart(px.bar(imp, x="Importance", y="Feature", orientation="h", title="Feature importance"), use_container_width=True)
    c2.plotly_chart(px.imshow(m["confusion"], text_auto=True, x=["Not placed", "Placed"], y=["Not placed", "Placed"], title="Confusion matrix (test set)", labels=dict(x="Predicted", y="Actual")), use_container_width=True)
    if st.button("🔁 Retrain model"):
        ml.train(); st.cache_resource.clear(); st.rerun()

# ------------------------------------------------------------------ companies
elif page == "🏢 Companies":
    df = co.check(P, skills, ready)
    only = st.checkbox("Show only eligible companies", value=False)
    view = df[df.Eligible == "Yes"] if only else df
    st.plotly_chart(px.bar(view.head(10), x="Company", y="Compatibility", color="Eligible", title="Top company compatibility %"), use_container_width=True)
    st.dataframe(view, use_container_width=True, hide_index=True)
    st.caption("Eligibility criteria are illustrative (data/companies.csv) - edit the file or the `companies` table with real campus criteria.")

# ------------------------------------------------------------------ roadmap
elif page == "🛣️ Skill Gap & Roadmap":
    gap, pct = rm.gap_analysis(skills, role)
    st.metric(f"Skill coverage for {role}", f"{pct:.0f}%")
    hrs = st.slider("Hours you can study per week", 5, 40, 10)
    road, weeks = rm.build_roadmap(skills, role, hrs)
    if road.empty: st.success("No skill gaps for this role! Focus on mock interviews and projects.")
    else:
        st.info(f"Estimated time to close all gaps: **{weeks} weeks** at {hrs} hrs/week")
        st.dataframe(road, use_container_width=True, hide_index=True)
        st.plotly_chart(px.bar(road, x="Weeks", y="Skill", color="Priority", orientation="h", title="Learning plan (weeks per skill)"), use_container_width=True)

# ------------------------------------------------------------------ interview
elif page == "🎤 Interview Prep":
    r2 = st.selectbox("Prepare for role", list(career.ROLES), index=list(career.ROLES).index(role))
    per = st.slider("Questions per skill", 1, 2, 2)
    tech, hr = iv.questions(r2, skills, per)
    st.subheader("Technical questions (your strong skills first)")
    done = 0
    for i, (sk, q, h) in enumerate(tech):
        with st.expander(f"[{sk}] {q}"):
            st.write(f"💡 Hint: {h}")
            done += st.checkbox("I can answer this confidently", key=f"t{i}")
    st.subheader("HR questions")
    for i, (_, q, h) in enumerate(hr):
        with st.expander(q):
            st.write(f"💡 Hint: {h}")
            done += st.checkbox("I have prepared this", key=f"h{i}")
    total = len(tech) + len(hr)
    st.progress(done / total if total else 0, text=f"Preparation progress: {done}/{total}")

# ------------------------------------------------------------------ report
elif page == "📥 Report":
    rec, comp = career.recommend_roles(skills), co.check(P, skills, ready)
    road, weeks = rm.build_roadmap(skills, role)
    pdf = rp.build_pdf(S, role, ready, parts, band, prob, rec, comp, road, weeks)
    st.write("Your PDF includes profile, readiness score, ML probability, top roles, best companies and roadmap.")
    st.download_button("📥 Download PDF report", pdf, file_name=f"{S['name'].replace(' ', '_')}_career_report.pdf", mime="application/pdf")

# ------------------------------------------------------------------ about
elif page == "ℹ️ About":
    st.markdown(ui.author_card(config.AUTHOR), unsafe_allow_html=True)
    st.subheader("About this project")
    st.write("**AI Career & Placement System** helps B.Tech students analyse their skills, check placement readiness, "
             "discover suitable job roles and companies, close skill gaps with a personal roadmap, and prepare for interviews. "
             "It combines a SQL database (MySQL/SQLite), rule-based analytics and a scikit-learn machine-learning model inside a Streamlit app.")
    st.markdown(ui.badges(["Python", "Pandas", "NumPy", "Scikit-learn", "Streamlit", "Plotly", "MySQL", "SQLite", "fpdf2", "pytest", "Docker", "GitHub Actions"]), unsafe_allow_html=True)
    a, b = st.columns(2)
    with a:
        st.markdown("#### How it works")
        st.markdown("1. Register and fill your profile\n2. Upload a resume → skills are extracted\n3. Readiness score + ML probability are computed\n"
                    "4. Roles, companies and a roadmap are recommended\n5. Practise interview questions and download your PDF report")
    with b:
        st.markdown("#### Important notes")
        st.markdown("- The ML model is trained on **synthetic** data (indicative only)\n- Company criteria are **illustrative**\n- Educational / college project")
    st.caption(f"Contact: {config.AUTHOR['email']} · v1.1.0")
