"""from flask import Flask, render_template, request, send_file
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
""" 
from flask import Flask, render_template, request, send_file
from fpdf import FPDF
import os
import tempfile
from datetime import datetime  # Importer la bibliothèque pour la date

app = Flask(__name__)

class PDF(FPDF):
    def header(self):
        # Logo
        self.image('static/images/logo-immob.jpg', 10, 8, 33)  # Assurez-vous d'avoir un fichier logo.png
        
        # Informations sur l'émetteur (Med-Immobilier)
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Med-Immobilier', 0, 1, 'R')  # Nom de l'émetteur
        self.cell(0, 10, 'Adresse: 2 Mars Casablanca', 0, 1, 'R')  # Adresse
        self.cell(0, 10, 'Téléphone: 0611223344', 0, 1, 'R')  # Numéro de téléphone
        self.ln(20)  # Ajouter un espace après l'en-tête
        
    def footer(self):
        # Positionnement à 1.5 cm du bas
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    client = request.form['client']
    produit = request.form['produit']
    quantite = request.form['quantite']  # Récupérer la quantité
    montant = request.form['montant']
    description = request.form['description']

    # Vérifier que tous les champs sont remplis
    if not client or not produit or not montant or not description:
        return "Veuillez remplir tous les champs", 400

  # Obtenir la date et l'heure actuelles
    now = datetime.now()
    date_str = now.strftime("%d/%m/%Y %H:%M:%S")  # Format de la date (jour/mois/année heure:minute:seconde)


    # Créer un PDF
    pdf = PDF()
    pdf.add_page()

    # Ajouter le titre
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, "Facture", ln=True, align='C')
    pdf.ln(10)  # Ajoute un espace

# Ajouter la date de génération de la facture
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f"Date: {date_str}", ln=True)  # Affiche la date et l'heure

    # Informations sur le client
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f"Client: {client}", ln=True)
    pdf.cell(0, 10, f"Produit: {produit}", ln=True)
    pdf.cell(0, 10, f"Quantité: {quantite}", ln=True)  # Afficher la quantité
    pdf.cell(0, 10, f"Montant: {montant} DH", ln=True)
    pdf.cell(0, 10, f"Description: {description}", ln=True)
    pdf.ln(10)

    # Ajouter un tableau (si nécessaire)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(40, 10, 'Produit', 1)
    pdf.cell(40, 10, 'Montant (DH)', 1)
    pdf.cell(0, 10, '', 0, 1)  # Ligne vide

    # Ajoute les détails de la facture
    pdf.set_font('Arial', '', 12)
    pdf.cell(40, 10, produit, 1)
    pdf.cell(40, 10, quantite, 1)  # Ajouter la quantité dans le tableau
    pdf.cell(40, 10, montant, 1)
    pdf.cell(0, 10, '', 0, 1)  # Ligne vide

    # Total
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(40, 10, 'Total:', 0)
    pdf.cell(40, 10, f"{montant} DH", 0)
    
    # Sauvegarder le fichier PDF sur le serveur
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp:
        pdf.output(temp.name)
        filename = temp.name

    return send_file(filename, as_attachment=True, download_name=f"facture_{client}.pdf")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
