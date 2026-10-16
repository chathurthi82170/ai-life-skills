import base64
import os

bg_path = os.path.join(os.path.dirname(__file__), "bg_kids.png")
style_path = os.path.join(os.path.dirname(__file__), "style.css")

with open(bg_path, "rb") as f:
    encoded_str = base64.b64encode(f.read()).decode("utf-8")

css_content = f"""/* Custom Kids Illustration Background Theme */
.stApp {{
    background-image: linear-gradient(rgba(245, 255, 250, 0.78), rgba(230, 245, 240, 0.78)), url("data:image/png;base64,{encoded_str}") !important;
    background-size: contain !important;
    background-position: center right !important;
    background-repeat: no-repeat !important;
    background-attachment: fixed !important;
}}

/* Colorful Sidebar */
[data-testid="stSidebar"] {{ background: linear-gradient(180deg, #ffecd2 0%, #fcb69f 100%) !important; }}

/* Colorful Buttons */
.stButton>button {{ background: linear-gradient(90deg, #FF6B6B 0%, #FF8E53 100%) !important; color: white !important; border-radius: 20px !important; font-weight: 800 !important; box-shadow: 0 4px 15px rgba(255,107,107,0.4) !important; }}

/* Colorful Translucent Cards */
.kpi-card, .story-card, .emotion-card, .test-card, .routine-card, .step-box, .teacher-card, .admin-card, .feature-box, .login-card {{ 
    background: rgba(255, 255, 255, 0.85) !important; 
    backdrop-filter: blur(12px) !important; 
    border: 3px solid #ff9a9e !important; 
    border-radius: 15px !important; 
    box-shadow: 0 8px 32px rgba(31,38,135,0.12) !important; 
    color: #1a202c !important; 
}}

/* Colorful Tabs */
.stTabs [data-baseweb="tab"] {{ background-color: #fecfef !important; border-radius: 10px 10px 0 0 !important; margin-right: 5px !important; border: 2px solid #ff9a9e !important; border-bottom: none !important; }}
.stTabs [aria-selected="true"] {{ background-color: #FF6B6B !important; color: white !important; }}

/* Text styling */
.hero-text {{ font-size: 4rem !important; font-weight: 900; background: -webkit-linear-gradient(45deg, #2563EB, #7C3AED); -webkit-background-clip: text; -webkit-text-fill-color: transparent; line-height: 1.2; margin-bottom: 20px; }}
.sub-hero {{ font-size: 1.5rem; color: #1a202c !important; margin-bottom: 40px; text-shadow: 1px 1px 2px rgba(255,255,255,0.8); }}
h1, h2, h3, p, label, .stMarkdown {{ color: #1a202c !important; }}
"""

with open(style_path, "w", encoding="utf-8") as f:
    f.write(css_content)

print("Background image applied to style.css successfully!")
