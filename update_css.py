import os
import re

# We will completely clean main.py of the hardcoded <style> blocks and replace it with reading style.css
with open("main.py", "r", encoding="utf-8") as f:
    main_c = f.read()

# Remove all existing <style> blocks in main.py
main_c = re.sub(r'<style>.*?</style>', '', main_c, flags=re.DOTALL)

# Insert the reliable style.css loader right after st.set_page_config
inject_code = """
import os
try:
    with open(os.path.join(os.path.dirname(__file__), 'style.css'), 'r', encoding='utf-8') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except Exception:
    pass
"""

main_c = main_c.replace('import os\nfrom dotenv import load_dotenv', inject_code + '\nimport os\nfrom dotenv import load_dotenv', 1)

# Ensure it's imported at the top if the replace missed it due to spacing
if 'style.css' not in main_c:
    # Just put it right under import streamlit as st
    main_c = main_c.replace('import streamlit as st', 'import streamlit as st\n' + inject_code, 1)

# Also remove the specific inline style for hiding the sidebar on the login page since we already removed <style> block
# But we still need the sidebar hidden on the login page! So we add a small specific block just for that.
sidebar_hide = """
        st.markdown('<style>[data-testid="stSidebar"] { display: none; }</style>', unsafe_allow_html=True)
"""
# Replace the old empty st.markdown(""" """) block with this
main_c = re.sub(r'st\.markdown\("""\s*""", unsafe_allow_html=True\)', sidebar_hide, main_c)

with open("main.py", "w", encoding="utf-8") as f:
    f.write(main_c)

print("main.py sanitized and updated to use style.css globally.")
