import streamlit as st
import streamlit.components.v1 as components
import os
import sys
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.profiler import ProfilerAgent, DISABILITY_PROFILES
import agents.task_planner
import importlib
importlib.reload(agents.task_planner)
from agents.task_planner import TaskPlannerAgent
from rbac import enforce_access
import database
importlib.reload(database)
import skills_library
importlib.reload(skills_library)
from skills_library import UNIFIED_SKILL_TOPICS, get_all_topics, get_topic_data, adapt_steps_for_age

st.set_page_config(page_title="Learn Skill", page_icon="🧠", layout="wide")
enforce_access()

# ── Session init ────────────────────────────────────────────────────────────
CACHE_VERSION = "v4"

if 'stage' not in st.session_state:
    st.session_state.stage = 'input'
if 'mcq_answered' not in st.session_state:
    st.session_state.mcq_answered = False

# Auto-clear stale session data when code is updated
if st.session_state.get("cache_version") != CACHE_VERSION:
    for key in ["stage", "task_name", "task_steps", "mcq_data",
                "completed_steps", "mcq_answered", "mcq_result", "quick_task"]:
        st.session_state.pop(key, None)
    st.session_state.cache_version = CACHE_VERSION
    st.session_state.stage = 'input'

username = st.session_state.get("username", "Student")

# Fetch real student age from database for age-based adaptation
s_prof = database.get_student_profile(username)
if s_prof and str(s_prof[1]).isdigit():
    student_age = int(s_prof[1])
else:
    student_age = int(st.session_state.get("student_age", 12))

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Profile Setup")
    disability_type = st.selectbox("Select Learning Style:", list(DISABILITY_PROFILES.keys()))
    profiler = ProfilerAgent(disability_type)
    st.info(f"**UI Hints:** {profiler.get_ui_hints()}")
    if st.button("🔄 Reset Module"):
        for key in ["stage", "mcq_answered", "task_name", "task_steps", "mcq_data", "completed_steps", "mcq_result", "auto_loaded_topic"]:
            st.session_state.pop(key, None)
        st.rerun()

planner = TaskPlannerAgent(profiler)

st.title("🧠 Skill Builder — Learn Life Skills Step-by-Step")

# Age Adaptation Banner
if student_age <= 8:
    mode_badge = f"🌱 Junior Mode (Age {student_age}): 3-4 simple visual steps for young learners"
elif student_age <= 13:
    mode_badge = f"🚀 Intermediate Mode (Age {student_age}): 5-6 structured practical steps"
else:
    mode_badge = f"🎓 Senior Independence Mode (Age {student_age}): Full real-world independent steps"

st.info(f"🎂 **Student Age:** **{student_age} years** | **Adaptive Complexity:** **{mode_badge}**")

