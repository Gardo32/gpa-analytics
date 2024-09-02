import os

deps = ['streamlit', 'pandas','plotly']

os.system("pip install uv")

for dep in deps:
    os.system("uv pip install " + dep)
