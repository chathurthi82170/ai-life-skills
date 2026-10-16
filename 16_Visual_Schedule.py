import streamlit as st
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rbac import enforce_access
import database
import importlib
importlib.reload(database)

st.set_page_config(page_title="Visual Schedule", page_icon="📅", layout="wide")
enforce_access()

username = st.session_state.get("username", "Student")

st.title("📅 My Visual Schedule")
st.write("A visual, step-by-step breakdown of your Morning, Afternoon, and Evening routines to build independence!")

# Initialize session state routines if not present
if "morning_tasks" not in st.session_state:
    st.session_state.morning_tasks = [
        {"task": "🛏️ Make the bed", "done": False},
        {"task": "🦷 Brush teeth for 2 mins", "done": False},
        {"task": "👕 Get dressed in clean clothes", "done": False},
        {"task": "🥞 Eat a nutritious breakfast", "done": False},
        {"task": "🎒 Pack school bag & water bottle", "done": False}
    ]

if "afternoon_tasks" not in st.session_state:
    st.session_state.afternoon_tasks = [
        {"task": "🍲 Eat lunch & clean plate", "done": False},
        {"task": "📚 Complete homework & reading (20 mins)", "done": False},
        {"task": "🎨 Creative time / Outdoor play", "done": False},
        {"task": "🧹 Help with a quick home chore", "done": False}
    ]

if "evening_tasks" not in st.session_state:
    st.session_state.evening_tasks = [
        {"task": "🍽️ Eat dinner with family", "done": False},
        {"task": "🛁 Take a bath or shower", "done": False},
        {"task": "🪥 Brush teeth before bed", "done": False},
        {"task": "👕 Put on comfortable pajamas", "done": False},
        {"task": "📖 Read bedtime story / quiet relaxation", "done": False},
        {"task": "😴 Lights out & sleep on time", "done": False}
    ]

col1, col2 = st.columns([2, 1])

with col1:
    # ── MORNING ROUTINE ───────────────────────────────────────────────────────
    st.markdown('<div class="routine-card" style="border-left: 6px solid #F59E0B;">', unsafe_allow_html=True)
    st.subheader("☀️ Morning Routine")
    m_done = 0
    for idx, item in enumerate(st.session_state.morning_tasks):
        chk = st.checkbox(item["task"], value=item["done"], key=f"morn_chk_{idx}")
        st.session_state.morning_tasks[idx]["done"] = chk
        if chk:
            m_done += 1
    m_pct = int((m_done / len(st.session_state.morning_tasks)) * 100) if st.session_state.morning_tasks else 0
    st.progress(m_pct / 100.0)
    st.caption(f"Morning Progress: {m_done} / {len(st.session_state.morning_tasks)} tasks completed ({m_pct}%)")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ── AFTERNOON ROUTINE ─────────────────────────────────────────────────────
    st.markdown('<div class="routine-card" style="border-left: 6px solid #3B82F6;">', unsafe_allow_html=True)
    st.subheader("🎒 Afternoon Routine")
    a_done = 0
    for idx, item in enumerate(st.session_state.afternoon_tasks):
        chk = st.checkbox(item["task"], value=item["done"], key=f"aft_chk_{idx}")
        st.session_state.afternoon_tasks[idx]["done"] = chk
        if chk:
            a_done += 1
    a_pct = int((a_done / len(st.session_state.afternoon_tasks)) * 100) if st.session_state.afternoon_tasks else 0
    st.progress(a_pct / 100.0)
    st.caption(f"Afternoon Progress: {a_done} / {len(st.session_state.afternoon_tasks)} tasks completed ({a_pct}%)")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ── EVENING ROUTINE ───────────────────────────────────────────────────────
    st.markdown('<div class="routine-card" style="border-left: 6px solid #8B5CF6;">', unsafe_allow_html=True)
    st.subheader("🌙 Evening Routine")
    e_done = 0
    for idx, item in enumerate(st.session_state.evening_tasks):
        chk = st.checkbox(item["task"], value=item["done"], key=f"eve_chk_{idx}")
        st.session_state.evening_tasks[idx]["done"] = chk
        if chk:
            e_done += 1
    e_pct = int((e_done / len(st.session_state.evening_tasks)) * 100) if st.session_state.evening_tasks else 0
    st.progress(e_pct / 100.0)
    st.caption(f"Evening Progress: {e_done} / {len(st.session_state.evening_tasks)} tasks completed ({e_pct}%)")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Summary Card
    total_tasks = len(st.session_state.morning_tasks) + len(st.session_state.afternoon_tasks) + len(st.session_state.evening_tasks)
    total_done = m_done + a_done + e_done
    overall_pct = int((total_done / total_tasks) * 100) if total_tasks else 0

    st.markdown('<div class="kpi-card" style="text-align: center;">', unsafe_allow_html=True)
    st.subheader("🌟 Overall Daily Progress")
    st.markdown(f"# **{overall_pct}%**")
    st.write(f"Completed **{total_done} of {total_tasks}** daily tasks today!")
    st.progress(overall_pct / 100.0)
    
    if overall_pct == 100:
        st.balloons()
        st.success("🎉 Champion! You completed your full Visual Schedule today!")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Add Custom Task Form
    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
    st.subheader("➕ Add Custom Task")
    new_task = st.text_input("New Task Name", placeholder="e.g. 🐶 Feed the pet")
    routine_sec = st.selectbox("Select Routine:", ["Morning", "Afternoon", "Evening"])
    if st.button("Add Task to Schedule 🚀", type="primary", use_container_width=True):
        if new_task.strip():
            if routine_sec == "Morning":
                st.session_state.morning_tasks.append({"task": new_task.strip(), "done": False})
            elif routine_sec == "Afternoon":
                st.session_state.afternoon_tasks.append({"task": new_task.strip(), "done": False})
            else:
                st.session_state.evening_tasks.append({"task": new_task.strip(), "done": False})
            st.success(f"Added '{new_task.strip()}' to {routine_sec} Routine!")
            st.rerun()
        else:
            st.warning("Please type a task name!")
    st.markdown('</div>', unsafe_allow_html=True)
