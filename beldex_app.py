import streamlit as st
import json
import random

st.set_page_config(page_title="Beldex Smart App", page_icon="💰")

# ---------- HEADER ----------
st.markdown(
    "<h1 style='text-align:center; color:#00ffc3;'>💰 Beldex Smart App</h1>",
    unsafe_allow_html=True
)

# ---------- SIDEBAR ----------
st.sidebar.title("💰 Vibha Beldex App")
st.sidebar.markdown("Learn • Decide • Grow")

menu = st.sidebar.radio(
    "📌 Select Module",
    ["📊 Profit Calculator", "📈 Staking Planner", "⚠ Risk Checker", "📘 Learning"]
)

# ---------------------------
# PROFIT CALCULATOR
# ---------------------------
if menu == "📊 Profit Calculator":

    st.header("📊 Profit Calculator")

    buy_price = st.number_input("Buy Price (₹)", min_value=0.0)
    current_price = st.number_input("Current Price (₹)", min_value=0.0)
    quantity = st.number_input("Quantity", min_value=0.0)

    if st.button("Calculate Profit"):
        investment = buy_price * quantity
        current_value = current_price * quantity
        profit = current_value - investment

        roi = (profit / investment) * 100 if investment > 0 else 0

        st.success(f"Profit/Loss: ₹{profit:.2f}")
        st.write(f"ROI: {roi:.2f}%")

# ---------------------------
# STAKING PLANNER
# ---------------------------
elif menu == "📈 Staking Planner":

    st.header("📈 Staking Planner")

    amount = st.number_input("Investment Amount (₹)", min_value=0.0)
    months = st.slider("Duration (Months)", 1, 60)

    reward_rate = 0.01
    estimated_reward = amount * reward_rate * months

    st.success(f"Estimated Reward: ₹{estimated_reward:.2f}")

# ---------------------------
# SMART RISK ANALYZER
# ---------------------------
elif menu == "⚠ Risk Checker":

    st.header("⚠ Smart Risk Analyzer")

    guarantee = st.selectbox("Guaranteed profit promised?", ["No", "Yes"])
    referral = st.selectbox("Income mainly from referrals?", ["No", "Yes"])
    transparency = st.selectbox("Is project clearly explained?", ["Yes", "No"])
    urgency = st.selectbox("Are you pressured to join quickly?", ["No", "Yes"])
    withdraw = st.selectbox("Is withdrawal process clear?", ["Yes", "No"])

    score = 0
    reasons = []

    if guarantee == "Yes":
        score += 2
        reasons.append("❌ Guaranteed profit is unrealistic")

    if referral == "Yes":
        score += 2
        reasons.append("⚠ Referral-heavy model risk")

    if transparency == "No":
        score += 2
        reasons.append("❌ Lack of clarity")

    if urgency == "Yes":
        score += 1
        reasons.append("⚠ Pressure tactics")

    if withdraw == "No":
        score += 2
        reasons.append("❌ Withdrawal unclear")

    if st.button("Analyze Risk"):

        st.markdown("### 🔍 Analysis")

        for r in reasons:
            st.write(r)

        if score <= 2:
            st.success("✅ Low Risk")
        elif score <= 5:
            st.warning("⚠ Moderate Risk")
        else:
            st.error("🚨 High Risk")

# ---------------------------
# LEARNING + REAL QUIZ + CERTIFICATE
# ---------------------------
elif menu == "📘 Learning":

    st.header("📘 Beldex Learning")

    with open("faq.json", "r", encoding="utf-8") as f:
        topics = json.load(f)

    # Session state
    if "learn_index" not in st.session_state:
        st.session_state.learn_index = 0
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "answered" not in st.session_state:
        st.session_state.answered = False

    topic = topics[st.session_state.learn_index]

    # Progress
    progress = (st.session_state.learn_index + 1) / len(topics)
    st.progress(progress)

    st.write(f"📘 Question {st.session_state.learn_index + 1} of {len(topics)}")
    st.markdown("### ❓ " + topic["question"])
    st.info(topic["answer"])

    # Shuffle options
    options = topic["options"].copy()
    random.shuffle(options)

    # Quiz
    st.markdown("### 🧠 Quiz")

    user_answer = st.radio(
        "Choose correct answer:",
        options,
        key=f"quiz_{st.session_state.learn_index}"
    )

    if st.button("Submit Answer"):
        if not st.session_state.answered:

            if user_answer == topic["correct"]:
                st.session_state.score += 1
                st.success("Correct ✅")
            else:
                st.error(f"Wrong ❌ Correct: {topic['correct']}")

            st.session_state.answered = True

    st.write(f"🏆 Score: {st.session_state.score}")

    # Navigation
    col1, col2, col3 = st.columns([1,2,1])

    with col1:
        if st.button("⬅ Previous"):
            if st.session_state.learn_index > 0:
                st.session_state.learn_index -= 1
                st.session_state.answered = False

    with col3:
        if st.button("Next ➡"):
            if st.session_state.learn_index < len(topics) - 1:
                st.session_state.learn_index += 1
                st.session_state.answered = False

    # Final Result
    if st.session_state.learn_index == len(topics) - 1:

        st.markdown("### 🎯 Final Result")

        if st.session_state.score >= len(topics) * 0.6:
            st.success("🎉 Passed!")

            name = st.text_input("Enter your name")

            if st.button("Generate Certificate"):

                certificate = f"""
Certificate of Completion

This certifies that {name}
has successfully completed the
Beldex Learning Program.

Score: {st.session_state.score}/{len(topics)}
"""

                st.download_button(
                    label="📄 Download Certificate",
                    data=certificate,
                    file_name="certificate.txt"
                )
        else:
            st.error("❌ Try Again")

    # Restart
    if st.button("🔄 Restart Learning"):
        st.session_state.learn_index = 0
        st.session_state.score = 0
        st.session_state.answered = False