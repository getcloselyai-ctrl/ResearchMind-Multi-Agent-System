import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

st.set_page_config(
    page_title="ResearchMind · AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Premium dark/orange UI ───────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --orange: #ff8c32;
    --orange-light: #ffad62;
    --text: #f0ebe0;
    --muted: #a09890;
    --green: #50c878;
    --border: rgba(255,255,255,.08);
}
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; color:var(--text); }
.stApp {
    background:#09090e;
    background-image:
      radial-gradient(ellipse 70% 45% at 15% 0%,rgba(255,140,50,.14),transparent 65%),
      radial-gradient(ellipse 60% 40% at 90% 100%,rgba(255,80,30,.10),transparent 65%),
      radial-gradient(ellipse 50% 35% at 50% 50%,rgba(90,65,120,.05),transparent 75%);
    background-attachment:fixed;
}
#MainMenu,footer,header { visibility:hidden; }
.block-container { padding:2rem 3rem 4rem; max-width:1250px; }

@keyframes fadeUp {
  from { opacity:0; transform:translateY(14px); }
  to { opacity:1; transform:translateY(0); }
}
@keyframes glow {
  0%,100% { box-shadow:0 0 12px rgba(255,140,50,.08); }
  50% { box-shadow:0 0 24px rgba(255,140,50,.18); }
}
@keyframes pulse { 0%,100%{opacity:1;} 50%{opacity:.45;} }

.hero {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    text-align: center !important;
    padding: 4rem 0 3rem;
    animation: fadeUp .8s ease both;
}
.hero-eyebrow {
    display: inline-block;
    font: 500 .7rem 'DM Mono', monospace;
    letter-spacing: .25em;
    text-transform: uppercase;
    color: var(--orange);
    padding: .55rem 1rem;
    border: 1px solid rgba(255,140,50,.25);
    border-radius: 30px;
    background: rgba(255,140,50,.06);
    margin-bottom: 1.5rem;
}
.hero h1 {
    font: 800 clamp(3rem,7vw,5.5rem)/1 'Syne', sans-serif;
    letter-spacing: -.055em;
    color: var(--text);
    margin: 0 0 1.2rem;
}
.hero h1 span {
    color: var(--orange);
    text-shadow: 0 0 35px rgba(255,140,50,.25);
}
.hero-sub,
.hero p.hero-sub {
    display: block;
    font-size: 1.02rem;
    font-weight: 300;
    color: var(--muted);
    width: 100% !important;
    max-width: 100% !important;
    margin: 0 auto !important;
    align-self: center !important;
    line-height: 1.8;
    text-align: center !important;
    position: static !important;
    transform: none !important;
}
.divider {
    height: 1px;
    margin: 2.3rem 0;
    background: linear-gradient(
        90deg,
        transparent,
        rgba(255,140,50,.35),
        rgba(255,255,255,.08),
        rgba(255,140,50,.35),
        transparent
    );
}

