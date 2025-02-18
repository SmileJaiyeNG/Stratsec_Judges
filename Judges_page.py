import streamlit as st # type: ignore

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
ADMIN_PASSWORD = "mummygo_of_mtn"

# Initialize session state for storing scores and admin check
if "scores" not in st.session_state:
    st.session_state.scores = {judge: None for judge in judges}

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
    st.subheader("Judges, please score the performance of this department (1 to 5):")

    # Loop through the judges and ask each one to provide a score
    for judge in judges:
        # Check if the judge has already submitted a score
        if st.session_state.scores[judge] is None:
            score = st.slider(f"Rate the performance by {judge}", 1, 5, key=judge)
            st.session_state.scores[judge] = score  # Store the score in session state
        else:
            st.write(f"{judge} has already submitted a score of {st.session_state.scores[judge]}")

    # Optionally, calculate and show the average score
    if all(score is not None for score in st.session_state.scores.values()):
        avg_score = sum(st.session_state.scores.values()) / len(st.session_state.scores)
        st.subheader(f"Average Score: {avg_score:.2f}")
    else:
        st.write("Not all judges have submitted their scores yet.")

    # Display the scores (admin can see all scores)
    if st.session_state.is_admin:
        st.subheader("Scores (Visible to Admin only):")
        for judge, score in st.session_state.scores.items():
            st.write(f"{judge}: {score}" if score is not None else f"{judge}: No score submitted")
