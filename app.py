import pdfplumber
from flask import Flask, render_template, request, url_for

app = Flask(__name__)

# Config: Path to your resume PDF (placed in /static folder)
RESUME_PATH = "static/Abhishek_CKAD.pdf"

def extract_resume_text(path):
    try:
        with pdfplumber.open(path) as pdf:
            return " ".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    except Exception:
        return "Error: Resume PDF not found or unreadable."

# Pre-load text for fast searching
RESUME_TEXT = extract_resume_text(RESUME_PATH)

@app.route('/resume', methods=['GET'])
def index():
    query = request.args.get('q', '').strip()
    results = []
    
    if query:
        # Find sentences or lines containing the search term
        lines = RESUME_TEXT.split('\n')
        results = [line.strip() for line in lines if query.lower() in line.lower()]

    return render_template('index.html', query=query, results=results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)