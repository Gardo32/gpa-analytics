import os

deps = ['streamlit','st-supabase-connection','pandas']

os.system("pip install uv")

for dep in deps:
    os.system("uv pip install " + dep)
