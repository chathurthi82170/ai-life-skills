import streamlit as st
import random
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rbac import enforce_access
enforce_access()

st.title("📅 My Daily Routines")
st.write("Learn, practice, and test your knowledge on Morning, Afternoon, and Evening routines with randomized quiz questions!")

if "custom_routines" not in st.session_state:
    st.session_state.custom_routines = [
        {"title": "📚 After-School Homework Routine", "steps": ["Unpack school bag", "Eat a healthy snack", "Complete 20 minutes of homework", "Pack bag for tomorrow"]}
    ]

# ── QUESTION POOLS ────────────────────────────────────────────────────────────
MORNING_QUESTIONS = [
    {
        "q": "After you wake up and stretch, what is the VERY NEXT thing you should do?",
        "options": ["Play video games", "Wash face and brush teeth", "Eat dinner"],
        "answer": "Wash face and brush teeth",
        "tip": "Keeping clean is a great way to start the morning!"
    },
    {
        "q": "Why is eating a nutritious breakfast in the morning important?",
        "options": ["Gives your body and brain energy for learning", "Makes you fall asleep", "It is not needed"],
        "answer": "Gives your body and brain energy for learning",
        "tip": "Breakfast fuels your body and brain for the whole day!"
    },
    {
        "q": "What should you check when packing your school bag in the morning?",
        "options": ["Check your books, lunchbox, and water bottle", "Fill bag with heavy stones", "Leave bag empty"],
        "answer": "Check your books, lunchbox, and water bottle",
        "tip": "Checking your timetable ensures you don't forget important books!"
    },
    {
        "q": "What should you do after washing your face in the morning?",
        "options": ["Dry your face with a clean towel", "Wipe on dirty clothes", "Leave water dripping on shirt"],
        "answer": "Dry your face with a clean towel",
        "tip": "A clean towel keeps your skin clean and fresh!"
    },
    {
        "q": "What is the best way to get dressed for school in the morning?",
        "options": ["Put on clean weather-appropriate clothes neatly", "Wear muddy pajamas to school", "Wear 5 winter coats in summer"],
        "answer": "Put on clean weather-appropriate clothes neatly",
        "tip": "Clean clothes make you feel comfortable and ready to learn!"
    }
]

AFTERNOON_QUESTIONS = [
    {
        "q": "You should complete your homework BEFORE having free play time. True or False?",
        "options": ["True", "False"],
        "answer": "True",
        "tip": "Finishing work first lets you relax and play without worrying!"
    },
    {
        "q": "What is a healthy afternoon habit after coming home from school?",
        "options": ["Wash your hands and eat a healthy snack", "Eat 10 bars of candy", "Scream loudly"],
        "answer": "Wash your hands and eat a healthy snack",
        "tip": "A healthy snack recharges your energy after school!"
    },
    {
        "q": "How can helping with a small household chore in the afternoon help your family?",
        "options": ["Builds teamwork and keeps your home clean", "Makes your parents angry", "Destroys toys"],
        "answer": "Builds teamwork and keeps your home clean",
        "tip": "Small chores like putting away shoes build great responsibility!"
    },
    {
        "q": "If you have 30 minutes of free afternoon time, what is a great outdoor or creative activity?",
        "options": ["Drawing, playing sports, or reading a book", "Staring at a blank wall", "Throwing trash"],
        "answer": "Drawing, playing sports, or reading a book",
        "tip": "Creative activities stimulate your brain and body!"
    },
    {
        "q": "What should you do with your school bag when you return home in the afternoon?",
        "options": ["Place it neatly in your study corner", "Throw it in the kitchen sink", "Leave it on driveway"],
        "answer": "Place it neatly in your study corner",
        "tip": "Keeping your bag in a dedicated spot prevents lost homework!"
    }
]

