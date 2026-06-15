import streamlit as st
import streamlit.components.v1 as components
import time

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Gallopi",
    page_icon="🐴",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# SESSION STATE DEFAULTS
# ─────────────────────────────────────────────
defaults = {
    "onboarded": False,
    "onboard_step": 1,
    "nickname": "",
    "avatar": "",
    "focus_areas": [],
    "current_page": "path",
    "streak": 7,
    "xp": 1240,
    "gems": 85,
    "energy": 4,
    "completed_levels": [1, 2, 3],
    "current_level": 4,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: #0b141a !important;
    font-family: 'Nunito', sans-serif !important;
    color: #e8f4f8;
}

/* Hide default Streamlit chrome */
#MainMenu, footer, header, [data-testid="stSidebar"],
[data-testid="collapsedControl"], .stDeployButton { display: none !important; }

[data-testid="stAppViewContainer"] { padding-bottom: 90px !important; }

/* ── Cards ── */
.g-card {
    background: #131f24;
    border: 2px solid #203038;
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 14px;
}

/* ── 3D Buttons ── */
.g-btn {
    display: inline-block;
    padding: 14px 28px;
    border-radius: 16px;
    font-family: 'Nunito', sans-serif;
    font-weight: 800;
    font-size: 16px;
    cursor: pointer;
    border: none;
    transition: transform 0.08s, box-shadow 0.08s;
    text-decoration: none;
    text-align: center;
    letter-spacing: 0.5px;
    user-select: none;
}
.g-btn:active { transform: translateY(3px); }

