from flask import Flask
from app.routes import routes
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
app.register_blueprint(routes)
app.config['UPLOAD_FOLDER'] = "uploaded_cvs"
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

if __name__ == "__main__":
    app.run(debug=True)
