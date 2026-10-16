import streamlit as st
import streamlit.components.v1 as components
import sys, os, random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rbac import enforce_access
import database
import importlib
importlib.reload(database)
from skills_library import UNIFIED_SKILL_TOPICS, get_all_topics, get_topic_data

st.set_page_config(page_title="AI Assessment", page_icon="🧠", layout="wide")
enforce_access()

st.title("🧠 Topic-Based AI Assessment")
st.write("Select any of the 22 unified life skill topics to test your ability and calculate your skill level!")

username = st.session_state.get("username", "Student")

# Initialize topic selection state
if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = None
if "assessment_done" not in st.session_state:
    st.session_state.assessment_done = False

# ── STAGE 2A: SELECT TOPIC (22 UNIFIED TOPICS) ──────────────────────────────
if not st.session_state.selected_topic:
    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
    st.subheader(f"🎯 Select Assessment Topic for {username} (22 Skills Available)")
    
    # Category filter pills
    categories = ["All", "Personal Hygiene", "Kitchen & Meals", "Household Skills", "Daily Routines", "Safety Skills", "Financial Skills", "Emotional Regulation", "Communication Skills"]
    selected_cat = st.radio("Filter by Category:", categories, horizontal=True)
    st.markdown("---")
    
    topics_list = get_all_topics()
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
                padding: 18px 12px; 
                border-radius: 16px; 
                background: linear-gradient(135deg, rgba(30,41,59,0.9), rgba(15,23,42,0.95)); 
                border: 1px solid rgba(255, 255, 255, 0.15); 
                box-shadow: 0 6px 20px rgba(0,0,0,0.3); 
                margin-bottom: 12px;
                min-height: 140px;
            ">
                <div style="font-size:2.8rem; filter: drop-shadow(0 2px 8px rgba(0,0,0,0.4)); margin-bottom:4px;">{t_info['icon']}</div>
                <div style="font-weight:800; font-size:1.05rem; color:#f8fafc; letter-spacing:0.5px;">{t_name}</div>
                <div style="font-size:0.8rem; color:#94a3b8; margin-top:2px;">{t_info['category']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Take Assessment: {t_name}", key=f"top_btn_{idx}", use_container_width=True, type="primary"):
                st.session_state.selected_topic = t_name
                st.session_state.assessment_done = False
                st.rerun()
                
    st.markdown('</div>', unsafe_allow_html=True)

# ── STAGE 2B: TAKE TOPIC ASSESSMENT ─────────────────────────────────────────
elif not st.session_state.assessment_done:
    chosen_topic = st.session_state.selected_topic
    t_info = get_topic_data(chosen_topic)
    questions = t_info["questions"]
    
    st.markdown('<div class="test-card">', unsafe_allow_html=True)
    st.subheader(f"📝 {t_info['icon']} {chosen_topic} Ability Assessment ({username})")
    st.info(f"💡 *Answer these 5 questions on **{chosen_topic}** to calculate your skill level:*")
    
    user_answers = {}
    
    with st.form("topic_assessment_form"):
        for idx, q_item in enumerate(questions, 1):
            q_text = q_item['q']
            st.markdown(f"**Question {idx}: {q_text}**")
            
            clean_q = q_text.replace("'", "\\'").replace('"', '\\"')
            tts_html = f"""
            <button type="button" onclick="speakQ{idx}()" style="
                background-color: #3B82F6;
                color: white;
                border: none;
                padding: 4px 12px;
                border-radius: 12px;
                font-weight: 600;
                font-size: 0.8rem;
                cursor: pointer;
                margin-bottom: 8px;
            ">
                🔊 Listen to Question {idx}
            </button>
            <script>
            function speakQ{idx}() {{
                if ('speechSynthesis' in window) {{
                    window.speechSynthesis.cancel();
                    var msg = new SpeechSynthesisUtterance("{clean_q}");
                    msg.rate = 0.9;
                    window.speechSynthesis.speak(msg);
                }}
            }}
            </script>
            """
            components.html(tts_html, height=36)
            
            # Shuffle options deterministically using topic & question text as seed so correct answer isn't always first
            q_options = list(q_item["options"])
            seed = sum(ord(c) for c in chosen_topic + q_text)
            random.Random(seed).shuffle(q_options)
            
            user_answers[idx] = st.radio(
                f"Select answer for Q{idx}:",
                q_options,
                index=None,
                key=f"tq_{idx}"
            )
            st.markdown("---")
            
        col1, col2 = st.columns([3, 1])
        with col1:
            submitted = st.form_submit_button("Submit Assessment & Calculate My Level 🎯", type="primary", use_container_width=True)
        with col2:
            change_topic = st.form_submit_button("↩️ Change Topic", use_container_width=True)
            
        if change_topic:
            st.session_state.selected_topic = None
            st.rerun()
            
        if submitted:
            if any(user_answers[i] is None for i in range(1, len(questions) + 1)):
                st.warning("⚠️ Please select an answer for all questions before submitting!")
            else:
                score = 0
                for idx, q_item in enumerate(questions, 1):
                    if user_answers[idx] == q_item["answer"]:
                        score += 1
                
                if score == 5:
                    calc_level = "Good 🏆"
                elif score >= 3:
                    calc_level = "Intermediate ⭐"
                else:
                    calc_level = "Beginner 🌱"
                    
                # Permanently save score into database
                database.save_assessment_score(username, score, 5, f"{chosen_topic}: {calc_level}")
                
                st.session_state.assessment_score = score
                st.session_state.assessment_topic = chosen_topic
                st.session_state.skill_level = calc_level
                st.session_state.assessment_done = True
                st.session_state.xp_balance = st.session_state.get('xp_balance', 450) + 100
                st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)

