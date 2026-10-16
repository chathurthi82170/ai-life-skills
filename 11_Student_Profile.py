import streamlit as st
import streamlit.components.v1 as components
import sys, os
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rbac import enforce_access
import database
import importlib
importlib.reload(database)

st.set_page_config(page_title="Student Profile", page_icon="📝", layout="wide")
enforce_access()

st.title("📝 Step 1: Student Profile & Personal Details")
st.write("Fill in your personal details and learning preferences. All details are saved in the database.")

username = st.session_state.get("username", "vv")

# Load existing profile from SQLite database if available
existing_profile = database.get_student_profile(username)
if existing_profile:
    default_name, default_age, default_dob, default_gender, default_style = existing_profile
    try:
        default_dob_date = datetime.datetime.strptime(default_dob, "%Y-%m-%d").date()
    except Exception:
        default_dob_date = datetime.date(2012, 1, 1)
else:
    default_name = username
    default_age = 12
    default_dob_date = datetime.date(2012, 1, 1)
    default_gender = "Male"
    default_style = "Visual & Structured Learner"

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
    st.subheader("👤 Personal Details (Saved to Database)")
    
    name = st.text_input("Full Name", value=default_name)
    age = st.number_input("Age", min_value=3, max_value=25, value=int(default_age))
    dob = st.date_input("Date of Birth (DOB)", value=default_dob_date)
    
    gender_list = ["Male", "Female", "Other"]
    g_idx = gender_list.index(default_gender) if default_gender in gender_list else 0
    gender = st.selectbox("Gender", gender_list, index=g_idx)
    
    profiles = ["Visual & Structured Learner", "Active & High-Energy Learner", "Reading & Word Builder", "Hands-On Kinesthetic Learner", "Auditory & Speech Learner", "Gentle Pace Learner"]
    p_idx = profiles.index(default_style) if default_style in profiles else 0
    learning_style = st.selectbox("Primary Learning Style", profiles, index=p_idx)
    
    if st.button("💾 Save Profile to Database & Continue ➡️", type="primary", use_container_width=True):
        if name.strip():
            database.save_student_profile(username, name.strip(), age, str(dob), gender, learning_style)
            st.session_state.username = username
            st.session_state.student_age = age
            st.session_state.primary_profile = learning_style
            st.session_state.learning_preference = learning_style
            st.session_state.profile_completed = True
            st.success("✅ Profile saved to database successfully!")
            st.switch_page("pages/12_AI_Assessment.py")
        else:
            st.error("Please enter a valid student name.")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
    st.subheader("🎯 Active Profile Summary")
    st.write(f"**Student Username:** **{username}**")
    st.write(f"**Selected Gender:** {gender}")
    st.write(f"**Date of Birth:** **{dob}**")
    st.write(f"**Age:** {age} years old")
    st.write(f"**Active Learning Style:** **{learning_style}**")
    
    st.markdown("---")
    st.info("👁️ **AI Customization Active:** Lessons, voice prompts, and task steps will automatically adapt to your age and selected learning style.")
    st.markdown('</div>', unsafe_allow_html=True)
