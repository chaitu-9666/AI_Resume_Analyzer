import json
from flask import Flask, render_template, request
from services.llm_analyzer import analyze_resume
from utils.pdf_parser import extract_text_from_pdf


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        resume_text = request.form.get("resume", "").strip()

        # If PDF is uploaded, override text
        if "resume_pdf" in request.files:
            pdf_file = request.files["resume_pdf"]
            if pdf_file.filename != "":
                resume_text = extract_text_from_pdf(pdf_file)
        jd_text = request.form["jd"]

        raw_output = analyze_resume(resume_text, jd_text)

        try:
            result = json.loads(raw_output)
        except Exception:
            result = {
                "error": "Failed to parse AI response",
                "raw_output": raw_output
            }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
