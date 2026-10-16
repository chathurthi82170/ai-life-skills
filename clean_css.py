import os
import re

for file in os.listdir("pages"):
    if file.endswith(".py"):
        path = os.path.join("pages", file)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Remove any .stApp styling blocks from individual pages
        # so they don't conflict with rbac.py's global animated background
        content = re.sub(r'\.stApp\s*\{[^}]*\}', '', content)
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

print("CSS conflicts cleared from all pages.")
