import streamlit as st
import pandas as pd
import altair as alt
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rbac import enforce_access
import database
import importlib
importlib.reload(database)

st.set_page_config(page_title="Student Performance Dashboard", page_icon="📊", layout="wide")
enforce_access()

username = st.session_state.get("username", "Student")

# Fetch student profile & performance data from database
profile = database.get_student_profile(username)
if profile:
    s_name, s_age, s_dob, s_gender, s_style = profile
else:
    s_name = username
    s_age = st.session_state.get("student_age", 12)
    s_dob = "N/A"
    s_gender = "N/A"
    s_style = st.session_state.get("primary_profile", "Visual & Structured Learner")

summary = database.get_student_xp_summary(username)
completed_skills = database.get_completed_skills(username)
assessments_history = database.get_student_assessments_history(username)

# Calculate dynamic performance rank
skills_cnt = summary["skills_completed"]
avg_acc = summary["avg_score"]

if skills_cnt >= 10 and avg_acc >= 85:
    rank_title = "🏆 Master Champion"
    rank_color = "#EAB308"
elif skills_cnt >= 5 or avg_acc >= 70:
    rank_title = "🧠 Proficient Learner"
    rank_color = "#3B82F6"
elif skills_cnt >= 1 or avg_acc > 0:
    rank_title = "🚀 Skill Explorer"
    rank_color = "#10B981"
else:
    rank_title = "🌟 Beginner Learner"
    rank_color = "#A855F7"

# Header
st.title(f"📊 Student Performance Dashboard: {s_name}")
st.markdown(f"**Username:** `{username}` | **Age:** {s_age} years | **Learning Style:** {s_style} | **Performance Rank:** <span style='color:{rank_color}; font-weight:800; font-size:1.1rem;'>{rank_title}</span>", unsafe_allow_html=True)
st.markdown("---")

# 4 Key Performance Indicator (KPI) Cards
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'''
    <div class="kpi-card">
        <div class="kpi-value">{skills_cnt}</div>
        <div class="kpi-label">Skills Mastered</div>
    </div>
    ''', unsafe_allow_html=True)

with col2:
    acc_display = f"{int(avg_acc)}%" if summary["assessments_taken"] > 0 else "N/A"
    st.markdown(f'''
    <div class="kpi-card">
        <div class="kpi-value">{acc_display}</div>
        <div class="kpi-label">Quiz Accuracy</div>
    </div>
    ''', unsafe_allow_html=True)

with col3:
    streak = min(skills_cnt + (1 if summary["assessments_taken"] > 0 else 0), 7)
    st.markdown(f'''
    <div class="kpi-card">
        <div class="kpi-value">{streak} 🔥</div>
        <div class="kpi-label">Active Streak</div>
    </div>
    ''', unsafe_allow_html=True)

