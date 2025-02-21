import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin.exceptions import FirebaseError

# Custom CSS for styling
st.markdown(
    """
    <style>
    .stSlider > div > div > div > div {
        background-color: #4CAF50;  /* Green color for slider */
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 10px 20px;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #4CAF50;
    }
    .stMarkdown p {
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sample task data for departments
departments = {
    "CFO’s OFFICE": {
        "task": "The Silent Disco",
        "description": "Everyone wears headphones playing different songs, but they must dance together in sync without speaking.",
        "objective": "A hilarious, non-verbal way to build teamwork."
    },
    # (Other departments remain the same)
}

# List of judges
judges = ["Modupe", "Nixon", "Oluyemisi", "Samsudeen", "Atolani", "Adeola"]

# Admin password for authentication
ADMIN_PASSWORD = "mummygo1ofmtn"  # Change this to a secure password

# Initialize Firebase
def initialize_firebase():
    try:
        if not firebase_admin._apps:
            st.write("Initializing Firebase...")
            cred = credentials.Certificate(st.secrets["firebase_credentials"])  # Using the Streamlit secrets
            firebase_admin.initialize_app(cred)
            st.write("Firebase initialized successfully!")
        return firestore.client()  # Return the Firestore client
    except FirebaseError as e:
        st.error(f"Firebase initialization failed: {e}")
        return None
    except KeyError:
        st.error("Firebase credentials not found in Streamlit secrets.")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred during Firebase initialization: {e}")
        return None

# Initialize Firestore client
db = initialize_firebase()

# Function to save scores to Firebase
def save_scores():
    if db:
        try:
            for judge in judges:
                for department in departments:
                    score = st.session_state.scores[judge][department]
                    if score is not None:
                        db.collection("scores").document(f"{judge}_{department}").set({
                            "judge": judge,
                            "department": department,
                            "score": score
                        })
        except FirebaseError as e:
            st.error(f"Failed to save scores to Firebase: {e}")

# Function to load scores from Firebase
def load_scores():
    if db:
        try:
            scores = {judge: {department: None for department in departments} for judge in judges}
            docs = db.collection("scores").stream()
            for doc in docs:
                data = doc.to_dict()
                judge = data["judge"]
                department = data["department"]
                score = data["score"]
                scores[judge][department] = score
            return scores
        except FirebaseError as e:
            st.error(f"Failed to load scores from Firebase: {e}")
            return {judge: {department: None for department in departments} for judge in judges}
    return {judge: {department: None for department in departments} for judge in judges}

# Initialize session state with loaded scores
if "scores" not in st.session_state:
    st.session_state.scores = load_scores()
if "submitted" not in st.session_state:
    st.session_state.submitted = {judge: {department: False for department in departments} for judge in judges}

# Function to calculate total score
def calculate_total_score(department):
    department_scores = [
        st.session_state.scores[judge][department]
        for judge in judges
        if st.session_state.scores[judge][department] is not None
    ]
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
st.markdown("---")

# Admin functionality
authenticate_admin()

# Select a department
department_name = st.selectbox("Select a Department", list(departments.keys()))

if department_name:
    # Display department details
    st.subheader(f"Task for {department_name}: {departments[department_name]['task']}")
    st.write(f"**Description:** {departments[department_name]['description']}")
    st.write(f"**Objective:** {departments[department_name]['objective']}")
    st.markdown("---")

    # Judge selection
    judge_name = st.selectbox("Select Your Name", judges)

    # Show score slider and submit button for the selected judge
    if judge_name:
        if st.session_state.submitted[judge_name][department_name]:
            st.write("✅ You have already submitted your score for this department.")
        else:
            score = st.slider(
                f"Rate the performance of {department_name} (1 to 5)",
                1, 5, key=f"{judge_name}_{department_name}"
            )
            if st.button("Submit Score"):
                st.session_state.scores[judge_name][department_name] = score
                st.session_state.submitted[judge_name][department_name] = True
                st.success("Score submitted successfully!")
                save_scores()  # Save scores to Firebase
                st.experimental_rerun()  # Force re-render

    # Calculate and display the total score
    if "total_score" not in st.session_state:
        st.session_state.total_score = calculate_total_score(department_name)
    
    if st.session_state.total_score is not None:
        st.subheader(f"Total Score for {department_name}: {st.session_state.total_score}")
    else:
        st.write("Waiting for all judges to submit their scores...")

    # Reset button for admin
    if st.session_state.get("is_admin", False):
        if st.button("Reset Scores for This Department"):
            for judge in judges:
                st.session_state.scores[judge][department_name] = None
                st.session_state.submitted[judge][department_name] = False
            st.session_state.total_score = None
            st.success("Scores reset successfully!")
            save_scores()  # Save scores to Firebase
            st.experimental_rerun()  # Force re-render

# Admin view of all scores
if st.session_state.get("is_admin", False):
    st.subheader("Scores for All Departments (Admin View)")
    st.markdown("---")

    for department_name in departments:
        st.write(f"### {department_name}")
        
        # Calculate total score for the department
        total_score = calculate_total_score(department_name)
        if total_score is not None:
            st.write(f"**Total Score:** {total_score}")
        else:
            st.write("**Total Score:** Not yet available")
        
        # Show individual scores from judges
        for judge in judges:
            judge_score = st.session_state.scores[judge][department_name]
            if judge_score is not None:
                st.write(f"{judge}: {judge_score}")
            else:
                st.write(f"{judge}: No score submitted yet")
        st.markdown("---")
