import streamlit as st
from main import main

# Initialize session state for presets and input values
if 'presets' not in st.session_state:
    st.session_state.presets = {'Default (Empty)': {'num_subjects': 0, 'subjects': [], 'hours': []}}
if 'selected_preset' not in st.session_state:
    st.session_state.selected_preset = 'Default (Empty)'
if 'num_subjects' not in st.session_state:
    st.session_state.num_subjects = 0
if 'subjects' not in st.session_state:
    st.session_state.subjects = []
if 'hours' not in st.session_state:
    st.session_state.hours = []
if 'grades' not in st.session_state:
    st.session_state.grades = []

if __name__ == "__main__":
    main()
