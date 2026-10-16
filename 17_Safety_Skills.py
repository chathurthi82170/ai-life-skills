import streamlit as st
import sys, os
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rbac import enforce_access

st.set_page_config(page_title="Safety Skills", page_icon="🦺", layout="wide")
enforce_access()

st.title("🦺 Safety Skills Trainer")
st.write("Learn how to stay safe at home, on the road, and online through fun interactive scenarios!")

tab1, tab2, tab3 = st.tabs(["🚦 Road Safety", "🏠 Home Safety", "💻 Digital Safety"])

with tab1:
    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
    st.subheader("🚦 Road Safety Scenarios")
    
    scenarios = [
        {
            "q": "You want to cross the road. The traffic light for pedestrians is RED. What should you do?",
            "options": ["Cross quickly while no car is coming", "Wait for the light to turn GREEN", "Run across immediately"],
            "answer": "Wait for the light to turn GREEN",
            "tip": "Always wait for the GREEN pedestrian signal before crossing!"
        },
        {
            "q": "You are walking on a road without a footpath. Which side should you walk on?",
            "options": ["Right side (same as traffic)", "Left side (facing traffic)", "Middle of the road"],
            "answer": "Left side (facing traffic)",
            "tip": "Walk facing oncoming traffic so you can see vehicles coming towards you!"
        },
        {
            "q": "Before crossing a road, what should you do first?",
            "options": ["Look at your phone", "Look left, right, then left again", "Run across quickly"],
            "answer": "Look left, right, then left again",
            "tip": "The 'Look Left, Right, Left' rule ensures you see traffic from both directions!"
        },
    ]
    
    scenario = random.choice(scenarios)
    if 'road_q' not in st.session_state:
        st.session_state.road_q = random.choice(scenarios)
    
    scenario = st.session_state.road_q
    st.info(f"**Scenario:** {scenario['q']}")
    
    if 'road_options' not in st.session_state or st.session_state.get('current_road_q') != scenario['q']:
        opts = list(scenario['options'])
        random.shuffle(opts)
        st.session_state.road_options = opts
        st.session_state.current_road_q = scenario['q']
        
    answer = st.radio("Choose your answer:", st.session_state.road_options, index=None, key="road_ans")
    
    if st.button("Submit Answer 🚦", key="road_submit"):
        if answer is None:
            st.warning("⚠️ Please select an answer first!")
        elif answer == scenario['answer']:
            st.success(f"✅ Correct! {scenario['tip']}")
            st.balloons()
        else:
            st.error(f"❌ Incorrect! You selected: '{answer}'. The correct answer is: '{scenario['answer']}'. {scenario['tip']}")
    
    if st.button("Try Another Scenario 🔄", key="road_next"):
        st.session_state.road_q = random.choice(scenarios)
        if 'road_options' in st.session_state:
            del st.session_state['road_options']
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
    st.subheader("🏠 Home Safety Quiz")
    
    home_scenarios = [
        {
            "q": "You see a socket with water near it. What should you do?",
            "options": ["Touch the socket to see if it works", "Tell an adult immediately", "Ignore it"],
            "answer": "Tell an adult immediately",
            "tip": "Water and electricity are very dangerous together. Always tell an adult!"
        },
        {
            "q": "You accidentally break a glass on the floor. What is the SAFEST first step?",
            "options": ["Pick it up with bare hands", "Walk away and ignore it", "Warn others and get an adult to clean it"],
            "answer": "Warn others and get an adult to clean it",
            "tip": "Broken glass is sharp. Always warn others to stay away and get adult help!"
        },
    ]
    
    if 'home_q' not in st.session_state:
        st.session_state.home_q = random.choice(home_scenarios)
    
    hs = st.session_state.home_q
    st.warning(f"**Situation:** {hs['q']}")
    
    if 'home_options' not in st.session_state or st.session_state.get('current_home_q') != hs['q']:
        h_opts = list(hs['options'])
        random.shuffle(h_opts)
        st.session_state.home_options = h_opts
        st.session_state.current_home_q = hs['q']
        
    h_ans = st.radio("What will you do?", st.session_state.home_options, index=None, key="home_ans")
    
    if st.button("Check Answer 🏠", key="home_submit"):
        if h_ans is None:
            st.warning("⚠️ Please select an answer first!")
        elif h_ans == hs['answer']:
            st.success(f"✅ Great job! {hs['tip']}")
        else:
            st.error(f"❌ Incorrect! You selected: '{h_ans}'. The safest option is: '{hs['answer']}'. {hs['tip']}")
    
    if st.button("New Scenario 🔄", key="home_next"):
        st.session_state.home_q = random.choice(home_scenarios)
        if 'home_options' in st.session_state:
            del st.session_state['home_options']
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
    st.subheader("💻 Digital Safety Rules")
    
    st.write("**Complete each digital safety pledge:**")
    p1 = st.checkbox("I will NEVER share my home address or phone number with strangers online.")
    p2 = st.checkbox("I will tell a trusted adult if someone online makes me feel uncomfortable.")
    p3 = st.checkbox("I will not click on links from people I don't know.")
    p4 = st.checkbox("I will use strong passwords and not share them with friends.")
    p5 = st.checkbox("I will only spend time online when an adult knows about it.")
    
    if all([p1, p2, p3, p4, p5]):
        st.success("🏅 Excellent! You are now a **Certified Digital Safety Champion!** +200 XP Earned!")
        st.balloons()
    else:
        checked = sum([p1, p2, p3, p4, p5])
        st.info(f"You have agreed to {checked}/5 safety pledges. Complete all to earn your Digital Safety Badge!")
    st.markdown('</div>', unsafe_allow_html=True)
