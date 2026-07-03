import re
import pandas as pd
import google.generativeai as genai
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"

# =========================
# 1. Read Resume Text
# =========================
def clean_text(text: str) -> str:
    """
    Basic text cleaning for resume / JD text.
    """
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9+#.\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# =========================
# 2. Extract Skills
# =========================
def extract_skills(text: str, skill_list: list) -> list:
    """
    Extract skills present in the text using a predefined skill list.
    """
    text = clean_text(text)
    found_skills = []

    for skill in skill_list:
        skill_clean = skill.lower().strip()
        # word boundary for cleaner matching
        pattern = rf"\b{re.escape(skill_clean)}\b"
        if re.search(pattern, text):
            found_skills.append(skill)

    return sorted(list(set(found_skills)))


# =========================
# 3. Extract Experience (simple rule-based)
# =========================
def extract_experience_years(text: str) -> int:
    """
    Tries to detect years of experience from resume text.
    Example matches:
    - 2 years
    - 3+ years
    - 1 year of experience
    """
    text = text.lower()

    patterns = [
        r"(\d+)\+?\s+years",
        r"(\d+)\+?\s+year",
    ]

    years_found = []

    for pattern in patterns:
        matches = re.findall(pattern, text)
        for m in matches:
            try:
                years_found.append(int(m))
            except:
                pass

    if years_found:
        return max(years_found)

    return 0


# =========================
# 4. Extract Education Level
# =========================
def extract_education_level(text: str) -> str:
    """
    Simple rule-based education extraction.
    """
    text = text.lower()

    if "phd" in text or "doctorate" in text:
        return "PhD"
    elif "master" in text or "m.tech" in text or "mtech" in text or "mba" in text:
        return "Master's"
    elif "bachelor" in text or "b.tech" in text or "btech" in text or "b.e" in text or "be " in text:
        return "Bachelor's"
    elif "diploma" in text:
        return "Diploma"
    else:
        return "Unknown"


# =========================
# 5. Parse Job Description Requirements
# =========================
def parse_job_description_requirements(job_description: str):
    """
    Extract basic JD requirements:
    - required skills
    - required experience
    - required education
    """
    jd_text = job_description.lower()

    required_experience = extract_experience_years(jd_text)
    required_education = extract_education_level(jd_text)

    return required_experience, required_education


# =========================
# 6. Candidate Scoring
# =========================
def score_candidate(
    resume_text: str,
    job_description: str,
    skill_list: list
):
    """
    Returns a dictionary with:
    - matched skills
    - missing skills
    - skill match score
    - experience match score
    - education match score
    - overall match score
    """

    # Resume parsing
    resume_skills = extract_skills(resume_text, skill_list)
    resume_experience = extract_experience_years(resume_text)
    resume_education = extract_education_level(resume_text)

    # JD parsing
    jd_skills = extract_skills(job_description, skill_list)
    jd_experience, jd_education = parse_job_description_requirements(job_description)

    # Skill matching
    matched_skills = list(set(resume_skills) & set(jd_skills))
    missing_skills = list(set(jd_skills) - set(resume_skills))

    if len(jd_skills) > 0:
        skill_match_score = round((len(matched_skills) / len(jd_skills)) * 100, 2)
    else:
        skill_match_score = 0.0

    # Experience scoring
    if jd_experience == 0:
        experience_match_score = 100.0
    else:
        experience_match_score = round(min(resume_experience / jd_experience, 1.0) * 100, 2)

    # Education scoring
    education_rank = {
        "Unknown": 0,
        "Diploma": 1,
        "Bachelor's": 2,
        "Master's": 3,
        "PhD": 4
    }

    resume_edu_rank = education_rank.get(resume_education, 0)
    jd_edu_rank = education_rank.get(jd_education, 0)

    if jd_edu_rank == 0:
        education_match_score = 100.0
    elif resume_edu_rank >= jd_edu_rank:
        education_match_score = 100.0
    else:
        education_match_score = round((resume_edu_rank / jd_edu_rank) * 100, 2)

    # Overall score (weighted)
    overall_match_score = round(
        (0.5 * skill_match_score) +
        (0.25 * experience_match_score) +
        (0.25 * education_match_score),
        2
    )

    result = {
        "Skill Match Score": skill_match_score,
        "Experience Match Score": experience_match_score,
        "Education Match Score": education_match_score,
        "Overall Match Score": overall_match_score,
        "Matched Skills": ", ".join(sorted(matched_skills)) if matched_skills else "None",
        "Missing Skills": ", ".join(sorted(missing_skills)) if missing_skills else "None",
        "Candidate Experience": resume_experience,
        "Candidate Education": resume_education,
        "Resume Skills": resume_skills,
        "JD Skills": jd_skills
    }

    return result


