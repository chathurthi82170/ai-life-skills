import streamlit as st
import time

st.set_page_config(page_title="Visual Focus Timer", page_icon="⏱️", layout="centered")
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rbac import enforce_access
enforce_access()






st.markdown("""
<style>
    
    .timer-display { font-size: 5rem; font-weight: bold; color: #2563EB; text-align: center; margin-top: 20px;}
</style>
""", unsafe_allow_html=True)

st.title("⏱️ Visual Focus Timer")
st.write("Use this visual timer to help you focus on your daily routines. Great for keeping attention on micro-steps!")

minutes = st.slider("Select Minutes to Focus:", 1, 30, 5)

if st.button("🚀 Start Focus Session", type="primary", use_container_width=True):
    progress_bar = st.progress(0.0)
    status_text = st.empty()
    
    total_seconds = minutes * 60
    
    # Fast simulation for demo purposes so you don't actually wait 5 minutes
    st.info("*(Running in fast-simulation mode for the project demo)*")
    for i in range(total_seconds):
        time.sleep(0.01) # Simulated fast timer
        
        progress = (i + 1) / total_seconds
        progress_bar.progress(progress)
        
        remaining = total_seconds - i
        mins, secs = divmod(remaining, 60)
        status_text.markdown(f'<div class="timer-display">{mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
        
    status_text.markdown('<div class="timer-display" style="color: #10B981;">00:00</div>', unsafe_allow_html=True)
    st.success("Time's up! Incredible focus! 🎉")
    st.balloons()
