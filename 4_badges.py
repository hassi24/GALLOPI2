import streamlit as st

st.set_page_config(page_title="Badges · Gallopi", page_icon="🏅",
                   layout="centered", initial_sidebar_state="collapsed")

defaults = {"nickname": "Learner", "avatar": "🐴", "streak": 7, "xp": 1240, "completed_levels": [1, 2, 3]}
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
    background:#a346ff !important; color:#fff !important; border:none !important;
    border-radius:16px !important; font-family:'Nunito',sans-serif !important;
    font-weight:800 !important; font-size:16px !important; padding:14px 28px !important;
    box-shadow:0 4px 0 #8238cc !important; width:100% !important;
}
div[data-testid="stButton"] > button:active { transform:translateY(3px) !important; box-shadow:0 1px 0 #8238cc !important; }
div[data-testid="stButton"] > button:hover { background:#b85cff !important; border:none !important; }
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="top-bar">
    <a href="/" style="font-size:22px;text-decoration:none">←</a>
    <div style="font-weight:900;font-size:16px">🏅 Badge Collection</div>
    <div style="color:#1cb0f6;font-weight:800">💎 {st.session_state.xp:,}</div>
</div>
""", unsafe_allow_html=True)

completed = st.session_state.completed_levels

BADGES = [
    # Earned badges
    {
        "icon": "🗣️", "name": "First Words",       "desc": "Completed your first practice session",
        "color": "#58cc02", "shadow": "#46a302", "earned": True,
        "category": "Milestone",
    },
    {
        "icon": "🔥", "name": "On Fire",            "desc": "Maintained a 7-day streak",
        "color": "#ff9600", "shadow": "#e58500", "earned": True,
        "category": "Streak",
    },
    {
        "icon": "👂", "name": "Deep Listener",      "desc": "Scored 90%+ on Active Listening level",
        "color": "#1cb0f6", "shadow": "#1899d6", "earned": len(completed) >= 2,
        "category": "Skill",
    },
    # Unearned badges
    {
        "icon": "🏆", "name": "Podium Star",        "desc": "Reach Top 3 on the leaderboard",
        "color": "#ffd700", "shadow": "#e8b400", "earned": False,
        "category": "Social",
    },
    {
        "icon": "🎙️", "name": "Stage Ready",        "desc": "Complete the Public Speaking track",
        "color": "#a346ff", "shadow": "#8238cc", "earned": False,
        "category": "Track",
    },
    {
        "icon": "⚡", "name": "Speed Talker",       "desc": "Complete a level in under 2 minutes",
        "color": "#ff9600", "shadow": "#e58500", "earned": False,
        "category": "Skill",
    },
    {
        "icon": "💎", "name": "Gem Collector",       "desc": "Earn 5,000 total XP",
        "color": "#1cb0f6", "shadow": "#1899d6", "earned": st.session_state.xp >= 5000,
        "category": "Milestone",
    },
    {
        "icon": "👑", "name": "Boardroom Master",   "desc": "Complete all 8 levels",
        "color": "#ffd700", "shadow": "#e8b400", "earned": len(completed) >= 8,
        "category": "Milestone",
    },
    {
        "icon": "🌟", "name": "Perfect Score",      "desc": "Get 100% on any level",
        "color": "#58cc02", "shadow": "#46a302", "earned": False,
        "category": "Skill",
    },
    {
        "icon": "🤝", "name": "Team Player",        "desc": "Invite 3 friends to Gallopi",
        "color": "#a346ff", "shadow": "#8238cc", "earned": False,
        "category": "Social",
    },
    {
        "icon": "📖", "name": "Storyteller",        "desc": "Complete the Storytelling level",
        "color": "#1cb0f6", "shadow": "#1899d6", "earned": len(completed) >= 3,
        "category": "Track",
    },
    {
        "icon": "🚀", "name": "Pitch Perfect",      "desc": "Score 95%+ on an Elevator Pitch",
        "color": "#ff9600", "shadow": "#e58500", "earned": False,
        "category": "Skill",
    },
]

earned_count = sum(1 for b in BADGES if b["earned"])

st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

# Header stats
st.markdown(f"""
<div class="g-card" style="text-align:center;border-color:#a346ff">
    <div style="font-size:48px;font-weight:900;color:#a346ff">{earned_count}</div>
    <div style="font-size:13px;color:#4a6572;font-weight:700">of {len(BADGES)} badges earned</div>
    <div style="background:#203038;border-radius:50px;height:12px;overflow:hidden;margin-top:12px">
        <div style="background:linear-gradient(90deg,#a346ff,#c87aff);width:{int(earned_count/len(BADGES)*100)}%;
                    height:100%;border-radius:50px"></div>
    </div>
</div>
""", unsafe_allow_html=True)

# Category filter
categories = ["All", "Milestone", "Streak", "Skill", "Social", "Track"]
selected_cat = st.selectbox("Filter by category", categories, label_visibility="collapsed")

filtered = [b for b in BADGES if selected_cat == "All" or b["category"] == selected_cat]

# Earned section
earned_badges = [b for b in filtered if b["earned"]]
if earned_badges:
    st.markdown('<div class="section-header">✅ Earned Badges</div>', unsafe_allow_html=True)

    # 3-column grid
    for row_start in range(0, len(earned_badges), 3):
        row = earned_badges[row_start:row_start + 3]
        cols = st.columns(3)
        for col_i, badge in enumerate(row):
            with cols[col_i]:
                st.markdown(f"""
                <div style="display:flex;flex-direction:column;align-items:center;gap:8px;padding:12px 4px;
                            text-align:center">
                    <div style="width:72px;height:72px;border-radius:50%;
                                background:radial-gradient(circle at 35% 35%, {badge['color']}dd, {badge['shadow']});
                                display:flex;align-items:center;justify-content:center;font-size:30px;
                                box-shadow:0 4px 0 {badge['shadow']},0 0 24px {badge['color']}55;
                                border:3px solid {badge['color']}">
                        {badge['icon']}
                    </div>
                    <div style="font-size:12px;font-weight:800;color:#e8f4f8;line-height:1.3">{badge['name']}</div>
                    <div style="font-size:10px;color:#4a6572;font-weight:600;line-height:1.3">{badge['category']}</div>
                </div>
                """, unsafe_allow_html=True)

# Locked section
locked_badges = [b for b in filtered if not b["earned"]]
if locked_badges:
    st.markdown('<div class="section-header">🔒 Locked Badges</div>', unsafe_allow_html=True)

    for row_start in range(0, len(locked_badges), 3):
        row = locked_badges[row_start:row_start + 3]
        cols = st.columns(3)
        for col_i, badge in enumerate(row):
            with cols[col_i]:
                st.markdown(f"""
                <div style="display:flex;flex-direction:column;align-items:center;gap:8px;padding:12px 4px;
                            text-align:center">
                    <div style="width:72px;height:72px;border-radius:50%;
                                background:{badge['color']}22;
                                display:flex;align-items:center;justify-content:center;font-size:30px;
                                border:3px solid #203038;
                                filter:grayscale(100%);opacity:0.4">
                        {badge['icon']}
                    </div>
                    <div style="font-size:12px;font-weight:800;color:#4a6572;line-height:1.3">{badge['name']}</div>
                    <div style="font-size:10px;color:#3c4d55;font-weight:600;line-height:1.3">{badge['desc']}</div>
                </div>
                """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
if st.button("🎙️ Earn More Badges — Practice Now!", use_container_width=True):
    st.switch_page("pages/2_Practice_Arena.py")

if st.button("← Back to Path", use_container_width=True):
    st.switch_page("Home.py")

st.markdown('</div>', unsafe_allow_html=True)