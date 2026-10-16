import streamlit as st
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rbac import enforce_access
import database
import importlib
importlib.reload(database)

st.set_page_config(page_title="Reward Shop", page_icon="🛍️", layout="wide")
enforce_access()

username = st.session_state.get("username", "Student")

# ── Dynamic XP Balance & Unlocked Items from SQLite ────────────────────────────
summary = database.get_student_xp_summary(username)
db_unlocked = database.get_unlocked_rewards(username)

# Calculate total XP earned from Learn Skills & AI Assessments
total_earned_xp = summary["total_xp"]

# Calculate XP spent on unlocked items
SHOP_ITEMS = [
    {"id": "fox",        "icon": "🦊", "name": "Fox Avatar",          "cost": 100,  "desc": "A clever fox companion"},
    {"id": "rainbow",    "icon": "🌈", "name": "Rainbow Theme",        "cost": 150,  "desc": "Brighten your learning space"},
    {"id": "star",       "icon": "⭐", "name": "Star Learner Badge",   "cost": 200,  "desc": "Wear your star with pride!"},
    {"id": "rocket",     "icon": "🚀", "name": "Rocket Theme",         "cost": 250,  "desc": "Blast off with this space theme!"},
    {"id": "dragon",     "icon": "🐉", "name": "Dragon Avatar",        "cost": 400,  "desc": "A mighty dragon companion"},
    {"id": "crown",      "icon": "👑", "name": "Golden Crown Badge",   "cost": 500,  "desc": "Show everyone you're a champion!"},
]

item_costs = {i["id"]: i["cost"] for i in SHOP_ITEMS}
spent_xp = sum(item_costs.get(item_id, 0) for item_id in db_unlocked)
current_xp_balance = max(0, total_earned_xp - spent_xp)

st.title("🛍️ Skill & Assessment Reward Shop")
st.write(f"Rewards for **{username}** based on completed **Learn Skills** and **AI Assessments**!")

# ── XP & Source Breakdown Header ───────────────────────────────────────────────
c1, c2 = st.columns([2, 1])

with c1:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #6366f1, #a855f7); padding:20px 24px; border-radius:18px;
         display:flex; align-items:center; gap:16px; box-shadow: 0 4px 20px rgba(168,85,247,0.3);">
        <span style="font-size:3rem;">💎</span>
        <div>
            <div style="color:#e0e7ff; font-size:0.95rem; font-weight:700; text-transform:uppercase; letter-spacing:1px;">Available XP Balance</div>
            <div style="color:white; font-size:2.4rem; font-weight:900;">{current_xp_balance} XP</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div style="background: rgba(30, 41, 59, 0.9); padding:16px; border-radius:18px; border:1px solid rgba(255,255,255,0.15);">
        <div style="font-weight:700; font-size:0.9rem; color:#94a3b8;">XP EARNED SOURCES</div>
        <div style="font-size:0.95rem; color:#f8fafc; margin-top:4px;">
            📚 <b>Skills:</b> +{summary["skill_points"]} XP ({summary["skills_completed"]} completed)<br>
            📝 <b>Assessments:</b> +{summary["assessment_points"]} XP ({summary["assessments_taken"]} taken)<br>
            🎁 <b>Welcome Bonus:</b> +100 XP
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ── Shop Items Display ────────────────────────────────────────────────────────
cols = st.columns(3)

for idx, item in enumerate(SHOP_ITEMS):
    col = cols[idx % 3]
    item_id = item["id"]
    is_unlocked = item_id in db_unlocked
    can_afford = current_xp_balance >= item["cost"]

    with col:
        if is_unlocked:
            bg = "rgba(16, 185, 129, 0.25)"
            border = "#10B981"
        elif can_afford:
            bg = "rgba(99, 102, 241, 0.25)"
            border = "#6366F1"
        else:
            bg = "rgba(30, 41, 59, 0.6)"
            border = "#64748B"

        st.markdown(f"""
        <div style="background:{bg}; border: 2px solid {border}; border-radius:16px;
             text-align:center; padding:24px 16px; margin-bottom:16px; box-shadow: 0 4px 12px rgba(0,0,0,0.2);">
            <div style="font-size:3.5rem;">{item["icon"]}</div>
            <div style="font-weight:800; font-size:1.15rem; color:#ffffff; margin:8px 0 4px;">{item["name"]}</div>
            <div style="color:#94a3b8; font-size:0.9rem; margin-bottom:12px;">{item["desc"]}</div>
            <div style="font-weight:800; font-size:1.1rem; color:{border};">
                {"✅ UNLOCKED" if is_unlocked else f"💎 {item['cost']} XP"}
            </div>
        </div>
        """, unsafe_allow_html=True)

        if is_unlocked:
            st.success("Unlocked! 🎉", icon="✅")
        elif can_afford:
            if st.button(f"🔓 Unlock {item['name']}", key=f"btn_{item_id}", use_container_width=True, type="primary"):
                database.save_unlocked_reward(username, item_id)
                st.balloons()
                st.rerun()
        else:
            needed = item["cost"] - current_xp_balance
            st.button(f"🔒 Need {needed} more XP (Learn Skills / Take Assessment)", key=f"btn_{item_id}", disabled=True, use_container_width=True)

# ── Unlocked Collection ───────────────────────────────────────────────────────
if db_unlocked:
    st.markdown("---")
    st.subheader("🏆 Your Unlocked Collection")
    unlocked_display = [
        f"{next(i['icon'] for i in SHOP_ITEMS if i['id'] == uid)} {next(i['name'] for i in SHOP_ITEMS if i['id'] == uid)}"
        for uid in db_unlocked
    ]
    st.success("  |  ".join(unlocked_display))
