import streamlit as st
import pandas as pd
import plotly.express as px

from login import authenticate
from loan_engine import calculate_risk
from ml_model import predict_default
from chat_assistant import loan_advisor
from pdf_generator import create_pdf

# ----------------------------
# PAGE CONFIG
# ----------------------------

st.set_page_config(
    page_title="Smart Loan Approval Assistant",
    page_icon="🏦",
    layout="wide"
)

# ----------------------------
# LOGIN
# ----------------------------

if "logged" not in st.session_state:
    st.session_state.logged = False

if not st.session_state.logged:

    st.title("🏦 Smart Loan Approval Assistant")

    st.subheader("Banker Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if authenticate(
            username,
            password
        ):

            st.session_state.logged = True

            st.success(
                "Login Successful"
            )

            st.rerun()

        else:

            st.error(
                "Invalid Credentials"
            )

    st.stop()

# ----------------------------
# HEADER
# ----------------------------

st.title(
    "🏦 Smart Loan Approval Assistant"
)

st.caption(
    "AI-Powered Banking Risk Assessment Platform"
)

# ----------------------------
# TABS
# ----------------------------

tab1, tab2, tab3 = st.tabs(
    [
        "Loan Assessment",
        "Portfolio Dashboard",
        "AI Loan Advisor"
    ]
)

# =====================================================
# TAB 1
# =====================================================

with tab1:

    st.subheader(
        "Customer Loan Assessment"
    )

    col1, col2 = st.columns(2)

    with col1:

        income = st.number_input(
            "Monthly Income (₹)",
            min_value=10000,
            value=80000
        )

        credit_score = st.slider(
            "Credit Score",
            300,
            900,
            750
        )

    with col2:

        emi = st.number_input(
            "Existing EMI (₹)",
            min_value=0,
            value=10000
        )

        requested_loan = st.number_input(
            "Requested Loan Amount (₹)",
            min_value=50000,
            value=1200000
        )

    if st.button(
        "Analyze Loan Application"
    ):

        # ------------------------
        # Risk Engine
        # ------------------------

        risk_score = calculate_risk(
            income,
            credit_score,
            emi
        )

        decision = (
            "APPROVED"
            if risk_score >= 80
            else "MANUAL REVIEW"
            if risk_score >= 60
            else "REJECTED"
        )

        # ------------------------
        # ML Prediction
        # ------------------------

        default_probability = predict_default(
            income,
            credit_score,
            emi
        )

        # ------------------------
        # Display KPIs
        # ------------------------

        k1, k2, k3 = st.columns(3)

        with k1:

            st.metric(
                "Risk Score",
                f"{risk_score}/100"
            )

        with k2:

            st.metric(
                "Decision",
                decision
            )

        with k3:

            st.metric(
                "Default Risk %",
                default_probability
            )

        # ------------------------
        # Save Session
        # ------------------------

        st.session_state.customer = {

            "income":
                income,

            "credit_score":
                credit_score,

            "emi":
                emi,

            "loan":
                requested_loan,

            "risk_score":
                risk_score,

            "default_probability":
                default_probability,

            "decision":
                decision
        }

        # ------------------------
        # AI REPORT
        # ------------------------

        try:

            with st.spinner(
                "Generating AI Assessment..."
            ):

                ai_report = loan_advisor(
                    income,
                    credit_score,
                    emi,
                    """
                    Generate:

                    1. Executive Summary
                    2. Risk Analysis
                    3. Recommendation
                    4. Final Decision
                    """
                )

            st.subheader(
                "🤖 AI Loan Officer Report"
            )

            st.markdown(
                ai_report
            )

        except Exception as e:

            st.warning(
                f"Azure OpenAI not configured: {e}"
            )

        # ------------------------
        # PDF REPORT
        # ------------------------

        try:

            report_text = f"""
Loan Assessment

Income: {income}

Credit Score: {credit_score}

Existing EMI: {emi}

Requested Loan:
{requested_loan}

Risk Score:
{risk_score}

Decision:
{decision}

Default Probability:
{default_probability}%
"""

            pdf_file = "loan_report.pdf"

            create_pdf(
                pdf_file,
                report_text
            )

            with open(
                pdf_file,
                "rb"
            ) as file:

                st.download_button(
                    "📄 Download PDF Report",
                    file,
                    file_name=pdf_file,
                    mime="application/pdf"
                )

        except Exception as e:

            st.error(
                f"PDF Error: {e}"
            )

# =====================================================
# TAB 2
# =====================================================

with tab2:

    st.subheader(
        "Portfolio Analytics"
    )

    try:

        df = pd.read_csv(
            "data/customers.csv"
        )

        m1, m2, m3 = st.columns(3)

        with m1:

            st.metric(
                "Customers",
                len(df)
            )

        with m2:

            st.metric(
                "Average Income",
                f"₹{int(df['Income'].mean())}"
            )

        with m3:

            st.metric(
                "Average Credit Score",
                int(
                    df["CreditScore"].mean()
                )
            )

        fig1 = px.bar(
            df,
            x="Customer",
            y="Income",
            title="Customer Income"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

        fig2 = px.histogram(
            df,
            x="CreditScore",
            title="Credit Score Distribution"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

        st.dataframe(
            df,
            use_container_width=True
        )

    except Exception as e:

        st.warning(
            f"Dashboard Data Error: {e}"
        )

# =====================================================
# TAB 3
# =====================================================

with tab3:

    st.subheader(
        "💬 Azure OpenAI Loan Advisor"
    )

    question = st.text_input(
        "Ask a banking question"
    )

    if question:

        if "customer" not in st.session_state:

            st.warning(
                "Analyze a customer first."
            )

        else:

            data = st.session_state.customer

            try:

                with st.spinner(
                    "Generating Recommendation..."
                ):

                    response = loan_advisor(
                        data["income"],
                        data["credit_score"],
                        data["emi"],
                        question
                    )

                st.markdown(
                    response
                )

            except Exception as e:

                st.error(
                    f"Azure OpenAI Error: {e}"
                )

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.success(
        "Logged in as Banker"
    )

    if st.button(
        "Logout"
    ):

        st.session_state.logged = False

        st.rerun()
