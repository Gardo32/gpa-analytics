import streamlit as st
import pandas as pd
import datetime as dt
import os


def save_grades_to_csv(subjects, grades, final_gpa):
    # Create a DataFrame to store the data
    data = {
        'Date/Time': [dt.datetime.now().strftime('%Y-%m-%d')],
        'GPA': [final_gpa]
    }
    for i, grade in enumerate(grades):
        data[f'Subject {i + 1}'] = [grade]

    df = pd.DataFrame(data)

    # Define the path for the CSV file
    file_path = 'csv/Grades.csv'

    # Check if file exists
    file_exists = os.path.exists(file_path)

    # If file exists, append without header; else, write with header
    if file_exists:
        df.to_csv(file_path, mode='a', header=False, index=False)
    else:
        df.to_csv(file_path, mode='w', header=True, index=False)

    st.success('Grades and GPA saved successfully!')


def main():
    # Set page title
    st.title("GPA Calculator")
    # Input for number of subjects
    num_subjects = st.number_input("Enter the number of subjects:", min_value=0, value=0, step=1)
    st.markdown("---")
    # Initialize lists
    hours = []
    total = []
    grades = []

    # Loop for each subject
    for i in range(num_subjects):

        # Input for marks and hours
        marks = st.number_input(f"Enter the marks of subject {i + 1}: ", min_value=1,max_value=100)
        hour = st.number_input(f"Enter the hours of subject {i + 1}: ", min_value=1,max_value=12)
        st.markdown("---")
        # Validate inputs
        if marks > 0 and hour > 0:
            total.append(marks * hour)
            hours.append(hour)
            grades.append(marks)
        else:
            st.error("Invalid input. Please enter positive numbers.")

    # Calculate GPA
    if len(hours) > 0:
        final_gpa = sum(total) / sum(hours)
        st.success(f"Your GPA is: {final_gpa:.2f}")

        # Add button to save grades and GPA
        if st.button('Save Grades and GPA'):
            save_grades_to_csv(hours, grades, final_gpa)
    else:
        st.warning("No subjects entered. Please add at least one subject.")


if __name__ == "__main__":
    main()
