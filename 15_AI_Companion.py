import streamlit as st
import sys, os
import time
from openai import OpenAI

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rbac import enforce_access

st.set_page_config(page_title="AI Companion", page_icon="🤖", layout="wide")
enforce_access()

st.title("💬 Agentic AI Companion")
st.write("Chat with your personal AI buddy! I can help explain difficult tasks, talk about your day, or practice social conversations.")

# Custom CSS for high contrast chat
st.markdown("""
<style>
    .chat-card {
        background: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 20px !important;
        padding: 20px !important;
        margin-bottom: 20px !important;
    }
    .chat-bubble-user {
        background: linear-gradient(135deg, #6366f1, #a855f7) !important;
        color: #ffffff !important;
        padding: 14px 20px;
        border-radius: 18px 18px 4px 18px;
        margin-bottom: 12px;
        max-width: 80%;
        margin-left: auto;
        box-shadow: 0 4px 15px rgba(168,85,247,0.4);
        font-size: 1.05rem;
        font-weight: 600;
    }
    .chat-bubble-user * {
        color: #ffffff !important;
    }
    .chat-bubble-bot {
        background: #1e293b !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.25);
        padding: 14px 20px;
        border-radius: 18px 18px 18px 4px;
        margin-bottom: 12px;
        max-width: 80%;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
        font-size: 1.05rem;
        font-weight: 500;
    }
    .chat-bubble-bot * {
        color: #ffffff !important;
    }
    [data-testid="stChatInput"] textarea {
        color: #ffffff !important;
        background-color: #0f172a !important;
    }
</style>
""", unsafe_allow_html=True)

def generate_ai_response(prompt, history):
    username = st.session_state.get("username", "Friend")
    student_age = st.session_state.get("student_age", 12)
    profile_type = st.session_state.get("primary_profile", "Visual Learner")
    
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key and "your_actual_openai_key" not in api_key and len(api_key) > 20:
        try:
            client = OpenAI(api_key=api_key)
            system_prompt = (
                f"You are a compassionate, encouraging AI Buddy and Life Coach for {username}, "
                f"a student aged {student_age} with a '{profile_type}' learning style. "
                "Keep responses warm, friendly, positive, easy to read, with relevant emojis, and concise (2-3 sentences max). "
                "Help them practice social skills, manage emotions, or learn daily routines."
            )
            messages = [{"role": "system", "content": system_prompt}]
            for m in history[-6:]:
                messages.append({"role": m["role"], "content": m["content"]})
            messages.append({"role": "user", "content": prompt})

            resp = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=150
            )
            return resp.choices[0].message.content
        except Exception:
            pass

    # Comprehensive intelligent fallback logic (no API key needed)
    p_lower = prompt.lower()
    if any(w in p_lower for w in ["sad", "angry", "upset", "crying", "scared", "worried", "lonely", "hurt", "bad"]):
        return f"I hear you, {username}. It's completely okay to feel that way. 💙 Take a deep slow breath with me (in 1.. 2.. 3.. out 1.. 2.. 3..). You are safe, strong, and doing amazing!"
    elif any(w in p_lower for w in ["happy", "good", "great", "awesome", "excited", "fun", "yay", "smile"]):
        return f"Yay! 🎉 I'm so happy to hear that, {username}! Smiling makes the day bright. What fun skill or game are you enjoying today?"
    elif any(w in p_lower for w in ["brush", "teeth", "wash", "hands", "routine", "schedule", "clean", "eat", "cook", "bed"]):
        return f"Great job practicing your daily life skills, {username}! 🌟 You can track your steps in Daily Routines or Learn Skill module to earn reward points!"
    elif any(w in p_lower for w in ["help", "stuck", "don't know", "difficult", "hard", "problem"]):
        return f"Don't worry, {username}! We can break it down into 1 small step at a time. 🧩 What task can I help guide you with right now?"
    elif any(w in p_lower for w in ["hi", "hello", "hey", "namaste", "halo", "morning", "evening"]):
        return f"Hello {username}! 👋 I'm your AI Buddy. I'm always here to chat, practice social conversations, or help with your daily skills!"
    elif any(w in p_lower for w in ["who are you", "your name", "what can you do"]):
        return f"I am your personal Agentic AI Companion! 🤖 I help you practice daily routines, learn life skills, manage emotions, and answer any questions!"
    else:
        return f"That's wonderful to share, {username}! 🌟 Tell me more about it, or ask me anything about your daily routines and life skills!"

if "messages" not in st.session_state:
    username = st.session_state.get("username", "friend")
    st.session_state.messages = [
        {"role": "assistant", "content": f"Hi {username}! 👋 I'm your AI buddy. How are you feeling today?"}
    ]

# Render chat history
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-bubble-user">👤 <b>You:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bubble-bot">🤖 <b>AI Buddy:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Primary st.chat_input
user_prompt = st.chat_input("Type your message to AI Buddy here...")

# Fallback form input if chat_input isn't supported in browser window
with st.expander("💬 Alternative Text Input (If Chat Input is disabled)", expanded=False):
    with st.form("fallback_chat_form", clear_on_submit=True):
        form_prompt = st.text_input("Type message:")
        form_submit = st.form_submit_button("Send Message 📤", type="primary")
        if form_submit and form_prompt.strip():
            user_prompt = form_prompt.strip()

if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    ai_reply = generate_ai_response(user_prompt, st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
    st.rerun()