EVENING_QUESTIONS = [
    {
        "q": "Which of these is a relaxing step right before going to sleep?",
        "options": ["Reading a calm bedtime story", "Playing loud video games", "Drinking caffeinated soda"],
        "answer": "Reading a calm bedtime story",
        "tip": "Reading a story helps your mind slow down before sleep!"
    },
    {
        "q": "Why should you brush your teeth before going to sleep at night?",
        "options": ["Removes food particles & stops cavity bacteria overnight", "Makes your hair grow", "It changes eye color"],
        "answer": "Removes food particles & stops cavity bacteria overnight",
        "tip": "Night brushing protects your teeth while you sleep!"
    },
    {
        "q": "What should you do with electronic screens (phones/tablets/TV) 30 minutes before bed?",
        "options": ["Turn them off to help your brain rest", "Hold screen 1 inch from eyes", "Watch scary movies"],
        "answer": "Turn them off to help your brain rest",
        "tip": "Screen light tricks your brain into thinking it's daylight!"
    },
    {
        "q": "What should you put on before getting into bed for sleep?",
        "options": ["Clean, comfortable pajamas", "Raincoat and heavy boots", "Dirty outdoor shoes"],
        "answer": "Clean, comfortable pajamas",
        "tip": "Comfy pajamas regulate body temperature for deep sleep!"
    },
    {
        "q": "What is the recommended amount of sleep for a growing student every night?",
        "options": ["8 to 10 hours of restorative sleep", "2 hours", "24 hours"],
        "answer": "8 to 10 hours of restorative sleep",
        "tip": "Sleep grows your muscles, memory, and immunity!"
    }
]

# Initialize random question in session state if not present
if "morn_q" not in st.session_state:
    st.session_state.morn_q = random.choice(MORNING_QUESTIONS)
if "aft_q" not in st.session_state:
    st.session_state.aft_q = random.choice(AFTERNOON_QUESTIONS)
if "eve_q" not in st.session_state:
    st.session_state.eve_q = random.choice(EVENING_QUESTIONS)


t_morn, t_aft, t_eve, t_custom = st.tabs(["🌅 Morning Routine", "☀️ Afternoon Routine", "🌙 Evening Routine", "➕ Custom Routines"])

# ── MORNING TAB ───────────────────────────────────────────────────────────────
with t_morn:
    st.markdown('<div class="routine-card"><h3>📖 Teach Mode: Morning Steps</h3>'
                '<ol>'
                '<li>Wake up and stretch your body gently</li>'
                '<li>Wash your face and brush your teeth for 2 minutes</li>'
                '<li>Get dressed for the day</li>'
                '<li>Eat a nutritious breakfast</li>'
                '<li>Pack your backpack for school</li>'
                '</ol></div>', unsafe_allow_html=True)

    m_item = st.session_state.morn_q
    st.markdown('<div class="test-card"><h3>🧠 Test Mode: Randomized Morning Quiz</h3></div>', unsafe_allow_html=True)
    st.info(f"**Question:** {m_item['q']}")
    
    q1 = st.radio("Choose your answer:", m_item["options"], index=None, key=f"morn_ans_{m_item['q'][:10]}")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button("Check Answer 🌅", key="btn_morn", type="primary", use_container_width=True):
            if q1 is None:
                st.warning("⚠️ Please select an answer first!")
            elif q1 == m_item["answer"]:
                st.success(f"✅ Correct! {m_item['tip']} 🎉")
                st.balloons()
            else:
                st.error(f"❌ Not quite! **Correct Answer:** {m_item['answer']}. {m_item['tip']}")
    with col2:
        if st.button("New Random Question 🎲", key="btn_morn_next", use_container_width=True):
            st.session_state.morn_q = random.choice(MORNING_QUESTIONS)
            st.rerun()

