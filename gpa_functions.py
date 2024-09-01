import streamlit as st
import pandas as pd
import datetime as dt
import os
import json

def create_directory_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def save_grades_to_csv(subjects, grades, final_gpa):
    # Create directory if not exists
    create_directory_if_not_exists('csv/grades')

    file_path = 'csv/grades/Grades.csv'
    date_time_str = dt.datetime.now().strftime('%Y%m%d_%H%M%S')
    if os.path.exists(file_path):
        existing_df = pd.read_csv(file_path)
        existing_columns = existing_df.columns.tolist()
        new_columns = ['Date/Time', 'GPA'] + subjects

        # Check if columns match
        if set(existing_columns) == set(new_columns):
            mode = 'a'
            header = False
        else:
            mode = 'w'
            header = True
            file_path = f'csv/grades/Grades_{date_time_str}.csv'

        data = {
            'Date/Time': [dt.datetime.now().strftime('%Y-%m-%d')],
            'GPA': [final_gpa]
        }
        for subject, grade in zip(subjects, grades):
            data[subject] = [grade]

        df = pd.DataFrame(data)
        df.to_csv(file_path, mode=mode, header=header, index=False)
    else:
        data = {
            'Date/Time': [dt.datetime.now().strftime('%Y-%m-%d')],
            'GPA': [final_gpa]
        }
        for subject, grade in zip(subjects, grades):
            data[subject] = [grade]

        df = pd.DataFrame(data)
        df.to_csv(file_path, mode='w', header=True, index=False)

    st.success('Grades saved successfully!')

def save_marks_hours_to_csv(subjects, marks, hours):
    # Create directory if not exists
    create_directory_if_not_exists('csv/mark_hours')

    file_path = 'csv/mark_hours/Marks_Hours.csv'
    date_time_str = dt.datetime.now().strftime('%Y%m%d_%H%M%S')
    if os.path.exists(file_path):
        existing_df = pd.read_csv(file_path)
        existing_columns = existing_df.columns.tolist()
        new_columns = ['Date/Time'] + subjects + ['Total']

        # Check if columns match
        if set(existing_columns) == set(new_columns):
            mode = 'a'
            header = False
        else:
            mode = 'w'
            header = True
            file_path = f'csv/mark_hours/Marks_Hours_{date_time_str}.csv'

        data = {
            'Date/Time': [dt.datetime.now().strftime('%Y-%m-%d')]
        }
        total = []
        for subject, mark, hour in zip(subjects, marks, hours):
            mark_hour_value = mark * hour
            data[subject] = [mark_hour_value]
            total.append(mark_hour_value)

        data['Total'] = [sum(total)]

        df = pd.DataFrame(data)
        df.to_csv(file_path, mode=mode, header=header, index=False)
    else:
        data = {
            'Date/Time': [dt.datetime.now().strftime('%Y-%m-%d')]
        }
        total = []
        for subject, mark, hour in zip(subjects, marks, hours):
            mark_hour_value = mark * hour
            data[subject] = [mark_hour_value]
            total.append(mark_hour_value)

        data['Total'] = [sum(total)]

        df = pd.DataFrame(data)
        df.to_csv(file_path, mode='w', header=True, index=False)

    st.success('Marks and Hours saved successfully!')

def save_preset_to_file(preset_name, subjects, hours, num_subjects):
    preset_data = {
        'num_subjects': num_subjects,
        'subjects': subjects,
        'hours': hours
    }
    return json.dumps(preset_data)

def load_preset_from_file(uploaded_file):
    preset_data = json.load(uploaded_file)
    return preset_data

def apply_preset(preset_name):
    if preset_name in st.session_state.presets:
        preset_data = st.session_state.presets[preset_name]
        st.session_state.num_subjects = preset_data.get('num_subjects', 0)
        st.session_state.subjects = list(preset_data.get('subjects', []))
        st.session_state.hours = list(preset_data.get('hours', []))
        st.session_state.grades = [0] * st.session_state.num_subjects
