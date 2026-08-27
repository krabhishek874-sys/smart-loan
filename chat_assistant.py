def loan_advisor(
    income,
    credit_score,
    emi,
    question
):
    return f"""
Income: {income}

Credit Score: {credit_score}

EMI: {emi}

Question:
{question}

Recommendation:
Based on the provided information, the application appears suitable for review.

Suggested Actions:
• Verify customer income documents
• Check repayment capacity
• Review existing liabilities
• Proceed with manual approval review
"""
