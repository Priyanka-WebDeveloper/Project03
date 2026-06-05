from flask import Flask, render_template, request, redirect, url_for, send_file
from blockchain import Blockchain
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import io

app = Flask(__name__)

# ---------------- INITIALIZE BLOCKCHAIN ----------------
blockchain = Blockchain()


# ---------------- HOME ----------------
@app.route("/")
def index():
    return render_template("index.html")


# ---------------- ADD HABIT ----------------
@app.route("/add", methods=["GET", "POST"])
def add_habit():
    if request.method == "POST":
        habit = request.form.get("habit", "").strip()

        if habit:
            blockchain.add_block(habit)
            blockchain.save_chain()

        return redirect(url_for("view_chain"))

    return render_template("add.html")


# ---------------- VIEW CHAIN ----------------
@app.route("/chain")
def view_chain():
    return render_template("chain.html", blockchain=blockchain.chain)


# ---------------- DELETE BLOCK ----------------
@app.route("/delete/<int:index>", methods=["POST"])
def delete(index):
    if index != 0:  # Genesis block protect
        blockchain.delete_block(index)
        blockchain.save_chain()

    return redirect(url_for("view_chain"))


# ---------------- SEARCH ----------------
@app.route("/search", methods=["GET", "POST"])
def search():
    results = []
    query = ""

    if request.method == "POST":
        query = request.form.get("query", "").strip()

        if query:
            results = [
                block for block in blockchain.chain
                if query.lower() in block["data"].lower()
            ]

    return render_template("search.html", results=results, query=query)


# ---------------- VISUALIZE ----------------
@app.route("/visualize")
def visualize():
    is_valid = blockchain.is_chain_valid()

    return render_template(
        "visualize.html",
        chain=blockchain.chain,
        is_valid=is_valid
    )


# ---------------- EXPORT PDF ----------------
@app.route("/export")
def export_pdf():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    elements = []

    for block in blockchain.chain:
        elements.append(
            Paragraph(
                f"Block {block['index']} - {block['data']}",
                styles["Normal"]
            )
        )

    doc.build(elements)
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="blockchain.pdf",
        mimetype="application/pdf"
    )


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)