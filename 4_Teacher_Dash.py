import streamlit as st
import pandas as pd
import sys, os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rbac import enforce_access
import database
import importlib
importlib.reload(database)

st.set_page_config(page_title="Teacher Dashboard", page_icon="👩‍🏫", layout="wide")
enforce_access()

st.title("👩‍🏫 Teacher Dashboard")

# Fetch all registered students from SQLite Database
db_students = database.get_all_users("Student")
student_names = [s[0] for s in db_students] if db_students else ["vv", "Alex", "Jordan", "Sam"]
if "vv" not in student_names:
    student_names.insert(0, "vv")

t1, t2, t3, t4 = st.tabs(["📊 Class Progress & Student Drilldown", "📝 Assign Tasks", "📄 Generate Reports", "✉️ Parent Messages & Replies"])

with t1:
    st.markdown('<div class="teacher-card">', unsafe_allow_html=True)
    st.subheader("📊 Class Progress Tracker (Live Database)")
    st.write("Overview of all students, their total skills mastered, AI assessment scores, and total XP.")
    
    # Build live table of registered students, completed skills, and SQLite assessment scores
    table_data = []
    
    for idx, s_name in enumerate(student_names):
        prof = database.get_student_profile(s_name)
        s_display_name = prof[0] if prof else s_name
        s_age = prof[1] if prof else "N/A"
        s_style = prof[4] if prof else "N/A"
        
        summary = database.get_student_xp_summary(s_name)
        latest_asm = database.get_latest_assessment(s_name)
        
        if latest_asm:
            score_text = f"{latest_asm[0]} / {latest_asm[1]} ({int((latest_asm[0]/latest_asm[1])*100)}%)"
            level_text = latest_asm[2]
        else:
            score_text = "Pending"
            level_text = "Not Taken Yet ⭐"
            
        table_data.append({
            "Username": s_name,
            "Full Name": s_display_name,
            "Age": s_age,
            "Learning Profile": s_style,
            "Skills Mastered": summary["skills_completed"],
            "Latest AI Assessment": score_text,
            "Assigned Level": level_text,
            "Total XP": f"{summary['total_xp']} 💎"
        })
        
    students_df = pd.DataFrame(table_data)
    st.dataframe(students_df, use_container_width=True, hide_index=True)
    st.info(f"Total Registered Students in Database: **{len(student_names)}**")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Detailed Individual Student Inspector
    st.markdown('<div class="feature-box" style="border-left: 5px solid #3B82F6;">', unsafe_allow_html=True)
    st.subheader("🔍 Individual Student Progress Inspector")
    st.write("Select a student below to inspect their complete Learn Skill log and AI Assessment test history:")
    
    selected_inspect_student = st.selectbox("Select Student to Inspect:", student_names, key="inspect_student_select")
    
    s_prof = database.get_student_profile(selected_inspect_student)
    s_summary = database.get_student_xp_summary(selected_inspect_student)
    s_completed_skills = database.get_completed_skills(selected_inspect_student)
    s_asm_history = database.get_student_assessments_history(selected_inspect_student)
    
    st.markdown(f"### 👤 Progress File for: **{selected_inspect_student}** ({s_prof[0] if s_prof else selected_inspect_student})")
    
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        st.metric("Skills Mastered", s_summary["skills_completed"])
    with col_stat2:
        acc_val = f"{int(s_summary['avg_score'])}%" if s_summary["assessments_taken"] > 0 else "N/A"
        st.metric("Avg Assessment Accuracy", acc_val)
    with col_stat3:
        st.metric("Total XP Balance", f"{s_summary['total_xp']} 💎")
        
    st.markdown("---")
    
    col_insp1, col_insp2 = st.columns(2)
    
    with col_insp1:
        st.markdown("#### 🧠 Completed Learn Skill Modules")
        if s_completed_skills:
            df_sk = pd.DataFrame([
                {
                    "Skill Title": r[0],
                    "XP Earned": f"+{r[1]} XP",
                    "Completed Date": r[2][:10] if r[2] else "N/A"
                } for r in s_completed_skills
            ])
            st.dataframe(df_sk, use_container_width=True, hide_index=True)
        else:
            st.info(f"Student '{selected_inspect_student}' has not completed any Learn Skill modules yet.")

    with col_insp2:
        st.markdown("#### 📝 AI Assessment Test Records")
        if s_asm_history:
            df_asm = pd.DataFrame([
                {
                    "Date": r[3][:10] if r[3] else "N/A",
                    "Score": f"{r[0]} / {r[1]} ({int(r[0]/r[1]*100)}%)" if r[1] > 0 else "0%",
                    "Level Assigned": r[2]
                } for r in s_asm_history
            ])
            st.dataframe(df_asm, use_container_width=True, hide_index=True)
        else:
            st.info(f"Student '{selected_inspect_student}' has not taken any AI Assessment tests yet.")
            
    st.markdown('</div>', unsafe_allow_html=True)

