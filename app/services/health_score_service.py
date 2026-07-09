def calculate_health_score(lab_findings):

    score = 100

    for finding in lab_findings:

        if finding["status"] == "High":
            score -= 10

        elif finding["status"] == "Low":
            score -= 10

    if score < 0:
        score = 0

    return score