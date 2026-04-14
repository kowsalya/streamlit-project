import streamlit as st
import json

st.set_page_config(page_title="Vibha Crypto Learning ")

st.title("📘Vibha Crypto Learning ")
st.subheader("Learn Step by Step")

# Load JSON
with open("faq.json", "r", encoding="utf-8") as f:
    all_topics = json.load(f)

# ---------------------------
# CATEGORY FILTER
# ---------------------------
categories = ["All"] + sorted(list(set([t["category"] for t in all_topics])))

selected_category = st.selectbox("📂 Select Category", categories)

# Filter topics
if selected_category == "All":
    topics = all_topics
else:
    topics = [t for t in all_topics if t["category"] == selected_category]

# ---------------------------
# SESSION STATE INDEX
# ---------------------------
if "index" not in st.session_state:
    st.session_state.index = 0

# Reset index when category changes
if "last_category" not in st.session_state:
    st.session_state.last_category = selected_category

if st.session_state.last_category != selected_category:
    st.session_state.index = 0
    st.session_state.last_category = selected_category

# Safety check
if len(topics) == 0:
    st.warning("No questions available")
    st.stop()

# Ensure index is in range
st.session_state.index = min(st.session_state.index, len(topics) - 1)

# ---------------------------
# DISPLAY CURRENT QUESTION (NEW UI)
# ---------------------------

# ---------- CUSTOM STYLE ----------
st.markdown("""
<style>
.title {
    text-align: center;
    font-size: 36px;
    font-weight: bold;
    color: #00ffc3;
}
.card {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 0px 10px rgba(0,255,200,0.2);
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("<div class='title'>🚀 Vibha Crypto Learning</div>", unsafe_allow_html=True)

# ---------- PROGRESS ----------
progress = (st.session_state.index + 1) / len(topics)
st.progress(progress)

st.write(f"📘 Question {st.session_state.index + 1} of {len(topics)}")

# ---------- CARD ----------
topic = topics[st.session_state.index]

st.markdown("<div class='card'>", unsafe_allow_html=True)

st.markdown(f"### ❓ {topic['question']}")
st.markdown("#### 💡 Answer")
st.success(topic["answer"])

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# ---------------------------
# NAVIGATION BUTTONS
# ---------------------------
col1, col2, col3 = st.columns([1,2,1])

with col1:
    if st.button("⬅ Previous"):
        if st.session_state.index > 0:
            st.session_state.index -= 1

with col2:
    st.write(f"{st.session_state.index + 1} / {len(topics)}")

with col3:
    if st.button("Next ➡"):
        if st.session_state.index < len(topics) - 1:
            st.session_state.index += 1
           # ---------------------------
# EXTRA (TIP SECTION)
# ---------------------------
st.info("⚠ Always understand crypto before investing.")