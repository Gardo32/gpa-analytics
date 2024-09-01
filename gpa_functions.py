import os
import json
import zipfile
import pandas as pd
import datetime as dt
import streamlit as st


# Create a directory if it does not exist
def create_directory_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


# Save grades to CSV
def save_grades_to_csv(subjects, grades, final_gpa):
    create_directory_if_not_exists('csv/grades')
    file_path = 'csv/grades/Grades.csv'
    date_time_str = dt.datetime.now().strftime('%Y%m%d_%H%M%S')

    if os.path.exists(file_path):
        existing_df = pd.read_csv(file_path)
        existing_columns = existing_df.columns.tolist()
        new_columns = ['Date/Time', 'GPA'] + subjects

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


# Save marks and hours to CSV
def save_marks_hours_to_csv(subjects, marks, hours):
    create_directory_if_not_exists('csv/mark_hours')
    file_path = 'csv/mark_hours/Marks_Hours.csv'
    date_time_str = dt.datetime.now().strftime('%Y%m%d_%H%M%S')

    if os.path.exists(file_path):
        existing_df = pd.read_csv(file_path)
        existing_columns = existing_df.columns.tolist()
        new_columns = ['Date/Time'] + subjects + ['Total']

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


# Save preset to session state
def save_preset(preset_name, subjects, hours, num_subjects):
    st.session_state.presets[preset_name] = {
        'num_subjects': num_subjects,
        'subjects': subjects,
        'hours': hours
    }


# Load preset from uploaded file
def load_preset_from_file(uploaded_file):
    preset_data = json.load(uploaded_file)
    return preset_data


# Save preset to file and return the file path
def save_preset_to_file(preset_name, subjects, hours, num_subjects):
    preset_data = {
        'num_subjects': num_subjects,
        'subjects': subjects,
        'hours': hours
    }
    file_path = f'presets/{preset_name}.json'
    create_directory_if_not_exists('presets')
    with open(file_path, 'w') as f:
        json.dump(preset_data, f)
    return file_path


# Apply preset from session state
def apply_preset(preset_name):
    if preset_name in st.session_state.presets:
        preset_data = st.session_state.presets[preset_name]
        st.session_state.num_subjects = preset_data.get('num_subjects', 0)
        st.session_state.subjects = list(preset_data.get('subjects', []))
        st.session_state.hours = list(preset_data.get('hours', []))
        st.session_state.grades = [0] * st.session_state.num_subjects
    else:
        st.session_state.num_subjects = 0
        st.session_state.subjects = []
        st.session_state.hours = []
        st.session_state.grades = []


# Append grades from uploaded ZIP file
def append_grades_from_zip(uploaded_zip):
    create_directory_if_not_exists('temp_zip')
    with zipfile.ZipFile(uploaded_zip, 'r') as zip_ref:
        zip_ref.extractall('temp_zip')

    # Process each file in the extracted ZIP
    for file_name in os.listdir('temp_zip'):
        if file_name.endswith('.csv'):
            file_path = os.path.join('temp_zip', file_name)
            if 'Grades.csv' in file_name:
                grades_df = pd.read_csv(file_path)
                # Handle appending logic for Grades.csv
                st.success(f"Grades appended from {file_name} successfully!")
            elif 'Marks_Hours.csv' in file_name:
                marks_hours_df = pd.read_csv(file_path)
                # Handle appending logic for Marks_Hours.csv
                st.success(f"Marks and Hours appended from {file_name} successfully!")

    # Create a new ZIP file with the updated data
def create_zip_with_csv(zip_name='gpa.zip', source_dir='csv'):
    """Create a ZIP file containing all CSV files from the specified source directory."""
    zip_path = os.path.join(source_dir, zip_name)
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                if file.endswith('.csv'):
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, source_dir))
    return zip_path