# ── STAGE 2C: ASSESSMENT RESULTS & DIRECT AUTO-LEARNING ─────────────────────
else:
    score = st.session_state.assessment_score
    chosen_topic = st.session_state.assessment_topic
    level_name = st.session_state.skill_level
    t_info = get_topic_data(chosen_topic)
    
    if "Good" in level_name:
        badge_color = "#10B981"
        level_desc = f"Outstanding! Perfect 5/5 on **{chosen_topic}**! You demonstrate expert ability. Let me guide you through key steps!"
    elif "Intermediate" in level_name:
        badge_color = "#F59E0B"
        level_desc = f"Great job! You scored {score}/5 on **{chosen_topic}**! Solid foundation. The AI will guide you through key routine steps."
    else:
        badge_color = "#3B82F6"
        level_desc = f"Good effort! You scored {score}/5 on **{chosen_topic}**. The AI will start with basic, easy visual steps."
        
    t_icon = t_info.get("icon", "🧠") if (t_info and isinstance(t_info, dict)) else "🧠"
        
    st.markdown('<div class="kpi-card" style="text-align: center; border-left: 8px solid ' + badge_color + ';">', unsafe_allow_html=True)
    st.subheader(f"🎉 Assessment Complete for {t_icon} {chosen_topic}")
    st.markdown(f"## Score: **{score} / 5**")
    
    st.markdown(f"""
    <div style="background: rgba(30,41,59,0.9); padding: 20px; border-radius: 15px; margin: 15px 0; border:2px solid {badge_color};">
        <span style="font-size: 1.2rem; color:#f8fafc;">Assigned Ability Level for <b>{chosen_topic}</b>:</span><br>
        <span style="font-size: 3rem; font-weight: 900; color: {badge_color};">{level_name}</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.info(f"🤖 **Agentic AI Recommendation:** {level_desc}")
    
    st.markdown("---")
    colA, colB = st.columns(2)
    with colA:
        if st.button("🎯 Pick Another Topic for Assessment", use_container_width=True):
            st.session_state.selected_topic = None
            st.session_state.assessment_done = False
            st.rerun()
    with colB:
        if st.button(f"🚀 Start Learning {chosen_topic} Now ➡️", type="primary", use_container_width=True):
            st.session_state.task_name = chosen_topic
            st.switch_page("pages/1_Learn_Skill.py")
                
    st.markdown('</div>', unsafe_allow_html=True)
