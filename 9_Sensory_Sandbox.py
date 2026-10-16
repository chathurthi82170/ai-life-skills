import streamlit as st
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rbac import enforce_access

st.set_page_config(page_title="Sensory Sandbox", page_icon="🧘", layout="centered")
enforce_access()

st.title("🧘 Sensory Sandbox")
st.write("Take a deep breath and relax. Follow the breathing circle below.")

# An HTML/CSS animation for a relaxing breathing exercise
st.components.v1.html("""
    <div style="display:flex; flex-direction: column; justify-content:center; align-items:center; height:400px; font-family: sans-serif;">
        <h2 id="breathe-text" style="color: #38BDF8;">Breathe In...</h2>
        <div style="width: 150px; height: 150px; background: radial-gradient(circle, #38BDF8 0%, #818CF8 100%); border-radius: 50%; animation: breathe 8s infinite ease-in-out; box-shadow: 0px 0px 20px rgba(56, 189, 248, 0.5);"></div>
    </div>
    <script>
        const text = document.getElementById('breathe-text');
        setInterval(() => {
            text.innerText = text.innerText === 'Breathe In...' ? 'Breathe Out...' : 'Breathe In...';
        }, 4000);
    </script>
    <style>
        @keyframes breathe {
            0% { transform: scale(1); opacity: 0.8; }
            50% { transform: scale(1.8); opacity: 0.4; }
            100% { transform: scale(1); opacity: 0.8; }
        }
    </style>
""", height=450)

st.info("💡 **Tip:** Use this module whenever you feel overwhelmed and need a moment to reset your brain.")