# =========================
# 7. Convert score result to DataFrame
# =========================
def build_candidate_score_dataframe(score_result: dict) -> pd.DataFrame:
    """
    Converts score dictionary into a single-row dataframe
    compatible with your dashboard.
    """
    df = pd.DataFrame([{
        "Skill Match Score": score_result["Skill Match Score"],
        "Experience Match Score": score_result["Experience Match Score"],
        "Education Match Score": score_result["Education Match Score"],
        "Overall Match Score": score_result["Overall Match Score"],
        "Matched Skills": score_result["Matched Skills"],
        "Missing Skills": score_result["Missing Skills"],
        "Candidate Experience": score_result["Candidate Experience"],
        "Candidate Education": score_result["Candidate Education"],
    }])
    return df


# =========================
# 8. Generate AI Candidate Report
# =========================
def generate_candidate_report(
    candidate_name: str,
    resume_text: str,
    job_description: str,
    score_result: dict,
    model=None
) -> str:
    """
    Generates an AI recruiter report using Gemini if model is passed.
    If no model is passed, returns a rule-based report.
    """

    matched_skills = score_result["Matched Skills"]
    missing_skills = score_result["Missing Skills"]
    overall_score = score_result["Overall Match Score"]
    exp_score = score_result["Experience Match Score"]
    edu_score = score_result["Education Match Score"]
    skill_score = score_result["Skill Match Score"]
    candidate_experience = score_result["Candidate Experience"]
    candidate_education = score_result["Candidate Education"]

    # If Gemini model is available
    if model is not None:
        prompt = f"""
You are a Senior HR Recruiter.

Create a professional recruiter evaluation report for this candidate.

Candidate Name: {candidate_name}

Job Description:
{job_description}

Resume:
{resume_text}

Candidate Evaluation Scores:
- Skill Match Score: {skill_score}
- Experience Match Score: {exp_score}
- Education Match Score: {edu_score}
- Overall Match Score: {overall_score}
- Matched Skills: {matched_skills}
- Missing Skills: {missing_skills}
- Candidate Experience: {candidate_experience} years
- Candidate Education: {candidate_education}

Write a structured recruiter report with:
1. Candidate Summary
2. Strengths
3. Gaps / Concerns
4. Hiring Recommendation
5. Suggested Next Steps

Keep it professional and concise.
"""
        response = model.generate_content(prompt)
        return response.text

    # Fallback rule-based report
    report = f"""
## Recruiter Report: {candidate_name}

### 1. Candidate Summary
The candidate has an overall match score of **{overall_score}%** for the target role.

### 2. Strengths
- Matched Skills: {matched_skills}
- Education Level: {candidate_education}
- Experience Detected: {candidate_experience} years

### 3. Gaps / Concerns
- Missing Skills: {missing_skills}
- Experience Match Score: {exp_score}%
- Education Match Score: {edu_score}%

### 4. Hiring Recommendation
Based on the current screening, the candidate shows a **{overall_score}%** overall fit for the role.

### 5. Suggested Next Steps
- Validate technical depth in the matched skill areas.
- Check whether missing skills can be learned quickly.
- Use interview rounds to assess project experience and role readiness.
"""
    return report