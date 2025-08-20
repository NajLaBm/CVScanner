from sentence_transformers import util
from werkzeug.utils import secure_filename
import os

def get_top_matching_cvs(job_offer_text, files, model):
    job_embedding = model.encode(job_offer_text, convert_to_tensor=True)
    scores = []

    for file in files:
        filename = secure_filename(file.filename)
        path = os.path.join("uploaded_cvs", filename)
        file.save(path)

        from app.utils.text_extraction import extract_text_from_pdf
        cv_text = extract_text_from_pdf(path)
        cv_embedding = model.encode(cv_text, convert_to_tensor=True)
        score = util.pytorch_cos_sim(job_embedding, cv_embedding).item()
        scores.append((filename, score))

    scores = sorted(scores, key=lambda x: x[1], reverse=True)[:5]

    results = [{
        "filename": name,
        "score": round(score * 100, 2),
        "url": f"/cv/{name}"
    } for name, score in scores]

    return results
