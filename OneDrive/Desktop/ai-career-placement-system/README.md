# 🎓 AI Career & Placement System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-App-ff4b4b) ![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange) ![MySQL](https://img.shields.io/badge/MySQL%20%7C%20SQLite-DB-green) ![License](https://img.shields.io/badge/License-MIT-yellow) ![CI](https://img.shields.io/badge/CI-GitHub%20Actions-black)

> 👨‍💻 **Created by Ankit** – B.Tech CSE (Final Year) · 📧 ankitchadrabad9389@gmail.com · [LinkedIn](https://www.linkedin.com/in/ankit-b47699332)

A full-stack, data-driven web app that helps B.Tech students **analyse skills, check placement readiness, find suitable job roles and companies, close skill gaps and prepare for interviews** — powered by Python, SQL (MySQL/SQLite), scikit-learn and Streamlit.

> ⚠️ **Data disclaimer:** No real placement data is bundled. The ML model is trained on a clearly labelled **synthetic dataset** (`data/generate_data.py`). Company criteria in `data/companies.csv` are **illustrative**. Replace them with your college's real data for real use.

## ✨ Features
| # | Feature | How it works |
|---|---------|--------------|
| 1 | Registration & profile | Email/password (PBKDF2-hashed) stored in SQL; full academic/skills profile |
| 2 | Resume upload & skill extraction | PDF/DOCX/TXT parsing (`pypdf`, `python-docx`) + regex taxonomy of 40+ skills; also extracts email & CGPA |
| 3 | Career / job-role recommendation | Weighted skill coverage blended with cosine similarity (scikit-learn) over 9 roles |
| 4 | Placement readiness score | Transparent 0-100 score: Academics 25, Skills 30, Experience 20, Coding & Aptitude 15, Communication 10 |
| 5 | Company eligibility & compatibility | Rule checks (CGPA, backlogs, 10th/12th) + skill match, read from the `companies` SQL table |
| 6 | ML placement prediction | Logistic Regression vs Random Forest vs Gradient Boosting, best chosen by 5-fold CV ROC-AUC; accuracy/precision/recall/F1/AUC, confusion matrix, feature importance, **what-if analysis** |
| 7 | Skill gap & roadmap | Missing skills ranked by importance → week-by-week plan adjusted to your weekly study hours |
| 8 | Dashboard | Plotly radar, gauges, progress history (from DB), cohort analytics |
| 9 | Interview prep | Question bank per skill (strong skills first) + HR questions, with hints and a progress tracker |
| 11 | Animated UI + About page | Animated gradient hero, count-up KPI cards, hover effects, typing intro, author card (set in `.env`) |
| 10 | PDF report | Downloadable report (`fpdf2`) with all results |

## 🧰 Technologies
Python 3.10+, Pandas, NumPy, Scikit-learn, Joblib, Streamlit, Plotly, MySQL (PyMySQL) or SQLite, fpdf2, pypdf, python-docx, python-dotenv, pytest.

## 📁 Folder structure
```
ai-career-placement-system/
├── app.py                     # Streamlit UI (all pages)
├── requirements.txt
├── .env.example               # copy to .env
├── .gitignore
├── Dockerfile  .dockerignore  LICENSE
├── .streamlit/config.toml     # dark theme
├── .github/workflows/ci.yml   # automated tests
├── pytest.ini
├── README.md
├── database/schema.sql        # MySQL schema (5 tables)
├── data/
│   ├── generate_data.py       # creates SYNTHETIC data
│   ├── synthetic_students.csv # 3000 synthetic rows
│   └── companies.csv          # illustrative company criteria
├── models/                    # trained model saved here (auto-created)
├── uploads/  screenshots/
├── src/
│   ├── config.py   db.py   skills_extractor.py   career.py
│   ├── readiness.py   ml_model.py   companies.py
│   └── roadmap.py   interview.py   report.py   ui.py (animations)
└── tests/ (conftest.py, test_core.py)
```

## 🖥️ Installation (Windows + VS Code)
1. Install **Python 3.10+** (tick *Add Python to PATH*) and **VS Code**. For MySQL also install **MySQL Server + Workbench**.
2. Put this folder anywhere, e.g. `C:\Projects\ai-career-placement-system`, then in VS Code: **File → Open Folder**.
3. Open the terminal (**Ctrl + `**) and run:
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```
(If activation is blocked: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.) In VS Code press **Ctrl+Shift+P → Python: Select Interpreter → venv**.

## 🗄️ Database setup
**Option A – SQLite (zero setup, default).** Keep `DB_BACKEND=sqlite` in `.env`. The file `career_ai.db` and all tables are created automatically.

**Option B – MySQL.**
1. Open MySQL Workbench (or `mysql -u root -p`) and run: `CREATE DATABASE career_ai CHARACTER SET utf8mb4;`
2. Edit `.env`: `DB_BACKEND=mysql`, `DB_USER`, `DB_PASSWORD`, `DB_NAME=career_ai`.
3. Tables are created automatically on first run from `database/schema.sql` (or run that file manually in Workbench) and the `companies` table is seeded from `data/companies.csv`.

## ▶️ Run
```powershell
python data/generate_data.py      # optional: regenerate synthetic dataset
streamlit run app.py              # opens http://localhost:8501
```
The model trains automatically on first launch (~10-20 s) and is saved to `models/placement_model.joblib`. Use the **Retrain model** button to retrain anytime.

**Quick demo:** Register → *Profile* (fill details + skills) → *Resume & Skills* (upload a resume) → *Readiness & Prediction* → *Companies* → *Skill Gap & Roadmap* → *Report*.

## 📓 Jupyter Notebook (optional)
`notebooks/AI_Career_Placement_Walkthrough.ipynb` runs the whole pipeline step by step (data → ML → resume skills → readiness → roles → companies → roadmap → PDF).
```powershell
pip install jupyter ipykernel nbformat
jupyter notebook notebooks/AI_Career_Placement_Walkthrough.ipynb
```
In VS Code: install the *Jupyter* extension, open the `.ipynb`, choose the `venv` kernel and click **Run All**.

## 🐳 Docker (optional)
```bash
docker build -t career-ai .
docker run -p 8501:8501 career-ai
```

## 🧪 Testing
```powershell
pytest -q
```
Tests use an isolated temporary SQLite DB and cover skill extraction, registration/login, DB writes, role recommendation, readiness bounds, ML training + monotonic sanity check, company eligibility, roadmap, interview bank and PDF generation.

## 🏗️ Architecture
`Streamlit UI (app.py)` → `src/` business logic → `db.py` → MySQL/SQLite. The same SQL (named `:params`) runs on both databases. ML artifacts live in `models/`.

## 🖼️ Screenshots
Run the app, take screenshots, save them in `screenshots/` and link them here:
```
![Dashboard](screenshots/dashboard.png)
![Prediction](screenshots/prediction.png)
![Roadmap](screenshots/roadmap.png)
```

## ⚠️ Limitations
- ML model is trained on **synthetic** data (CV ROC-AUC ≈ 0.75 by design: the data contains noise); predictions are indicative only.
- Skill extraction is keyword/regex based (no deep NLP); scanned/image PDFs are not supported (no OCR).
- Company criteria are illustrative; no admin panel (edit the `companies` table/CSV).
- Simple email/password auth for a college project — not production-grade (no email verification, rate-limiting or HTTPS).
- Interview bank is small; extend `BANK` in `src/interview.py`.

## 🚀 Future scope
Real college placement data for retraining, admin/TPO portal, OCR + spaCy NER for resumes, LLM-powered mock interviews, job-API integration, Docker deployment.

## ⬆️ GitHub upload
```powershell
git init
git add .
git commit -m "Initial commit: AI Career & Placement System"
git branch -M main
git remote add origin https://github.com/<your-username>/ai-career-placement-system.git
git push -u origin main
```
Create the empty repo on github.com first. `.gitignore` already excludes `.env`, the venv, DB files and trained models — **never push your real `.env`**. Deploy free on Streamlit Community Cloud with `DB_BACKEND=sqlite` (set secrets in the dashboard).

## 💬 Interview talking points
Why Logistic Regression won (small tabular data, well-calibrated); how synthetic data was generated and why that's a limitation; weighted coverage + cosine similarity for recommendations; PBKDF2 password hashing; one SQL layer supporting two databases; what-if analysis for explainability.

## ⚙️ CI/CD
`.github/workflows/ci.yml` runs the test-suite automatically on every push / pull request.

## 👤 Author
**Ankit** – B.Tech CSE · [GitHub](https://github.com/your-username) · [LinkedIn](https://www.linkedin.com/in/ankit-b47699332) · ankitchadrabad9389@gmail.com
The same details appear on the in-app **ℹ️ About** page (edit the `AUTHOR_*` values in `.env`).

## 📜 License
MIT © 2026 Ankit – see [LICENSE](LICENSE).
