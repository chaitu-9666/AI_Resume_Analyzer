import spacy
from utils.skills_db import SKILLS

nlp = spacy.load("en_core_web_sm")

def extract_skills(text):
    doc = nlp(text)
    found_skills = set()

    text_lower = text.lower()

    for skill in SKILLS:
        if skill in text_lower:
            found_skills.add(skill)

    return list(found_skills)
