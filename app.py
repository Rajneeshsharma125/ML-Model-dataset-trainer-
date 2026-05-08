import streamlit as st
from utils.session_manager import init_session_state

st.set_page_config(
    page_title="HyperTuneML Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_session_state()

# ── CSS ───────────────────────────────────────────────────────────────────────
CSS = '''
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html,body,[data-testid="stAppViewContainer"],[data-testid="stMain"]{
    background-color:#eef2f7!important;
    font-family:'Inter','Segoe UI',sans-serif!important;
}
[data-testid="stSidebar"]{background-color:#1a2233!important;}
[data-testid="stSidebar"] *{color:#cbd5e1!important;}
#MainMenu,footer,header{visibility:hidden;}
.block-container{padding:0!important;max-width:100%!important;}
.navbar{width:100%;background:#1e2d40;display:flex;align-items:center;
    justify-content:space-between;padding:11px 36px;
    box-shadow:0 2px 8px rgba(0,0,0,0.18);}
.navbar-brand{display:flex;align-items:center;gap:10px;text-decoration:none;}
.navbar-title{font-size:1.22rem;font-weight:800;color:#fff;letter-spacing:0.5px;}
.navbar-title span{color:#38bdf8;}
.navbar-right{display:flex;align-items:center;gap:12px;}
.search-wrap{position:relative;display:flex;align-items:center;}
.search-icon{position:absolute;left:10px;}
.search-input{background:#2d3f55;border:none;border-radius:8px;
    padding:7px 14px 7px 34px;color:#94a3b8;font-size:13px;width:160px;outline:none;}
.nav-avatar{width:34px;height:34px;border-radius:50%;background:#38bdf8;
    display:flex;align-items:center;justify-content:center;
    font-weight:700;color:#1a2233;font-size:14px;flex-shrink:0;}
.nav-username{color:#e2e8f0;font-size:14px;font-weight:500;
    display:flex;align-items:center;gap:4px;}
.nav-btn{display:flex;align-items:center;gap:6px;background:#2d3f55;
    color:#e2e8f0!important;border:none;border-radius:8px;padding:7px 15px;
    font-size:13px;font-weight:600;text-decoration:none!important;transition:background 0.2s;}
.nav-btn:hover{background:#38bdf8;color:#fff!important;}
.nav-icon-btn{background:#2d3f55;border-radius:8px;padding:7px 10px;
    display:flex;align-items:center;text-decoration:none;transition:background 0.2s;}
.nav-icon-btn:hover{background:#38bdf8;}
.main-wrap{padding:36px 48px 0 48px;background:#eef2f7;}
.hero-row{display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:26px;}
.hero-left{flex:1;}
.hero-title{font-size:2.1rem;font-weight:800;color:#1a2233;margin-bottom:8px;
    display:flex;align-items:center;gap:12px;}
.hero-sub{color:#4a6080;font-size:0.95rem;line-height:1.6;max-width:680px;}
.hero-right{flex-shrink:0;width:290px;margin-left:24px;opacity:0.72;}
.card-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:32px;}
.feat-card{background:#fff;border-radius:12px;padding:18px 16px 16px;
    box-shadow:0 1px 6px rgba(0,0,0,0.07);border:1px solid #e2e8f0;
    transition:transform 0.15s,box-shadow 0.15s;}
.feat-card:hover{transform:translateY(-3px);box-shadow:0 6px 20px rgba(0,0,0,0.10);}
.feat-card-header{display:flex;align-items:center;gap:10px;margin-bottom:9px;}
.feat-icon{width:28px;height:28px;flex-shrink:0;}
.feat-title{font-size:0.97rem;font-weight:700;color:#1a2233;}
.feat-desc{font-size:0.79rem;color:#64748b;line-height:1.55;}
.section-title{font-size:1.35rem;font-weight:700;color:#1a2233;
    margin:4px 0 18px;display:flex;align-items:center;gap:10px;}
.steps-row{display:flex;align-items:stretch;gap:0;
    margin-bottom:36px;overflow-x:auto;}
.step-card{min-width:115px;max-width:130px;background:#1e2d40;
    border-radius:10px;padding:14px 12px;color:#e2e8f0;
    flex-shrink:0;position:relative;overflow:hidden;}
.step-bg{position:absolute;top:0;left:0;right:0;height:52px;
    background-image:linear-gradient(rgba(56,189,248,0.07) 1px,transparent 1px),
    linear-gradient(90deg,rgba(56,189,248,0.07) 1px,transparent 1px);
    background-size:12px 12px;border-radius:10px 10px 0 0;}
.step-num{font-size:2rem;font-weight:800;color:rgba(255,255,255,0.2);
    line-height:1;margin-bottom:10px;position:relative;z-index:1;}
.step-text{font-size:0.75rem;color:#94a3b8;line-height:1.5;
    position:relative;z-index:1;}
.step-text strong{color:#e2e8f0;}
.step-arrow{display:flex;align-items:center;justify-content:center;
    color:#38bdf8;font-size:1.1rem;padding:0 4px;flex-shrink:0;align-self:center;}
.models-wrap{display:grid;grid-template-columns:1fr 1fr;gap:0;
    min-height:260px;margin-bottom:0;}
.models-left{padding-right:40px;}
.models-cols{display:grid;grid-template-columns:1fr 1fr;gap:40px;}
.model-group h3{font-size:1.15rem;font-weight:700;color:#1a2233;margin-bottom:10px;}
.model-group ul{list-style:disc;padding-left:18px;color:#334155;
    line-height:2.0;font-size:0.93rem;}
.models-right{display:flex;align-items:center;justify-content:flex-end;overflow:hidden;}
.network-svg{width:100%;max-width:480px;opacity:0.6;}
.footer-note{font-size:0.78rem;color:#94a3b8;padding:14px 48px;
    border-top:1px solid #dde3ec;background:#eef2f7;}
.footer-bar{background:#1e2d40;display:flex;justify-content:space-between;
    align-items:center;padding:14px 48px;font-size:0.82rem;}
.footer-bar-left{color:#94a3b8;}
.footer-bar-right a{color:#94a3b8;text-decoration:none;margin-left:18px;}
.footer-bar-right a:hover{color:#38bdf8;}
.footer-built{background:#111827;text-align:center;color:#475569;
    font-size:0.74rem;padding:7px;}
</style>
'''
st.markdown(CSS, unsafe_allow_html=True)

# ── NAVBAR ────────────────────────────────────────────────────────────────────
NAVBAR = (
    '<div class="navbar">'
    '<div class="navbar-brand">'
    '<svg width="36" height="36" viewBox="0 0 36 36" fill="none">'
    '<rect width="36" height="36" rx="7" fill="#162030"/>'
    '<circle cx="18" cy="18" r="6" stroke="#38bdf8" stroke-width="1.8" fill="none"/>'
    '<circle cx="18" cy="18" r="2" fill="#38bdf8"/>'
    '<circle cx="18" cy="6" r="2.2" fill="#38bdf8"/>'
    '<circle cx="18" cy="30" r="2.2" fill="#38bdf8"/>'
    '<circle cx="6" cy="18" r="2.2" fill="#38bdf8"/>'
    '<circle cx="30" cy="18" r="2.2" fill="#38bdf8"/>'
    '<circle cx="9.5" cy="9.5" r="1.8" fill="#38bdf8" opacity="0.7"/>'
    '<circle cx="26.5" cy="9.5" r="1.8" fill="#38bdf8" opacity="0.7"/>'
    '<circle cx="9.5" cy="26.5" r="1.8" fill="#38bdf8" opacity="0.7"/>'
    '<circle cx="26.5" cy="26.5" r="1.8" fill="#38bdf8" opacity="0.7"/>'
    '<line x1="18" y1="8.2" x2="18" y2="12" stroke="#38bdf8" stroke-width="1.5"/>'
    '<line x1="18" y1="24" x2="18" y2="27.8" stroke="#38bdf8" stroke-width="1.5"/>'
    '<line x1="8.2" y1="18" x2="12" y2="18" stroke="#38bdf8" stroke-width="1.5"/>'
    '<line x1="24" y1="18" x2="27.8" y2="18" stroke="#38bdf8" stroke-width="1.5"/>'
    '</svg>'
    '<span class="navbar-title">HYPER<span>TUNEML</span></span>'
    '</div>'
    '<div class="navbar-right">'
    '<div class="search-wrap">'
    '<svg class="search-icon" width="14" height="14" viewBox="0 0 24 24" fill="none"'
    ' stroke="#64748b" stroke-width="2.5">'
    '<circle cx="11" cy="11" r="7"/>'
    '<line x1="16.5" y1="16.5" x2="22" y2="22"/>'
    '</svg>'
    '<input class="search-input" type="text" placeholder="Search"/>'
    '</div>'
    '<div class="nav-avatar">R</div>'
    '<span class="nav-username">Rajneesh'
    '<svg width="11" height="11" viewBox="0 0 24 24" fill="none"'
    ' stroke="#94a3b8" stroke-width="2.5"><path d="M6 9l6 6 6-6"/></svg>'
    '</span>'
    '<a class="nav-btn" href="https://github.com/Rajneeshsharma125/ML-Model-dataset-trainer-"'
    ' target="_blank">'
    '<svg width="14" height="14" viewBox="0 0 24 24" fill="none"'
    ' stroke="#e2e8f0" stroke-width="2.2" stroke-linecap="round">'
    '<circle cx="6" cy="6" r="3"/><circle cx="18" cy="6" r="3"/>'
    '<circle cx="12" cy="18" r="3"/>'
    '<path d="M6 9v1a3 3 0 0 0 3 3h6a3 3 0 0 0 3-3V9"/>'
    '<line x1="12" y1="15" x2="12" y2="21"/>'
    '</svg>Fork</a>'
    '<a class="nav-icon-btn" href="https://github.com/Rajneeshsharma125" target="_blank">'
    '<svg width="22" height="22" viewBox="0 0 24 24" fill="#e2e8f0">'
    '<path d="M12 2C6.477 2 2 6.484 2 12.021c0 4.428 2.865 8.184 6.839 9.504'
    '.5.092.682-.217.682-.482 0-.237-.009-.868-.013-1.703-2.782.605-3.369-1.342'
    '-3.369-1.342-.454-1.155-1.11-1.463-1.11-1.463-.908-.62.069-.608.069-.608'
    ' 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832'
    '.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951'
    ' 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0'
    ' .84-.27 2.75 1.026A9.564 9.564 0 0 1 12 6.844a9.59 9.59 0 0 1 2.504.337'
    'c1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651'
    '.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943'
    '.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.743'
    ' 0 .267.18.578.688.48C19.138 20.2 22 16.447 22 12.021 22 6.484 17.523 2 12 2z"/>'
    '</svg></a>'
    '</div></div>'
)
st.markdown(NAVBAR, unsafe_allow_html=True)

st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────────────────────────────
HERO = (
    '<div class="hero-row">'
    '<div class="hero-left">'
    '<div class="hero-title">'
    '<svg width="46" height="46" viewBox="0 0 46 46" fill="none">'
    '<circle cx="23" cy="23" r="21" stroke="#1a2233" stroke-width="2.2" fill="none"/>'
    '<circle cx="23" cy="23" r="10" stroke="#1a2233" stroke-width="1.8" fill="none"/>'
    '<circle cx="23" cy="23" r="3.5" fill="#1a2233"/>'
    '<line x1="23" y1="2" x2="23" y2="13" stroke="#1a2233" stroke-width="2"/>'
    '<line x1="23" y1="33" x2="23" y2="44" stroke="#1a2233" stroke-width="2"/>'
    '<line x1="2" y1="23" x2="13" y2="23" stroke="#1a2233" stroke-width="2"/>'
    '<line x1="33" y1="23" x2="44" y2="23" stroke="#1a2233" stroke-width="2"/>'
    '<circle cx="23" cy="2" r="2.5" fill="#1a2233"/>'
    '<circle cx="23" cy="44" r="2.5" fill="#1a2233"/>'
    '<circle cx="2" cy="23" r="2.5" fill="#1a2233"/>'
    '<circle cx="44" cy="23" r="2.5" fill="#1a2233"/>'
    '</svg>'
    'HyperTuneML Platform'
    '</div>'
    '<div class="hero-sub">'
    'An end-to-end Machine Learning platform &mdash; upload your data, preprocess, explore, '
    'train, evaluate, compare, predict, and download your model.'
    '</div>'
    '</div>'
    '<div class="hero-right">'
    '<svg viewBox="0 0 300 190" fill="none" xmlns="http://www.w3.org/2000/svg">'
    '<circle cx="28" cy="95" r="11" fill="#c8d8e8" stroke="#7a98b0" stroke-width="1.5"/>'
    '<circle cx="100" cy="55" r="11" fill="#c8d8e8" stroke="#7a98b0" stroke-width="1.5"/>'
    '<circle cx="100" cy="95" r="11" fill="#c8d8e8" stroke="#7a98b0" stroke-width="1.5"/>'
    '<circle cx="100" cy="135" r="11" fill="#c8d8e8" stroke="#7a98b0" stroke-width="1.5"/>'
    '<circle cx="180" cy="55" r="11" fill="#c8d8e8" stroke="#7a98b0" stroke-width="1.5"/>'
    '<circle cx="180" cy="95" r="11" fill="#c8d8e8" stroke="#7a98b0" stroke-width="1.5"/>'
    '<circle cx="180" cy="135" r="11" fill="#c8d8e8" stroke="#7a98b0" stroke-width="1.5"/>'
    '<circle cx="252" cy="95" r="14" fill="#7a98b0" stroke="#4a6880" stroke-width="2"/>'
    '<line x1="39" y1="90" x2="89" y2="61" stroke="#7a98b0" stroke-width="1.3"/>'
    '<line x1="39" y1="95" x2="89" y2="95" stroke="#7a98b0" stroke-width="1.3"/>'
    '<line x1="39" y1="100" x2="89" y2="129" stroke="#7a98b0" stroke-width="1.3"/>'
    '<line x1="111" y1="60" x2="169" y2="60" stroke="#7a98b0" stroke-width="1.3"/>'
    '<line x1="111" y1="58" x2="169" y2="93" stroke="#7a98b0" stroke-width="1.3"/>'
    '<line x1="111" y1="57" x2="169" y2="133" stroke="#7a98b0" stroke-width="1.3"/>'
    '<line x1="111" y1="95" x2="169" y2="60" stroke="#7a98b0" stroke-width="1.3"/>'
    '<line x1="111" y1="95" x2="169" y2="95" stroke="#7a98b0" stroke-width="1.3"/>'
    '<line x1="111" y1="95" x2="169" y2="130" stroke="#7a98b0" stroke-width="1.3"/>'
    '<line x1="111" y1="133" x2="169" y2="62" stroke="#7a98b0" stroke-width="1.3"/>'
    '<line x1="111" y1="133" x2="169" y2="97" stroke="#7a98b0" stroke-width="1.3"/>'
    '<line x1="111" y1="135" x2="169" y2="135" stroke="#7a98b0" stroke-width="1.3"/>'
    '<line x1="191" y1="60" x2="238" y2="90" stroke="#7a98b0" stroke-width="1.5"/>'
    '<line x1="191" y1="95" x2="238" y2="95" stroke="#7a98b0" stroke-width="1.5"/>'
    '<line x1="191" y1="130" x2="238" y2="100" stroke="#7a98b0" stroke-width="1.5"/>'
    '<rect x="258" y="62" width="38" height="30" rx="4" fill="#7a98b0" opacity="0.85"/>'
    '<line x1="264" y1="84" x2="264" y2="76" stroke="white" stroke-width="2.2" stroke-linecap="round"/>'
    '<line x1="271" y1="84" x2="271" y2="70" stroke="white" stroke-width="2.2" stroke-linecap="round"/>'
    '<line x1="278" y1="84" x2="278" y2="74" stroke="white" stroke-width="2.2" stroke-linecap="round"/>'
    '<line x1="285" y1="84" x2="285" y2="66" stroke="white" stroke-width="2.2" stroke-linecap="round"/>'
    '</svg>'
    '</div>'
    '</div>'
)
st.markdown(HERO, unsafe_allow_html=True)

# ── FEATURE CARDS ─────────────────────────────────────────────────────────────
def card(icon_svg, title, desc):
    return (
        '<div class="feat-card">'
        '<div class="feat-card-header">'
        + icon_svg +
        '<div class="feat-title">' + title + '</div>'
        '</div>'
        '<div class="feat-desc">' + desc + '</div>'
        '</div>'
    )

ICON_UPLOAD = (
    '<svg class="feat-icon" viewBox="0 0 28 28" fill="none">'
    '<rect x="4" y="3" width="20" height="22" rx="2" stroke="#1a2233" stroke-width="1.8"/>'
    '<line x1="4" y1="9" x2="24" y2="9" stroke="#1a2233" stroke-width="1.4"/>'
    '<line x1="9" y1="3" x2="9" y2="9" stroke="#1a2233" stroke-width="1.4"/>'
    '<line x1="8" y1="14" x2="20" y2="14" stroke="#c8d8e8" stroke-width="1.4"/>'
    '<line x1="8" y1="18" x2="20" y2="18" stroke="#c8d8e8" stroke-width="1.4"/>'
    '<line x1="8" y1="22" x2="15" y2="22" stroke="#c8d8e8" stroke-width="1.4"/>'
    '<circle cx="21" cy="21" r="5" fill="#38bdf8" opacity="0.9"/>'
    '<line x1="19.5" y1="21" x2="22.5" y2="21" stroke="white" stroke-width="1.5"/>'
    '<line x1="21" y1="19.5" x2="21" y2="22.5" stroke="white" stroke-width="1.5"/>'
    '</svg>'
)
ICON_PREPROC = (
    '<svg class="feat-icon" viewBox="0 0 28 28" fill="none">'
    '<circle cx="14" cy="14" r="9.5" stroke="#1a2233" stroke-width="1.8"/>'
    '<circle cx="14" cy="14" r="3" fill="#38bdf8"/>'
    '<line x1="14" y1="4.5" x2="14" y2="8.5" stroke="#1a2233" stroke-width="1.5"/>'
    '<line x1="14" y1="19.5" x2="14" y2="23.5" stroke="#1a2233" stroke-width="1.5"/>'
    '<line x1="4.5" y1="14" x2="8.5" y2="14" stroke="#1a2233" stroke-width="1.5"/>'
    '<line x1="19.5" y1="14" x2="23.5" y2="14" stroke="#1a2233" stroke-width="1.5"/>'
    '<line x1="7.5" y1="7.5" x2="10.3" y2="10.3" stroke="#1a2233" stroke-width="1.3"/>'
    '<line x1="17.7" y1="17.7" x2="20.5" y2="20.5" stroke="#1a2233" stroke-width="1.3"/>'
    '<line x1="20.5" y1="7.5" x2="17.7" y2="10.3" stroke="#1a2233" stroke-width="1.3"/>'
    '<line x1="10.3" y1="17.7" x2="7.5" y2="20.5" stroke="#1a2233" stroke-width="1.3"/>'
    '</svg>'
)
ICON_EDA = (
    '<svg class="feat-icon" viewBox="0 0 28 28" fill="none">'
    '<rect x="3" y="5" width="22" height="18" rx="2" stroke="#1a2233" stroke-width="1.8"/>'
    '<line x1="3" y1="10" x2="25" y2="10" stroke="#1a2233" stroke-width="1.2"/>'
    '<line x1="8" y1="5" x2="8" y2="10" stroke="#1a2233" stroke-width="1.2"/>'
    '<line x1="7" y1="21" x2="7" y2="15" stroke="#1a2233" stroke-width="2" stroke-linecap="round"/>'
    '<line x1="12" y1="21" x2="12" y2="12" stroke="#38bdf8" stroke-width="2" stroke-linecap="round"/>'
    '<line x1="17" y1="21" x2="17" y2="14" stroke="#1a2233" stroke-width="2" stroke-linecap="round"/>'
    '<line x1="22" y1="21" x2="22" y2="11" stroke="#1a2233" stroke-width="2" stroke-linecap="round"/>'
    '</svg>'
)
ICON_TRAIN = (
    '<svg class="feat-icon" viewBox="0 0 28 28" fill="none">'
    '<rect x="3" y="3" width="22" height="22" rx="3" stroke="#1a2233" stroke-width="1.8"/>'
    '<circle cx="14" cy="13" r="4.5" stroke="#1a2233" stroke-width="1.5"/>'
    '<circle cx="14" cy="13" r="1.8" fill="#38bdf8"/>'
    '<line x1="14" y1="3" x2="14" y2="8.5" stroke="#1a2233" stroke-width="1.5"/>'
    '<line x1="14" y1="17.5" x2="14" y2="25" stroke="#1a2233" stroke-width="1.5"/>'
    '<line x1="3" y1="13" x2="9.5" y2="13" stroke="#1a2233" stroke-width="1.5"/>'
    '<line x1="18.5" y1="13" x2="25" y2="13" stroke="#1a2233" stroke-width="1.5"/>'
    '</svg>'
)
ICON_EVAL = (
    '<svg class="feat-icon" viewBox="0 0 28 28" fill="none">'
    '<rect x="3" y="3" width="22" height="22" rx="2" stroke="#1a2233" stroke-width="1.8"/>'
    '<rect x="6" y="6" width="7" height="7" rx="1" fill="#c8d8e8" stroke="#1a2233" stroke-width="1.2"/>'
    '<rect x="15" y="6" width="7" height="7" rx="1" fill="none" stroke="#1a2233" stroke-width="1.2"/>'
    '<rect x="6" y="15" width="7" height="7" rx="1" fill="none" stroke="#1a2233" stroke-width="1.2"/>'
    '<rect x="15" y="15" width="7" height="7" rx="1" fill="#38bdf8" stroke="#1a2233" stroke-width="1.2"/>'
    '</svg>'
)
ICON_COMPARE = (
    '<svg class="feat-icon" viewBox="0 0 28 28" fill="none">'
    '<rect x="3" y="3" width="22" height="22" rx="2" stroke="#1a2233" stroke-width="1.8"/>'
    '<line x1="3" y1="25" x2="25" y2="3" stroke="#1a2233" stroke-width="1.2" opacity="0.4"/>'
    '<circle cx="8.5" cy="8.5" r="3" fill="#38bdf8" stroke="#1a2233" stroke-width="1"/>'
    '<circle cx="19.5" cy="19.5" r="3" fill="#38bdf8" stroke="#1a2233" stroke-width="1"/>'
    '<circle cx="8.5" cy="19.5" r="3" fill="#c8d8e8" stroke="#1a2233" stroke-width="1"/>'
    '<circle cx="19.5" cy="8.5" r="3" fill="#c8d8e8" stroke="#1a2233" stroke-width="1"/>'
    '</svg>'
)
ICON_PREDICT = (
    '<svg class="feat-icon" viewBox="0 0 28 28" fill="none">'
    '<circle cx="14" cy="14" r="10.5" stroke="#1a2233" stroke-width="1.8"/>'
    '<circle cx="14" cy="14" r="5.5" stroke="#1a2233" stroke-width="1.4"/>'
    '<circle cx="14" cy="14" r="2.2" fill="#38bdf8"/>'
    '<line x1="14" y1="3.5" x2="14" y2="8.5" stroke="#1a2233" stroke-width="1.5"/>'
    '<line x1="14" y1="19.5" x2="14" y2="24.5" stroke="#1a2233" stroke-width="1.5"/>'
    '<line x1="3.5" y1="14" x2="8.5" y2="14" stroke="#1a2233" stroke-width="1.5"/>'
    '<line x1="19.5" y1="14" x2="24.5" y2="14" stroke="#1a2233" stroke-width="1.5"/>'
    '</svg>'
)
ICON_DOWNLOAD = (
    '<svg class="feat-icon" viewBox="0 0 28 28" fill="none">'
    '<rect x="3" y="20" width="22" height="5" rx="2" stroke="#1a2233" stroke-width="1.8"/>'
    '<line x1="14" y1="3" x2="14" y2="18" stroke="#1a2233" stroke-width="2" stroke-linecap="round"/>'
    '<polyline points="8,12 14,19 20,12" stroke="#1a2233" stroke-width="2"'
    ' stroke-linecap="round" stroke-linejoin="round" fill="none"/>'
    '<rect x="19" y="21.5" width="4" height="2" rx="1" fill="#38bdf8"/>'
    '</svg>'
)

CARDS_HTML = (
    '<div class="card-grid">'
    + card(ICON_UPLOAD,   'Upload Data',    'CSV / XLSX upload, Preview data, Missing value report, Duplicate removal.')
    + card(ICON_PREPROC,  'Preprocessing',  'Configure imputation, scaling, encoding. Split train/test (no data leakage).')
    + card(ICON_EDA,      'EDA',            'Histograms, Box plots, Scatter plots, Heatmaps, Target analysis.')
    + card(ICON_TRAIN,    'Train Model',    'Choose algorithm, Tune hyperparameters, Run cross-validation.')
    + card(ICON_EVAL,     'Evaluate',       'Confusion matrix, ROC curve, Feature importance, Full metrics.')
    + card(ICON_COMPARE,  'Compare Models', 'Benchmark all algorithms side-by-side with radar chart.')
    + card(ICON_PREDICT,  'Predict',        'Single sample prediction, Batch CSV upload prediction.')
    + card(ICON_DOWNLOAD, 'Download Model', 'Export complete sklearn Pipeline (.joblib) + metadata (.json).')
    + '</div>'
)
st.markdown(CARDS_HTML, unsafe_allow_html=True)

# ── QUICK START ───────────────────────────────────────────────────────────────
def step(num, text):
    return (
        '<div class="step-card">'
        '<div class="step-bg"></div>'
        '<div class="step-num">' + str(num) + '.</div>'
        '<div class="step-text">' + text + '</div>'
        '</div>'
    )

LIGHTNING = (
    '<svg width="26" height="26" viewBox="0 0 24 24" fill="none">'
    '<path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" fill="#f59e0b" stroke="#d97706" stroke-width="0.8"/>'
    '</svg>'
)

STEPS_HTML = (
    '<div class="section-title">' + LIGHTNING + 'Quick Start</div>'
    '<div class="steps-row">'
    + step(1, "Navigate to <strong>'Upload Data'</strong> on sidebar &amp; load CSV/Excel.")
    + '<div class="step-arrow">&#8594;</div>'
    + step(2, 'Select <strong>target</strong> column and feature columns.')
    + '<div class="step-arrow">&#8594;</div>'
    + step(3, "Configure <strong>'Preprocessing'</strong> (imputation, scaling, encoding).")
    + '<div class="step-arrow">&#8594;</div>'
    + step(4, "Explore your data in <strong>'EDA'</strong>.")
    + '<div class="step-arrow">&#8594;</div>'
    + step(5, "<strong>'Train'</strong> a model and <strong>'Evaluate'</strong> performance.")
    + '<div class="step-arrow">&#8594;</div>'
    + step(6, "<strong>'Compare'</strong> multiple models to find the best one.")
    + '<div class="step-arrow">&#8594;</div>'
    + step(7, "Use <strong>'Predict'</strong> for new data.")
    + '<div class="step-arrow">&#8594;</div>'
    + step(8, "<strong>'Download'</strong> the final pipeline.")
    + '</div>'
)
st.markdown(STEPS_HTML, unsafe_allow_html=True)

# ── MODELS + NETWORK ──────────────────────────────────────────────────────────
NETWORK_SVG = (
    '<svg class="network-svg" viewBox="0 0 480 290" fill="none">'
    '<circle cx="55" cy="145" r="5" fill="#8aa8c0"/>'
    '<circle cx="135" cy="85" r="5" fill="#8aa8c0"/>'
    '<circle cx="135" cy="145" r="5" fill="#8aa8c0"/>'
    '<circle cx="135" cy="205" r="5" fill="#8aa8c0"/>'
    '<circle cx="235" cy="65" r="5" fill="#8aa8c0"/>'
    '<circle cx="235" cy="115" r="5" fill="#8aa8c0"/>'
    '<circle cx="235" cy="165" r="5" fill="#8aa8c0"/>'
    '<circle cx="235" cy="215" r="5" fill="#8aa8c0"/>'
    '<circle cx="335" cy="95" r="5" fill="#8aa8c0"/>'
    '<circle cx="335" cy="145" r="5" fill="#8aa8c0"/>'
    '<circle cx="335" cy="195" r="5" fill="#8aa8c0"/>'
    '<circle cx="415" cy="145" r="8" fill="#5a7a98"/>'
    '<line x1="55" y1="145" x2="135" y2="85" stroke="#8aa8c0" stroke-width="1"/>'
    '<line x1="55" y1="145" x2="135" y2="145" stroke="#8aa8c0" stroke-width="1"/>'
    '<line x1="55" y1="145" x2="135" y2="205" stroke="#8aa8c0" stroke-width="1"/>'
    '<line x1="135" y1="85" x2="235" y2="65" stroke="#8aa8c0" stroke-width="1"/>'
    '<line x1="135" y1="85" x2="235" y2="115" stroke="#8aa8c0" stroke-width="1"/>'
    '<line x1="135" y1="145" x2="235" y2="115" stroke="#8aa8c0" stroke-width="1"/>'
    '<line x1="135" y1="145" x2="235" y2="165" stroke="#8aa8c0" stroke-width="1"/>'
    '<line x1="135" y1="205" x2="235" y2="165" stroke="#8aa8c0" stroke-width="1"/>'
    '<line x1="135" y1="205" x2="235" y2="215" stroke="#8aa8c0" stroke-width="1"/>'
    '<line x1="235" y1="65" x2="335" y2="95" stroke="#8aa8c0" stroke-width="1"/>'
    '<line x1="235" y1="115" x2="335" y2="95" stroke="#8aa8c0" stroke-width="1"/>'
    '<line x1="235" y1="115" x2="335" y2="145" stroke="#8aa8c0" stroke-width="1"/>'
    '<line x1="235" y1="165" x2="335" y2="145" stroke="#8aa8c0" stroke-width="1"/>'
    '<line x1="235" y1="165" x2="335" y2="195" stroke="#8aa8c0" stroke-width="1"/>'
    '<line x1="235" y1="215" x2="335" y2="195" stroke="#8aa8c0" stroke-width="1"/>'
    '<line x1="335" y1="95" x2="415" y2="145" stroke="#8aa8c0" stroke-width="1.5"/>'
    '<line x1="335" y1="145" x2="415" y2="145" stroke="#8aa8c0" stroke-width="1.5"/>'
    '<line x1="335" y1="195" x2="415" y2="145" stroke="#8aa8c0" stroke-width="1.5"/>'
    '</svg>'
)

MODELS_HTML = (
    '<div class="models-wrap">'
    '<div class="models-left">'
    '<div class="models-cols">'
    '<div class="model-group">'
    '<h3>Classification Models</h3>'
    '<ul>'
    '<li>Logistic Regression</li>'
    '<li>Decision Tree</li>'
    '<li>Random Forest</li>'
    '<li>K-Nearest Neighbors</li>'
    '<li>Support Vector Machine</li>'
    '</ul>'
    '</div>'
    '<div class="model-group">'
    '<h3>Regression Models</h3>'
    '<ul>'
    '<li>Linear Regression</li>'
    '<li>Random Forest Regressor</li>'
    '</ul>'
    '</div>'
    '</div>'
    '</div>'
    '<div class="models-right">' + NETWORK_SVG + '</div>'
    '</div>'
)
st.markdown(MODELS_HTML, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
FOOTER = (
    '<div class="footer-note">'
    'random_state=42 &nbsp;&middot;&nbsp; stratify=y for classification &nbsp;&middot;&nbsp; '
    'Train/test split BEFORE preprocessing &nbsp;&middot;&nbsp; Complete pipeline saved with joblib'
    '</div>'
    '<div class="footer-bar">'
    '<span class="footer-bar-left">Copyright &copy; HYPERTUNEML</span>'
    '<span class="footer-bar-right">'
    '<a href="#">About</a>'
    '<a href="#">Basic</a>'
    '<a href="#">Links</a>'
    '&nbsp;'
    '<svg style="vertical-align:middle;" width="20" height="20" viewBox="0 0 24 24" fill="#38bdf8">'
    '<polygon points="12,2 15.09,8.26 22,9.27 17,14.14 18.18,21.02 12,17.77 5.82,21.02 7,14.14 2,9.27 8.91,8.26"/>'
    '</svg>'
    '</span>'
    '</div>'
    '<div class="footer-built">Built with Streamlit (Customized)</div>'
)
st.markdown(FOOTER, unsafe_allow_html=True)
