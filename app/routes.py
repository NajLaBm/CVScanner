from flask import Blueprint, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
import os
from app.utils.text_extraction import extract_text_from_pdf
from app.utils.similarity import get_top_matching_cvs
from sentence_transformers import SentenceTransformer

routes = Blueprint('routes', __name__)
model = SentenceTransformer('distiluse-base-multilingual-cased-v2')
UPLOAD_FOLDER = "uploaded_cvs"

@routes.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        job_offer_text = request.form.get("job_offer", "")
        files = request.files.getlist("cv_files")

        if job_offer_text and files:
            results = get_top_matching_cvs(job_offer_text, files, model)
    return render_template("index.html", results=results)

@routes.route("/cv/<filename>")
def get_cv(filename):
    return send_from_directory("uploaded_cvs", filename)

@routes.route("/details/<filename>")
def show_details(filename):
    score = request.args.get("score")
    if score is None:
        return "Score manquant", 400
    return render_template("details.html", filename=filename, score=score)
