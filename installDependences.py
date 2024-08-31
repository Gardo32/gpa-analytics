import os

deps = ['streamlit','pyinstaller']

os.system("pip install uv")

for dep in deps:
    os.system("uv pip install " + dep)
