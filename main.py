import streamlit as st


def main():
    # Set page title
    st.title("GPA Calculator")

    # Input for number of subjects
    num_subjects = st.number_input("Enter the number of subjects:", min_value=0, value=0, step=0)
    st.markdown("---")
    # Initialize lists
    hours = []
    total = []

    # Loop for each subject
    for i in range(num_subjects):

        # Input for marks and hours
        marks = st.number_input(f"Enter the marks of subject {i + 1}: ", min_value=0)
        hour = st.number_input(f"Enter the hours of subject {i + 1}: ", min_value=0)
        st.markdown("---")
        # Validate inputs
        if marks > 0 and hour > 0:
            total.append(marks * hour)
            hours.append(hour)
        else:
            st.error("Invalid input. Please enter positive numbers.")

    # Calculate GPA
    if len(hours) > 0:
        final_gpa = sum(total) / sum(hours)
        st.success(f"Your GPA is: {final_gpa:.2f}")
    else:
        st.warning("No subjects entered. Please add at least one subject.")


if __name__ == "__main__":
    main()