with t2:
    st.markdown('<div class="teacher-card">', unsafe_allow_html=True)
    st.subheader("Assign Learning Modules to Students")
    c1, c2 = st.columns(2)
    with c1:
        selected_student = st.selectbox("Select Student", ["Entire Class"] + student_names)
        selected_module = st.selectbox("Select Module", ["Learn Skill", "AI Assessment", "Emotion Explorer", "Daily Routines", "Focus Timer", "Interactive Stories", "Sensory Sandbox", "Money Manager", "Safety Skills"])
    with c2:
        due_date = st.date_input("Due Date")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Assign Module 📬", type="primary", use_container_width=True):
            teacher_user = st.session_state.get("username", "Teacher")
            database.assign_task(selected_student, teacher_user, selected_module, str(due_date))
            st.success(f"✅ Successfully assigned **{selected_module}** to **{selected_student}**! It will appear on their Student Dashboard.")
            st.balloons()
            
    st.markdown("---")
    st.subheader("📋 Active Assigned Modules (Live Database)")
    if student_names:
        all_assigned = []
        for s in student_names:
            tasks = database.get_assigned_tasks(s)
            for tid, t_user, mod, d_date, status, created in tasks:
                all_assigned.append({
                    "Student": s,
                    "Assigned Module": mod,
                    "Assigned By": t_user,
                    "Due Date": d_date,
                    "Status": status,
                    "Date Assigned": created[:10] if created else "N/A"
                })
        if all_assigned:
            st.dataframe(pd.DataFrame(all_assigned), use_container_width=True, hide_index=True)
        else:
            st.info("No active assigned modules yet.")
    st.markdown('</div>', unsafe_allow_html=True)

