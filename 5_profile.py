import streamlit as st

st.set_page_config(page_title="Profile · Gallopi", page_icon="👤",
                   layout="centered", initial_sidebar_state="collapsed")

defaults = {
    "nickname": "Learner", "avatar": "🐴", "streak": 7, "xp": 1240,
    "gems": 85, "energy": 4, "completed_levels": [1, 2, 3],
    "focus_areas": ["Interview Prep 🎤", "Public Speaking 🎙️"],
    "current_level": 4,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');
*, *::before, *::after { box-sizing:border-box; }
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background:#0b141a !important; font-family:'Nunito',sans-serif !important; color:#e8f4f8;
}
#MainMenu, footer, header, [data-testid="stSidebar"], [data-testid="collapsedControl"] { display:none !important; }
.top-bar {
    position:fixed; top:0; left:50%; transform:translateX(-50%);
    width:100%; max-width:480px; background:#0b141a;
    border-bottom:2px solid #203038; padding:10px 20px;
    display:flex; align-items:center; justify-content:space-between; z-index:9999; font-weight:800;
}
.main-wrap { max-width:480px; margin:0 auto; padding:72px 16px 20px; }
.g-card { background:#131f24; border:2px solid #203038; border-radius:20px; padding:20px; margin-bottom:14px; }
.section-header { font-size:13px; font-weight:800; color:#4a6572; text-transform:uppercase; letter-spacing:1.5px; margin:20px 0 12px; }
div[data-testid="stButton"] > button {
    background:#131f24 !important; color:#e8f4f8 !important; border:2px solid #203038 !important;
    border-radius:16px !important; font-family:'Nunito',sans-serif !important;
    font-weight:800 !important; font-size:16px !important; padding:14px 28px !important;
    box-shadow:0 4px 0 #0b141a !important; width:100% !important;
    transition: all 0.08s !important;
}
div[data-testid="stButton"] > button:active { transform:translateY(3px) !important; box-shadow:0 1px 0 #0b141a !important; }
div[data-testid="stButton"] > button:hover { border-color:#1cb0f6 !important; color:#1cb0f6 !important; }

/* Reset button override */
.reset-btn div[data-testid="stButton"] > button {
    background:#ff4b4b22 !important; border-color:#ff4b4b44 !important;
    color:#ff7b7b !important;
}
</style>
""", unsafe_allow_html=True)

nick    = st.session_state.nickname or "Learner"
avatar  = st.session_state.avatar or "🐴"
focus   = st.session_state.focus_areas
xp      = st.session_state.xp
streak  = st.session_state.streak
done    = st.session_state.completed_levels
energy  = st.session_state.energy
level   = st.session_state.current_level

# Rank calculation
RANKS = [
    (0,    "Nervous Newcomer 😰"),
    (200,  "Confident Talker 💬"),
    (500,  "Rising Star 🌟"),
    (1000, "Communication Pro 💼"),
    (2000, "Pitch Master 🎯"),
    (3500, "Boardroom Legend 👑"),
]
current_rank = RANKS[0][1]
next_rank_xp = RANKS[1][0]
for threshold, rank_name in RANKS:
    if xp >= threshold:
        current_rank = rank_name
for i, (threshold, _) in enumerate(RANKS):
    if xp < threshold:
        next_rank_xp = threshold
        break
else:
    next_rank_xp = RANKS[-1][0]

xp_to_next = max(0, next_rank_xp - xp)
prev_threshold = max(t for t, _ in RANKS if t <= xp)
rank_pct = min(100, int((xp - prev_threshold) / max(1, next_rank_xp - prev_threshold) * 100))

st.markdown(f"""
<div class="top-bar">
    <a href="/" style="font-size:22px;text-decoration:none">←</a>
    <div style="font-weight:900;font-size:16px">👤 Profile</div>
    <div style="color:#1cb0f6;font-weight:800">💎 {xp:,}</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

# ── Profile Hero Card ──
focus_pills = "".join(
    f'<span style="background:#a346ff22;border:1px solid #a346ff44;color:#a346ff;'
    f'padding:4px 12px;border-radius:50px;font-size:11px;font-weight:700">{f}</span> '
    for f in focus
) if focus else ""

st.markdown(f"""
<div class="g-card" style="text-align:center;padding:28px 20px;
     background:linear-gradient(160deg,#131f24,#0d1e1a)">
    <div style="font-size:80px;margin-bottom:8px;
                filter:drop-shadow(0 0 20px rgba(88,204,2,0.3))">{avatar}</div>
    <div style="font-size:26px;font-weight:900">{nick}</div>
    <div style="font-size:14px;color:#58cc02;font-weight:700;margin-top:4px">{current_rank}</div>
    <div style="margin:14px 0 6px">{focus_pills}</div>

    <!-- Rank Progress -->
    <div style="margin-top:16px">
        <div style="display:flex;justify-content:space-between;font-size:11px;font-weight:700;color:#4a6572;margin-bottom:6px">
            <span>{xp:,} XP</span>
            <span>{xp_to_next:,} XP to next rank</span>
        </div>
        <div style="background:#203038;border-radius:50px;height:14px;overflow:hidden">
            <div style="background:linear-gradient(90deg,#58cc02,#7be800);width:{rank_pct}%;
                        height:100%;border-radius:50px;box-shadow:0 0 12px #58cc0244"></div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Stats Grid ──
st.markdown('<div class="section-header">📊 Your Stats</div>', unsafe_allow_html=True)

stats = [
    ("🔥", str(streak),       "Day Streak",      "#ff9600"),
    ("💎", f"{xp:,}",         "Total XP",        "#1cb0f6"),
    ("✅", str(len(done)),     "Levels Done",     "#58cc02"),
    ("⚡", f"{energy}/5",      "Energy Left",     "#a346ff"),
    ("🏅", "3",               "Badges Earned",   "#ffd700"),
    ("🎯", f"Lv.{level}",     "Current Level",   "#ff9600"),
]

for row_start in range(0, len(stats), 2):
    row = stats[row_start:row_start + 2]
    cols = st.columns(2)
    for i, (icon, value, label, color) in enumerate(row):
        with cols[i]:
            st.markdown(f"""
            <div class="g-card" style="text-align:center;padding:16px 10px;margin-bottom:10px">
                <div style="font-size:26px;margin-bottom:4px">{icon}</div>
                <div style="font-size:26px;font-weight:900;color:{color}">{value}</div>
                <div style="font-size:11px;color:#4a6572;font-weight:700">{label}</div>
            </div>
            """, unsafe_allow_html=True)

# ── Session History ──
st.markdown('<div class="section-header">📅 Recent Sessions</div>', unsafe_allow_html=True)

HISTORY = [
    {"level": "Storytelling",      "icon": "📖", "score": 88, "xp": 110, "date": "Today"},
    {"level": "Active Listening",  "icon": "👂", "score": 92, "xp": 75,  "date": "Yesterday"},
    {"level": "First Impressions", "icon": "👋", "score": 76, "xp": 50,  "date": "Jun 13"},
]

for session in HISTORY:
    score_color = "#58cc02" if session["score"] >= 80 else "#ff9600"
    st.markdown(f"""
    <div class="g-card" style="display:flex;align-items:center;gap:14px;padding:14px 16px">
        <div style="font-size:32px">{session['icon']}</div>
        <div style="flex:1">
            <div style="font-weight:800;font-size:14px">{session['level']}</div>
            <div style="font-size:11px;color:#4a6572;font-weight:600;margin-top:2px">{session['date']}</div>
        </div>
        <div style="text-align:right">
            <div style="font-weight:900;color:{score_color};font-size:16px">{session['score']}%</div>
            <div style="font-size:11px;color:#1cb0f6;font-weight:700">+{session['xp']} XP</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Weekly Activity Heatmap ──
st.markdown('<div class="section-header">📈 This Week\'s Activity</div>', unsafe_allow_html=True)

days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
activity = [3, 1, 2, 3, 3, 0, 1]  # 0=none, 1=low, 2=med, 3=high

heat_colors = ["#203038", "#1a4a20", "#2d7a28", "#58cc02"]
heat_html = '<div style="display:flex;gap:6px;align-items:flex-end;justify-content:center;margin-bottom:8px">'
for day, act in zip(days, activity):
    color = heat_colors[act]
    height = [20, 32, 48, 64][act]
    heat_html += f"""
    <div style="display:flex;flex-direction:column;align-items:center;gap:4px">
        <div style="width:36px;height:{height}px;background:{color};border-radius:8px;
                    box-shadow:{'0 0 12px ' + color + '88' if act == 3 else 'none'}"></div>
        <div style="font-size:10px;color:#4a6572;font-weight:700">{day}</div>
    </div>
    """
heat_html += '</div>'

st.markdown(f'<div class="g-card">{heat_html}<div style="text-align:center;font-size:11px;color:#4a6572;font-weight:600">Sessions completed per day</div></div>', unsafe_allow_html=True)

# ── Actions ──
st.markdown("<br>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    if st.button("🏅 View Badges", use_container_width=True):
        st.switch_page("pages/4_Badges.py")
with col2:
    if st.button("🎙️ Practice", use_container_width=True):
        st.switch_page("pages/2_Practice_Arena.py")

if st.button("← Back to Home", use_container_width=True):
    st.switch_page("Home.py")

st.markdown("<br>", unsafe_allow_html=True)

with st.expander("⚠️ Danger Zone"):
    st.markdown('<p style="color:#ff7b7b;font-size:13px;font-weight:600">This will reset all your progress and restart onboarding.</p>', unsafe_allow_html=True)
    if st.button("🗑️ Reset All Progress", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.switch_page("Home.py")

st.markdown('</div>', unsafe_allow_html=True)