with col4:
    st.markdown(f'''
    <div class="kpi-card">
        <div class="kpi-value">{summary["total_xp"]} 💎</div>
        <div class="kpi-label">Total Performance XP</div>
    </div>
    ''', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 📌 Assigned Modules from Teacher
assigned_tasks = database.get_assigned_tasks(username)
st.markdown('<div class="feature-box" style="border-left: 5px solid #F59E0B; background: rgba(245, 158, 11, 0.15);">', unsafe_allow_html=True)
st.subheader("📌 Assigned Modules from Teacher")

if assigned_tasks:
    st.write(f"Your teacher has assigned **{len(assigned_tasks)}** learning task(s) for you:")
    for tid, t_user, mod_name, d_date, status, created in assigned_tasks:
        col_t1, col_t2 = st.columns([3, 1])
        with col_t1:
            st.markdown(f"🔹 **Module:** `{mod_name}` | **Assigned By:** Teacher `{t_user}` | **Due Date:** `{d_date}` | **Status:** `{status}`")
        with col_t2:
            if status == "Completed":
                st.success("Completed ✅")
            else:
                if st.button(f"Start {mod_name} 🚀", key=f"start_assign_{tid}", type="primary", use_container_width=True):
                    database.complete_assigned_task(tid)
                    mod_lower = mod_name.lower()
                    if "learn" in mod_lower or "skill" in mod_lower:
                        st.switch_page("pages/1_Learn_Skill.py")
                    elif "assessment" in mod_lower:
                        st.switch_page("pages/12_AI_Assessment.py")
                    elif "emotion" in mod_lower:
                        st.switch_page("pages/8_Emotion_Explorer.py")
                    elif "routine" in mod_lower:
                        st.switch_page("pages/7_Daily_Routines.py")
                    elif "focus" in mod_lower:
                        st.switch_page("pages/6_Focus_Timer.py")
                    elif "stori" in mod_lower:
                        st.switch_page("pages/5_Interactive_Stories.py")
                    elif "sensory" in mod_lower:
                        st.switch_page("pages/9_Sensory_Sandbox.py")
                    elif "money" in mod_lower:
                        st.switch_page("pages/18_Money_Manager.py")
                    elif "safety" in mod_lower:
                        st.switch_page("pages/17_Safety_Skills.py")
                    else:
                        st.switch_page("pages/1_Learn_Skill.py")
        st.markdown("<hr style='margin:8px 0;'>", unsafe_allow_html=True)
else:
    st.info("ℹ️ No pending module assignments from your teacher right now. You are all caught up! Feel free to pick any skill in **Learn Skill** or **AI Assessment**!")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# 🤖 Agentic AI Performance Evaluator
st.markdown('<div class="feature-box" style="border-left: 5px solid #6366F1;">', unsafe_allow_html=True)
st.subheader("🤖 Agentic AI Performance Evaluator")

if assessments_history:
    latest = assessments_history[0]
    score, total, level, asm_date = latest
    pct = int((score / total) * 100) if total > 0 else 0
    st.write(f"**Latest AI Assessment Score:** **{pct}% ({score}/{total})** — *{level}* (Taken on {asm_date[:10]})")
    
    if pct >= 80:
        st.success("🌟 **Outstanding Performance!** You demonstrate high mastery across your active skills. AI recommends attempting advanced road safety or money management!")
        rec_task = "Road Safety & Crossing"
    elif pct >= 50:
        st.info("👍 **Good Progress!** You have a solid grasp of core skills, but can improve speed and accuracy. AI recommends practicing sandwich preparation.")
        rec_task = "Making a sandwich"
    else:
        st.warning("💪 **Practice Needed:** Let's focus on step-by-step foundation skills to build your confidence!")
        rec_task = "Washing Hands"
else:
    st.info("💡 **Getting Started:** Take your first **AI Assessment** to unlock personalized AI task recommendations!")
    rec_task = "Brushing Teeth"

c_rec1, c_rec2 = st.columns([2, 1])
with c_rec1:
    if st.button(f"🚀 Start Recommended Task: {rec_task}", type="primary"):
        st.session_state.task_name = rec_task
        st.switch_page("pages/1_Learn_Skill.py")
with c_rec2:
    if st.button("📝 Take New AI Assessment", use_container_width=True):
        st.switch_page("pages/12_AI_Assessment.py")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Tabs for Performance Analytics, Assessment History, Achievements, and Teacher Messaging
tab1, tab2, tab3, tab4 = st.tabs(["📊 Performance & Mastery Breakdown", "📝 Assessment & Quiz Logs", "🏆 Badges & Milestones", "✉️ Message Teacher"])

with tab1:
    st.subheader(f"Category Mastery & Performance Analytics")
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("#### 🎯 Skill Domain Mastery Level")
        
        # Calculate mastery percentages based on completed skills & assessments
        completed_titles = [c[0].lower() for c in completed_skills]
        asm_titles = [a[2].lower() for a in assessments_history]
        all_activities = completed_titles + asm_titles

        hygiene_mastery  = min(100, (sum(1 for t in all_activities if any(k in t for k in ["brush", "wash", "hand", "teeth", "bath", "hair", "groom", "hygiene"])) / 2) * 100)
        kitchen_mastery  = min(100, (sum(1 for t in all_activities if any(k in t for k in ["sandw", "rice", "cook", "milk", "tea", "fruit", "veg", "meal", "kitchen"])) / 2) * 100)
        house_mastery    = min(100, (sum(1 for t in all_activities if any(k in t for k in ["table", "sweep", "fold", "laundry", "bed", "clean", "house"])) / 2) * 100)
        routine_mastery  = min(100, (sum(1 for t in all_activities if any(k in t for k in ["morn", "afternoon", "evening", "pack", "bag", "sched", "routin"])) / 2) * 100)
        safety_mastery   = min(100, (sum(1 for t in all_activities if any(k in t for k in ["road", "cross", "electric", "bus", "safet"])) / 2) * 100)
        finance_mastery  = min(100, (sum(1 for t in all_activities if any(k in t for k in ["money", "sav", "groc", "shop", "finan"])) / 2) * 100)
        emot_mastery     = min(100, (sum(1 for t in all_activities if any(k in t for k in ["calm", "breath", "emot", "feel", "sensory", "sandbox"])) / 2) * 100)
        comm_mastery     = min(100, (sum(1 for t in all_activities if any(k in t for k in ["help", "listen", "communicat", "social", "speak", "polit"])) / 2) * 100)

        # Personal Hygiene
        st.write("**🧼 Personal Hygiene:**")
        st.progress(hygiene_mastery / 100.0)
        st.caption(f"{int(hygiene_mastery)}% Mastered")

        # Kitchen / Cooking
        st.write("**🥪 Kitchen & Meal Prep:**")
        st.progress(kitchen_mastery / 100.0)
        st.caption(f"{int(kitchen_mastery)}% Mastered")

        # Household Skills
        st.write("**🧹 Household Chore Skills:**")
        st.progress(house_mastery / 100.0)
        st.caption(f"{int(house_mastery)}% Mastered")

        # Daily Routines
        st.write("**🕒 Daily Routine Management:**")
        st.progress(routine_mastery / 100.0)
        st.caption(f"{int(routine_mastery)}% Mastered")

        # Safety Skills
        st.write("**🚦 Safety & Road Skills:**")
        st.progress(safety_mastery / 100.0)
        st.caption(f"{int(safety_mastery)}% Mastered")

        # Financial Skills
        st.write("**💰 Financial & Money Skills:**")
        st.progress(finance_mastery / 100.0)
        st.caption(f"{int(finance_mastery)}% Mastered")

        # Emotional Regulation
        st.write("**😤 Emotional Regulation:**")
        st.progress(emot_mastery / 100.0)
        st.caption(f"{int(emot_mastery)}% Mastered")

        # Communication Skills
        st.write("**🗣️ Communication & Social Skills:**")
        st.progress(comm_mastery / 100.0)
        st.caption(f"{int(comm_mastery)}% Mastered")

    with col_b:
        st.markdown("#### 📈 XP & Performance Source Breakdown")
        df_chart = pd.DataFrame({
            "Source": ["Welcome Bonus", "Learn Skills", "Assessments"],
            "XP": [100, summary["skill_points"], summary["assessment_points"]]
        })
        chart = alt.Chart(df_chart).mark_bar(color='#6366F1', cornerRadius=8).encode(
            x=alt.X('Source:N', title="Activity Source"),
            y=alt.Y('XP:Q', title="XP Earned"),
            tooltip=['Source', 'XP']
        ).properties(height=280)
        st.altair_chart(chart, use_container_width=True)

with tab2:
    st.subheader("📝 Past Assessment Results & Skill History")
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown("##### 📝 AI Assessment Test Records")
        if assessments_history:
            df_asm = pd.DataFrame([
                {
                    "Date": r[3][:10] if r[3] else "N/A",
                    "Score": f"{r[0]} / {r[1]} ({int(r[0]/r[1]*100)}%)" if r[1] > 0 else "0%",
                    "Assessed Level": r[2]
                } for r in assessments_history
            ])
            st.dataframe(df_asm, use_container_width=True, hide_index=True)
        else:
            st.info("No assessment records found. Complete an AI Assessment to track your test history!")

    with col_t2:
        st.markdown("##### 🧠 Completed Learn Skill Modules")
        if completed_skills:
            df_sk = pd.DataFrame([
                {
                    "Skill Title": r[0],
                    "XP Earned": f"+{r[1]} XP",
                    "Completed On": r[2][:10] if r[2] else "N/A"
                } for r in completed_skills
            ])
            st.dataframe(df_sk, use_container_width=True, hide_index=True)
        else:
            st.info("No completed skills yet. Finish steps in Learn Skill to earn XP!")

with tab3:
    st.subheader("🏆 Your Trophy Room & Achievement Milestones")
    bc1, bc2, bc3, bc4 = st.columns(4)
    with bc1:
        has_first = skills_cnt >= 1
        st.markdown(f'''
        <div class="kpi-card" style="opacity: {1.0 if has_first else 0.4}">
            <div class="badge-icon">🌟</div>
            <b>First Step</b><br>
            <span style="color:#94a3b8;font-size:0.9rem;">{"Completed 1st skill" if has_first else "Complete 1 skill"}</span>
        </div>
        ''', unsafe_allow_html=True)
    with bc2:
        has_streak = skills_cnt >= 3
        st.markdown(f'''
        <div class="kpi-card" style="opacity: {1.0 if has_streak else 0.4}">
            <div class="badge-icon">🔥</div>
            <b>On Fire</b><br>
            <span style="color:#94a3b8;font-size:0.9rem;">{"3 Skills Completed" if has_streak else "Complete 3 skills"}</span>
        </div>
        ''', unsafe_allow_html=True)
    with bc3:
        has_asm = summary["assessments_taken"] >= 1
        st.markdown(f'''
        <div class="kpi-card" style="opacity: {1.0 if has_asm else 0.4}">
            <div class="badge-icon">🧠</div>
            <b>Assessment Star</b><br>
            <span style="color:#94a3b8;font-size:0.9rem;">{"Completed Assessment" if has_asm else "Take AI Assessment"}</span>
        </div>
        ''', unsafe_allow_html=True)
    with bc4:
        has_master = skills_cnt >= 5 and avg_acc >= 80
        st.markdown(f'''
        <div class="kpi-card" style="opacity: {1.0 if has_master else 0.4}">
            <div class="badge-icon">👑</div>
            <b>Skill Master</b><br>
            <span style="color:#94a3b8;font-size:0.9rem;">{"Mastered 5 Skills & >80%" if has_master else "Complete 5 Skills & >80% Quiz"}</span>
        </div>
        ''', unsafe_allow_html=True)

with tab4:
    st.subheader("✉️ Send a Message to Your Teacher")
    st.write(f"Have a question or need help with a skill, **{s_name}**? Send a message directly to your teacher below!")
    
    with st.form("student_msg_form", clear_on_submit=True):
        stu_msg_text = st.text_area("Write your message to your teacher:", placeholder="Hello Teacher, I have a question about my daily routine schedule...")
        stu_submitted = st.form_submit_button("Send Message to Teacher 📤", type="primary")
        
        if stu_submitted:
            if stu_msg_text.strip():
                if database.send_message(username, "Teacher", s_name, stu_msg_text.strip()):
                    st.success("✅ Message sent to Teacher successfully!")
                    st.balloons()
                else:
                    st.error("Failed to send message.")
            else:
                st.warning("Please enter a message before sending.")
    
    st.markdown("---")
    st.subheader("💬 Active Messenger Thread with Teacher")
    stu_history = database.get_messages(username)
    
    if stu_history:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for m_id, sender, receiver, s_name_ref, msg, reply, created_at in reversed(stu_history):
            if sender == username:
                # Student outgoing bubble (Right)
                st.markdown(f'''
                <div class="chat-bubble-user">
                    <div class="chat-meta">🎒 <b>You ({s_name})</b> • {created_at[:16]}</div>
                    <div>{msg}</div>
                </div>
                ''', unsafe_allow_html=True)
                
                # Teacher reply bubble (Left)
                if reply:
                    st.markdown(f'''
                    <div class="chat-bubble-other">
                        <div class="chat-meta">👩‍🏫 <b>Teacher Reply</b></div>
                        <div>{reply}</div>
                    </div>
                    ''', unsafe_allow_html=True)
                else:
                    st.caption("⏳ *Awaiting Teacher response...*")
            else:
                # Teacher incoming bubble (Left)
                st.markdown(f'''
                <div class="chat-bubble-other">
                    <div class="chat-meta">👩‍🏫 <b>Teacher</b> • {created_at[:16]}</div>
                    <div>{msg}</div>
                </div>
                ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No active chat messages with your teacher yet. Send a message above to start your conversation!")
