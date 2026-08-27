def loan_advisor(
    income,
    credit_score,
    emi,
    question
):
    dti = (emi / income) * 100

    if credit_score >= 750 and dti < 30:

        decision = "APPROVED"

        recommendation = f"""
Decision: {decision}

Reasoning:
• Strong credit score ({credit_score})
• Healthy debt-to-income ratio ({dti:.1f}%)
• Good repayment capacity

Suggested Actions:
• Proceed with approval.
• Verify supporting documents.
• Offer preferential interest rates.
"""

    elif credit_score >= 700 and dti < 40:

        decision = "MANUAL REVIEW"

        recommendation = f"""
Decision: {decision}

Reasoning:
• Moderate credit profile ({credit_score})
• Debt-to-income ratio of {dti:.1f}%
• Additional assessment recommended

Suggested Actions:
• Review bank statements.
• Verify employment stability.
• Evaluate requested loan amount.
• Consider adjusted loan tenure.
"""

    else:

        decision = "REJECTED"

        recommendation = f"""
Decision: {decision}

Reasoning:
• Elevated lending risk.
• Credit score ({credit_score}) is below preferred threshold or debt obligations are high.
• Debt-to-income ratio is {dti:.1f}%.

Suggested Actions:
• Improve credit score.
• Reduce existing EMI obligations.
• Increase down payment contribution.
• Reapply after improving financial profile.
"""

    return recommendation

if "why" in question.lower():

    return recommendation

elif "improve" in question.lower():

    return """
Ways to improve approval chances:

• Reduce existing EMI commitments.
• Increase monthly income.
• Improve credit score above 750.
• Reduce requested loan amount.
"""

else:

    return recommendation