.g-btn-green  { background:#58cc02; color:#fff; box-shadow:0 4px 0 #46a302; }
.g-btn-green:active  { box-shadow:0 1px 0 #46a302; }

.g-btn-blue   { background:#1cb0f6; color:#fff; box-shadow:0 4px 0 #1899d6; }
.g-btn-blue:active   { box-shadow:0 1px 0 #1899d6; }

.g-btn-orange { background:#ff9600; color:#fff; box-shadow:0 4px 0 #e58500; }
.g-btn-orange:active { box-shadow:0 1px 0 #e58500; }

.g-btn-grey   { background:#3c4d55; color:#8a9baa; box-shadow:0 4px 0 #2c393f; cursor:not-allowed; }

.g-btn-purple { background:#a346ff; color:#fff; box-shadow:0 4px 0 #8238cc; }
.g-btn-purple:active { box-shadow:0 1px 0 #8238cc; }

/* ── Top Metric Bar ── */
.top-bar {
    position: fixed; top: 0; left: 50%; transform: translateX(-50%);
    width: 100%; max-width: 480px;
    background: #0b141a;
    border-bottom: 2px solid #203038;
    padding: 10px 20px;
    display: flex; align-items: center; justify-content: space-between;
    z-index: 9999;
    font-weight: 800;
}
.top-bar .metric { display:flex; align-items:center; gap:5px; font-size:15px; }
.top-bar .streak  { color:#ff9600; }
.top-bar .xp      { color:#1cb0f6; }
.top-bar .energy  { color:#a346ff; }
.top-bar .flag    { font-size:20px; }

/* ── Bottom Nav ── */
.bottom-nav {
    position: fixed; bottom: 0; left: 50%; transform: translateX(-50%);
    width: 100%; max-width: 480px;
    background: #0b141a;
    border-top: 2px solid #203038;
    display: flex; z-index: 9999;
}
.nav-item {
    flex: 1; display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    padding: 10px 4px 12px;
    cursor: pointer; font-size: 11px; font-weight: 700;
    color: #4a6572; gap: 3px; transition: color 0.15s;
    text-decoration: none;
}
.nav-item .nav-icon { font-size: 24px; line-height: 1; }
.nav-item.active { color: #58cc02; }

/* ── Main content area ── */
.main-wrap {
    max-width: 480px;
    margin: 0 auto;
    padding: 70px 16px 16px;
}

/* ── Onboarding ── */
.onboard-wrap { max-width: 480px; margin: 0 auto; padding: 60px 20px 20px; }

.speech-bubble {
    background: #1cb0f6;
    border-radius: 20px;
    padding: 16px 20px;
    color: #fff;
    font-weight: 700;
    font-size: 17px;
    position: relative;
    margin-bottom: 20px;
    line-height: 1.4;
}
.speech-bubble::after {
    content: '';
    position: absolute; bottom: -16px; left: 50%; transform: translateX(-50%);
    border: 8px solid transparent;
    border-top-color: #1cb0f6;
}

.mascot-bounce {
    font-size: 80px;
    text-align: center;
    animation: bounce 1.2s infinite;
    display: block;
    margin: 16px auto 32px;
}
@keyframes bounce {
    0%,100% { transform: translateY(0); }
    50%      { transform: translateY(-16px); }
}

.focus-pill {
    display: inline-block;
    padding: 10px 18px;
    border-radius: 50px;
    border: 2px solid #203038;
    background: #131f24;
    color: #e8f4f8;
    font-family: 'Nunito', sans-serif;
    font-weight: 700;
    font-size: 14px;
    cursor: pointer;
    margin: 5px;
    transition: all 0.15s;
}
.focus-pill.selected {
    background: #a346ff;
    border-color: #8238cc;
    color: #fff;
    box-shadow: 0 3px 0 #8238cc;
}

.avatar-card {
    background: #131f24;
    border: 3px solid #203038;
    border-radius: 20px;
    padding: 20px 10px;
    text-align: center;
    cursor: pointer;
    transition: all 0.15s;
    font-size: 50px;
}
.avatar-card.selected {
    border-color: #58cc02;
    box-shadow: 0 4px 0 #46a302;
    transform: translateY(-3px);
}
.avatar-label {
    font-size: 11px; font-weight: 700;
    color: #4a6572; margin-top: 6px;
}

/* ── Progress dots ── */
.step-dots { display:flex; gap:8px; justify-content:center; margin-bottom:24px; }
.dot {
    width:10px; height:10px; border-radius:50%;
    background: #203038;
    transition: background 0.3s;
}
.dot.active { background: #1cb0f6; }
.dot.done   { background: #58cc02; }

/* ── Path Nodes ── */
.path-node {
    width: 80px; height: 80px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 28px;
    font-weight: 900;
    cursor: pointer;
    border: none;
    transition: transform 0.08s;
    box-shadow: 0 5px 0 rgba(0,0,0,0.4);
    text-decoration: none;
}
.path-node:active { transform: translateY(4px); box-shadow: 0 1px 0 rgba(0,0,0,0.4); }
.node-done   { background: #58cc02; box-shadow: 0 5px 0 #46a302; color: #fff; }
.node-active { background: #1cb0f6; box-shadow: 0 5px 0 #1899d6; color: #fff;
               animation: pulse-node 1.8s infinite; }
.node-locked { background: #3c4d55; box-shadow: 0 5px 0 #2c393f; color: #8a9baa; cursor:not-allowed; }

@keyframes pulse-node {
    0%,100% { box-shadow: 0 5px 0 #1899d6, 0 0 0 0 rgba(28,176,246,0); }
    50%      { box-shadow: 0 5px 0 #1899d6, 0 0 0 16px rgba(28,176,246,0); }
}

.node-label {
    font-size: 12px; font-weight: 700; color: #4a6572;
    text-align: center; margin-top: 6px; max-width: 90px;
}

.treasure-chest {
    font-size: 52px;
    text-align: center;
    filter: drop-shadow(0 0 18px #ff9600aa);
    animation: float 3s ease-in-out infinite;
}
@keyframes float {
    0%,100% { transform: translateY(0); }
    50%      { transform: translateY(-8px); }
}

.section-header {
    font-size: 13px; font-weight: 800; color: #4a6572;
    text-transform: uppercase; letter-spacing: 1.5px;
    margin: 20px 0 12px;
}

/* ── Streamlit widget overrides ── */
.stTextInput input {
    background: #131f24 !important;
    border: 2px solid #203038 !important;
    color: #e8f4f8 !important;
    border-radius: 14px !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    padding: 14px 18px !important;
}
.stTextInput input:focus {
    border-color: #1cb0f6 !important;
    box-shadow: none !important;
}
label[data-testid="stWidgetLabel"] {
    color: #8a9baa !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
}

/* Fix stButton to look 3D */
div[data-testid="stButton"] > button {
    background: #58cc02 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 16px !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 800 !important;
    font-size: 16px !important;
    padding: 14px 28px !important;
    box-shadow: 0 4px 0 #46a302 !important;
    width: 100% !important;
    transition: transform 0.08s, box-shadow 0.08s !important;
}
div[data-testid="stButton"] > button:active {
    transform: translateY(3px) !important;
    box-shadow: 0 1px 0 #46a302 !important;
}
div[data-testid="stButton"] > button:hover {
    background: #65d900 !important;
    border: none !important;
}

.stMarkdown p { font-family: 'Nunito', sans-serif; color: #e8f4f8; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# TOP METRIC BAR
# ─────────────────────────────────────────────
def render_top_bar():
    st.markdown(f"""
    <div class="top-bar">
        <div class="metric flag">🇺🇸</div>
        <div class="metric streak">🔥 {st.session_state.streak}</div>
        <div class="metric xp">💎 {st.session_state.xp}</div>
        <div class="metric energy">⚡ {st.session_state.energy}/5</div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# BOTTOM NAV
# ─────────────────────────────────────────────
def render_bottom_nav():
    p = st.session_state.current_page
    pages = [
        ("path",        "🏠", "Path"),
        ("quests",      "🏅", "Quests"),
        ("leaderboard", "🏆", "Leaders"),
        ("profile",     "👤", "Profile"),
    ]
    cols = st.columns(4)
    for i, (page_id, icon, label) in enumerate(pages):
        with cols[i]:
            active = "active" if p == page_id else ""
            if st.button(f"{icon}\n{label}", key=f"nav_{page_id}", use_container_width=True):
                st.session_state.current_page = page_id
                st.rerun()

    # Style the nav buttons to look like a bottom nav
    st.markdown("""
    <style>
    div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] > button {
        background: transparent !important;
        box-shadow: none !important;
        border-radius: 12px !important;
        color: #4a6572 !important;
        font-size: 11px !important;
        padding: 8px 4px !important;
        white-space: pre-line;
        line-height: 1.6;
    }
    div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] > button:hover {
        background: #131f24 !important;
        color: #58cc02 !important;
    }
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# ONBOARDING FLOW
# ─────────────────────────────────────────────
def render_onboarding():
    step = st.session_state.onboard_step

    # Progress dots
    dots_html = '<div class="step-dots">'
    for i in range(1, 5):
        cls = "dot done" if i < step else ("dot active" if i == step else "dot")
        dots_html += f'<div class="{cls}"></div>'
    dots_html += '</div>'
    st.markdown(dots_html, unsafe_allow_html=True)

    # ── Step 1: Hook ──
    if step == 1:
        st.markdown("""
        <div class="onboard-wrap">
            <div class="speech-bubble">
                Neigh! 🐴 Let's get you ready for that boardroom pitch!<br>
                <span style="font-size:13px;opacity:0.85">I'm Gallopi — your communication coach. Let's level up together!</span>
            </div>
            <span class="mascot-bounce">🐴</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Let's GO! 🚀", use_container_width=True):
            st.session_state.onboard_step = 2
            st.rerun()

    # ── Step 2: Nickname ──
    elif step == 2:
        st.markdown("""
        <div style="text-align:center;font-size:40px;margin:10px 0 6px">✏️</div>
        <h2 style="text-align:center;font-family:Nunito,sans-serif;font-size:22px;margin-bottom:6px">What should I call you?</h2>
        <p style="text-align:center;color:#4a6572;font-size:14px;font-weight:600;margin-bottom:20px">Pick a name that'll look great on the leaderboard!</p>
        """, unsafe_allow_html=True)
        nick = st.text_input("Your nickname", placeholder="e.g. SpeechWizard99", label_visibility="collapsed")
        if st.button("Continue →", use_container_width=True):
            if nick.strip():
                st.session_state.nickname = nick.strip()
                st.session_state.onboard_step = 3
                st.rerun()
            else:
                st.warning("Give yourself a name first! 😄")

    # ── Step 3: Avatar ──
    elif step == 3:
        st.markdown("""
        <h2 style="text-align:center;font-family:Nunito,sans-serif;font-size:22px;margin-bottom:6px">Pick your avatar</h2>
        <p style="text-align:center;color:#4a6572;font-size:14px;font-weight:600;margin-bottom:20px">Who are you in the boardroom?</p>
        """, unsafe_allow_html=True)
        avatars = [("👨🏽‍💼", "The Executive"), ("👩🏼‍💻", "The Innovator"), ("🦙", "The Wildcard")]
        cols = st.columns(3)
        for i, (emoji, label) in enumerate(avatars):
            with cols[i]:
                selected = st.session_state.avatar == emoji
                sel_class = "selected" if selected else ""
                st.markdown(f"""
                <div class="avatar-card {sel_class}" onclick="">
                    {emoji}
                    <div class="avatar-label">{label}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(label, key=f"av_{i}", use_container_width=True):
                    st.session_state.avatar = emoji
                    st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)
        if st.session_state.avatar:
            if st.button("Continue →", use_container_width=True):
                st.session_state.onboard_step = 4
                st.rerun()

    # ── Step 4: Focus Areas ──
    elif step == 4:
        st.markdown("""
        <h2 style="text-align:center;font-family:Nunito,sans-serif;font-size:22px;margin-bottom:6px">What do you want to master?</h2>
        <p style="text-align:center;color:#4a6572;font-size:14px;font-weight:600;margin-bottom:20px">Choose all that apply</p>
        """, unsafe_allow_html=True)
        focus_options = ["Interview Prep 🎤", "Public Speaking 🎙️", "Leadership Pitching 💼", "Active Listening 👂"]
        cols = st.columns(2)
        for i, opt in enumerate(focus_options):
            with cols[i % 2]:
                is_sel = opt in st.session_state.focus_areas
                sel_class = "selected" if is_sel else ""
                if st.button(opt, key=f"focus_{i}", use_container_width=True):
                    if is_sel:
                        st.session_state.focus_areas.remove(opt)
                    else:
                        st.session_state.focus_areas.append(opt)
                    st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)
        if st.session_state.focus_areas:
            if st.button(f"Start Training 🐴 →", use_container_width=True):
                st.session_state.onboarded = True
                st.session_state.current_page = "path"
                st.rerun()
        else:
            st.markdown('<p style="text-align:center;color:#4a6572;font-size:13px;font-weight:600">Select at least one focus area</p>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PATH VIEW
# ─────────────────────────────────────────────
LEVELS = [
    {"id": 1, "title": "First Impressions",   "icon": "👋", "xp": 50},
    {"id": 2, "title": "Active Listening",     "icon": "👂", "xp": 75},
    {"id": 3, "title": "Storytelling",         "icon": "📖", "xp": 100},
    {"id": 4, "title": "Elevator Pitch",       "icon": "🚀", "xp": 125},
    {"id": 5, "title": "Conflict Resolution",  "icon": "🤝", "xp": 150},
    {"id": 6, "title": "Leadership Voice",     "icon": "🎙️", "xp": 175},
    {"id": 7, "title": "Data Storytelling",    "icon": "📊", "xp": 200},
    {"id": 8, "title": "Boardroom Master",     "icon": "👑", "xp": 250},
]

POSITIONS = ["center", "right", "center", "left", "center", "right", "center", "left"]

def render_path():
    nick = st.session_state.nickname or "Learner"
    avatar = st.session_state.avatar or "🐴"

    st.markdown(f"""
    <div class="main-wrap">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px">
            <div>
                <div style="font-size:13px;color:#4a6572;font-weight:700">Welcome back,</div>
                <div style="font-size:22px;font-weight:900">{avatar} {nick}</div>
            </div>
            <div class="g-card" style="padding:10px 16px;margin:0;display:flex;gap:8px;align-items:center">
                <span style="font-size:20px">⚡</span>
                <span style="font-weight:800;color:#a346ff">{st.session_state.energy}/5</span>
            </div>
        </div>

        <!-- Daily XP Bar -->
        <div class="g-card" style="margin-bottom:20px">
            <div style="display:flex;justify-content:space-between;margin-bottom:8px">
                <span style="font-weight:700;font-size:13px">Daily XP Goal</span>
                <span style="color:#58cc02;font-weight:800;font-size:13px">85 / 100 XP</span>
            </div>
            <div style="background:#203038;border-radius:50px;height:12px;overflow:hidden">
                <div style="background:linear-gradient(90deg,#58cc02,#7be800);width:85%;height:100%;border-radius:50px;
                            box-shadow:0 0 12px #58cc0266"></div>
            </div>
        </div>

        <div class="section-header">🗺️ Your Learning Path</div>
    </div>
    """, unsafe_allow_html=True)

    completed = st.session_state.completed_levels
    current = st.session_state.current_level

    for i, level in enumerate(LEVELS):
        pos = POSITIONS[i]
        lid = level["id"]

        if lid in completed:
            state_class, icon_display = "node-done", "✓"
        elif lid == current:
            state_class, icon_display = "node-active", level["icon"]
        else:
            state_class, icon_display = "node-locked", "🔒"

        # Treasure chest at midpoint
        if i == 3:
            st.markdown(f"""
            <div style="display:flex;flex-direction:column;align-items:center;margin:10px 0 20px">
                <div class="treasure-chest">🎁</div>
                <div style="font-size:12px;font-weight:700;color:#ff9600;margin-top:6px">⭐⭐⭐ Checkpoint Reward!</div>
                <div style="font-size:11px;color:#4a6572;font-weight:600;margin-top:2px">+200 XP Bonus Chest</div>
            </div>
            """, unsafe_allow_html=True)

        # Stagger alignment
        if pos == "left":
            align = "flex-start"
            margin = "ml"
        elif pos == "right":
            align = "flex-end"
            margin = "mr"
        else:
            align = "center"
            margin = ""

        # Render node
        col1, col2, col3 = st.columns([1, 1, 1])
        target_col = col1 if pos == "left" else (col3 if pos == "right" else col2)
        with target_col:
            if lid == current:
                if st.button(f"{icon_display}", key=f"level_{lid}", use_container_width=False):
                    st.session_state.target_level = lid
                    st.switch_page("pages/2_Practice_Arena.py")
            else:
                st.markdown(f"""
                <div style="display:flex;flex-direction:column;align-items:center;gap:6px;padding:8px 0">
                    <div class="path-node {state_class}">{icon_display}</div>
                    <div class="node-label">{level['title']}</div>
                    <div style="font-size:11px;color:#ff9600;font-weight:700">+{level['xp']} XP</div>
                </div>
                """, unsafe_allow_html=True)

        if lid != current:
            pass
        else:
            st.markdown(f"""
            <div style="text-align:center;margin-top:-10px;margin-bottom:10px">
                <div class="node-label">{level['title']}</div>
                <div style="font-size:11px;color:#ff9600;font-weight:700">+{level['xp']} XP</div>
                <div style="font-size:11px;color:#1cb0f6;font-weight:700;margin-top:3px">← TAP TO PRACTICE</div>
            </div>
            """, unsafe_allow_html=True)

        # Connector line
        if i < len(LEVELS) - 1:
            st.markdown("""
            <div style="display:flex;justify-content:center;margin:2px 0">
                <div style="width:3px;height:28px;background:linear-gradient(#203038,#203038);border-radius:2px;
                            background:repeating-linear-gradient(180deg,#203038 0,#203038 6px,transparent 6px,transparent 12px)"></div>
            </div>
            """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# QUESTS VIEW
# ─────────────────────────────────────────────
def render_quests():
    st.markdown("""
    <div class="main-wrap">
        <div style="font-size:22px;font-weight:900;margin-bottom:4px">🏅 Daily Quests</div>
        <div style="font-size:13px;color:#4a6572;font-weight:600;margin-bottom:20px">Resets in 14h 32m</div>
    </div>
    """, unsafe_allow_html=True)

    quests = [
        {"title": "Warm-Up Speaker",   "desc": "Complete 1 practice session today",   "reward": 20,  "progress": 1, "total": 1, "done": True},
        {"title": "Pitch Perfect",     "desc": "Score 80%+ on Tone & Warmth",         "reward": 35,  "progress": 0, "total": 1, "done": False},
        {"title": "Streak Keeper",     "desc": "Maintain your 7-day streak",           "reward": 50,  "progress": 7, "total": 7, "done": True},
        {"title": "Word Wizard",       "desc": "Use 5 power phrases in responses",     "reward": 25,  "progress": 3, "total": 5, "done": False},
    ]

    for q in quests:
        pct = min(100, int(q["progress"] / q["total"] * 100))
        done_style = "border-color:#58cc02;" if q["done"] else ""
        badge = "✅" if q["done"] else f"{q['progress']}/{q['total']}"
        st.markdown(f"""
        <div class="g-card" style="{done_style}display:flex;flex-direction:column;gap:10px">
            <div style="display:flex;justify-content:space-between;align-items:flex-start">
                <div>
                    <div style="font-weight:800;font-size:15px">{q['title']}</div>
                    <div style="font-size:12px;color:#4a6572;font-weight:600;margin-top:2px">{q['desc']}</div>
                </div>
                <div style="display:flex;flex-direction:column;align-items:center;gap:2px;min-width:56px">
                    <span style="font-size:20px">{'✅' if q['done'] else '💎'}</span>
                    <span style="font-size:12px;font-weight:800;color:#1cb0f6">+{q['reward']} XP</span>
                </div>
            </div>
            <div>
                <div style="background:#203038;border-radius:50px;height:10px;overflow:hidden">
                    <div style="background:{'#58cc02' if q['done'] else '#a346ff'};width:{pct}%;height:100%;border-radius:50px"></div>
                </div>
                <div style="font-size:11px;color:#4a6572;font-weight:700;margin-top:4px">{badge}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="main-wrap" style="padding-top:0">
        <div class="section-header">🔥 Weekly Challenge</div>
        <div class="g-card" style="border-color:#a346ff;background:linear-gradient(135deg,#131f24,#1a1030)">
            <div style="display:flex;gap:14px;align-items:center">
                <div style="font-size:48px">🏆</div>
                <div>
                    <div style="font-weight:900;font-size:16px">Master Communicator</div>
                    <div style="font-size:13px;color:#4a6572;font-weight:600">Complete 5 sessions this week</div>
                    <div style="font-size:13px;color:#a346ff;font-weight:800;margin-top:4px">3/5 done · +200 XP reward</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# LEADERBOARD VIEW
# ─────────────────────────────────────────────
def render_leaderboard():
    nick = st.session_state.nickname or "You"
    st.markdown(f"""
    <div class="main-wrap">
        <div style="font-size:22px;font-weight:900;margin-bottom:4px">🏆 Leaderboard</div>
        <div style="font-size:13px;color:#4a6572;font-weight:600;margin-bottom:24px">Top communicators this week</div>

        <!-- Podium -->
        <div style="display:flex;align-items:flex-end;justify-content:center;gap:12px;margin-bottom:32px">

            <!-- 2nd Place -->
            <div style="display:flex;flex-direction:column;align-items:center;gap:6px">
                <div style="font-size:32px">👩🏼‍💻</div>
                <div style="font-weight:800;font-size:13px">SarahS</div>
                <div style="background:#8a9baa;width:90px;height:100px;border-radius:14px 14px 0 0;
                            display:flex;flex-direction:column;align-items:center;justify-content:flex-end;padding-bottom:10px">
                    <div style="font-size:22px">🥈</div>
                    <div style="font-weight:900;font-size:18px;color:#0b141a">2</div>
                    <div style="font-size:11px;font-weight:700;color:#0b141a">2,180 XP</div>
                </div>
            </div>

            <!-- 1st Place -->
            <div style="display:flex;flex-direction:column;align-items:center;gap:6px">
                <div style="font-size:14px">👑</div>
                <div style="font-size:36px">🐴</div>
                <div style="font-weight:800;font-size:13px">PitchKing</div>
                <div style="background:linear-gradient(180deg,#ffd700,#e8b400);width:100px;height:130px;border-radius:14px 14px 0 0;
                            display:flex;flex-direction:column;align-items:center;justify-content:flex-end;padding-bottom:10px;
                            box-shadow:0 0 24px #ffd70066">
                    <div style="font-size:24px">🥇</div>
                    <div style="font-weight:900;font-size:20px;color:#0b141a">1</div>
                    <div style="font-size:11px;font-weight:700;color:#0b141a">3,450 XP</div>
                </div>
            </div>

            <!-- 3rd Place -->
            <div style="display:flex;flex-direction:column;align-items:center;gap:6px">
                <div style="font-size:32px">🦙</div>
                <div style="font-weight:800;font-size:13px">AlexT</div>
                <div style="background:#cd7f32;width:90px;height:80px;border-radius:14px 14px 0 0;
                            display:flex;flex-direction:column;align-items:center;justify-content:flex-end;padding-bottom:10px">
                    <div style="font-size:20px">🥉</div>
                    <div style="font-weight:900;font-size:18px;color:#fff">3</div>
                    <div style="font-size:11px;font-weight:700;color:#fff">1,920 XP</div>
                </div>
            </div>
        </div>

        <!-- Rankings list -->
        <div class="section-header">📋 Full Rankings</div>
    </div>
    """, unsafe_allow_html=True)

    players = [
        ("PitchKing", "🐴", 3450, 1, "#ffd700"),
        ("SarahS",    "👩🏼‍💻", 2180, 2, "#8a9baa"),
        ("AlexT",     "🦙", 1920, 3, "#cd7f32"),
        (nick,        st.session_state.avatar or "⚡", st.session_state.xp, 4, "#1cb0f6"),
        ("DominicV",  "👨🏽‍💼", 980,  5, "#4a6572"),
        ("MiaK",      "👩🏼‍💻", 740,  6, "#4a6572"),
    ]

    for name, avatar, xp, rank, color in players:
        is_you = name == nick
        bg = "#1a2f3a" if is_you else "#131f24"
        border = "#1cb0f6" if is_you else "#203038"
        st.markdown(f"""
        <div class="g-card" style="background:{bg};border-color:{border};
                   display:flex;align-items:center;gap:14px;padding:14px 16px">
            <div style="font-size:18px;font-weight:900;color:{color};min-width:28px;text-align:center">#{rank}</div>
            <div style="font-size:28px">{avatar}</div>
            <div style="flex:1">
                <div style="font-weight:800;font-size:14px">{name}{'  <span style="font-size:11px;background:#1cb0f6;color:#fff;padding:2px 8px;border-radius:50px">YOU</span>' if is_you else ''}</div>
            </div>
            <div style="font-weight:800;color:#1cb0f6;font-size:14px">💎 {xp:,}</div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PROFILE VIEW
# ─────────────────────────────────────────────
def render_profile():
    nick = st.session_state.nickname or "Learner"
    avatar = st.session_state.avatar or "🐴"
    focus = st.session_state.focus_areas

    st.markdown(f"""
    <div class="main-wrap">
        <!-- Profile Header -->
        <div class="g-card" style="text-align:center;padding:28px 20px">
            <div style="font-size:72px;margin-bottom:8px">{avatar}</div>
            <div style="font-size:24px;font-weight:900">{nick}</div>
            <div style="font-size:13px;color:#4a6572;font-weight:600;margin-top:4px">Communication Apprentice</div>
            <div style="display:flex;justify-content:center;gap:10px;margin-top:16px;flex-wrap:wrap">
                {''.join(f'<span style="background:#a346ff22;border:1px solid #a346ff44;color:#a346ff;padding:4px 12px;border-radius:50px;font-size:12px;font-weight:700">{f}</span>' for f in focus) if focus else ''}
            </div>
        </div>

        <!-- Stats Grid -->
        <div class="section-header">📊 Your Stats</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:20px">
            <div class="g-card" style="text-align:center;padding:16px">
                <div style="font-size:32px;font-weight:900;color:#ff9600">{st.session_state.streak}</div>
                <div style="font-size:12px;color:#4a6572;font-weight:700">🔥 Day Streak</div>
            </div>
            <div class="g-card" style="text-align:center;padding:16px">
                <div style="font-size:32px;font-weight:900;color:#1cb0f6">{st.session_state.xp:,}</div>
                <div style="font-size:12px;color:#4a6572;font-weight:700">💎 Total XP</div>
            </div>
            <div class="g-card" style="text-align:center;padding:16px">
                <div style="font-size:32px;font-weight:900;color:#58cc02">{len(st.session_state.completed_levels)}</div>
                <div style="font-size:12px;color:#4a6572;font-weight:700">✅ Levels Done</div>
            </div>
            <div class="g-card" style="text-align:center;padding:16px">
                <div style="font-size:32px;font-weight:900;color:#a346ff">3</div>
                <div style="font-size:12px;color:#4a6572;font-weight:700">🏅 Badges Earned</div>
            </div>
        </div>

        <!-- Achievements Preview -->
        <div class="section-header">🏅 Recent Badges</div>
        <div style="display:flex;gap:12px;overflow-x:auto;padding-bottom:10px">
    """, unsafe_allow_html=True)

    badges = [
        ("🗣️", "First Words",    "#58cc02", False),
        ("🔥", "On Fire",       "#ff9600", False),
        ("👂", "Deep Listener", "#1cb0f6", False),
        ("🏆", "Podium Star",   "#ffd700", True),
        ("🎙️", "Stage Ready",   "#a346ff", True),
    ]
    badges_html = '<div style="display:flex;gap:12px;padding:0 16px 10px">'
    for icon, name, color, locked in badges:
        filter_s = "filter:grayscale(100%);opacity:0.4;" if locked else ""
        glow = f"box-shadow:0 0 18px {color}66;" if not locked else ""
        badges_html += f"""
        <div style="display:flex;flex-direction:column;align-items:center;gap:6px;min-width:72px">
            <div style="width:64px;height:64px;border-radius:50%;background:{color}22;border:3px solid {color};
                        display:flex;align-items:center;justify-content:center;font-size:28px;{filter_s}{glow}">
                {icon}
            </div>
            <div style="font-size:10px;font-weight:700;color:#4a6572;text-align:center">{name}</div>
        </div>
        """
    badges_html += '</div>'
    st.markdown(badges_html, unsafe_allow_html=True)

    if st.button("🚪 Reset Onboarding", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()


# ─────────────────────────────────────────────
# MAIN ROUTER
# ─────────────────────────────────────────────
if not st.session_state.onboarded:
    render_top_bar()
    render_onboarding()
else:
    render_top_bar()
    page = st.session_state.current_page
    if page == "path":
        render_path()
    elif page == "quests":
        render_quests()
    elif page == "leaderboard":
        render_leaderboard()
    elif page == "profile":
        render_profile()
    render_bottom_nav()