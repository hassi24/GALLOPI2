import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import streamlit.components.v1 as components
from utils.state import init_state
from utils.helpers import inject_css, topbar, grade_response
from utils.content import LEVELS_BY_ID

st.set_page_config(
    page_title="Practice Arena · Gallopi",
    page_icon="🎙️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

init_state()
inject_css()
topbar(back_href="/")

if not st.session_state.active_scenario:
    st.markdown("""
<div style="text-align:center;padding:40px 20px;">
    <div style="font-size:48px;margin-bottom:16px;">🦄</div>
    <div style="font-size:18px;font-weight:800;margin-bottom:12px;">No level selected!</div>
    <div style="font-size:14px;color:#4a6572;font-weight:600;">Head back to the path and tap a level to begin.</div>
</div>
""", unsafe_allow_html=True)
    if st.button("← Back to Path", use_container_width=True):
        st.switch_page("Home.py")
    st.stop()

level    = LEVELS_BY_ID.get(st.session_state.active_scenario)
if not level:
    st.error("Level not found.")
    st.stop()

questions = level["questions"]
q_index   = st.session_state.arena_q_index
total_q   = len(questions)


# ═══════════════════════════════════════════════════════════
# RESULTS SCREEN
# ═══════════════════════════════════════════════════════════
def show_results():
    scores = st.session_state.arena_scores
    if not scores:
        return

    avg_clarity     = int(sum(s["clarity"]     for s in scores) / len(scores))
    avg_confidence  = int(sum(s["confidence"]  for s in scores) / len(scores))
    avg_vocabulary  = int(sum(s["vocabulary"]  for s in scores) / len(scores))
    avg_conciseness = int(sum(s["conciseness"] for s in scores) / len(scores))
    overall         = int(sum(s["overall"]      for s in scores) / len(scores))
    xp_earned       = int(level["xp"] * (overall / 100))

    all_passed = set()
    for s in scores:
        all_passed.update(s.get("rubric_passed", []))
    all_passed_list = sorted(all_passed)

    all_strengths, all_improvements = [], []
    for s in scores:
        all_strengths.extend(s.get("strengths", []))
        all_improvements.extend(s.get("improvements", []))

    seen_s, seen_i = set(), set()
    uniq_strengths, uniq_improvements = [], []
    for x in all_strengths:
        if x not in seen_s: seen_s.add(x); uniq_strengths.append(x)
    for x in all_improvements:
        if x not in seen_i: seen_i.add(x); uniq_improvements.append(x)

    uniq_strengths    = uniq_strengths[:3]
    uniq_improvements = uniq_improvements[:3]
    tip               = scores[-1].get("tip", "Keep practicing!")

    score_color = "#58cc02" if overall >= 80 else ("#ff9600" if overall >= 60 else "#ff4b4b")
    grade_label = "Excellent! 🌟" if overall >= 80 else ("Good Work! 💪" if overall >= 60 else "Keep Going! 🔄")

    if overall >= 80:
        st.markdown("""
<style>
@keyframes confetti-drop {
    0%   { transform: translateY(-30px) rotate(0deg); opacity:1; }
    100% { transform: translateY(100vh)  rotate(720deg); opacity:0; }
}
.ce { position:fixed; top:-20px; font-size:24px;
      animation: confetti-drop 3.5s ease-in forwards;
      pointer-events:none; z-index:99999; }
</style>
<div class="ce" style="left:5%;animation-delay:0s;">🎉</div>
<div class="ce" style="left:15%;animation-delay:0.3s;">⭐</div>
<div class="ce" style="left:30%;animation-delay:0.6s;">🌟</div>
<div class="ce" style="left:50%;animation-delay:0.2s;">✨</div>
<div class="ce" style="left:65%;animation-delay:0.5s;">🎊</div>
<div class="ce" style="left:80%;animation-delay:0.1s;">💎</div>
<div class="ce" style="left:90%;animation-delay:0.8s;">🏆</div>
""", unsafe_allow_html=True)

    st.markdown(f"""
<div style="background:linear-gradient(135deg,#131f24,#0f1e14);
            border:2px solid {score_color};border-radius:24px;
            padding:24px 20px;margin:0 16px 16px;text-align:center;">
    <div class="unicorn-mascot">🦄</div>
    <div style="font-size:72px;font-weight:900;color:{score_color};line-height:1;
                text-shadow:0 0 30px {score_color}88;">{overall}</div>
    <div style="font-size:12px;color:#4a6572;font-weight:700;margin:-4px 0 8px;">OVERALL SCORE</div>
    <div style="font-size:20px;font-weight:900;">{grade_label}</div>
    <div style="margin-top:12px;padding:8px 20px;background:#ffd70022;
                border:1px solid #ffd70044;border-radius:50px;display:inline-block;">
        <span style="font-size:14px;font-weight:800;color:#ffd700;">🏆 +{xp_earned} XP earned!</span>
    </div>
</div>
""", unsafe_allow_html=True)

    metrics = [
        ("🎯 Clarity",     avg_clarity,     "#1cb0f6"),
        ("💪 Confidence",  avg_confidence,  "#ff9600"),
        ("📚 Vocabulary",  avg_vocabulary,  "#a346ff"),
        ("✂️ Conciseness", avg_conciseness, "#58cc02"),
    ]
    cols = st.columns(2)
    for i, (label, val, color) in enumerate(metrics):
        with cols[i % 2]:
            st.markdown(f"""
<div style="background:#131f24;border:2px solid #203038;border-radius:16px;
            padding:14px 12px;margin-bottom:10px;">
    <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
        <span style="font-size:12px;font-weight:700;">{label}</span>
        <span style="font-size:14px;font-weight:900;color:{color};">{val}</span>
    </div>
    <div style="background:#203038;border-radius:50px;height:10px;overflow:hidden;">
        <div style="background:{color};width:{val}%;height:100%;border-radius:50px;
                    box-shadow:0 0 8px {color}66;"></div>
    </div>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div style="font-size:12px;font-weight:800;color:#4a6572;text-transform:uppercase;letter-spacing:1.8px;padding:0 16px 10px;margin-top:4px;">📊 Detailed Feedback</div>', unsafe_allow_html=True)
    col_s, col_i = st.columns(2)
    with col_s:
        items_html = "".join(f'<div style="font-size:12px;font-weight:600;color:#e8f4f8;margin-bottom:6px;line-height:1.4;">• {s}</div>' for s in uniq_strengths)
        st.markdown(f'<div style="background:#0f2a0f;border:2px solid #58cc0244;border-radius:16px;padding:14px;margin-bottom:10px;"><div style="font-size:12px;font-weight:800;color:#58cc02;margin-bottom:8px;">✅ STRENGTHS</div>{items_html}</div>', unsafe_allow_html=True)
    with col_i:
        items_html = "".join(f'<div style="font-size:12px;font-weight:600;color:#e8f4f8;margin-bottom:6px;line-height:1.4;">• {imp}</div>' for imp in uniq_improvements)
        st.markdown(f'<div style="background:#2a1010;border:2px solid #ff4b4b44;border-radius:16px;padding:14px;margin-bottom:10px;"><div style="font-size:12px;font-weight:800;color:#ff7b7b;margin-bottom:8px;">🔧 IMPROVE</div>{items_html}</div>', unsafe_allow_html=True)

    st.markdown('<div style="font-size:12px;font-weight:800;color:#4a6572;text-transform:uppercase;letter-spacing:1.8px;padding:0 16px 10px;">📋 Checklist</div>', unsafe_allow_html=True)
    for idx, item in enumerate(level["rubric_items"]):
        passed = idx in all_passed_list
        icon   = "✅" if passed else "❌"
        color  = "#e8f4f8" if passed else "#ff7b7b"
        border = "#58cc0244" if passed else "#ff4b4b44"
        bg     = "#0f2a0f" if passed else "#2a1010"
        st.markdown(f'<div style="background:{bg};border:1.5px solid {border};border-radius:12px;padding:10px 14px;margin:0 16px 8px;display:flex;align-items:center;gap:10px;"><span style="font-size:16px;">{icon}</span><span style="font-size:13px;font-weight:600;color:{color};">{item}</span></div>', unsafe_allow_html=True)

    st.markdown(f"""
<div style="background:#0d1e26;border:2px solid #1cb0f6;border-radius:20px;
            padding:18px;margin:16px 16px;">
    <div style="font-size:13px;font-weight:800;color:#1cb0f6;margin-bottom:8px;">💡 Gallopi's Coaching Tip</div>
    <div style="font-size:14px;font-weight:600;line-height:1.6;">{tip}</div>
</div>
""", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🔄 Try Again", use_container_width=True):
            st.session_state.arena_q_index      = 0
            st.session_state.arena_answers      = []
            st.session_state.arena_show_results = False
            st.session_state.arena_scores       = None
            st.rerun()
    with col_b:
        if st.button("🏠 Back to Path", use_container_width=True):
            if overall >= 60:
                lid = st.session_state.active_scenario
                if lid not in st.session_state.completed_levels:
                    st.session_state.completed_levels.append(lid)
                    if lid == st.session_state.current_level:
                        st.session_state.current_level = lid + 1
                st.session_state.xp += xp_earned
                if st.session_state.energy > 0:
                    st.session_state.energy -= 1
                # Update streak
                st.session_state.streak += 1
                # Add to history
                st.session_state.session_history.insert(0, {
                    "level": level["title"],
                    "icon":  level["icon"],
                    "score": overall,
                    "xp":    xp_earned,
                    "date":  "Today"
                })
            st.session_state.active_scenario = None
            st.switch_page("Home.py")


# ═══════════════════════════════════════════════════════════
# ROUTER
# ═══════════════════════════════════════════════════════════
if st.session_state.arena_show_results and st.session_state.arena_scores:
    show_results()
    st.stop()

if q_index >= total_q:
    all_scores = []
    for idx, ans in enumerate(st.session_state.arena_answers):
        q_data = questions[idx]
        score  = grade_response(ans, q_data["keywords"], q_data["forbidden"])
        all_scores.append(score)
    st.session_state.arena_scores       = all_scores
    st.session_state.arena_show_results = True
    st.rerun()


# ═══════════════════════════════════════════════════════════
# QUESTION SCREEN
# ═══════════════════════════════════════════════════════════
current_q   = questions[q_index]
diff_colors = {"Beginner":"#58cc02","Intermediate":"#ff9600","Advanced":"#a346ff","Expert":"#ffd700"}
diff_color  = diff_colors.get(level["difficulty"], "#4a6572")

progress_pct = int((q_index / total_q) * 100)
st.markdown(f"""
<div style="padding:0 16px 16px;">
    <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
        <span style="font-size:12px;font-weight:700;color:#4a6572;">Question {q_index+1} of {total_q}</span>
        <span style="font-size:12px;font-weight:800;color:#58cc02;">{progress_pct}%</span>
    </div>
    <div style="background:#203038;border-radius:50px;height:10px;overflow:hidden;">
        <div style="background:linear-gradient(90deg,#1cb0f6,#58cc02);
                    width:{progress_pct}%;height:100%;border-radius:50px;"></div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="background:#131f24;border:2px solid #1cb0f6;border-radius:20px;
            padding:18px;margin:0 16px 16px;">
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
        <div style="font-size:40px;">{level['icon']}</div>
        <div>
            <div style="font-size:20px;font-weight:900;">{level['title']}</div>
            <div style="display:flex;gap:8px;margin-top:4px;flex-wrap:wrap;">
                <span style="background:{diff_color}22;color:{diff_color};border:1px solid {diff_color}44;
                             padding:3px 10px;border-radius:50px;font-size:11px;font-weight:800;">
                    {level['difficulty']}
                </span>
                <span style="background:#ffd70022;color:#ffd700;border:1px solid #ffd70044;
                             padding:3px 10px;border-radius:50px;font-size:11px;font-weight:800;">
                    +{level['xp']} XP
                </span>
            </div>
        </div>
    </div>
    <div style="font-size:12px;font-weight:800;color:#4a6572;text-transform:uppercase;
                letter-spacing:1.2px;margin-bottom:6px;">🎭 SCENARIO</div>
    <div style="font-size:13px;font-weight:600;line-height:1.6;color:#c8dde8;
                background:#0b141a;border-radius:12px;padding:12px;border:1px solid #203038;">
        {level['scenario']}
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="background:#1a2f3a;border:2px solid #1cb0f6;border-radius:20px;
            padding:18px;margin:0 16px 16px;">
    <div style="font-size:12px;font-weight:800;color:#1cb0f6;text-transform:uppercase;
                letter-spacing:1.2px;margin-bottom:10px;">🎙️ CHALLENGE {q_index+1}</div>
    <div style="font-size:16px;font-weight:800;line-height:1.5;margin-bottom:10px;">{current_q['q']}</div>
    <div style="background:#0b141a;border-radius:10px;padding:10px 12px;border-left:3px solid #ff9600;">
        <span style="font-size:11px;font-weight:700;color:#ff9600;">💡 HINT: </span>
        <span style="font-size:12px;font-weight:600;color:#8a9baa;">{current_q['hint']}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# VOICE RECORDER  (pure browser Web Speech API — no Python lib)
# The component renders a mic button; when the user finishes,
# it writes the transcript to a hidden <textarea> which we read
# back via a Streamlit text_area with the same key.
# ═══════════════════════════════════════════════════════════

voice_component = f"""
<!DOCTYPE html>
<html>
<head>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: transparent; font-family: 'Nunito', 'Segoe UI', sans-serif; }}

  #card {{
    background: #131f24; border: 2px solid #1cb0f6;
    border-radius: 18px; padding: 18px 16px 16px;
    text-align: center;
  }}
  #title {{
    font-size: 12px; font-weight: 800; color: #4a6572;
    text-transform: uppercase; letter-spacing: 1.5px;
    margin-bottom: 14px;
  }}

  #mic-btn {{
    width: 80px; height: 80px; border-radius: 50%;
    background: #58cc02; border: none;
    box-shadow: 0 5px 0 #46a302;
    font-size: 34px; cursor: pointer;
    display: inline-flex; align-items: center; justify-content: center;
    transition: transform .1s, box-shadow .1s;
    margin-bottom: 12px;
  }}
  #mic-btn.recording {{
    background: #ff4b4b !important;
    box-shadow: 0 5px 0 #cc3333 !important;
    animation: pulse 1.2s ease-in-out infinite;
  }}
  #mic-btn:active {{ transform: translateY(3px); box-shadow: 0 2px 0 #46a302; }}
  @keyframes pulse {{
    0%,100% {{ box-shadow: 0 5px 0 #cc3333, 0 0 0 0 rgba(255,75,75,0.5); }}
    50%      {{ box-shadow: 0 5px 0 #cc3333, 0 0 0 18px rgba(255,75,75,0); }}
  }}

  #status {{ font-size:13px; font-weight:700; color:#4a6572; margin-bottom:4px; }}
  #timer  {{ font-size:26px; font-weight:900; color:#1cb0f6; min-height:34px; font-variant-numeric:tabular-nums; }}

  #wave {{ display:flex; align-items:center; justify-content:center; gap:4px;
            height:36px; margin:8px 0; visibility:hidden; }}
  .bar {{ width:5px; border-radius:3px; background:#1cb0f6;
          animation: wave .9s ease-in-out infinite; }}
  @keyframes wave {{
    0%,100% {{ height:5px; opacity:.35; }}
    50%      {{ height:30px; opacity:1; }}
  }}

  #live-text {{
    background:#0b141a; border:2px solid #203038; border-radius:12px;
    padding:10px 12px; font-size:13px; font-weight:600; color:#c8dde8;
    min-height:52px; text-align:left; line-height:1.6;
    margin:10px 0 4px; display:none; word-break:break-word;
  }}

  #use-btn {{
    width:100%; background:#58cc02; color:#fff; border:none;
    border-radius:14px; font-size:15px; font-weight:800;
    padding:12px; box-shadow:0 4px 0 #46a302; cursor:pointer;
    margin-top:12px; transition:transform .1s, box-shadow .1s;
    display:none;
  }}
  #use-btn:active {{ transform:translateY(3px); box-shadow:0 1px 0 #46a302; }}
  #use-btn.sent {{ background:#1cb0f6; box-shadow:0 4px 0 #1899d6; }}

  #no-support {{
    color:#ff9600; font-size:12px; font-weight:700;
    background:#2a1a00; border-radius:10px; padding:8px 12px;
    margin-top:8px; display:none;
  }}
  #tip {{
    font-size:10px; color:#3c5566; font-weight:600; margin-top:10px;
  }}

  /* hidden bridge textarea */
  #bridge {{ display:none; }}
</style>
</head>
<body>
<div id="card">
  <div id="title">🎙️ Voice Recorder</div>
  <button id="mic-btn" onclick="toggle()">🎙️</button>
  <div id="status">Tap the mic to start recording</div>
  <div id="timer"></div>
  <div id="wave">
    {''.join(f'<div class="bar" style="animation-delay:{i*0.11:.2f}s"></div>' for i in range(10))}
  </div>
  <div id="live-text"></div>
  <div id="no-support">⚠️ Speech recognition not available in this browser. Use Chrome or Edge, or type below.</div>
  <button id="use-btn" onclick="send()">✅ Use This Response</button>
  <div id="tip">Works best in Chrome / Edge · Safari not supported</div>
</div>
<textarea id="bridge"></textarea>

<script>
const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
let rec = null, running = false, tick = null, secs = 0, transcript = "";

const micBtn   = document.getElementById("mic-btn");
const statusEl = document.getElementById("status");
const timerEl  = document.getElementById("timer");
const waveEl   = document.getElementById("wave");
const liveEl   = document.getElementById("live-text");
const useBtn   = document.getElementById("use-btn");
const noSup    = document.getElementById("no-support");
const bridge   = document.getElementById("bridge");

function fmt(s) {{
  return String(Math.floor(s/60)).padStart(2,"0")+":"+String(s%60).padStart(2,"0");
}}

function toggle() {{
  if (running) stop(); else start();
}}

function start() {{
  if (!SpeechRec) {{ noSup.style.display="block"; return; }}
  transcript = "";
  liveEl.textContent = "";
  liveEl.style.display = "none";
  useBtn.style.display = "none";
  useBtn.classList.remove("sent");

  rec = new SpeechRec();
  rec.continuous      = true;
  rec.interimResults  = true;
  rec.lang            = "en-US";
  rec.maxAlternatives = 1;

  rec.onresult = (e) => {{
    let final = "", interim = "";
    for (let i = e.resultIndex; i < e.results.length; i++) {{
      if (e.results[i].isFinal) final += e.results[i][0].transcript + " ";
      else interim += e.results[i][0].transcript;
    }}
    transcript = (transcript + final).trimStart();
    liveEl.textContent = transcript + interim;
    liveEl.style.display = "block";
  }};

  rec.onerror = (e) => {{
    if (e.error === "not-allowed" || e.error === "service-not-allowed") {{
      noSup.style.display = "block";
      statusEl.textContent = "Mic access denied — please allow microphone and reload.";
    }} else {{
      statusEl.textContent = "Error: " + e.error + " — try again.";
    }}
    stop();
  }};

  rec.onend = () => {{ if (running) rec.start(); }}; // keep alive

  rec.start();
  running = true;
  secs = 0;
  micBtn.classList.add("recording");
  micBtn.textContent = "⏹️";
  statusEl.textContent = "Recording… speak now!";
  waveEl.style.visibility = "visible";
  timerEl.textContent = fmt(0);
  tick = setInterval(() => {{ secs++; timerEl.textContent = fmt(secs); }}, 1000);
}}

function stop() {{
  running = false;
  if (rec) {{ rec.onend = null; rec.stop(); rec = null; }}
  clearInterval(tick);
  micBtn.classList.remove("recording");
  micBtn.textContent = "🎙️";
  waveEl.style.visibility = "hidden";

  if (transcript && transcript.trim().length > 2) {{
    statusEl.textContent = "✅ Done! Tap 'Use This Response' to submit.";
    liveEl.textContent   = transcript.trim();
    liveEl.style.display = "block";
    useBtn.style.display = "block";
    useBtn.textContent   = "✅ Use This Response";
  }} else {{
    statusEl.textContent = "No speech detected — tap mic to try again, or type below.";
  }}
}}

function send() {{
  const text = transcript.trim();
  if (!text) return;
  bridge.value = text;
  // Post to parent Streamlit frame
  window.parent.postMessage({{ type: "gallopiVoice", text: text, q: {q_index} }}, "*");
  useBtn.textContent = "✅ Sent! Scroll down and submit ↓";
  useBtn.classList.add("sent");
  statusEl.textContent = "Voice captured — now click Submit below ↓";
}}
</script>
</body>
</html>
"""

# Render the voice recorder iframe
components.html(voice_component, height=380, scrolling=False)

# JS bridge: listen for the postMessage and fill the Streamlit textarea
st.markdown("""
<script>
window.addEventListener("message", function(ev) {
    if (!ev.data || ev.data.type !== "gallopiVoice") return;
    const text = ev.data.text;
    // Find the first visible textarea in the Streamlit app and fill it
    const allTA = window.parent.document.querySelectorAll('textarea');
    allTA.forEach(function(ta) {
        if (ta.offsetParent !== null) {   // visible
            const setter = Object.getOwnPropertyDescriptor(
                window.HTMLTextAreaElement.prototype, "value"
            ).set;
            setter.call(ta, text);
            ta.dispatchEvent(new Event("input", { bubbles: true }));
        }
    });
});
</script>
""", unsafe_allow_html=True)

st.markdown('<div style="padding:0 16px 6px;"><div style="font-size:12px;font-weight:800;color:#4a6572;text-transform:uppercase;letter-spacing:1.5px;">📝 Response (voice fills this automatically)</div></div>', unsafe_allow_html=True)

user_response = st.text_area(
    "Response",
    height=130,
    placeholder="Voice transcript appears here after you record… or type your answer directly.",
    label_visibility="collapsed",
    key=f"response_{q_index}",
)

with st.expander("🔍 Power words for this question"):
    kw_pills = "".join(
        f'<span style="background:#1cb0f633;color:#1cb0f6;padding:4px 10px;'
        f'border-radius:50px;font-size:12px;font-weight:700;margin:3px;display:inline-block;">{kw}</span>'
        for kw in current_q["keywords"][:8]
    )
    st.markdown(f'<div style="padding:6px 0;display:flex;flex-wrap:wrap;gap:4px;">{kw_pills}</div>', unsafe_allow_html=True)

st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)

col_sub, col_skip = st.columns([3, 1])
with col_sub:
    btn_label = "✅ Submit & See Results" if q_index == total_q - 1 else f"Submit → Q{q_index + 2}"
    if st.button(btn_label, use_container_width=True):
        if user_response.strip():
            st.session_state.arena_answers.append(user_response.strip())
            st.session_state.arena_q_index += 1
            st.rerun()
        else:
            st.warning("🎙️ Record your voice or type a response first!")

with col_skip:
    if st.button("Skip ›", use_container_width=True):
        st.session_state.arena_answers.append("[Skipped]")
        st.session_state.arena_q_index += 1
        st.rerun()

if st.session_state.arena_answers:
    st.markdown(f'<div style="font-size:11px;color:#4a6572;font-weight:700;text-align:center;margin-top:8px;">✅ {len(st.session_state.arena_answers)} of {total_q} answered</div>', unsafe_allow_html=True)

st.markdown('<div style="height:30px;"></div>', unsafe_allow_html=True)
