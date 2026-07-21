from flask import Flask, render_template, request, redirect, send_file
import os

from analyzer import analyze_dataset
from cleaner import clean_dataset

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

uploaded_file_path = ""


@app.route("/", methods=["GET", "POST"])
def home():

    global uploaded_file_path

    message = ""
    report = None

    if request.method == "POST":

        file = request.files.get("file")

        if file:

            if file.filename.lower().endswith(".csv"):

                os.makedirs(UPLOAD_FOLDER, exist_ok=True)

                uploaded_file_path = os.path.join(
                    UPLOAD_FOLDER,
                    file.filename
                )

                file.save(uploaded_file_path)

                message = f"✅ {file.filename} uploaded successfully!"

                report = analyze_dataset(uploaded_file_path)

            else:

                message = "❌ Please upload only CSV files."

    elif uploaded_file_path and os.path.exists(uploaded_file_path):

        report = analyze_dataset(uploaded_file_path)

    return render_template(
        "index.html",
        message=message,
        report=report
    )


# ---------------- Clean Dataset ---------------- #

@app.route("/clean")
def clean():

    global uploaded_file_path

    if uploaded_file_path and os.path.exists(uploaded_file_path):

        # Clean dataset and get new file path
        uploaded_file_path = clean_dataset(uploaded_file_path)

    return redirect("/")


# ---------------- Download Cleaned Dataset ---------------- #

@app.route("/download")
def download():

    global uploaded_file_path

    if uploaded_file_path and os.path.exists(uploaded_file_path):

        return send_file(
            uploaded_file_path,
            as_attachment=True
        )

    return "❌ No cleaned file available to download."


if __name__ == "__main__":
    app.run(debug=True)