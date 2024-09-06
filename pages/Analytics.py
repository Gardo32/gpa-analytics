import streamlit as st
import pandas as pd
import json
import os
import io
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

    # Define paths
    csv_hours = '/csv/Hours/Hours.csv'
    csv_load_hours = load_data(csv_hours)

    # Check if the CSV file already exists
    if not os.path.exists(csv_hours):
        # File uploader to upload JSON file
        uploaded_file = st.sidebar.file_uploader("Upload JSON file", type="json")

        if uploaded_file is not None:
            json_data = uploaded_file.read().decode("utf-8")
            convert_json_to_csv(json_data, csv_hours)
            st.sidebar.success('Preset JSON has been converted to CSV and saved.')

    # Load data for both CSV files
    grades_data = load_data('csv/grades/Grades.csv')
    marks_hours_data = load_data('csv/mark_hours/Marks_Hours.csv')

    # Calculate GPA Average from the Grades data
    gpa_average = calculate_gpa_average(grades_data)

    # Dropdown menu to select which table to view
    file_choice = st.selectbox("Choose table to view:", ["Grades.csv", "Marks_Hours.csv","Hours.csv"])

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
        st.dataframe(csv_load_hours, height=400)  # Increase table height


    # Display Charts
    col3, col4 = st.columns([2, 2])

    with col3:
        st.subheader("Grades Over Time")
        if 'Date/Time' in grades_data.columns:
            # Convert 'Date/Time' column to datetime format for proper plotting
            grades_data['Date/Time'] = pd.to_datetime(grades_data['Date/Time'])

            # Create a line chart using graph_objects
            fig = go.Figure(go.Scatter(
                x=grades_data['Date/Time'],
                y=grades_data['GPA'],
                mode='lines+markers',  # 'lines' for just lines, 'markers' for markers, or 'lines+markers' for both
                name='GPA'
            ))
            fig.update_layout(xaxis_title='Date/Time', yaxis_title='GPA', height=400)
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
