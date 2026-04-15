import streamlit as st
import json
import random

st.set_page_config(page_title="Crypto Learning App", page_icon="📘")

# ---------- HEADER ----------
st.markdown(
    "<h1 style='text-align:center; color:#00ffc3;'>📘 Crypto Learning App</h1>",
    unsafe_allow_html=True
)

st.sidebar.title("📘 Learning App")

menu = st.sidebar.radio(
    "📌 Select Module",
    ["📘 Learning", "🧠 Quiz"]
)

# ---------- LOAD DATA ----------
with open("faq.json", "r", encoding="utf-8") as f:
    topics = json.load(f)

# ---------------------------
# 📘 LEARNING MODULE
# ---------------------------
if menu == "📘 Learning":

    st.header("📘 Learning Mode")

    if "learn_index" not in st.session_state:
        st.session_state.learn_index = 0

    topic = topics[st.session_state.learn_index]

    st.progress((st.session_state.learn_index + 1) / len(topics))

    st.write(f"{st.session_state.learn_index + 1} / {len(topics)}")

    st.markdown("### ❓ " + topic["question"])
    st.success(topic["answer"])

    col1, col2, col3 = st.columns([1,2,1])

    with col1:
        if st.button("⬅ Previous"):
            if st.session_state.learn_index > 0:
                st.session_state.learn_index -= 1

    with col3:
        if st.button("Next ➡"):
            if st.session_state.learn_index < len(topics) - 1:
                st.session_state.learn_index += 1

# ---------------------------
# 🧠 QUIZ MODULE
# ---------------------------
elif menu == "🧠 Quiz":

    st.header("🧠 Quiz Mode")

    # INIT
    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False
    if "quiz_index" not in st.session_state:
        st.session_state.quiz_index = 0
    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0
    if "quiz_answered" not in st.session_state:
        st.session_state.quiz_answered = False

    # START SCREEN
    if not st.session_state.quiz_started:

        st.subheader("Ready for Quiz?")
        st.write(f"Total Questions: {len(topics)}")

        if st.button("🚀 Start Quiz"):
            st.session_state.quiz_started = True
            st.session_state.quiz_index = 0
            st.session_state.quiz_score = 0
            st.session_state.quiz_answered = False

        st.stop()

    topic = topics[st.session_state.quiz_index]

    st.progress((st.session_state.quiz_index + 1) / len(topics))

    st.write(f"Question {st.session_state.quiz_index + 1} of {len(topics)}")

    st.markdown("### ❓ " + topic["question"])

    # Stable options
    key_name = f"options_{st.session_state.quiz_index}"

    if key_name not in st.session_state:
        opts = topic["options"].copy()
        random.shuffle(opts)
        st.session_state[key_name] = opts

    options = st.session_state[key_name]

    user_answer = st.radio(
        "Choose correct answer:",
        options,
        key=f"quiz_{st.session_state.quiz_index}"
    )

    if st.button("Submit Answer"):

        if not st.session_state.quiz_answered:

            if user_answer == topic["correct"]:
                st.session_state.quiz_score += 1
                st.success("Correct ✅")
            else:
                st.error(f"Wrong ❌ Correct: {topic['correct']}")

            st.session_state.quiz_answered = True

    if st.session_state.quiz_answered:
        st.info("Click Next ➡ to continue")
        st.stop()

    if st.button("Next ➡"):

        if st.session_state.quiz_index < len(topics) - 1:
            st.session_state.quiz_index += 1
            st.session_state.quiz_answered = False

    # FINAL RESULT
    if st.session_state.quiz_index == len(topics) - 1 and st.session_state.quiz_answered:

        st.markdown("### 🎯 Final Result")

        st.write(f"Score: {st.session_state.quiz_score}/{len(topics)}")

        if st.session_state.quiz_score >= len(topics) * 0.6:
            st.success("🎉 Passed!")

            name = st.text_input("Enter your name")

            if st.button("Generate Certificate"):

                certificate = f"""
Certificate of Completion

{name} successfully completed the Quiz

Score: {st.session_state.quiz_score}/{len(topics)}
"""

                st.download_button(
                    "📄 Download Certificate",
                    certificate,
                    file_name="certificate.txt"
                )
        else:
            st.error("❌ Try Again")

    if st.button("🔄 Restart Quiz"):
        st.session_state.quiz_started = False
        st.session_state.quiz_index = 0
        st.session_state.quiz_score = 0
        st.session_state.quiz_answered = False