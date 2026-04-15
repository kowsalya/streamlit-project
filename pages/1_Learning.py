import streamlit as st
import json
import os

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="Vibha Beldex Learning & Quiz App", layout="wide")

st.title("📘 Learning Module")

# -------------------------------
# Load JSON Data (FIXED PATH)
# -------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
file_path = os.path.join(BASE_DIR, "data", "faq.json")

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# -------------------------------
# Session State Setup
# -------------------------------
if "completed_sections" not in st.session_state:
    st.session_state.completed_sections = set()

if "learning_done" not in st.session_state:
    st.session_state.learning_done = False

# -------------------------------
# Progress Bar
# -------------------------------
total_sections = len(data)
completed = len(st.session_state.completed_sections)

progress = completed / total_sections if total_sections > 0 else 0

st.progress(progress)
st.write(f"📊 Progress: {completed}/{total_sections}")

# -------------------------------
# Display Sections + Questions
# -------------------------------
for i, section in enumerate(data):

    section_name = section["category"]

    with st.expander(f"📂 {section_name}", expanded=False):

        # 🔥 Loop through ALL questions properly
        for qa in section["questions"]:
            st.markdown(f"### ❓ {qa['q']}")
            st.write(f"💡 {qa['a']}")
            st.divider()

        # -------------------------------
        # Mark Complete Button
        # -------------------------------
        if section_name not in st.session_state.completed_sections:
            if st.button(f"✅ Mark '{section_name}' as Completed", key=f"btn_{i}"):
                st.session_state.completed_sections.add(section_name)
                st.rerun()
        else:
            st.success("✔ Completed")

# -------------------------------
# Final Completion Check
# -------------------------------
if completed == total_sections:
    st.success("🎉 All sections completed! You can now take the Quiz.")
    st.session_state.learning_done = True
else:
    st.warning("⚠ Complete all sections to unlock the quiz.")

# -------------------------------
# DEBUG (optional - remove later)
# -------------------------------
# st.write("Total Sections:", total_sections)