# ────────────────────────────────────────────────────────────────────────────
# STAGE 1 — INPUT (22 UNIFIED SKILL TOPICS, RANDOMIZED PER STUDENT)
# ────────────────────────────────────────────────────────────────────────────
if st.session_state.stage == 'input':
    # If a topic was selected in AI Assessment, load steps directly adapted to age!
    pre_task = st.session_state.get("task_name")
    if pre_task and not st.session_state.get("auto_loaded_topic"):
        st.session_state.auto_loaded_topic = True
        t_data = get_topic_data(pre_task)
        if t_data:
            st.session_state.task_steps = adapt_steps_for_age(t_data["steps"], student_age)
            st.session_state.mcq_data = t_data["questions"]
        else:
            raw_steps = planner.plan_task(pre_task)
            st.session_state.task_steps = adapt_steps_for_age(raw_steps, student_age)
            st.session_state.mcq_data = planner.generate_mcq(pre_task)
        st.session_state.stage = 'steps'
        st.rerun()

    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
    
    col_hdr1, col_hdr2 = st.columns([3, 1])
    with col_hdr1:
        st.subheader("Select a Life Skill to Learn Today (Randomized for Your Profile):")
    with col_hdr2:
        if st.button("🎲 Shuffle Skills List", use_container_width=True):
            st.session_state.shuffle_seed = st.session_state.get("shuffle_seed", 0) + 1
            st.rerun()

    # Category filter pills
    categories = ["All", "Personal Hygiene", "Kitchen & Meals", "Household Skills", "Daily Routines", "Safety Skills", "Financial Skills", "Emotional Regulation", "Communication Skills"]
    selected_cat = st.radio("Filter by Category:", categories, horizontal=True, key="learn_cat_filter")
    st.markdown("---")

    topics_list = get_all_topics()
    
    # Shuffle order per user based on username hash & seed so each student gets unique randomized layout
    user_seed = sum(ord(c) for c in username) + st.session_state.get("shuffle_seed", 0)
    rnd = random.Random(user_seed)
    rnd.shuffle(topics_list)

    if selected_cat != "All":
        topics_list = [t for t in topics_list if UNIFIED_SKILL_TOPICS[t]["category"] == selected_cat or selected_cat in UNIFIED_SKILL_TOPICS[t]["category"]]

    cols = st.columns(4)
    for idx, t_name in enumerate(topics_list):
        t_info = UNIFIED_SKILL_TOPICS[t_name]
        col = cols[idx % 4]
        with col:
            st.markdown(f"""
            <div style="
                text-align: center; 
                padding: 16px 12px; 
                border-radius: 16px; 
                background: linear-gradient(135deg, rgba(30,41,59,0.9), rgba(15,23,42,0.95)); 
                border: 1px solid rgba(255, 255, 255, 0.15); 
                box-shadow: 0 6px 20px rgba(0,0,0,0.3); 
                margin-bottom: 12px;
                min-height: 135px;
            ">
                <div style="font-size:2.8rem; filter: drop-shadow(0 2px 8px rgba(0,0,0,0.4)); margin-bottom:4px;">{t_info['icon']}</div>
                <div style="font-weight:800; font-size:1.05rem; color:#f8fafc;">{t_name}</div>
                <div style="font-size:0.8rem; color:#94a3b8; margin-top:2px;">{t_info['category']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Learn {t_name}", key=f"learn_btn_{idx}", use_container_width=True, type="primary"):
                st.session_state.task_name = t_name
                # Adapt step complexity to student's age!
                st.session_state.task_steps = adapt_steps_for_age(t_info["steps"], student_age)
                st.session_state.mcq_data = t_info["questions"]
                st.session_state.stage = 'mcq'
                st.session_state.mcq_answered = False
                st.rerun()

    st.markdown("---")
    st.subheader("Or type any custom life skill:")
    custom_name = st.text_input("Custom Skill Name", placeholder="e.g. Riding a bicycle")
    if st.button("Start Custom Skill 🚀", type="primary"):
        if custom_name.strip():
            with st.spinner("AI is generating custom step-by-step module..."):
                st.session_state.task_name = custom_name.strip()
                st.session_state.mcq_data = planner.generate_mcq(custom_name)
                raw_steps = planner.plan_task(custom_name)
                st.session_state.task_steps = adapt_steps_for_age(raw_steps, student_age)
                st.session_state.stage = 'mcq'
                st.session_state.mcq_answered = False
                st.rerun()
        else:
            st.warning("Please type a skill name!")
            
    st.markdown('</div>', unsafe_allow_html=True)

# ────────────────────────────────────────────────────────────────────────────
# STAGE 2 — MCQ KNOWLEDGE CHECK
# ────────────────────────────────────────────────────────────────────────────
elif st.session_state.stage == 'mcq':
    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
    st.subheader(f"📚 Quick Knowledge Check — {st.session_state.task_name}")
    st.write("Answer this question before we begin the lesson:")

    question_data = st.session_state.mcq_data[0]
    selected = st.radio(
        f"**{question_data.get('q', question_data.get('question'))}**",
        question_data.get('options', []),
        index=None,
        key="mcq_radio"
    )

    if not st.session_state.mcq_answered:
        if st.button("Submit Answer ✅", type="primary"):
            if selected is None:
                st.warning("⚠️ Please select an answer first!")
            else:
                st.session_state.mcq_answered = True
                st.session_state.mcq_result = (selected == question_data.get('answer'))
                st.rerun()
    else:
        # Show result feedback
        if st.session_state.mcq_result:
            st.success("🎉 Correct! Great thinking! You're ready to start the lesson.")
        else:
            st.warning(f"Not quite! The best answer is: **{question_data.get('answer')}** — don't worry, the lesson will help!")

        if st.button("➡️ Go to Step-by-Step Lesson", type="primary"):
            st.session_state.stage = 'steps'
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ────────────────────────────────────────────────────────────────────────────
# STAGE 3 — STEP-BY-STEP LESSON (AGE ADAPTED)
# ────────────────────────────────────────────────────────────────────────────
elif st.session_state.stage == 'steps':
    num_steps = len(st.session_state.task_steps)
    if 'completed_steps' not in st.session_state or len(st.session_state.completed_steps) != num_steps:
        st.session_state.completed_steps = [False] * num_steps

    completed_count = sum(st.session_state.completed_steps)
    progress = completed_count / num_steps

    # Header
    st.markdown(f"### 📋 Learning Module: **{st.session_state.task_name}** (Adapted for Age {student_age})")

    # Progress bar
    st.progress(progress)
    st.markdown("---")

    full_lesson_text = f"Learning module for {st.session_state.task_name}. " + " ".join([f"Step {idx+1}: {st.session_state.task_steps[idx]}." for idx in range(num_steps)])
    clean_full_text = full_lesson_text.replace("'", "\\'").replace('"', '\\"').replace("\n", " ")
    
    full_tts_html = f"""
    <div style="display:flex; gap:12px; align-items:center;">
        <button onclick="speakFullLesson()" style="
            background: linear-gradient(135deg, #6366f1, #a855f7);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 20px;
            font-weight: 700;
            font-size: 0.95rem;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(99,102,241,0.4);
        ">
            🎧 Play Full Audio Lesson
        </button>
        <button onclick="stopAudio()" style="
            background: rgba(239,68,68,0.8);
            color: white;
            border: none;
            padding: 10px 16px;
            border-radius: 20px;
            font-weight: 700;
            font-size: 0.95rem;
            cursor: pointer;
        ">
            ⏹️ Stop Audio
        </button>
    </div>
    <script>
    function speakFullLesson() {{
        if ('speechSynthesis' in window) {{
            window.speechSynthesis.cancel();
            var msg = new SpeechSynthesisUtterance("{clean_full_text}");
            msg.rate = 0.9;
            msg.pitch = 1.0;
            window.speechSynthesis.speak(msg);
        }}
    }}
    function stopAudio() {{
        if ('speechSynthesis' in window) {{
            window.speechSynthesis.cancel();
        }}
    }}
    </script>
    """
    components.html(full_tts_html, height=52)

    tab1, tab2 = st.tabs(["📖 Step-by-Step Guide", "ℹ️ Why is this important?"])

    with tab1:
        for i, step in enumerate(st.session_state.task_steps, 1):
            is_done = st.session_state.completed_steps[i - 1]
            bg = "rgba(16,185,129,0.25)" if is_done else "rgba(30, 41, 59, 0.9)"
            border = "#10B981" if is_done else "#FF6B6B"
            status_icon = "✅" if is_done else f"🔵 {i}"

            # Full step card rendered as HTML
            st.markdown(f"""
            <div style="
                background: {bg};
                border-left: 8px solid {border};
                border-radius: 12px;
                padding: 20px 24px;
                margin-bottom: 12px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            ">
                <div style="font-size:0.85rem; font-weight:700; color:{border}; margin-bottom:8px; text-transform:uppercase; letter-spacing:1px;">
                    STEP {i}  {status_icon}
                </div>
                <div style="font-size:1.25rem; font-weight:500; color:#f8fafc; line-height:1.7;">
                    {step}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Text-to-Speech Read Aloud button
            clean_text = step.replace("'", "\\'").replace('"', '\\"').replace("\n", " ")
            tts_html = f"""
            <button onclick="speakStep{i}()" style="
                background-color: #3B82F6;
                color: white;
                border: none;
                padding: 6px 14px;
                border-radius: 14px;
                font-weight: 600;
                font-size: 0.85rem;
                cursor: pointer;
                margin-bottom: 10px;
            ">
                🔊 Read Step {i} Aloud
            </button>
            <script>
            function speakStep{i}() {{
                if ('speechSynthesis' in window) {{
                    window.speechSynthesis.cancel();
                    var msg = new SpeechSynthesisUtterance("{clean_text}");
                    msg.rate = 0.9;
                    window.speechSynthesis.speak(msg);
                }}
            }}
            </script>
            """
            components.html(tts_html, height=42)

            if not is_done:
                if st.button(f"✅ Mark Step {i} as Done", key=f"btn_{i}", type="primary"):
                    st.session_state.completed_steps[i - 1] = True
                    st.rerun()
            else:
                st.markdown(
                    '<p style="color:#10B981; font-weight:700; margin-top:-10px; margin-bottom:12px;">🎉 Step Completed!</p>',
                    unsafe_allow_html=True
                )

        # All done!
        if all(st.session_state.completed_steps):
            st.balloons()
            st.success("🏆 Amazing! You completed ALL the steps! You earned +50 XP! Saved to your profile!")
            if "skill_xp_awarded" not in st.session_state:
                database.save_completed_skill(username, st.session_state.task_name, 50)
                st.session_state.skill_xp_awarded = True
            if st.button("🎊 Finish & Learn Another Skill", type="primary"):
                for key in ["stage", "task_name", "task_steps", "mcq_data",
                            "completed_steps", "mcq_answered", "mcq_result", "skill_xp_awarded", "auto_loaded_topic"]:
                    st.session_state.pop(key, None)
                st.rerun()

    with tab2:
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.markdown(f"""
        ### Why learn **{st.session_state.task_name}**?

        Learning this skill helps you:
        - 🌟 **Build independence** — you can do it yourself without asking for help
        - 💪 **Gain confidence** — every skill mastered makes you stronger
        - 🧠 **Train your brain** — breaking big tasks into steps makes everything easier
        - 🤝 **Earn trust** — adults around you see how capable you are

        > *"Every expert was once a beginner. Every step you take today makes tomorrow easier!"*
        """)
        st.markdown('</div>', unsafe_allow_html=True)
