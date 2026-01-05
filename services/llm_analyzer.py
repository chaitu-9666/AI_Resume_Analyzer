import os
from dotenv import load_dotenv
from openai import OpenAI

from services.resume_parser import parse_resume
from services.jd_parser import parse_jd
from services.skill_extractor import extract_skills

load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analyze_resume(resume_text, jd_text):
    """
    Analyzes resume and job description using NLP + LLM
    and returns structured JSON output.
    """

    # Preprocess text
    resume_clean = parse_resume(resume_text)
    jd_clean = parse_jd(jd_text)

    # Extract skills using NLP
    resume_skills = extract_skills(resume_clean)
    jd_skills = extract_skills(jd_clean)

    # Prompt for LLM
    prompt = f"""
You are an AI recruitment assistant.

Resume Skills:
{resume_skills}

Job Description Required Skills:
{jd_skills}

Based on the skills above, return ONLY valid JSON in the following format:
{{
  "match_percentage": "",
  "skills_found": [],
  "missing_skills": [],
  "suggestions": []
}}

Rules:
- skills_found must be skills present in both resume and job description
- missing_skills must be required skills not found in resume
- match_percentage should be a number between 0 and 100
- suggestions should be short and practical
"""

    # Call OpenAI LLM
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    return response.choices[0].message.content
