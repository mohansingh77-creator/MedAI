# ==========================================================
# Calculate Overall Health Score
# ==========================================================

def calculate_health_score(lab_findings):

    score = 100

    # lab_findings is now a dictionary
    for finding in lab_findings.values():

        status = finding.get("status")

        if status == "High":
            score -= 10

        elif status == "Low":
            score -= 10

    # Prevent negative score
    score = max(score, 0)

    return score