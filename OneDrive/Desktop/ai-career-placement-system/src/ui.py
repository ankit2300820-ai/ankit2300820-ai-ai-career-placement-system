"""UI helpers: animated CSS theme, hero banner, animated KPI cards, author card."""
import html

CSS = """<style>
@property --n{syntax:'<integer>';initial-value:0;inherits:false}
@keyframes shift{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
@keyframes fadeUp{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:none}}
@keyframes cnt{from{--n:0}}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-7px)}}
@keyframes typing{from{width:0}to{width:100%}}
@keyframes blink{50%{border-color:transparent}}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(124,58,237,.5)}100%{box-shadow:0 0 0 18px rgba(124,58,237,0)}}
.stApp{background:radial-gradient(circle at top left,#1b1f3b 0%,#0e1117 55%)}
.hero{padding:1.2rem 1.6rem;border-radius:18px;color:#fff;margin-bottom:1rem;
  background:linear-gradient(120deg,#4f46e5,#7c3aed,#db2777,#4f46e5);background-size:300% 300%;
  animation:shift 9s ease infinite,fadeUp .7s both;box-shadow:0 10px 30px rgba(124,58,237,.25)}
.hero h2{margin:0;font-size:1.9rem}.hero p{margin:.3rem 0 0;opacity:.92}
.hero .typing{display:inline-block;max-width:100%;overflow:hidden;white-space:nowrap;border-right:2px solid #fff;
  animation:typing 3s steps(48) .3s both,blink .8s step-end infinite}
.float{display:inline-block;animation:float 3s ease-in-out infinite}
.kpi{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);border-radius:16px;padding:1rem 1.2rem;
  animation:fadeUp .7s both;transition:transform .25s,box-shadow .25s,border-color .25s}
.kpi:hover{transform:translateY(-5px);box-shadow:0 12px 28px rgba(124,58,237,.35);border-color:#7c3aed}
.kpi .kl{font-size:.75rem;opacity:.7;text-transform:uppercase;letter-spacing:.07em}
.kpi .kv{font-size:2rem;font-weight:800}.kpi .ks{font-size:.8rem;opacity:.75}
.count{animation:cnt 1.6s ease-out both;counter-reset:num var(--n)}.count::before{content:counter(num)}
div[data-testid="stMetric"],.stPlotlyChart,div[data-testid="stDataFrame"]{animation:fadeUp .8s both}
div[data-testid="stMetric"]{background:rgba(124,58,237,.10);border:1px solid rgba(124,58,237,.25);padding:.7rem 1rem;border-radius:14px;transition:transform .25s}
div[data-testid="stMetric"]:hover{transform:translateY(-4px)}
.stButton>button,.stDownloadButton>button{border-radius:10px;transition:transform .2s,box-shadow .2s}
.stButton>button:hover,.stDownloadButton>button:hover{transform:translateY(-2px) scale(1.02);box-shadow:0 8px 20px rgba(124,58,237,.4)}
.author{display:flex;gap:1.2rem;align-items:center;flex-wrap:wrap;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);
  border-radius:18px;padding:1.3rem 1.5rem;animation:fadeUp .8s both}
.avatar{width:84px;height:84px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:2.4rem;font-weight:800;color:#fff;
  background:linear-gradient(135deg,#7c3aed,#db2777);animation:pulse 2.2s infinite}
.author h3{margin:0}.author p{margin:.2rem 0 .6rem;opacity:.8}
.pill{display:inline-block;margin:.2rem .3rem .2rem 0;padding:.35rem .9rem;border-radius:999px;background:#2b2150;border:1px solid #4c3a8f;
  color:#e8eaf6!important;text-decoration:none!important;font-size:.85rem;transition:all .2s}
.pill:hover{background:#7c3aed;transform:translateY(-2px)}
.badge{display:inline-block;margin:.15rem;padding:.25rem .7rem;border-radius:8px;background:rgba(255,255,255,.08);font-size:.8rem;animation:fadeUp .8s both}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
</style>"""

def inject_css():
    import streamlit as st
    st.markdown(CSS, unsafe_allow_html=True)

def hero(title, sub="", typing=False):
    p = f'<span class="typing">{html.escape(sub)}</span>' if typing else html.escape(sub)
    return f'<div class="hero"><h2>{html.escape(title)}</h2><p>{p}</p></div>'

def kpi(label, value, suffix="", note="", delay=0.0):
    """Animated count-up number card (CSS only, works without JavaScript)."""
    n = int(round(float(value)))
    return (f'<div class="kpi" style="animation-delay:{delay}s"><div class="kl">{html.escape(label)}</div>'
            f'<div class="kv"><span class="count" style="--n:{n}"></span>{html.escape(suffix)}</div>'
            f'<div class="ks">{html.escape(note) or "&nbsp;"}</div></div>')

def kpi_text(label, text, note="", delay=0.0):
    return (f'<div class="kpi" style="animation-delay:{delay}s"><div class="kl">{html.escape(label)}</div>'
            f'<div class="kv" style="font-size:1.25rem">{html.escape(text)}</div><div class="ks">{html.escape(note) or "&nbsp;"}</div></div>')

def _safe_url(u):
    u = (u or "").strip()
    if u.startswith("www.") or u.startswith("linkedin.com") or u.startswith("github.com"):
        u = "https://" + u                      # allow links typed without https://
    return html.escape(u, quote=True) if u.startswith(("https://", "http://", "mailto:")) else "#"

def author_card(a):
    return (f'<div class="author"><div class="avatar">{html.escape(a["name"][:1].upper())}</div><div>'
            f'<h3>{html.escape(a["name"])}</h3><p>{html.escape(a["college"])} · Creator of this project</p>'
            f'<a class="pill" href="{_safe_url("mailto:" + a["email"])}">✉️ {html.escape(a["email"])}</a>'
            f'<a class="pill" href="{_safe_url(a["github"])}" target="_blank">🐙 GitHub</a>'
            f'<a class="pill" href="{_safe_url(a["linkedin"])}" target="_blank">💼 LinkedIn</a></div></div>')

def author_strip(a):
    return f'<p style="opacity:.75;font-size:.9rem">Built by <b>{html.escape(a["name"])}</b> · {html.escape(a["email"])}</p>'

def badges(items):
    return "".join(f'<span class="badge" style="animation-delay:{i*0.05}s">{html.escape(x)}</span>' for i, x in enumerate(items))
