import streamlit as st
import json
import os

# -------------------------------
# LOAD JSON (for learning lock)
# -------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
file_path = os.path.join(BASE_DIR, "data", "faq.json")

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# -------------------------------
# LOCK QUIZ (Learning must complete)
# -------------------------------
TOTAL_SECTIONS = len(data)
completed = len(st.session_state.get("completed_sections", set()))

if completed < TOTAL_SECTIONS:
    st.warning("⚠️ Please complete all Learning sections first!")
    st.stop()

# -------------------------------
# QUESTIONS (FULL SET)
# -------------------------------
questions = [
    {
        "section": "அடிப்படை",
        "q": "Nexus தளத்தின் தலைமையகம் எங்குள்ளது?",
        "options": ["லண்டன்", "பனாமா சிட்டி", "சிங்கப்பூர்", "துபாய்"],
        "answer": "பனாமா சிட்டி"
    },
    {
        "section": "அடிப்படை",
        "q": "பதிவு செய்யும் போது எவற்றை மாற்றவே முடியாது?",
        "options": ["கடவுச்சொல் மற்றும் பயனர் பெயர்", "மின்னஞ்சல் முகவரி மற்றும் முழு பெயர்", "மொபைல் எண் மற்றும் நாடு", "இவை அனைத்தையும் மாற்றலாம்"],
        "answer": "மின்னஞ்சல் முகவரி மற்றும் முழு பெயர்"
    },
    {
        "section": "அடிப்படை",
        "q": "கடவுச்சொல்லை மறந்துவிட்டால் எதன் மூலம் மீட்டெடுக்கலாம்?",
        "options": ["மொபைல் OTP", "மின்னஞ்சல் Reset Link", "Customer care", "New ID"],
        "answer": "மின்னஞ்சல் Reset Link"
    },
    {
        "section": "Staking",
        "q": "BVS திட்டத்தின் கால வரம்பு என்ன?",
        "options": ["1 வருடம்", "3 ஆண்டுகள்", "5 ஆண்டுகள்", "வரம்பு இல்லை"],
        "answer": "5 ஆண்டுகள்"
    },
    {
        "section": "Staking",
        "q": "ஸ்டேக்கிங் வருமானம் எப்போது தொடங்கும்?",
        "options": ["6 மாதம்", "முதல் மாதம்", "5 ஆண்டு", "1 ஆண்டு"],
        "answer": "முதல் மாதம்"
    },
    {
        "section": "Rewards",
        "q": "Referral bonus எவ்வளவு?",
        "options": ["5%", "8%", "10%", "20%"],
        "answer": "10%"
    },
    {
        "section": "Rewards",
        "q": "Group incentive பெற தகுதி?",
        "options": ["Daily login", "Left & Right active ID", "1000 crypto", "Club member"],
        "answer": "Left & Right active ID"
    },
    {
        "section": "Wallet",
        "q": "Withdrawal fee எப்போது?",
        "options": ["Every time", "4th withdrawal", "10th withdrawal", "No fee"],
        "answer": "4th withdrawal"
    },
    {
        "section": "Wallet",
        "q": "Crypto எந்த balance-ல் மாற்றலாம்?",
        "options": ["Earning", "Staking", "Exchange", "Available"],
        "answer": "Exchange"
    },
    {
        "section": "Wallet",
        "q": "Max withdrawal time?",
        "options": ["12h", "24h", "48h", "72h"],
        "answer": "48h"
    },
    {
        "section": "Club",
        "q": "Decider Club GI?",
        "options": ["500", "1000", "5000", "7500"],
        "answer": "1000"
    },
    {
        "section": "Club",
        "q": "Highest club?",
        "options": ["Mooning", "Oberon", "Callisto", "Titan"],
        "answer": "Titan"
    },
    {
        "section": "Club",
        "q": "Believer target?",
        "options": ["1-1", "2-2", "5-5", "None"],
        "answer": "2-2"
    },
    {
        "section": "Rules",
        "q": "Inactive months for stop incentive?",
        "options": ["1", "2", "3", "6"],
        "answer": "3"
    }
]

# -------------------------------
# SESSION STATE
# -------------------------------
if "q_index" not in st.session_state:
    st.session_state.q_index = 0

if "score" not in st.session_state:
    st.session_state.score = 0

# -------------------------------
# UI
# -------------------------------
st.title("🧠 Nexus Mega Quiz")

st.write(f"Total Questions: {len(questions)}")

progress = st.session_state.q_index / len(questions)
st.progress(progress)

# -------------------------------
# QUIZ FLOW
# -------------------------------
if st.session_state.q_index < len(questions):

    current_q = questions[st.session_state.q_index]

    st.markdown(f"### 📂 Section: {current_q['section']}")
    st.subheader(f"Q{st.session_state.q_index + 1}: {current_q['q']}")

    selected = st.radio(
        "Choose your answer:",
        current_q["options"],
        key=st.session_state.q_index
    )

    if st.button("Submit Answer"):
        if selected == current_q["answer"]:
            st.success("✅ சரியான பதில்!")
            st.session_state.score += 1
        else:
            st.error(f"❌ தவறு! சரியான பதில்: {current_q['answer']}")

        st.session_state.q_index += 1
        st.rerun()

# -------------------------------
# RESULT
# -------------------------------
else:
    st.success("🎉 Quiz Completed!")

    score = st.session_state.score
    total = len(questions)

    st.subheader(f"Score: {score}/{total}")

    percentage = (score / total) * 100
    st.write(f"Percentage: {percentage:.2f}%")

    if percentage >= 70:
        st.balloons()
        st.success("🏆 நீங்கள் தேர்ச்சி பெற்றீர்கள்!")
    else:
        st.warning("❌ மீண்டும் முயற்சிக்கவும்!")

    if st.button("🔁 Restart Quiz"):
        st.session_state.q_index = 0
        st.session_state.score = 0
        st.rerun()