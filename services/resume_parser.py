from utils.text_cleaner import clean_text

def parse_resume(resume_text):
    cleaned_resume = clean_text(resume_text)
    return cleaned_resume
