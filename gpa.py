import streamlit as st
import pandas as pd
import datetime as dt
import os
import json

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


def save_preset(preset_name, subjects, hours, num_subjects):
    st.session_state.presets[preset_name] = {
        'num_subjects': num_subjects,
        'subjects': subjects,
        'hours': hours
    }


def load_preset_from_file(uploaded_file):
    preset_data = json.load(uploaded_file)
    return preset_data


def save_preset_to_file(preset_name, subjects, hours, num_subjects):
    preset_data = {
        'num_subjects': num_subjects,
        'subjects': subjects,
        'hours': hours
    }
    return json.dumps(preset_data)


def apply_preset(preset_name):
    if preset_name in st.session_state.presets:
        preset_data = st.session_state.presets[preset_name]
        st.session_state.num_subjects = preset_data.get('num_subjects', 0)
        st.session_state.subjects = list(preset_data.get('subjects', []))
        st.session_state.hours = list(preset_data.get('hours', []))
        st.session_state.grades = [0] * st.session_state.num_subjects


def main():
    st.title("GPA Calculator")

    # Preset management
    st.sidebar.header("Manage Presets")

    # File upload
    uploaded_file = st.sidebar.file_uploader("Upload a Preset JSON file", type="json")
    if uploaded_file:
        preset_data = load_preset_from_file(uploaded_file)
        preset_name = st.text_input("Enter a name for the uploaded preset:", "")
        if preset_name:
            st.session_state.presets[preset_name] = {
                'num_subjects': preset_data.get('num_subjects', 0),
                'subjects': preset_data.get('subjects', []),
                'hours': preset_data.get('hours', [])
            }
            st.session_state.selected_preset = preset_name
            st.success(f"Preset '{preset_name}' loaded successfully!")

    # Preset selection
    preset_name = st.sidebar.radio("Select or Create Preset:", list(st.session_state.presets.keys()),
                                   index=list(st.session_state.presets.keys()).index(st.session_state.selected_preset))
    st.session_state.selected_preset = preset_name
    apply_preset(preset_name)

    # Input for number of subjects
    num_subjects = st.number_input("Enter the number of subjects:", min_value=0, value=st.session_state.num_subjects,
                                   step=1)
    st.session_state.num_subjects = num_subjects

    # Ensure the session state lists have the correct length
    if len(st.session_state.subjects) < num_subjects:
        st.session_state.subjects.extend(
            [f"Subject {i + 1}" for i in range(len(st.session_state.subjects), num_subjects)])
    if len(st.session_state.hours) < num_subjects:
        st.session_state.hours.extend([1 for _ in range(len(st.session_state.hours), num_subjects)])
    if len(st.session_state.grades) < num_subjects:
        st.session_state.grades.extend([0 for _ in range(len(st.session_state.grades), num_subjects)])

    total = []

    for i in range(num_subjects):
        subject_name = st.text_input(f"Enter the name of subject {i + 1} (optional): ",
                                     value=st.session_state.subjects[i] if i < len(st.session_state.subjects) else "",
                                     key=f"subject_name_{i}")

        col1, col2 = st.columns([3, 1])
        with col1:
            default_marks = st.session_state.grades[i] if i < len(st.session_state.grades) else 0
            marks = st.number_input(f"Enter the marks of {subject_name}: ", min_value=0, max_value=100,
                                    value=default_marks,
                                    key=f"marks_{i}")
        with col2:
            default_hour = st.session_state.hours[i] if i < len(st.session_state.hours) else 1
            hour = st.number_input(f"Hours", min_value=1, max_value=12,
                                   value=default_hour,
                                   key=f"hours_{i}")
        st.session_state.subjects[i] = subject_name
        st.session_state.hours[i] = hour
        st.session_state.grades[i] = marks

        st.markdown("---")

        if marks > 0 and hour > 0:
            total.append(marks * hour)
        else:
            st.error("Invalid input. Please enter positive numbers.")

    if len(st.session_state.hours) > 0:
        final_gpa = sum(total) / sum(st.session_state.hours)
        st.success(f"Your GPA is: {final_gpa:.2f}")

        # Save and download preset buttons
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button('Save Preset'):
                preset_name = st.text_input("Enter a name for the new preset:")
                if preset_name and preset_name not in st.session_state.presets:
                    save_preset(preset_name, st.session_state.subjects, st.session_state.hours, num_subjects)
                    st.session_state.selected_preset = preset_name
                    st.sidebar.radio("Select or Create Preset:", list(st.session_state.presets.keys()),
                                     index=list(st.session_state.presets.keys()).index(preset_name))
                    st.success(f"Preset '{preset_name}' saved successfully!")
        with col2:
            preset_json = save_preset_to_file(st.session_state.selected_preset, st.session_state.subjects,
                                              st.session_state.hours, num_subjects)
            st.download_button(
                label="Download Current Preset",
                data=preset_json,
                file_name=f"{st.session_state.selected_preset}.json",
                mime="application/json"
            )
    else:
        st.warning("No subjects entered. Please add at least one subject.")


if __name__ == "__main__":
    main()
