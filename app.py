import json
import os
from flask import Flask, render_template, request
from services.llm_analyzer import analyze_resume
from utils.pdf_parser import extract_text_from_pdf


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max file size
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')  # Required for sessions

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error_message = None

    if request.method == "POST":
        resume_text = request.form.get("resume", "").strip()
        jd_text = request.form.get("jd", "").strip()

        # Validate job description
        if not jd_text:
            error_message = "Please provide a job description."
        else:
            # If PDF is uploaded, override text
            if "resume_pdf" in request.files:
                pdf_file = request.files["resume_pdf"]
                if pdf_file and pdf_file.filename != "":
                    # Validate file extension
                    if not pdf_file.filename.lower().endswith('.pdf'):
                        error_message = "Please upload a PDF file."
                    else:
                        try:
                            # Reset file pointer to beginning
                            pdf_file.seek(0)
                            resume_text = extract_text_from_pdf(pdf_file)
                            if not resume_text.strip():
                                error_message = "Could not extract text from PDF. The file might be corrupted or image-based."
                        except Exception as e:
                            error_message = f"Error reading PDF: {str(e)}. Please try another file or paste your resume text directly."

            # Validate resume text
            if not error_message and not resume_text.strip():
                error_message = "Please provide your resume either by uploading a PDF or pasting the text."

            # Process if no errors
            if not error_message:
                try:
                    raw_output = analyze_resume(resume_text, jd_text)
                    try:
                        result = json.loads(raw_output)
                    except json.JSONDecodeError:
                        result = {
                            "error": "Failed to parse AI response",
                            "raw_output": raw_output
                        }
                except Exception as e:
                    error_message = f"Error analyzing resume: {str(e)}"

    return render_template("index.html", result=result, error_message=error_message)

if __name__ == "__main__":
    app.run(debug=True)