with t3:
    st.markdown('<div class="teacher-card">', unsafe_allow_html=True)
    st.subheader("📄 Export Formatted Student Reports")
    st.write("Generate and download structured progress reports for parents and conferences.")
    report_student = st.selectbox("Select Student for Report", student_names, key="rpt_stu_sel")
    
    rpt = database.generate_formatted_student_report(report_student)
    st.markdown('<div class="feature-box" style="border-left: 6px solid #6366F1; background: rgba(30,41,59,0.95); padding: 20px; border-radius: 16px;">', unsafe_allow_html=True)
    st.code(rpt['formatted_text'], language="text")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.download_button(
        label=f"Generate & Download {report_student}'s Formatted Report 📥",
        data=rpt['formatted_text'],
        file_name=f"{report_student}_Progress_Report.txt",
        mime="text/plain",
        type="primary",
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

with t4:
    st.markdown('<div class="teacher-card">', unsafe_allow_html=True)
    st.subheader("💬 Teacher Messenger Center")
    st.write("Live 1-on-1 Messenger interface for Student and Parent conversations.")
    
    chat_tab_stu, chat_tab_par = st.tabs(["🎒 Student Messenger", "👨‍👩‍👧 Parent Messenger"])
    
    all_messages = database.get_messages()
    
    with chat_tab_stu:
        # Allow selecting any registered student from student_names list
        sel_stu = st.selectbox("💬 Select Student to Chat With:", student_names, key="sel_stu_chat_v2")
        stu_messages = [m for m in all_messages if m[1] == sel_stu or (m[1] == "Teacher" and m[2] == sel_stu)]
        
        if stu_messages:
            # Chat Container Box
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            for m_id, sender, receiver, s_name, msg_text, reply, created_at in reversed(stu_messages):
                if sender == sel_stu:
                    # Student incoming bubble (Left)
                    st.markdown(f'''
                    <div class="chat-bubble-other">
                        <div class="chat-meta">🎒 <b>{sender}</b> ({s_name}) • {created_at[:16]}</div>
                        <div>{msg_text}</div>
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    # Teacher reply bubble (Right)
                    if reply:
                        st.markdown(f'''
                        <div class="chat-bubble-user">
                            <div class="chat-meta">👩‍🏫 <b>You (Teacher)</b></div>
                            <div>{reply}</div>
                        </div>
                        ''', unsafe_allow_html=True)
                else:
                    # Teacher outgoing bubble (Right)
                    st.markdown(f'''
                    <div class="chat-bubble-user">
                        <div class="chat-meta">👩‍🏫 <b>You (Teacher)</b> • {created_at[:16]}</div>
                        <div>{msg_text}</div>
                    </div>
                    ''', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            latest_unreplied = [m for m in stu_messages if m[1] == sel_stu and not m[5]]
            
            with st.form(key=f"stu_messenger_form_{sel_stu}", clear_on_submit=True):
                reply_input = st.text_input("Type your message...", placeholder=f"Send message to {sel_stu}...", key=f"stu_input_{sel_stu}")
                btn_send = st.form_submit_button("Send Message 📤", type="primary")
                if btn_send:
                    if reply_input.strip():
                        if latest_unreplied:
                            database.reply_message(latest_unreplied[0][0], reply_input.strip())
                        else:
                            database.send_message("Teacher", sel_stu, sel_stu, reply_input.strip())
                        st.success(f"Message sent to {sel_stu}!")
                        st.rerun()
                    else:
                        st.warning("Please type a message first.")
        else:
            st.info(f"No previous chat history with **{sel_stu}**. Type a message below to start a conversation!")
            with st.form(key=f"stu_init_form_{sel_stu}", clear_on_submit=True):
                init_msg = st.text_input("Start conversation:", placeholder=f"Hello {sel_stu}! How are your daily skills going?")
                btn_init = st.form_submit_button("Send Message 📤", type="primary")
                if btn_init and init_msg.strip():
                    database.send_message("Teacher", sel_stu, sel_stu, init_msg.strip())
                    st.success(f"Message sent to {sel_stu}!")
                    st.rerun()

    with chat_tab_par:
        # Build parent list indexed by student names so teacher can select conversation by child name
        parent_users = database.get_all_users("Parent")
        
        # Collect all parent messages and associate with student name
        par_messages_all = [m for m in all_messages if m[1] not in student_names and m[1] != "Teacher"]
        
        # Build options for selector: "Parent_User (Child: vv)"
        par_options = []
        par_map = {} # map label -> (parent_username, student_name)
        
        for m in par_messages_all:
            p_user = m[1]
            c_name = m[3] if m[3] else "Student"
            label = f"👨‍👩‍👧 {p_user} (Child: {c_name})"
            if label not in par_options:
                par_options.append(label)
                par_map[label] = (p_user, c_name)
                
        # Also add registered students with default parent label if not in list
        for s in student_names:
            label = f"👨‍👩‍👧 Parent of {s}"
            if label not in par_options:
                par_options.append(label)
                par_map[label] = (f"Parent_{s}", s)

        sel_label = st.selectbox("💬 Select Parent Conversation (by Student):", par_options, key="sel_par_chat_v3")
        target_par, target_child = par_map[sel_label]
        
        par_messages = [m for m in all_messages if (m[1] == target_par or (m[1] == "Teacher" and m[2] == target_par)) or (m[3] == target_child and m[1] not in student_names)]
        
        if par_messages:
            # Chat Container Box
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            for m_id, sender, receiver, s_name, msg_text, reply, created_at in reversed(par_messages):
                if sender != "Teacher":
                    # Parent incoming bubble (Left)
                    st.markdown(f'''
                    <div class="chat-bubble-other">
                        <div class="chat-meta">👨‍👩‍👧 <b>Parent: {sender}</b> (Child: <b>{s_name or target_child}</b>) • {created_at[:16]}</div>
                        <div>{msg_text}</div>
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    # Teacher reply bubble (Right)
                    if reply:
                        st.markdown(f'''
                        <div class="chat-bubble-user">
                            <div class="chat-meta">👩‍🏫 <b>You (Teacher)</b></div>
                            <div>{reply}</div>
                        </div>
                        ''', unsafe_allow_html=True)
                else:
                    # Teacher outgoing bubble (Right)
                    st.markdown(f'''
                    <div class="chat-bubble-user">
                        <div class="chat-meta">👩‍🏫 <b>You (Teacher)</b> • {created_at[:16]}</div>
                        <div>{msg_text}</div>
                    </div>
                    ''', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            latest_unreplied = [m for m in par_messages if m[1] != "Teacher" and not m[5]]
            
            with st.form(key=f"par_messenger_form_{target_par}_{target_child}", clear_on_submit=True):
                reply_input = st.text_input("Type your message to parent...", placeholder=f"Reply regarding {target_child}...", key=f"par_input_{target_par}_{target_child}")
                btn_send = st.form_submit_button("Send Message to Parent 📤", type="primary")
                if btn_send:
                    if reply_input.strip():
                        if latest_unreplied:
                            database.reply_message(latest_unreplied[0][0], reply_input.strip())
                        else:
                            database.send_message("Teacher", target_par, target_child, reply_input.strip())
                        st.success(f"Message sent to Parent of {target_child}!")
                        st.rerun()
                    else:
                        st.warning("Please type a message first.")
        else:
            st.info(f"No previous chat history with Parent of **{target_child}**. Type a message below to send them an update!")
            with st.form(key=f"par_init_form_{target_par}_{target_child}", clear_on_submit=True):
                init_msg = st.text_input("Start conversation:", placeholder=f"Hello! Sending update regarding {target_child}'s progress...")
                btn_init = st.form_submit_button("Send Message to Parent 📤", type="primary")
                if btn_init and init_msg.strip():
                    database.send_message("Teacher", target_par, target_child, init_msg.strip())
                    st.success(f"Message sent to Parent of {target_child}!")
                    st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
