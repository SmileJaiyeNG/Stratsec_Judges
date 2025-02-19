import streamlit as st  # type: ignore

# Sample task data for departments
departments = {
    "CFO’s OFFICE": {
        "task": "The Silent Disco",
        "description": "Everyone wears headphones playing different songs, but they must dance together in sync without speaking.",
        "objective": "A hilarious, non-verbal way to build teamwork."
    },
    "BUSINESS PARTNERING": {
        "task": "Around the World - Cultural Showcase",
        "description": "Team represents a country (not home country) and must prepare a fun cultural performance (a dance, chant, or a short drama).",
        "objective": "Fosters diversity, inclusivity and fun learning moments."
    },
    "FINANCIAL PLANNING": {
        "task": "Lights, Camera, Action! – Skit",
        "description": "Team selects a random topic (e.g., futuristic workplace, The day technology took over, a day in the life of a CFO) and must create and perform a short skit.",
        "objective": "Enhances storytelling, improvisation, and laughter."
    },
    "BUSINESS ASSURANCE": {
        "task": "The Ultimate Dance-Off",
        "description": "Team will pick a dance style (e.g., salsa, hip-hop, local traditional) and perform a short routine.",
        "objective": "Encourage energy and confidence."
    },
    "FINANCIAL OPERATIONS": {
        "task": "Reverse Talent Show",
        "description": "Instead of showcasing their real talents, team performs something they are terrible at (e.g., off-key singing, awkward dancing, or bad poetry).",
        "objective": "Creates a safe space for fun and laughter, and embracing imperfection."
    },
    "TREASURY": {
        "task": "Team Anthem",
        "description": "Team rewrites the lyrics of a popular song to reflect their team spirit or workplace fun.",
        "objective": "Boosts creativity, humor, and musical talents."
    },
    "GSSC (Group 1)": {
        "task": "The Office Commercial",
        "description": "The team prepares a fun 30-second advertisement for a fake or real office product.",
        "objective": "Encourages creativity, teamwork, and marketing skills."
    },
    "GSSC (Group 2)": {
        "task": "Musical Mashup",
        "description": "Team mixes and mashup two different popular songs of different genres and perform a musical act.",
        "objective": "Encourages teamwork, creativity, and love for music."
    }
}

# List of judges
judges = ["Modupe", "Nixon", "Oluyemisi", "Samsudeen", "Atolani", "Adeola"]

# Admin password for authentication
ADMIN_PASSWORD = "mummygo1ofmtn"

# Initialize session state for storing scores and admin check
if "scores" not in st.session_state:
    st.session_state.scores = {judge: {department: None for department in departments} for judge in judges}

if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

# Admin password check
admin_password = st.text_input("Enter Admin Password (If you are an admin)", type="password")

# Check if admin password is correct
if admin_password == ADMIN_PASSWORD:
    st.session_state.is_admin = True

# Streamlit UI: Display title
st.title('Department Tasks & Performance Scoring')

# Display a dropdown to select a department
department_name = st.selectbox("Select a Department", list(departments.keys()))

# Display the task, description, and objective for the selected department
if department_name:
    st.subheader(f"Task for {department_name}:")
    st.write(departments[department_name]["task"])

    st.subheader("Description:")
    st.write(departments[department_name]["description"])

    st.subheader("Objective:")
    st.write(departments[department_name]["objective"])

    # Scoring (simplified for judges)
    st.subheader("Judges, please rate the performance of this department (1 to 5):")

    # Loop through the judges and ask each one to provide a score for this department
    for judge in judges:
        # Check if the judge has already submitted a score for this department
        if st.session_state.scores[judge][department_name] is None:
            score = st.slider(f"{judge} - Rate the performance of {department_name}", 1, 5, key=f"{judge}_{department_name}")
            st.session_state.scores[judge][department_name] = score  # Store the score in session state

    # Calculate and display the total score for this department (updated as judges submit scores)
    department_scores = [st.session_state.scores[judge][department_name] for judge in judges if st.session_state.scores[judge][department_name] is not None]
    if department_scores:
        total_score = sum(department_scores)
        st.subheader(f"Total Score for {department_name}: {total_score}")
    else:
        st.write(f"Not all judges have submitted their scores for {department_name} yet.")

# Display the scores (admin can see all scores as judges make them)
if st.session_state.is_admin:
    st.subheader("Scores (Visible to Admin only):")
    for department_name in departments:
        st.write(f"Scores for {department_name}:")
        
        # Calculate the total score for this department
        department_scores = [st.session_state.scores[judge][department_name] for judge in judges if st.session_state.scores[judge][department_name] is not None]
        if department_scores:
            total_score = sum(department_scores)
            st.write(f"Total Score for {department_name}: {total_score}")
        else:
            st.write(f"Total Score for {department_name}: Not yet available")

        # Display each judge's score for the department (even as they submit it)
        for judge in judges:
            judge_score = st.session_state.scores[judge][department_name]
            if judge_score is not None:
                st.write(f"{judge}: {judge_score}")
            else:
                st.write(f"{judge}: No score submitted yet")