# ── AFTERNOON TAB ─────────────────────────────────────────────────────────────
with t_aft:
    st.markdown('<div class="routine-card"><h3>📖 Teach Mode: Afternoon Steps</h3>'
                '<ol>'
                '<li>Eat a wholesome lunch</li>'
                '<li>Do homework or reading time</li>'
                '<li>Have free play or outdoor hobby time</li>'
                '<li>Help with a small household chore</li>'
                '</ol></div>', unsafe_allow_html=True)

    a_item = st.session_state.aft_q
    st.markdown('<div class="test-card"><h3>🧠 Test Mode: Randomized Afternoon Quiz</h3></div>', unsafe_allow_html=True)
    st.info(f"**Question:** {a_item['q']}")
    
    q2 = st.radio("Choose your answer:", a_item["options"], index=None, key=f"aft_ans_{a_item['q'][:10]}")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button("Check Answer ☀️", key="btn_aft", type="primary", use_container_width=True):
            if q2 is None:
                st.warning("⚠️ Please select an answer first!")
            elif q2 == a_item["answer"]:
                st.success(f"✅ Correct! {a_item['tip']} 🎉")
                st.balloons()
            else:
                st.error(f"❌ Not quite! **Correct Answer:** {a_item['answer']}. {a_item['tip']}")
    with col2:
        if st.button("New Random Question 🎲", key="btn_aft_next", use_container_width=True):
            st.session_state.aft_q = random.choice(AFTERNOON_QUESTIONS)
            st.rerun()

# ── EVENING TAB ───────────────────────────────────────────────────────────────
with t_eve:
    st.markdown('<div class="routine-card"><h3>📖 Teach Mode: Evening Steps</h3>'
                '<ol>'
                '<li>Eat dinner with your family</li>'
                '<li>Take a bath or shower</li>'
                '<li>Put on your comfortable pajamas</li>'
                '<li>Brush your teeth again</li>'
                '<li>Read a calming bedtime story</li>'
                '<li>Turn off the lights and go to sleep</li>'
                '</ol></div>', unsafe_allow_html=True)

    e_item = st.session_state.eve_q
    st.markdown('<div class="test-card"><h3>🧠 Test Mode: Randomized Evening Quiz</h3></div>', unsafe_allow_html=True)
    st.info(f"**Question:** {e_item['q']}")
    
    q3 = st.radio("Choose your answer:", e_item["options"], index=None, key=f"eve_ans_{e_item['q'][:10]}")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button("Check Answer 🌙", key="btn_eve", type="primary", use_container_width=True):
            if q3 is None:
                st.warning("⚠️ Please select an answer first!")
            elif q3 == e_item["answer"]:
                st.success(f"✅ Correct! {e_item['tip']} 🎉")
                st.balloons()
            else:
                st.error(f"❌ Not quite! **Correct Answer:** {e_item['answer']}. {e_item['tip']}")
    with col2:
        if st.button("New Random Question 🎲", key="btn_eve_next", use_container_width=True):
            st.session_state.eve_q = random.choice(EVENING_QUESTIONS)
            st.rerun()

# ── CUSTOM ROUTINES TAB ───────────────────────────────────────────────────────
with t_custom:
    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
    st.subheader("🛠️ Create & Save Your Custom Routine")
    st.write("Add your own custom daily routines (e.g. Weekend Routine, Pet Care Routine, Reading Routine):")
    
    with st.form("add_routine_form", clear_on_submit=True):
        c_title = st.text_input("Routine Title (e.g., 🐶 Pet Care Routine):")
        c_step1 = st.text_input("Step 1:")
        c_step2 = st.text_input("Step 2:")
        c_step3 = st.text_input("Step 3:")
        c_step4 = st.text_input("Step 4 (Optional):")
        
        save_routine = st.form_submit_button("Save Custom Routine 💾", type="primary")
        if save_routine:
            if c_title.strip() and c_step1.strip() and c_step2.strip():
                steps_list = [c_step1.strip(), c_step2.strip()]
                if c_step3.strip(): steps_list.append(c_step3.strip())
                if c_step4.strip(): steps_list.append(c_step4.strip())
                
                st.session_state.custom_routines.append({"title": c_title.strip(), "steps": steps_list})
                st.success(f"✅ Successfully created **{c_title.strip()}**!")
                st.balloons()
            else:
                st.warning("Please provide a title and at least 2 steps.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("### 📜 Saved Custom Routines")
    for cr in st.session_state.custom_routines:
        st.markdown(f'<div class="routine-card"><h4>{cr["title"]}</h4><ol>', unsafe_allow_html=True)
        for st_item in cr["steps"]:
            st.markdown(f"<li>{st_item}</li>", unsafe_allow_html=True)
        st.markdown('</ol></div>', unsafe_allow_html=True)
