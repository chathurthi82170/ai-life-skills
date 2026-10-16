import streamlit as st
import sys, os
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rbac import enforce_access

st.set_page_config(page_title="Money Manager", page_icon="💰", layout="wide")
enforce_access()

st.title("💰 Money Management Trainer")
st.write("Learn how to count money, plan a budget, and make smart spending choices through fun interactive activities!")

tab1, tab2, tab3 = st.tabs(["🪙 Count My Money", "🛒 Budget Planner", "🧠 Money Quiz"])

with tab1:
    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
    st.subheader("🪙 Counting Practice")
    st.write("Let's practice counting coins and notes. Enter how many of each you have:")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        coins_1 = st.number_input("🟡 ₹1 Coins", min_value=0, max_value=50, value=0, step=1)
        coins_2 = st.number_input("🔵 ₹2 Coins", min_value=0, max_value=50, value=0, step=1)
    with c2:
        coins_5 = st.number_input("🟠 ₹5 Coins", min_value=0, max_value=50, value=0, step=1)
        coins_10 = st.number_input("⚪ ₹10 Coins", min_value=0, max_value=50, value=0, step=1)
    with c3:
        notes_50 = st.number_input("🟩 ₹50 Notes", min_value=0, max_value=20, value=0, step=1)
        notes_100 = st.number_input("🟦 ₹100 Notes", min_value=0, max_value=20, value=0, step=1)
    
    total = (coins_1 * 1) + (coins_2 * 2) + (coins_5 * 5) + (coins_10 * 10) + (notes_50 * 50) + (notes_100 * 100)
    
    st.markdown(f"""
    <div style="text-align:center; padding: 20px; background: rgba(255,255,255,0.5); border-radius: 15px; margin-top: 15px;">
        <h2>💵 Total Amount: <span style="color: #10B981;">₹{total}</span></h2>
    </div>
    """, unsafe_allow_html=True)
    
    if total > 0:
        st.success(f"✅ Great counting! You have ₹{total} in total.")
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
    st.subheader("🛒 Weekly Budget Planner")
    st.write("You have **₹500** for the week. Plan your spending wisely!")
    
    weekly_budget = 500
    
    food = st.slider("🍎 Food & Snacks (₹)", 0, 300, 150, step=10)
    transport = st.slider("🚌 Transport (₹)", 0, 200, 80, step=10)
    stationery = st.slider("📚 Stationery / Books (₹)", 0, 200, 50, step=10)
    fun = st.slider("🎮 Entertainment / Fun (₹)", 0, 200, 50, step=10)
    savings = st.slider("🏦 Savings (₹)", 0, 300, 100, step=10)
    
    total_spent = food + transport + stationery + fun + savings
    remaining = weekly_budget - total_spent
    
    if remaining >= 0:
        st.success(f"✅ Budget balanced! You have ₹{remaining} left over. Excellent planning!")
    else:
        st.error(f"⚠️ You are over budget by ₹{abs(remaining)}. Try reducing some spending categories.")
    
    st.progress(min(total_spent / weekly_budget, 1.0))
    st.write(f"**Spending: ₹{total_spent} / ₹{weekly_budget}**")
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
    st.subheader("🧠 Smart Money Quiz")
    
    questions = [
        {
            "q": "You want to buy a toy that costs ₹150 but you only have ₹100. What should you do?",
            "options": ["Buy it anyway and hope no one notices", "Save money until you have enough", "Ask a stranger for money"],
            "answer": "Save money until you have enough",
            "tip": "Saving up for things you want is a great life skill!"
        },
        {
            "q": "A shopkeeper gives you ₹20 change for a ₹30 item when you paid ₹50. Is the change correct?",
            "options": ["Yes, ₹20 is correct", "No, I should get ₹30 change", "I don't know, I'll just take it"],
            "answer": "Yes, ₹20 is correct",
            "tip": "₹50 - ₹30 = ₹20. Always count your change carefully!"
        },
        {
            "q": "Which of these is a NEED (not a want)?",
            "options": ["New video game", "Food and water", "Designer shoes"],
            "answer": "Food and water",
            "tip": "Needs are things we must have to survive. Wants are extras!"
        },
    ]
    
    if 'money_q' not in st.session_state:
        st.session_state.money_q = random.choice(questions)
    
    q = st.session_state.money_q
    st.info(f"**Question:** {q['q']}")
    m_ans = st.radio("Your answer:", q['options'], index=None, key="money_ans")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Submit Answer 💰", type="primary"):
            if m_ans is None:
                st.warning("⚠️ Please select an answer first!")
            elif m_ans == q['answer']:
                st.success(f"✅ Correct! {q['tip']}")
                st.balloons()
            else:
                st.error(f"❌ Not quite! **Correct Answer:** {q['answer']}. {q['tip']}")
    with c2:
        if st.button("Next Question 🔄"):
            st.session_state.money_q = random.choice(questions)
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
