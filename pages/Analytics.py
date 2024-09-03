import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def load_data(file_path):
    return pd.read_csv(file_path)

def calculate_gpa_average(grades_data):
    total_sum = grades_data['GPA'].sum()
    num_entries = len(grades_data)
    gpa_average = total_sum / num_entries if num_entries > 0 else 0
    return gpa_average

def main():
    st.title("Analytics Dashboard")

    # Load data for both CSV files
    grades_data = load_data('csv/grades/Grades.csv')
    marks_hours_data = load_data('csv/mark_hours/Marks_Hours.csv')

    # Calculate GPA Average from the Grades data
    gpa_average = calculate_gpa_average(grades_data)

    # Dropdown menu to select which table to view
    file_choice = st.selectbox("Choose table to view:", ["Grades.csv", "Marks_Hours.csv"])

    # Display the selected table
    if file_choice == "Grades.csv":
        st.subheader("Grades Table")
        st.write(f"GPA Average: {gpa_average:.2f}")
        st.dataframe(grades_data, height=400)  # Increase table height
    elif file_choice == "Marks_Hours.csv":
        st.subheader("Totals Table")
        st.write(f"GPA Average: {gpa_average:.2f}")
        st.dataframe(marks_hours_data, height=400)  # Increase table height

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
