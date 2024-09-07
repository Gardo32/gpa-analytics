import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import json
from algo import final_grade, final_exam_mark_estimation

# Load data from a file
def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        st.error("File not found. Please upload the required files.")
        st.stop()

# Convert a JSON preset to CSV
def convert_json_to_csv(json_data, csv_file_path):
    data = json.loads(json_data)
    subjects = data['subjects']
    hours = data['hours']

    df = pd.DataFrame([hours], columns=subjects)
    directory = os.path.dirname(csv_file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    df.to_csv(csv_file_path, index=False)

# Calculate GPA average from Grades data
def calculate_gpa_average(grades_data):
    total_sum = grades_data['GPA'].sum()
    num_entries = len(grades_data)
    gpa_average = total_sum / num_entries if num_entries > 0 else 0
    return gpa_average

# Calculate final GPA based on grades and hours
def calculate_final_gpa(row, hours_row, start, finish, subjects_for_50):
    total_sum = 0
    for subject, grade, hour in zip(row.index[2:], row[2:], hours_row):
        # Correct weightage assignment
        subject_type = 'f5' if subject in subjects_for_50 else 'f4'
        final_exam = final_exam_mark_estimation(start, finish, hour, 50 if subject_type == 'f5' else 40)
        final_gpa = final_grade(grade, final_exam, hour, subject_type)
        total_sum += final_gpa
    gpa = total_sum / 40
    return gpa

# Main function
def main():
    st.title("Analytics Dashboard")

    # File paths
    base_csv_dir = 'csv/mark_hours/'
    grades_csv_path = 'csv/grades/Grades.csv'
    hours_csv_path = 'csv/Hours/Hours.csv'

    # Load data
    grades_data = load_data(grades_csv_path)
    marks_hours_data = load_data(os.path.join(base_csv_dir, 'Marks_Hours.csv'))
    hours_data = load_data(hours_csv_path)

    # Select subjects that are 50-weighted
    subjects = list(hours_data.columns)
    subjects_for_50 = st.sidebar.multiselect("Select subjects for 50-weighted GPA", subjects)

    # Grade goal input
    grade_goal = st.sidebar.number_input("Grade Goal", min_value=0.0, max_value=100.0, value=50.0)

    # Input range for final exam estimation
    start = st.sidebar.number_input("Minimum mistakes in finals", min_value=0)
    finish = st.sidebar.number_input("Maximum mistakes in finals", min_value=1)

    # Calculate GPA over time for final estimation
    gpa_over_time = []
    for index, row in grades_data.iterrows():
        timestamp = row['Date/Time']
        hours_row = hours_data.iloc[0].values
        gpa = calculate_final_gpa(row, hours_row, start, finish, subjects_for_50)
        gpa_over_time.append((timestamp, gpa))

    gpa_df = pd.DataFrame(gpa_over_time, columns=['Date/Time', 'GPA'])
    gpa_df['Date/Time'] = pd.to_datetime(gpa_df['Date/Time'])

    # Calculate GPA Average from Grades data
    gpa_average = calculate_gpa_average(grades_data)

    # Table selection dropdown
    file_choice = st.selectbox("Choose table to view:", ["Grades.csv", "Marks_Hours.csv", "Hours.csv"])

    if file_choice == "Grades.csv":
        st.subheader("Grades Table")
        st.write(f"GPA Average: {gpa_average:.2f}")
        st.dataframe(grades_data, height=400)
    elif file_choice == "Marks_Hours.csv":
        st.subheader("Totals Table")
        st.write(f"GPA Average: {gpa_average:.2f}")
        st.dataframe(marks_hours_data, height=400)
    elif file_choice == "Hours.csv":
        st.subheader("Hours Table")
        st.write(f"GPA Average: {gpa_average:.2f}")
        st.dataframe(hours_data, height=400)

    # Display charts for Grades and Weightage
    col3, col4 = st.columns([2, 2])

    with col3:
        st.subheader("Grades Over Time")
        if 'Date/Time' in grades_data.columns:
            grades_data['Date/Time'] = pd.to_datetime(grades_data['Date/Time'])

            fig = go.Figure()

            # Plot grade goal
            fig.add_trace(go.Scatter(
                x=grades_data['Date/Time'],
                y=[grade_goal] * len(grades_data),
                mode='lines',
                name='Grade Goal',
                line=dict(color='red', dash='dash')
            ))

            # Plot GPA over time
            fig.add_trace(go.Scatter(
                x=grades_data['Date/Time'],
                y=grades_data['GPA'],
                mode='lines',
                name='GPA',
                line=dict(color='blue'),
                marker=dict(color='blue', size=8)
            ))

            # Add shaded areas
            fig.add_trace(go.Scatter(
                x=pd.concat([grades_data['Date/Time'], grades_data['Date/Time'][::-1]]),
                y=pd.concat([grades_data['GPA'], pd.Series([grade_goal] * len(grades_data))[::-1]]),
                fill='tozeroy',
                fillcolor='rgba(0, 0, 255, 0.2)',  # Blue fill for above goal
                line=dict(color='rgba(255, 255, 255, 0)'),  # Transparent line
                showlegend=False
            ))

            fig.add_trace(go.Scatter(
                x=pd.concat([grades_data['Date/Time'], grades_data['Date/Time'][::-1]]),
                y=pd.concat([pd.Series([grade_goal] * len(grades_data)), grades_data['GPA'][::-1]]),
                fill='tozeroy',
                fillcolor='rgba(0, 0, 255, 0.2)',  # Blue fill for below goal
                line=dict(color='rgba(255, 255, 255, 0)'),  # Transparent line
                showlegend=False
            ))

            fig.update_layout(
                xaxis_title='Date/Time',
                yaxis_title='GPA',
                yaxis=dict(range=[max(0, grade_goal - 5), 100]),
                height=400,
                showlegend=True
            )

            st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.subheader("Grades Weightage")
        if 'Total' in marks_hours_data.columns:
            subject_sums = marks_hours_data.iloc[-1, 1:-1]
            fig = go.Figure(go.Pie(labels=subject_sums.index, values=subject_sums))
            fig.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)

    # Advance Tweaking Expander
    with st.expander("Advance Tweaking", expanded=False):
        st.subheader("Edit Final Exam Marks Estimation")

        # Create a DataFrame for final exam marks estimation
        final_exam_marks_df = pd.DataFrame({
            'Subject': hours_data.columns,
            'Results': [final_exam_mark_estimation(start, finish, hours_data.loc[0, subject],
                                                   50 if subject in subjects_for_50 else 40) for subject in
                        hours_data.columns],
        })

        edited_df = st.data_editor(final_exam_marks_df, use_container_width=True)

        # Update results based on edited values
        new_start = start  # Maintain original start
        new_finish = finish  # Maintain original finish
        edited_df['Results'] = [final_exam_mark_estimation(new_start, new_finish, hours_data.loc[0, subject],
                                                           50 if subject in subjects_for_50 else 40) for subject in
                                edited_df['Subject']]

        # Recalculate GPA over time with edited values
        gpa_over_time = []
        for index, row in grades_data.iterrows():
            timestamp = row['Date/Time']
            hours_row = [hours_data.loc[0, subject] for subject in edited_df['Subject']]
            gpa = calculate_final_gpa(row, hours_row, new_start, new_finish, subjects_for_50)
            gpa_over_time.append((timestamp, gpa))

        gpa_df = pd.DataFrame(gpa_over_time, columns=['Date/Time', 'GPA'])
        gpa_df['Date/Time'] = pd.to_datetime(gpa_df['Date/Time'])

    # Final Estimation Chart outside the expander
    st.subheader("Updated Final GPA Estimation")

    fig_final = go.Figure()

    fig_final.add_trace(go.Scatter(
        x=gpa_df['Date/Time'],
        y=[grade_goal] * len(gpa_df),
        mode='lines',
        name='Grade Goal',
        line=dict(color='red', dash='dash')
    ))

    fig_final.add_trace(go.Scatter(
        x=gpa_df['Date/Time'],
        y=gpa_df['GPA'],
        mode='lines',
        name='Final Estimated GPA',
        line=dict(color='green'),
        marker=dict(color='green', size=8)
    ))

    # Add shaded areas for Final Estimation Chart
    fig_final.add_trace(go.Scatter(
        x=pd.concat([gpa_df['Date/Time'], gpa_df['Date/Time'][::-1]]),
        y=pd.concat([gpa_df['GPA'], pd.Series([grade_goal] * len(gpa_df))[::-1]]),
        fill='tozeroy',
        fillcolor='rgba(0, 255, 0, 0.2)',  # Green fill
        line=dict(color='rgba(255, 255, 255, 0)'),  # Transparent line
        showlegend=False
    ))

    fig_final.add_trace(go.Scatter(
        x=pd.concat([gpa_df['Date/Time'], gpa_df['Date/Time'][::-1]]),
        y=pd.concat([pd.Series([grade_goal] * len(gpa_df)), gpa_df['GPA'][::-1]]),
        fill='tozeroy',
        fillcolor='rgba(0, 255, 0, 0.2)',  # Green fill
        line=dict(color='rgba(255, 255, 255, 0)'),  # Transparent line
        showlegend=False
    ))

    fig_final.update_layout(
        xaxis_title='Date/Time',
        yaxis_title='GPA',
        yaxis=dict(range=[max(0, grade_goal - 5), 100]),
        height=400,
        showlegend=True
    )

    st.plotly_chart(fig_final, use_container_width=True)

if __name__ == "__main__":
    main()
