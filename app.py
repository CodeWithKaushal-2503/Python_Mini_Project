from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Folder where uploaded files will be stored
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/", methods=["GET", "POST"])
def home():

    message = ""

    if request.method == "POST":

        file = request.files.get("file")

        if file:

            if file.filename.endswith(".csv"):

                save_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)

                file.save(save_path)

                message = "✅ File uploaded successfully!"

            else:

                message = "❌ Please upload only CSV files."

    return render_template("index.html", message=message)


if __name__ == "__main__":
    app.run(debug=True)