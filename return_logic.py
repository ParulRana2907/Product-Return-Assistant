def check_eligibility(days, unused):
    return days <= 7 and unused == "Yes"


def fraud_score(reason, attempts, trust_level):
    score = 10

    # High-risk reasons
    if reason in ["Damaged", "Wrong Item", "Empty Box"]:
        score += 35

    # Multiple attempts
    if attempts > 1:
        score += 25

    # Trust level impact
    if trust_level == "Low":
        score += 20
    elif trust_level == "High":
        score -= 10

    return min(score, 100)


def satisfaction_score(fraud):
    if fraud < 40:
        return 92
    elif fraud < 70:
        return 80
    return 65


def refund_status(eligible, fraud):
    if eligible and fraud < 70:
        return "Approved"
    elif fraud >= 70:
        return "Manual Review"
    return "Rejected"

