import spacy
from utils.skills_db import SKILLS

try:
    nlp = spacy.load("en_core_web_sm")
    SPACY_AVAILABLE = True
except OSError:
    SPACY_AVAILABLE = False
    nlp = None

def extract_skills(text):
    if SPACY_AVAILABLE and nlp is not None:
        doc = nlp(text)
    
    found_skills = set()
    text_lower = text.lower()

    for skill in SKILLS:
        if skill in text_lower:
            found_skills.add(skill)

    return list(found_skills)
