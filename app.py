from flask import Flask, render_template, request, send_file
import os
from datetime import datetime

from hashing import generate_hash
from blockchain import Blockchain
from database import create_table, add_evidence, get_all_evidence, total_evidence, search_case, get_hash

app = Flask(__name__)

create_table()

blockchain = Blockchain()

UPLOAD_FOLDER = "evidence"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        case_id = request.form["case_id"]
        investigator = request.form["investigator"]
        description = request.form["description"]

        file = request.files["evidence"]

        if file.filename != "":

            file_path = os.path.join(UPLOAD_FOLDER, file.filename)

            file.save(file_path)

            hash_value = generate_hash(file_path)

            blockchain.add_block(file.filename, hash_value)

            upload_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

            add_evidence(
                case_id,
                investigator,
                description,
                file.filename,
                hash_value,
                upload_time
            )

            return f"""
            <h2>Evidence Uploaded Successfully!</h2>

            <hr>

            <p><b>Case ID:</b> {case_id}</p>

            <p><b>Investigator:</b> {investigator}</p>

            <p><b>Description:</b> {description}</p>

            <p><b>Filename:</b> {file.filename}</p>

            <p><b>SHA-256 Hash:</b></p>

            <p>{hash_value}</p>

            <hr>

            <h3>Blockchain Status</h3>

            <p><b>Total Blocks:</b> {len(blockchain.chain)}</p>

            <p><b>Current Block:</b> {blockchain.chain[-1]['index']}</p>

            <br>

            <a href="/blockchain">View Blockchain</a>

            <br><br>

            <a href="/verify">Verify Evidence</a>

            <br><br>

            <a href="/">Upload Another Evidence</a>
            """

    return render_template(
        "index.html",
        total=total_evidence(),
        blocks=len(blockchain.chain)
    )

@app.route("/blockchain")
def view_blockchain():

    return render_template(
        "blockchain.html",
        blockchain=blockchain.display_chain()
    )


@app.route("/verify", methods=["GET", "POST"])
def verify():

    result = ""

    if request.method == "POST":

        case_id = request.form["case_id"]

        file = request.files["evidence"]

        if file.filename != "":

            file_path = os.path.join(UPLOAD_FOLDER, file.filename)

            file.save(file_path)

            new_hash = generate_hash(file_path)

            stored_hash = get_hash(case_id, file.filename)

            if stored_hash is None:

                result = "Case ID Not Found"

            elif stored_hash == new_hash:

                result = "Evidence Verified (Not Tampered)"

            else:

                result = "Evidence Tampered"

    return render_template("verify.html", result=result)

@app.route("/evidence")
def evidence():

    records = get_all_evidence()

    return render_template(
        "evidence.html",
        records=records
    )

@app.route("/search", methods=["GET", "POST"])
def search():

    records = []

    if request.method == "POST":

        case_id = request.form["case_id"]

        records = search_case(case_id)

    return render_template(
        "search.html",
        records=records
    )

@app.route("/download")
def download():

    return send_file(
        "blockchain.json",
        as_attachment=True
    )

if __name__ == "__main__":
    app.run(debug=True)