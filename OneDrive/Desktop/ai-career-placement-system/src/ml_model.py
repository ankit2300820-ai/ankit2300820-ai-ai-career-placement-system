"""Placement prediction: trains Logistic Regression, Random Forest, Gradient Boosting; keeps the best (ROC-AUC CV)."""
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from . import config

FEATURES = ["cgpa", "tenth_pct", "twelfth_pct", "backlogs", "internships", "projects",
            "certifications", "coding_score", "communication", "aptitude", "hackathons", "num_skills"]
_cache = {}

def load_data():
    path = config.DATA_DIR / "synthetic_students.csv"
    if not path.exists():
        import importlib.util
        spec = importlib.util.spec_from_file_location("gen", config.DATA_DIR / "generate_data.py")
        mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        mod.generate().to_csv(path, index=False)
    return pd.read_csv(path)

def train():
    df = load_data()
    X, y = df[FEATURES], df["placed"]
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    candidates = {
        "Logistic Regression": make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
        "Random Forest": RandomForestClassifier(n_estimators=200, max_depth=8, random_state=42, n_jobs=-1),
        "Gradient Boosting": GradientBoostingClassifier(random_state=42),
    }
    cv = {n: float(cross_val_score(m, Xtr, ytr, cv=5, scoring="roc_auc").mean()) for n, m in candidates.items()}
    best = max(cv, key=cv.get)
    model = candidates[best].fit(Xtr, ytr)
    pred, proba = model.predict(Xte), model.predict_proba(Xte)[:, 1]
    final = model[-1] if hasattr(model, "steps") else model
    imp = final.feature_importances_ if hasattr(final, "feature_importances_") else np.abs(final.coef_[0])
    bundle = dict(model=model, best_model=best, cv_auc=cv, features=FEATURES,
                  importances=dict(zip(FEATURES, (imp / imp.sum()).tolist())),
                  metrics=dict(accuracy=accuracy_score(yte, pred), precision=precision_score(yte, pred),
                               recall=recall_score(yte, pred), f1=f1_score(yte, pred), roc_auc=roc_auc_score(yte, proba),
                               confusion=confusion_matrix(yte, pred).tolist(), train_rows=len(Xtr), test_rows=len(Xte)))
    config.MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump(bundle, config.MODEL_PATH)
    (config.MODEL_DIR / "metrics.json").write_text(json.dumps({k: v for k, v in bundle.items() if k != "model"}, indent=2))
    _cache["b"] = bundle
    return bundle

def load_model():
    if "b" not in _cache:
        _cache["b"] = joblib.load(config.MODEL_PATH) if config.MODEL_PATH.exists() else train()
    return _cache["b"]

def predict_proba(profile: dict, num_skills: int) -> float:
    row = pd.DataFrame([{**{f: float(profile[f]) for f in FEATURES if f != "num_skills"}, "num_skills": num_skills}])[FEATURES]
    return float(load_model()["model"].predict_proba(row)[0, 1])

def what_if(profile: dict, num_skills: int) -> pd.DataFrame:
    """Re-run the real model under improvement scenarios to see which action helps most."""
    base = predict_proba(profile, num_skills)
    def tweak(**ch):
        p = dict(profile); n = num_skills
        for k, v in ch.items():
            if k == "num_skills": n += v
            else: p[k] = min(max(float(p[k]) + v, 0), {"cgpa": 10, "coding_score": 100, "aptitude": 100, "communication": 10}.get(k, 99))
        return predict_proba(p, n)
    sc = {"+1 internship": tweak(internships=1), "+2 projects": tweak(projects=2, num_skills=2),
          "+15 coding score": tweak(coding_score=15), "+15 aptitude": tweak(aptitude=15),
          "+2 communication": tweak(communication=2), "+1 certification": tweak(certifications=1),
          "+3 new skills": tweak(num_skills=3)}
    if profile["backlogs"] > 0: sc["Clear all backlogs"] = tweak(backlogs=-profile["backlogs"])
    df = pd.DataFrame({"Scenario": list(sc), "New probability %": [round(v * 100, 1) for v in sc.values()]})
    df["Change (pts)"] = (df["New probability %"] - round(base * 100, 1)).round(1)
    return df.sort_values("Change (pts)", ascending=False).reset_index(drop=True)