.stTextInput>div>div>input {
  background:rgba(255,255,255,.045)!important;
  border:1px solid rgba(255,140,50,.22)!important;
  border-radius:12px!important; color:var(--text)!important;
  font:1rem 'DM Sans',sans-serif!important; padding:.85rem 1rem!important;
  min-height:3.2rem; transition:all .25s ease!important;
}
.stTextInput>div>div>input:focus {
  border-color:var(--orange)!important;
  box-shadow:0 0 0 3px rgba(255,140,50,.12),0 0 22px rgba(255,140,50,.08)!important;
}
.stTextInput>label {
  font:500 .72rem 'DM Mono',monospace!important;
  letter-spacing:.15em!important; text-transform:uppercase!important;
  color:var(--orange)!important; margin-bottom:.7rem!important;
}
.stButton>button {
  background:linear-gradient(120deg,#ff9b45,#ff681f 55%,#f34d18)!important;
  color:#100c09!important; font:800 .95rem 'Syne',sans-serif!important;
  letter-spacing:.035em!important; border:1px solid rgba(255,190,120,.3)!important;
  border-radius:12px!important; padding:.85rem 1.5rem!important;
  min-height:3.1rem; transition:all .25s ease!important;
  box-shadow:0 5px 22px rgba(255,100,30,.2)!important; width:100%;
}
.stButton>button:hover {
  transform:translateY(-3px)!important;
  box-shadow:0 10px 32px rgba(255,100,30,.34)!important; filter:brightness(1.08);
}
.stButton>button:active { transform:scale(.985)!important; }
.section-heading {
  font:800 1.4rem 'Syne',sans-serif; color:var(--text);
  margin:1.5rem 0 1.2rem; letter-spacing:-.025em;
}
.step-card {
  background:linear-gradient(135deg,rgba(255,255,255,.045),rgba(255,255,255,.012));
  border:1px solid var(--border); border-radius:16px; padding:1.45rem 1.6rem;
  margin-bottom:1rem; position:relative; overflow:hidden;
  transition:all .3s ease; animation:fadeUp .5s ease both;
}
.step-card:hover { transform:translateX(4px); border-color:rgba(255,140,50,.22); }
.step-card.active {
  border-color:rgba(255,140,50,.48);
  background:linear-gradient(110deg,rgba(255,140,50,.10),rgba(255,140,50,.025));
  animation:glow 2.2s infinite;
}
.step-card.done {
  border-color:rgba(80,200,120,.3);
  background:linear-gradient(110deg,rgba(80,200,120,.075),rgba(80,200,120,.015));
}
.step-card:before {
  content:''; position:absolute; left:0; top:0; bottom:0; width:3px;
  background:rgba(255,255,255,.06);
}
.step-card.active:before { background:var(--orange); }
.step-card.done:before { background:var(--green); }
.step-header { display:flex; align-items:center; gap:.8rem; margin-bottom:.35rem; }
.step-num { font:500 .7rem 'DM Mono',monospace; letter-spacing:.15em; color:var(--orange); }
.step-title { font:700 .98rem 'Syne',sans-serif; color:var(--text); }
.step-status { margin-left:auto; font: .65rem 'DM Mono',monospace; letter-spacing:.1em; }
.status-waiting { color:#66616a; }
.status-running { color:var(--orange); animation:pulse 1.5s infinite; }
.status-done { color:var(--green); }

.result-panel {
  background:rgba(255,255,255,.025); border:1px solid var(--border);
  border-radius:16px; padding:1.8rem 2rem; margin:1rem 0 1.5rem;
}
.result-panel-title {
  font:500 .7rem 'DM Mono',monospace; letter-spacing:.2em;
  text-transform:uppercase; color:var(--orange); margin-bottom:1rem;
  padding-bottom:.8rem; border-bottom:1px solid rgba(255,140,50,.15);
}
.result-content {
  font-size:.9rem; line-height:1.85; color:#cdc8bf;
  white-space:pre-wrap; font-family:'DM Sans',sans-serif; overflow-wrap:anywhere;
}
.report-panel {
  background:linear-gradient(145deg,rgba(255,140,50,.055),rgba(255,255,255,.018));
  border:1px solid rgba(255,140,50,.24); border-radius:20px;
  padding:2.2rem 2.5rem; margin-top:1rem; box-shadow:0 15px 45px rgba(0,0,0,.18);
}
.report-panel h1,.report-panel h2,.report-panel h3 {
  font-family:'Syne',sans-serif; color:var(--text); letter-spacing:-.025em;
}
.report-panel p,.report-panel li { color:#d0cbc3; line-height:1.85; }
.report-panel strong { color:#ffb16c; }
.report-panel a { color:var(--orange-light); }
.feedback-panel {
  background:linear-gradient(145deg,rgba(80,200,120,.055),rgba(255,255,255,.015));
  border:1px solid rgba(80,200,120,.24); border-radius:20px;
  padding:2rem 2.5rem; margin-top:1.3rem;
}
.panel-label {
  font: .7rem 'DM Mono',monospace; letter-spacing:.2em;
  text-transform:uppercase; margin-bottom:1.2rem; padding-bottom:.8rem;
}
.panel-label.orange { color:var(--orange); border-bottom:1px solid rgba(255,140,50,.18); }
.panel-label.green { color:var(--green); border-bottom:1px solid rgba(80,200,120,.18); }
.stDownloadButton>button {
  background:rgba(255,140,50,.08)!important;
  border:1px solid rgba(255,140,50,.35)!important; border-radius:10px!important;
  color:#ffad62!important; font:.78rem 'DM Mono',monospace!important;
  transition:all .25s ease!important;
}
.stDownloadButton>button:hover {
  background:rgba(255,140,50,.16)!important; border-color:var(--orange)!important;
  transform:translateY(-2px);
}
details {
  border:1px solid rgba(255,255,255,.07)!important; border-radius:12px!important;
  background:rgba(255,255,255,.018)!important; margin-bottom:.7rem!important;
}
details summary {
  font:.75rem 'DM Mono',monospace!important; color:#c1b7aa!important;
  letter-spacing:.08em!important; padding:.5rem!important;
}
details summary:hover { color:var(--orange)!important; }
.stSpinner>div { color:var(--orange)!important; }
.stAlert { border-radius:12px!important; }
.notice {
  font:.68rem 'DM Mono',monospace; color:#625b55; text-align:center;
  margin-top:3.5rem; padding-top:1.5rem;
  border-top:1px solid rgba(255,255,255,.06); letter-spacing:.09em;
}
@media(max-width:768px) {
  .block-container { padding:1rem 1rem 2.5rem; }
  .hero { padding:2.5rem 0 1.8rem; }
  .hero h1 { font-size:3rem; }
  .input-card,.report-panel,.feedback-panel { padding:1.4rem; }
  .step-card { padding:1.2rem; }
}
@media(prefers-reduced-motion:reduce) {
  *,*:before,*:after { animation-duration:.01ms!important; transition-duration:.01ms!important; }
}
</style>
""", unsafe_allow_html=True)


# ── Helper: render a pipeline step card ───────────────────────────────────────
def step_card(num: str, title: str, state: str, desc: str = ""):
    status_map = {
        "waiting": ("WAITING", "status-waiting"),
        "running": ("● RUNNING", "status-running"),
        "done": ("✓ DONE", "status-done"),
    }
    label, cls = status_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done"}.get(state, "")

    st.markdown(f"""
    <div class="step-card {card_cls}">
        <div class="step-header">
            <span class="step-num">{num}</span>
            <span class="step-title">{title}</span>
            <span class="step-status {cls}">{label}</span>
        </div>
        {"<div style='font-size:0.82rem;color:#898078;margin-top:0.3rem;'>"+desc+"</div>" if desc else ""}
    </div>
    """, unsafe_allow_html=True)


# ── Session state initialization ──────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">✦ Multi-Agent Intelligence System</div>
    <h1>Research<span>Mind</span></h1>
    <p class="hero-sub">
        From a single question to a comprehensive research report.
        Let intelligent agents search, analyze, write and review.
    </p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ── Input and pipeline layout ─────────────────────────────────────────────────
col_input, col_spacer, col_pipeline = st.columns([5, 0.5, 4])

with col_input:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)

    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        key="topic_input",
        label_visibility="visible",
    )

    run_btn = st.button("⚡  Run Research Pipeline", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="display:flex;gap:.5rem;flex-wrap:wrap;margin-bottom:1.5rem;">
        <span style="font-family:'DM Mono',monospace;font-size:.68rem;color:#77706a;letter-spacing:.1em;">TRY →</span>
    """, unsafe_allow_html=True)

    examples = ["LLM agents 2025", "CRISPR gene editing", "Fusion energy progress"]
    for ex in examples:
        st.markdown(f"""
        <span style="
            display:inline-block;background:rgba(255,255,255,.04);
            border:1px solid rgba(255,255,255,.08);border-radius:7px;
            padding:.35rem .75rem;margin:.15rem .1rem;font-size:.75rem;
            color:#b4aaa0;font-family:'DM Sans',sans-serif;
        ">{ex}</span>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


with col_pipeline:
    st.markdown('<div class="section-heading">Pipeline</div>', unsafe_allow_html=True)
    r = st.session_state.results

    def get_step_state(step):
        if not r:
            return "waiting"

        steps = ["search", "reader", "writer", "critic"]

        if step in r:
            return "done"

        if st.session_state.running:
            for current_step in steps:
                if current_step not in r:
                    return "running" if current_step == step else "waiting"

        return "waiting"

    step_card("01", "Search Agent", get_step_state("search"), "Gathers recent web information")
    step_card("02", "Reader Agent", get_step_state("reader"), "Scrapes & extracts deep content")
    step_card("03", "Writer Chain", get_step_state("writer"), "Drafts the full research report")
    step_card("04", "Critic Chain", get_step_state("critic"), "Reviews & scores the report")


# ── Start research ────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()


# ── Execute the existing four-stage agent pipeline ────────────────────────────
if st.session_state.running and not st.session_state.done:
    results = {}
    topic_val = st.session_state.topic_input

    try:
        # Step 1: Search Agent
        with st.spinner("🔍  Search Agent is working…"):
            search_agent = build_search_agent()
            sr = search_agent.invoke({
                "messages": [
                    ("user", f"Find recent, reliable and detailed information about: {topic_val}")
                ]
            })
            results["search"] = sr["messages"][-1].content
            st.session_state.results = dict(results)

        # Step 2: Reader Agent
        with st.spinner("📄  Reader Agent is scraping top resources…"):
            reader_agent = build_reader_agent()
            rr = reader_agent.invoke({
                "messages": [
                    (
                        "user",
                        f"Based on the following search results about '{topic_val}', "
                        f"pick the most relevant URL and scrape it for deeper content.\n\n"
                        f"Search Results:\n{results['search'][:800]}"
                    )
                ]
            })
            results["reader"] = rr["messages"][-1].content
            st.session_state.results = dict(results)

        # Step 3: Writer Chain
        with st.spinner("✍️  Writer is drafting the report…"):
            research_combined = (
                f"SEARCH RESULTS:\n{results['search']}\n\n"
                f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
            )
            results["writer"] = writer_chain.invoke({
                "topic": topic_val,
                "research": research_combined
            })
            st.session_state.results = dict(results)

        # Step 4: Critic Chain
        with st.spinner("🧐  Critic is reviewing the report…"):
            results["critic"] = critic_chain.invoke({
                "report": results["writer"]
            })
            st.session_state.results = dict(results)

        st.session_state.running = False
        st.session_state.done = True
        st.rerun()

    except Exception as exc:
        st.session_state.running = False
        st.error(
            "The research pipeline could not complete. "
            "Check your API quota, API key, model availability, and terminal traceback."
        )
        st.exception(exc)


# ── Results display ───────────────────────────────────────────────────────────
r = st.session_state.results

if r:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Research Results</div>', unsafe_allow_html=True)

    if "search" in r:
        with st.expander("🔍  Search Results (raw)", expanded=False):
            st.markdown(
                '<div class="result-panel"><div class="result-panel-title">'
                'Search Agent Output</div>'
                f'<div class="result-content">{r["search"]}</div></div>',
                unsafe_allow_html=True
            )

    if "reader" in r:
        with st.expander("📄  Scraped Content (raw)", expanded=False):
            st.markdown(
                '<div class="result-panel"><div class="result-panel-title">'
                'Reader Agent Output</div>'
                f'<div class="result-content">{r["reader"]}</div></div>',
                unsafe_allow_html=True
            )

    if "writer" in r:
        st.markdown("""
        <div class="report-panel">
            <div class="panel-label orange">📝 Final Research Report</div>
        """, unsafe_allow_html=True)

        st.markdown(r["writer"])
        st.markdown("</div>", unsafe_allow_html=True)

        st.download_button(
            label="⬇  Download Report (.md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    if "critic" in r:
        st.markdown("""
        <div class="feedback-panel">
            <div class="panel-label green">🧐 Critic Feedback</div>
        """, unsafe_allow_html=True)

        st.markdown(r["critic"])
        st.markdown("</div>", unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="notice">
    ResearchMind · Powered by LangChain multi-agent pipeline · Built with Streamlit
</div>
""", unsafe_allow_html=True)