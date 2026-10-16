import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rbac import enforce_access
from content_generator import generate_emotions

st.set_page_config(page_title="Emotion Explorer", page_icon="😊", layout="wide")
enforce_access()

st.title("😊 Emotion Explorer")
st.write("Recognize and explore different feelings with visual emojis, coping strategies, and interactive scenarios!")

mode = st.radio("Select Activity Mode:", ["📖 Teach Me Emotions", "🧠 Test Me Scenario Quiz"], horizontal=True)

st.markdown("---")

if mode == "📖 Teach Me Emotions":
    st.subheader("Explore Different Feelings & Coping Tools")
    
    emotions_data = [
        {"emoji": "😊", "name": "Happy & Joyful", "looks": "Big smile, bright eyes, laughing.", "when": "Playing with friends, achieving a goal, receiving praise.", "coping": "Share your joy with others and celebrate!"},
        {"emoji": "😢", "name": "Sad & Hurt", "looks": "Tears, frowning, quiet body.", "when": "Losing a toy, missing someone, feeling left out.", "coping": "Ask for a hug, talk to a trusted adult, or listen to music."},
        {"emoji": "😤", "name": "Angry & Frustrated", "looks": "Clenched fists, red cheeks, tight jaw.", "when": "Something feels unfair or a task is too hard.", "coping": "Take 5 deep breaths, squeeze a stress ball, or visit the Sensory Sandbox."},
        {"emoji": "😨", "name": "Scared & Anxious", "looks": "Wide eyes, fast heartbeat, hiding.", "when": "Darkness, loud noises, trying new unfamiliar tasks.", "coping": "Hold a favorite comfort item, count to 10 slowly, ask an adult for help."},
        {"emoji": "🥳", "name": "Excited & Proud", "looks": "Jumping up, big smile, clapping hands.", "when": "Completing a hard skill, going to a fun place.", "coping": "Do a happy dance, tell your parents what you accomplished!"},
        {"emoji": "😌", "name": "Calm & Peaceful", "looks": "Relaxed shoulders, soft breathing, gentle smile.", "when": "Reading a book, relaxing in bed, after deep breathing.", "coping": "Enjoy the quiet moment and keep your mind peaceful."},
        {"emoji": "😲", "name": "Surprised & Amazed", "looks": "Open mouth, raised eyebrows, gasping.", "when": "Receiving an unexpected gift, seeing a cool magic trick.", "coping": "Take a moment to process the big surprise with a smile!"},
        {"emoji": "😳", "name": "Embarrassed & Shy", "looks": "Blushing cheeks, looking down, hiding face.", "when": "Making a mistake in front of others, spilling something.", "coping": "Remember everyone makes mistakes! Take a breath and smile."},
        {"emoji": "🤯", "name": "Overwhelmed & Tired", "looks": "Holding head, heavy sighing, feeling stuck.", "when": "Too many loud noises or too many tasks at once.", "coping": "Take a 5-minute break in a quiet spot or use the Focus Timer."},
        {"emoji": "🥺", "name": "Lonely & Left Out", "looks": "Quiet body, looking at others playing, feeling small.", "when": "Friends playing a game without you, being away from home.", "coping": "Politely ask 'Can I join your game?' or talk to your teacher."}
    ]
    
    cols = st.columns(3)
    for idx, em in enumerate(emotions_data):
        col = cols[idx % 3]
        with col:
            st.markdown(f"""
            <div class="kpi-card" style="text-align:center; padding:18px; margin-bottom:15px; border-left:6px solid #FF6B6B;">
                <div style="font-size:3.5rem; filter: drop-shadow(0 2px 8px rgba(0,0,0,0.3)); margin-bottom:8px;">{em['emoji']}</div>
                <h3 style="margin-bottom:8px;">{em['name']}</h3>
                <p style="text-align:left; font-size:0.95rem; line-height:1.5;">
                    <b>👀 Looks like:</b> {em['looks']}<br>
                    <b>💭 Happens when:</b> {em['when']}<br>
                    <b>💡 Helpful Coping Tool:</b> {em['coping']}
                </p>
            </div>
            """, unsafe_allow_html=True)

else:
    st.subheader("Test Your Knowledge!")
    st.write("Read the scenarios below and identify how the person is feeling.")
    
    if 'current_emotions' not in st.session_state:
        st.session_state.current_emotions = generate_emotions(3)

    if st.button("🔀 Load New Scenarios", type="primary"):
        st.session_state.current_emotions = generate_emotions(3)
        st.rerun()
        
    for i, em in enumerate(st.session_state.current_emotions, 1):
        st.markdown(f"#### Scenario {i}")
        st.info(em["scenario"])
        
        ans = st.selectbox("They feel...", ["Select..."] + em["options"], key=f"e_q{i}")
        
        if ans != "Select...":
            if ans == em["answer"]:
                st.success(f"✅ Correct! They probably feel {ans}.")
                if i == len(st.session_state.current_emotions):
                    st.balloons()
            else:
                st.warning(f"⚠️ Think about how you would feel if that happened to you. Try again!")
        st.markdown("---")
