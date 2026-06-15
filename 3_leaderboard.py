import streamlit as st

st.set_page_config(page_title="Leaderboard · Gallopi", page_icon="🏆",
                   layout="centered", initial_sidebar_state="collapsed")

defaults = {
    "nickname": "Learner", "avatar": "🐴", "streak": 7,
    "xp": 1240, "current_page": "leaderboard",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');
*, *::before, *::after { box-sizing: border-box; }
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: #0b141a !important; font-family: 'Nunito', sans-serif !important; color: #e8f4f8;
}
#MainMenu, footer, header, [data-testid="stSidebar"], [data-testid="collapsedControl"] { display:none !important; }
.top-bar {
    position: fixed; top: 0; left: 50%; transform: translateX(-50%);
    width: 100%; max-width: 480px; background: #0b141a;
    border-bottom: 2px solid #203038; padding: 10px 20px;
    display: flex; align-items: center; justify-content: space-between; z-index: 9999; font-weight: 800;
}
.main-wrap { max-width: 480px; margin: 0 auto; padding: 72px 16px 20px; }
.g-card { background:#131f24; border:2px solid #203038; border-radius:20px; padding:20px; margin-bottom:14px; }
div[data-testid="stButton"] > button {
    background: #1cb0f6 !important; color: #fff !important; border: none !important;
    border-radius:16px !important; font-family:'Nunito',sans-serif !important;
    font-weight:800 !important; font-size:16px !important; padding:14px 28px !important;
    box-shadow:0 4px 0 #1899d6 !important; width:100% !important;
}
div[data-testid="stButton"] > button:active { transform:translateY(3px) !important; box-shadow:0 1px 0 #1899d6 !important; }
div[data-testid="stButton"] > button:hover { background:#28c4ff !important; border:none !important; }
.section-header { font-size:13px; font-weight:800; color:#4a6572; text-transform:uppercase; letter-spacing:1.5px; margin:20px 0 12px; }
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="top-bar">
    <a href="/" style="font-size:22px;text-decoration:none">←</a>
    <div style="font-weight:900;font-size:16px">🏆 Leaderboard</div>
    <div style="color:#ff9600;font-weight:800">🔥 {st.session_state.streak}</div>
</div>
""", unsafe_allow_html=True)

nick = st.session_state.nickname or "You"
user_xp = st.session_state.xp
avatar = st.session_state.avatar or "⚡"

ALL_PLAYERS = [
    {"name": "PitchKing",  "avatar": "🐴", "xp": 3450, "streak": 21, "level": 8},
    {"name": "SarahS",     "avatar": "👩🏼‍💻", "xp": 2180, "streak": 14, "level": 7},
    {"name": "AlexT",      "avatar": "🦙", "xp": 1920, "streak": 9,  "level": 6},
    {"name": nick,          "avatar": avatar, "xp": user_xp, "streak": st.session_state.streak, "level": 4},
    {"name": "DominicV",   "avatar": "👨🏽‍💼", "xp": 980,  "streak": 5,  "level": 4},
    {"name": "MiaK",       "avatar": "👩🏼‍💻", "xp": 740,  "streak": 3,  "level": 3},
    {"name": "JorgeM",     "avatar": "🦙", "xp": 620,  "streak": 2,  "level": 3},
    {"name": "PriyaR",     "avatar": "👩🏼‍💻", "xp": 440,  "streak": 1,  "level": 2},
]

# Sort by XP
ALL_PLAYERS.sort(key=lambda p: p["xp"], reverse=True)

st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

# Filter tabs
tab_labels = ["Weekly", "All Time", "Friends"]
selected_tab = st.radio("View", tab_labels, horizontal=True, label_visibility="collapsed")

# Podium (top 3)
top3 = ALL_PLAYERS[:3]
p1, p2, p3 = top3[0], top3[1], top3[2]

st.markdown(f"""
<div class="g-card" style="background:linear-gradient(135deg,#0f1e14,#0b141a);border-color:#ffd70044;overflow:hidden">
    <div style="text-align:center;margin-bottom:20px">
        <div style="font-size:13px;font-weight:800;color:#ffd700;letter-spacing:2px">THIS WEEK'S CHAMPIONS</div>
    </div>

    <!-- Stars top decoration -->
    <div style="display:flex;justify-content:center;gap:6px;margin-bottom:16px;font-size:18px">
        ⭐⭐⭐
    </div>

    <div style="display:flex;align-items:flex-end;justify-content:center;gap:8px">

        <!-- 2nd Place -->
        <div style="display:flex;flex-direction:column;align-items:center;gap:4px;flex:1">
            <div style="font-size:30px">{p2['avatar']}</div>
            <div style="font-weight:800;font-size:12px;text-align:center">{p2['name']}</div>
            <div style="font-size:11px;color:#ff9600;font-weight:700">🔥{p2['streak']}</div>
            <div style="background:linear-gradient(180deg,#7a8f9a,#5a6f7a);width:100%;min-height:90px;border-radius:14px 14px 0 0;
                        display:flex;flex-direction:column;align-items:center;justify-content:flex-end;padding:10px;
                        box-shadow:0 0 20px rgba(138,159,170,0.3)">
                <div style="font-size:24px">🥈</div>
                <div style="font-weight:900;font-size:22px;color:#fff">#2</div>
                <div style="font-size:11px;font-weight:700;color:#ffffffaa">{p2['xp']:,} XP</div>
            </div>
        </div>

        <!-- 1st Place -->
        <div style="display:flex;flex-direction:column;align-items:center;gap:4px;flex:1.1">
            <div style="font-size:13px;line-height:1">👑</div>
            <div style="font-size:36px">{p1['avatar']}</div>
            <div style="font-weight:900;font-size:13px;text-align:center;color:#ffd700">{p1['name']}</div>
            <div style="font-size:11px;color:#ff9600;font-weight:700">🔥{p1['streak']}</div>
            <div style="background:linear-gradient(180deg,#ffd700,#e8a000);width:100%;min-height:120px;border-radius:14px 14px 0 0;
                        display:flex;flex-direction:column;align-items:center;justify-content:flex-end;padding:10px;
                        box-shadow:0 0 30px rgba(255,215,0,0.4)">
                <div style="font-size:28px">🥇</div>
                <div style="font-weight:900;font-size:24px;color:#0b141a">#1</div>
                <div style="font-size:11px;font-weight:800;color:#0b141a99">{p1['xp']:,} XP</div>
            </div>
        </div>

        <!-- 3rd Place -->
        <div style="display:flex;flex-direction:column;align-items:center;gap:4px;flex:1">
            <div style="font-size:30px">{p3['avatar']}</div>
            <div style="font-weight:800;font-size:12px;text-align:center">{p3['name']}</div>
            <div style="font-size:11px;color:#ff9600;font-weight:700">🔥{p3['streak']}</div>
            <div style="background:linear-gradient(180deg,#cd7f32,#a06020);width:100%;min-height:72px;border-radius:14px 14px 0 0;
                        display:flex;flex-direction:column;align-items:center;justify-content:flex-end;padding:10px;
                        box-shadow:0 0 20px rgba(205,127,50,0.3)">
                <div style="font-size:20px">🥉</div>
                <div style="font-weight:900;font-size:20px;color:#fff">#3</div>
                <div style="font-size:11px;font-weight:700;color:#ffffffaa">{p3['xp']:,} XP</div>
            </div>
        </div>

    </div>
</div>
""", unsafe_allow_html=True)

# Full rankings
st.markdown('<div class="section-header">📋 Full Rankings</div>', unsafe_allow_html=True)

for rank, player in enumerate(ALL_PLAYERS, 1):
    is_you = player["name"] == nick
    bg      = "#1a2f3a" if is_you else "#131f24"
    border  = "#1cb0f6" if is_you else "#203038"

    rank_display = {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, f"#{rank}")
    rank_color   = {1: "#ffd700", 2: "#8a9baa", 3: "#cd7f32"}.get(rank, "#4a6572")

    you_badge = '<span style="font-size:10px;background:#1cb0f6;color:#fff;padding:2px 8px;border-radius:50px;margin-left:6px">YOU</span>' if is_you else ""

    st.markdown(f"""
    <div style="background:{bg};border:2px solid {border};border-radius:16px;
                padding:14px 16px;margin-bottom:8px;
                display:flex;align-items:center;gap:14px">
        <div style="font-size:{'20px' if rank <= 3 else '15px'};font-weight:900;
                    color:{rank_color};min-width:32px;text-align:center">{rank_display}</div>
        <div style="font-size:30px">{player['avatar']}</div>
        <div style="flex:1;min-width:0">
            <div style="font-weight:800;font-size:14px">
                {player['name']}{you_badge}
            </div>
            <div style="font-size:11px;color:#4a6572;font-weight:600;margin-top:2px">
                Level {player['level']} · 🔥{player['streak']} day streak
            </div>
        </div>
        <div style="text-align:right">
            <div style="font-weight:900;color:#1cb0f6;font-size:14px">💎 {player['xp']:,}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Promo section
st.markdown("""
<div class="g-card" style="border-color:#a346ff;background:linear-gradient(135deg,#131f24,#1a1030);text-align:center;margin-top:20px">
    <div style="font-size:36px;margin-bottom:10px">🚀</div>
    <div style="font-weight:900;font-size:16px;margin-bottom:6px">Climb the ranks!</div>
    <div style="font-size:13px;color:#4a6572;font-weight:600;margin-bottom:14px">
        Complete daily practice sessions to earn XP and rise to the top
    </div>
</div>
""", unsafe_allow_html=True)

if st.button("🎙️ Practice Now", use_container_width=True):
    st.switch_page("pages/2_Practice_Arena.py")

if st.button("← Back to Path", use_container_width=True):
    st.switch_page("Home.py")

st.markdown('</div>', unsafe_allow_html=True)