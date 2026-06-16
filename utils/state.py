import streamlit as st

DEFAULTS = {
    "onboarded": False,
    "onboard_step": 1,
    "nickname": "",
    "avatar": "🦄",
    "avatar_label": "Unicorn",
    "focus_areas": [],
    "current_page": "path",
    "streak": 0,
    "xp": 0,
    "gems": 0,
    "energy": 5,
    "completed_levels": [],
    "current_level": 1,
    "active_scenario": None,
    "arena_q_index": 0,
    "arena_answers": [],
    "arena_show_results": False,
    "arena_scores": None,
    "session_history": [],
    "friends": [],
}

def init_state():
    for k, v in DEFAULTS.items():
        if k not in st.session_state:
            st.session_state[k] = v