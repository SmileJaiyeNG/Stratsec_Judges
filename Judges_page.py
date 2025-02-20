import streamlit as st

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
ADMIN_PASSWORD = "mummygo1ofmtn"  # Change this to a secure password

# Initialize session state for storing scores
if "scores" not in st.session_state:
    st.session_state.scores = {judge: {department: None for department in departments} for judge in judges}

# Function to calculate total score
def calculate_total_score(department):
    department_scores = [st.session_state.scores[judge][department] for judge in judges if st.session_state.scores[judge][department] is not None]
    if department_scores:
        return sum(department_scores)
    return None

# Admin authentication
def authenticate_admin():
    password = st.text_input("Enter Admin Password", type="password")
    if password == ADMIN_PASSWORD:
        st.session_state.is_admin = True
        st.success("Admin authenticated successfully!")
    else:
        st.session_state.is_admin = False

# Streamlit UI setup
st.title("Department Tasks & Performance Scoring")

# Admin functionality
authenticate_admin()

# Select a department
department_name = st.selectbox("Select a Department", list(departments.keys()))

if department_name:
    # Display department details
    st.subheader(f"Task for {department_name}: {departments[department_name]['task']}")
    st.write(f"Description: {departments[department_name]['description']}")
    st.write(f"Objective: {departments[department_name]['objective']}")

    # Show score sliders for judges
    for judge in judges:
        score = st.slider(f"{judge} - Rate the performance of {department_name} (1 to 5)", 1, 5, key=f"{judge}_{department_name}")
        st.session_state.scores[judge][department_name] = score  # Store the score in session state

    # Calculate and display the total score
    total_score = calculate_total_score(department_name)
    if total_score is not None:
        st.subheader(f"Total Score for {department_name}: {total_score}")
    else:
        st.write("Waiting for all judges to submit their scores...")

# Admin view of all scores
if st.session_state.get("is_admin", False):
    st.subheader("Scores for All Departments (Admin View)")

    for department_name in departments:
        st.write(f"Scores for {department_name}:")
        
        # Calculate total score for the department
        total_score = calculate_total_score(department_name)
        if total_score is not None:
            st.write(f"Total Score: {total_score}")
        else:
            st.write("Total Score: Not yet available")
        
        # Show individual scores from judges
        for judge in judges:
            judge_score = st.session_state.scores[judge][department_name]
            if judge_score is not None:
                st.write(f"{judge}: {judge_score}")
            else:
                st.write(f"{judge}: No score submitted yet")
