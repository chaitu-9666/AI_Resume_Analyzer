from utils.text_cleaner import clean_text

def parse_jd(jd_text):
    cleaned_jd = clean_text(jd_text)
    return cleaned_jd
