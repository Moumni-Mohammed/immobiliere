from flask import Flask, render_template, request, send_file
from fpdf import FPDF
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    client = request.form['client']
    montant = request.form['montant']
    description = request.form['description']

    # Générer le fichier PDF avec FPDF
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, txt="Facture", ln=True, align='C')

    pdf.set_font('Arial', '', 12)
    pdf.cell(200, 10, txt=f"Client: {client}", ln=True)
    pdf.cell(200, 10, txt=f"Montant: {montant} ", ln=True)
    pdf.cell(200, 10, txt=f"Description: {description}", ln=True)

    # Sauvegarder le fichier PDF sur le serveur
    filename = f"facture_{client}.pdf"
    pdf.output(filename)

    # Envoyer le fichier PDF à l'utilisateur
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

