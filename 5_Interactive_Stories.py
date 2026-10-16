import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rbac import enforce_access
from content_generator import generate_stories

st.set_page_config(page_title="Interactive Stories", page_icon="📚", layout="wide")
enforce_access()

st.markdown("""
<style>
    
    .story-card { background-color: #F8FAFC; padding: 25px; border-radius: 12px; border-left: 5px solid #7C3AED; font-size: 1.2rem; margin-bottom: 20px;}
</style>
""", unsafe_allow_html=True)

st.title("📚 Interactive Social Stories")
st.write("Welcome to the interactive story module! Read the randomly generated scenarios and choose what to do next to practice real-world situations.")

# Load random stories into session state so they don't change on every button click
if 'current_stories' not in st.session_state:
    st.session_state.current_stories = generate_stories(3)

if st.button("🔀 Generate New Scenarios", type="primary"):
    st.session_state.current_stories = generate_stories(3)
    st.rerun()

st.markdown("---")

for i, story in enumerate(st.session_state.current_stories, 1):
    st.markdown(f'<div class="story-card"><b>Scenario {i}:</b><br><br>{story["scenario"]}</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    opt1 = story["options"][0]
    opt2 = story["options"][1]
    
    with col1:
        if st.button(opt1[0], key=f"s{i}_btn1", use_container_width=True):
            if opt1[1]: # if correct
                st.success(f"✅ {opt1[2]}")
                st.balloons()
            else:
                st.warning(f"⚠️ {opt1[2]}")
    with col2:
        if st.button(opt2[0], key=f"s{i}_btn2", use_container_width=True):
            if opt2[1]: # if correct
                st.success(f"✅ {opt2[2]}")
                st.balloons()
            else:
                st.warning(f"⚠️ {opt2[2]}")
                
    st.markdown("---")
