import streamlit as st
import pandas as pd
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rbac import enforce_access
import database
import importlib
importlib.reload(database)

st.set_page_config(page_title="Parent Dashboard", page_icon="👨‍👩‍👧", layout="wide")
enforce_access()

st.title("👨‍👩‍👧 Parent Dashboard")
st.write("Welcome! Monitor your child's progress and stay involved in their learning journey.")

# Fetch all registered students from SQLite Database
db_students = database.get_all_users("Student")
student_names = [s[0] for s in db_students] if db_students else ["vv", "Alex", "Jordan", "Sam"]
if "vv" not in student_names:
    student_names.insert(0, "vv")

parent_user = st.session_state.get("username", "Parent")

selected_child = st.selectbox("👶 Select Your Child:", student_names)

t1, t2 = st.tabs(["📊 Child Performance & Reports", "✉️ Message Teacher"])

with t1:
    rpt = database.generate_formatted_student_report(selected_child)
    
    st.code(rpt['formatted_text'], language="text")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.download_button(
        label=f"📥 Download {rpt['student_name']}'s Formatted Progress Report",
        data=rpt['formatted_text'],
        file_name=f"{rpt['student_name']}_Life_Skills_Report.txt",
        mime="text/plain",
        type="primary",
        use_container_width=True
    )

with t2:
    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
    st.subheader(f"✉️ Send Message to Teacher regarding {selected_child}")
    
    with st.form("parent_msg_form", clear_on_submit=True):
        msg_text = st.text_area("Write your message to the teacher:", placeholder=f"Hello Teacher, I wanted to ask about {selected_child}'s progress in Money Management...")
        submitted = st.form_submit_button("Send Message 📤", type="primary")
        
        if submitted:
            if msg_text.strip():
                if database.send_message(parent_user, "Teacher", selected_child, msg_text.strip()):
                    st.success("✅ Message sent to Teacher successfully!")
                    st.balloons()
                else:
                    st.error("Failed to send message.")
            else:
                st.warning("Please enter a message before sending.")
    
    st.markdown("---")
    st.subheader("💬 Active Messenger Thread with Teacher")
    history = database.get_messages(parent_user)
    
    if history:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for m_id, sender, receiver, s_name, msg, reply, created_at in reversed(history):
            if sender == parent_user:
                # Parent outgoing bubble (Right)
                st.markdown(f'''
                <div class="chat-bubble-user">
                    <div class="chat-meta">👨‍👩‍👧 <b>You ({parent_user})</b> • Child: <b>{s_name or selected_child}</b> • {created_at[:16]}</div>
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
                    st.caption("⏳ *Awaiting Teacher reply...*")
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
        st.info("No active chat messages with teacher. Send a message above to start your conversation!")
    st.markdown('</div>', unsafe_allow_html=True)
