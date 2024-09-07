import streamlit as st
import pandas as pd
import json
import os
import plotly.graph_objects as go

def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        st.error("File not found. Please save your grades in the GPA Calculator to get analytics.")
        st.stop()

def convert_json_to_csv(json_data, csv_file_path):
    # Extract subjects and hours from JSON data
    data = json.loads(json_data)
    subjects = data['subjects']
    hours = data['hours']

    # Create a DataFrame
    df = pd.DataFrame([hours], columns=subjects)

    # Ensure directory exists
    directory = os.path.dirname(csv_file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Save DataFrame to CSV
    df.to_csv(csv_file_path, index=False)

def calculate_gpa_average(grades_data):
    total_sum = grades_data['GPA'].sum()
    num_entries = len(grades_data)
    gpa_average = total_sum / num_entries if num_entries > 0 else 0
    return gpa_average

def main():
    st.title("Analytics Dashboard")

    # Define the common base directory for all CSVs
    base_csv_dir = 'csv/mark_hours/'
    grades_csv_path = 'csv/grades/Grades.csv'
    hours_csv_path = os.path.join('csv/Hours/Hours.csv')

    # Check if the Hours CSV file exists
    if not os.path.exists(hours_csv_path):
        # File uploader to upload JSON file
        uploaded_file = st.sidebar.file_uploader("Upload JSON file", type="json")

        if uploaded_file is not None:
            json_data = uploaded_file.read().decode("utf-8")
            convert_json_to_csv(json_data, hours_csv_path)
            st.sidebar.success('Preset JSON has been converted to CSV and saved.')

    # Load data for both CSV files
    grades_data = load_data(grades_csv_path)
    marks_hours_data = load_data(os.path.join(base_csv_dir, 'Marks_Hours.csv'))
    hours_data = load_data(hours_csv_path)

    # Calculate GPA Average from the Grades data
    gpa_average = calculate_gpa_average(grades_data)

    # Dropdown menu to select which table to view
    file_choice = st.selectbox("Choose table to view:", ["Grades.csv", "Marks_Hours.csv", "Hours.csv"])

    # Display the selected table
    if file_choice == "Grades.csv":
        st.subheader("Grades Table")
        st.write(f"GPA Average: {gpa_average:.2f}")
        st.dataframe(grades_data, height=400)  # Increase table height
    elif file_choice == "Marks_Hours.csv":
        st.subheader("Totals Table")
        st.write(f"GPA Average: {gpa_average:.2f}")
        st.dataframe(marks_hours_data, height=400)  # Increase table height
    elif file_choice == "Hours.csv":
        st.subheader("Hours Table")
        st.write(f"GPA Average: {gpa_average:.2f}")
        st.dataframe(hours_data, height=400)  # Increase table height

    # Input for Grade Goal
    grade_goal = st.sidebar.number_input("Grade Goal", min_value=0.0, max_value=100.0, value=50.0)

    # Calculate the y-axis range
    y_min = max(0, grade_goal - 10)  # Ensure y_min is not negative
    y_max = 100

    # Display Charts
    col3, col4 = st.columns([2, 2])

    with col3:
        st.subheader("Grades Over Time")
        if 'Date/Time' in grades_data.columns:
            # Convert 'Date/Time' column to datetime format for proper plotting
            grades_data['Date/Time'] = pd.to_datetime(grades_data['Date/Time'])

            # Define colors
            goal_line_color = 'red'  # Red color for the grade goal line
            fillcolor = 'rgba(0, 0, 255, 0.3)'  # Blue fill for areas

            # Create a line chart where the Grade Goal is the middle line
            fig = go.Figure()

            # Add the Grade Goal as the middle line
            fig.add_trace(go.Scatter(
                x=grades_data['Date/Time'],
                y=[grade_goal] * len(grades_data),
                mode='lines',
                name='Grade Goal',
                line=dict(color=goal_line_color, dash='dash')  # Red dashed line for the goal
            ))

            # Add the GPA as a line going above and below the Grade Goal
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
                fillcolor=fillcolor,  # Blue fill for above goal
                line=dict(color='rgba(255, 255, 255, 0)'),  # Transparent line
                name='Above Goal',
                showlegend=False
            ))

            fig.add_trace(go.Scatter(
                x=pd.concat([grades_data['Date/Time'], grades_data['Date/Time'][::-1]]),
                y=pd.concat([pd.Series([grade_goal] * len(grades_data)), grades_data['GPA'][::-1]]),
                fill='tozeroy',
                fillcolor=fillcolor,  # Blue fill for below goal
                line=dict(color='rgba(255, 255, 255, 0)'),  # Transparent line
                name='Below Goal',
                showlegend=False
            ))

            fig.update_layout(
                xaxis_title='Date/Time',
                yaxis_title='GPA',
                yaxis=dict(range=[y_min, y_max]),  # Set y-axis range
                height=400,
                showlegend=True
            )

            st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.subheader("Grades Weightage")
        if 'Total' in marks_hours_data.columns:
            subject_sums = marks_hours_data.iloc[-1, 1:-1]  # Exclude 'Date/Time' and 'Total'
            fig = go.Figure(go.Pie(labels=subject_sums.index, values=subject_sums))
            fig.update_layout(showlegend=False, height=400)  # Hide legend and set height
            st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
