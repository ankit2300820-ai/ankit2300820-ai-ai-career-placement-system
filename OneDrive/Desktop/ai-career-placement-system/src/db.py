"""Database layer: MySQL (pymysql) or SQLite (stdlib). Same SQL works on both."""
import hashlib, hmac, re, secrets, sqlite3
import pandas as pd
from . import config

PROFILE_FIELDS = ["branch", "study_year", "cgpa", "tenth_pct", "twelfth_pct", "backlogs", "internships",
                  "projects", "certifications", "coding_score", "communication", "aptitude",
                  "hackathons", "target_role"]

def _mysql():
    return config.DB_BACKEND == "mysql"

def _connect():
    if _mysql():
        import pymysql
        return pymysql.connect(charset="utf8mb4", **config.MYSQL)
    con = sqlite3.connect(config.SQLITE_PATH)
    con.execute("PRAGMA foreign_keys=ON")
    return con

def _prep(sql):
    return re.sub(r":(\w+)", r"%(\1)s", sql) if _mysql() else sql   # :name -> %(name)s for MySQL

def run(sql, **params):
    """Execute INSERT/UPDATE/DELETE. Returns last inserted id."""
    con = _connect()
    try:
        cur = con.cursor(); cur.execute(_prep(sql), params); con.commit()
        return cur.lastrowid
    finally:
        con.close()

def query(sql, **params):
    """Execute SELECT and return a DataFrame."""
    con = _connect()
    try:
        cur = con.cursor(); cur.execute(_prep(sql), params)
        cols = [d[0] for d in cur.description]
        return pd.DataFrame(cur.fetchall(), columns=cols)
    finally:
        con.close()

def init_db():
    """Create tables from database/schema.sql and seed companies (idempotent)."""
    ddl = "\n".join(l for l in (config.ROOT / "database" / "schema.sql").read_text().splitlines()
                    if not l.strip().startswith("--"))
    if not _mysql():
        ddl = ddl.replace("INT AUTO_INCREMENT PRIMARY KEY", "INTEGER PRIMARY KEY AUTOINCREMENT").replace(" ENGINE=InnoDB", "")
    con = _connect()
    try:
        cur = con.cursor()
        for stmt in [s.strip() for s in ddl.split(";") if s.strip()]:
            cur.execute(stmt)
        con.commit()
    finally:
        con.close()
    if query("SELECT COUNT(*) AS n FROM companies").iloc[0, 0] == 0:
        for r in pd.read_csv(config.DATA_DIR / "companies.csv").to_dict("records"):
            run("INSERT INTO companies (name,tier,min_cgpa,max_backlogs,min_10th,min_12th,required_skills,roles,avg_package_lpa) "
                "VALUES (:name,:tier,:min_cgpa,:max_backlogs,:min_10th,:min_12th,:required_skills,:roles,:avg_package_lpa)", **r)

# ---------- passwords ----------
def hash_pw(pw, salt=None):
    salt = salt or secrets.token_hex(8)
    return f"{salt}${hashlib.pbkdf2_hmac('sha256', pw.encode(), salt.encode(), 100_000).hex()}"

def check_pw(pw, stored):
    return hmac.compare_digest(hash_pw(pw, stored.split("$")[0]), stored)

# ---------- students ----------
def create_student(name, email, password, branch="CSE"):
    email = email.strip().lower()
    if not name.strip() or "@" not in email or len(password) < 6:
        raise ValueError("Enter a name, valid email and a password of at least 6 characters.")
    if not query("SELECT id FROM students WHERE email=:e", e=email).empty:
        raise ValueError("This email is already registered.")
    return run("INSERT INTO students (name,email,password_hash,branch) VALUES (:n,:e,:p,:b)",
               n=name.strip(), e=email, p=hash_pw(password), b=branch)

def login(email, password):
    df = query("SELECT * FROM students WHERE email=:e", e=email.strip().lower())
    if df.empty or not check_pw(password, df.iloc[0]["password_hash"]):
        return None
    return int(df.iloc[0]["id"])

def get_student(sid):
    df = query("SELECT * FROM students WHERE id=:i", i=sid)
    return None if df.empty else df.iloc[0].to_dict()

def update_profile(sid, **fields):
    keys = [k for k in fields if k in PROFILE_FIELDS]
    if keys:
        run("UPDATE students SET " + ",".join(f"{k}=:{k}" for k in keys) + " WHERE id=:sid",
            sid=sid, **{k: fields[k] for k in keys})

# ---------- skills / resumes / predictions ----------
def get_skills(sid):
    return query("SELECT skill FROM student_skills WHERE student_id=:i ORDER BY skill", i=sid)["skill"].tolist()

def set_skills(sid, skills, source):
    """Replace this source's skills (manual/resume) without duplicating skills from the other source."""
    run("DELETE FROM student_skills WHERE student_id=:i AND source=:s", i=sid, s=source)
    existing = set(get_skills(sid))
    for sk in skills:
        if sk not in existing:
            run("INSERT INTO student_skills (student_id,skill,source) VALUES (:i,:k,:s)", i=sid, k=sk, s=source)

def skills_by_source(sid, source):
    return query("SELECT skill FROM student_skills WHERE student_id=:i AND source=:s", i=sid, s=source)["skill"].tolist()

def save_resume(sid, filename, content):
    run("INSERT INTO resumes (student_id,filename,content) VALUES (:i,:f,:c)", i=sid, f=filename, c=content[:60000])

def save_prediction(sid, prob, readiness, role):
    run("INSERT INTO predictions (student_id,probability,readiness,target_role) VALUES (:i,:p,:r,:t)",
        i=sid, p=float(prob), r=float(readiness), t=role)

def prediction_history(sid):
    return query("SELECT probability,readiness,target_role,created_at FROM predictions WHERE student_id=:i ORDER BY id", i=sid)
