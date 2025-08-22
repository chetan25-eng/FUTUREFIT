from flask import Flask, request, render_template
import os
from backend_logic import run_scraper_logic, run_analyzer_logic

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'resume' not in request.files:
            return "Error: No resume file selected.", 400

        resume_file = request.files['resume']
        domain = request.form.get('domain')

        if resume_file.filename == '' or not domain:
            return "Error: Please upload a resume and enter a domain.", 400

        resume_filepath = os.path.join(app.config['UPLOAD_FOLDER'], "uploaded_resume.pdf")
        resume_file.save(resume_filepath)

        scraper_success = run_scraper_logic(domain)
        if not scraper_success:
            return "<h1>Error</h1><p>Could not find any jobs for the specified domain. Please try another one.</p>", 400

        jobs_csv_path = "scraped_jobs.csv"
        matched_jobs = run_analyzer_logic(resume_filepath, jobs_csv_path)

        return render_template('answers.html', matched_jobs=matched_jobs)

    return render_template('index.html')


if __name__ == '__main__':
    # In production, set debug=False
    app.run(host='0.0.0.0', port=5000, debug=True)