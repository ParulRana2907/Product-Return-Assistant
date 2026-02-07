import streamlit as st
import pandas as pd
from logic.return_logic import *
from assets.emoji_icons import *

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Product Return Assistant",
    page_icon="📦",
    layout="wide"
)

# ---------------- LOAD STYLES ----------------
with open("ui/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "profile" not in st.session_state:
    st.session_state.profile = {
        "name": "Guest User",
        "email": "guest@email.com",
        "city": "Not Set",
        "avatar": "👤",
        "wallet": 250,
        "trust": "Medium"
    }

# ---------------- HEADER ----------------
st.markdown(
    """
    <div class="header">
        📦 Product Return Assistant<br>
        <span style="font-size:18px;">Smart • Fast • Fraud-Aware Returns</span>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------- SIDEBAR ----------------
st.sidebar.markdown("## 🛍️ Navigation")
page = st.sidebar.radio(
    "Go to",
    ["🏠 Dashboard", "🔁 Start Return", "👤 User Profile", "📊 Analytics"]
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    f"""
    **{st.session_state.profile['avatar']} {st.session_state.profile['name']}**  
    💰 Wallet: ₹{st.session_state.profile['wallet']}  
    🛡️ Trust: {st.session_state.profile['trust']}
    """
)

# ==================================================
# 🏠 DASHBOARD
# ==================================================
if page == "🏠 Dashboard":
    st.subheader("✨ Welcome Back!")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📦 Total Returns", "1,248")
    c2.metric("⚡ Faster Processing", "70%")
    c3.metric("🚨 Fraud Reduced", "30%")
    c4.metric("😊 Satisfaction", "92%")

    st.markdown("### 🛒 Recent Orders")

    cols = st.columns(4)
    for i, col in enumerate(cols):
        col.markdown(
            f"""
            <div class="card">
                <img src="https://source.unsplash.com/300x200/?shopping,product,{i}"
                     style="width:100%; border-radius:12px;">
                <br><b>Order #{1200+i}</b><br>
                Delivered • Eligible
            </div>
            """,
            unsafe_allow_html=True
        )

# ==================================================
# 🔁 START RETURN
# ==================================================
elif page == "🔁 Start Return":
    st.subheader("💬 Start Return Request")

    col1, col2, col3 = st.columns(3)
    days = col1.slider("📅 Days since delivery", 0, 30, 3)
    unused = col2.selectbox("✨ Product unused?", ["Yes", "No"])
    attempts = col3.number_input("🔁 Past return attempts", 0, 5, 0)

    reason = st.selectbox(
        "❓ Reason for return",
        ["Changed Mind", "Damaged", "Wrong Item", "Empty Box"]
    )

    if st.button("🚀 Submit Return"):
        eligible = check_eligibility(days, unused)

        # ✅ FIXED LINE (trust_level passed)
        fraud = fraud_score(
            reason,
            attempts,
            st.session_state.profile["trust"]
        )

        satisfaction = satisfaction_score(fraud)
        status = refund_status(eligible, fraud)

        st.divider()

        if status == "Approved":
            color = "#dcfce7"
            badge = CHECK
        elif status == "Manual Review":
            color = "#fef9c3"
            badge = WARNING
        else:
            color = "#fee2e2"
            badge = CROSS

        st.markdown(
            f"<div class='card' style='background:{color}; font-size:22px;'>"
            f"{badge} <b>{status}</b></div>",
            unsafe_allow_html=True
        )

        c1, c2, c3 = st.columns(3)
        c1.metric(f"{FRAUD} Fraud Risk", f"{fraud}%")
        c2.metric(f"{HAPPY} Satisfaction", f"{satisfaction}%")
        c3.metric(f"{SPEED} Speed", "70% Faster")

        st.info(f"🛡️ Trust Level Applied: {st.session_state.profile['trust']}")

        st.subheader(f"{TRACK} Refund Progress")
        st.progress(80 if status == "Approved" else 45)

        if status == "Approved":
            st.success(f"{LABEL} Return label generated (simulated)")
            st.balloons()
        else:
            st.subheader(f"{EXCHANGE} Exchange Suggestions")

            cols = st.columns(3)
            for i, col in enumerate(cols):
                col.markdown(
                    f"""
                    <div class="card">
                        <img src="https://source.unsplash.com/300x200/?electronics,product,{i}"
                             style="width:100%; border-radius:12px;">
                        <br><b>Alternate Product {i+1}</b><br>
                        ⭐ 4.{i+2}/5
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# ==================================================
# 👤 USER PROFILE
# ==================================================
elif page == "👤 User Profile":
    st.subheader("👤 My Profile")

    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        name = col1.text_input("Full Name", st.session_state.profile["name"])
        email = col2.text_input("Email", st.session_state.profile["email"])
        city = col1.text_input("City", st.session_state.profile["city"])
        avatar = col2.selectbox(
            "Avatar",
            ["👤", "🧑‍💻", "🧕", "🧔", "👩‍💼", "🧑‍🎓"]
        )
        trust = col2.selectbox(
            "Trust Level",
            ["Low", "Medium", "High"],
            index=["Low", "Medium", "High"].index(st.session_state.profile["trust"])
        )

        save = st.form_submit_button("💾 Save Profile")
        if save:
            st.session_state.profile.update({
                "name": name,
                "email": email,
                "city": city,
                "avatar": avatar,
                "trust": trust
            })
            st.success("✅ Profile Updated!")

    st.markdown(
        f"""
        <div class="card">
            {st.session_state.profile['avatar']} <b>{st.session_state.profile['name']}</b><br>
            📧 {st.session_state.profile['email']}<br>
            📍 {st.session_state.profile['city']}<br>
            🛡️ Trust Level: {st.session_state.profile['trust']}<br>
            💰 Wallet Balance: ₹{st.session_state.profile['wallet']}
        </div>
        """,
        unsafe_allow_html=True
    )

# ==================================================
# 📊 ANALYTICS
# ==================================================
elif page == "📊 Analytics":
    st.subheader("📊 Return Insights")

    df = pd.DataFrame({
        "Reason": ["Changed Mind", "Damaged", "Wrong Item", "Empty Box"],
        "Returns": [420, 280, 180, 120]
    })

    st.bar_chart(df.set_index("Reason"))

    st.markdown(
        """
        <div class="card">
        <b>Insights</b>
        <ul>
            <li>Changed Mind drives majority returns</li>
            <li>Empty box has highest fraud risk</li>
            <li>Trust-based scoring reduces false rejections</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

st.success("✔ App running perfectly — Ready for demo 🚀")

