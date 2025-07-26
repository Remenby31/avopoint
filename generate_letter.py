"""
Module amélioré de génération de lettres de contestation de contraventions
Inclut de meilleurs fallbacks et une gestion d'erreurs robuste
"""

import subprocess
import tempfile
from pathlib import Path
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class PDFGenerationError(Exception):
    """Exception personnalisée pour les erreurs de génération PDF"""
    pass

class LetterGenerator:
    """Classe principale pour générer les lettres de contestation"""
    
    def __init__(self):
        self.results_dir = Path("results")
        self.results_dir.mkdir(exist_ok=True)
        
    def generate_final_pdf(self, validated_data: dict, driver_visible: bool, task_id: str) -> str:
        """
        Génère un PDF de lettre de contestation avec fallbacks robustes
        """
        try:
            logger.info(f"Génération du PDF pour la tâche {task_id}")
            
            # Extraire les données nécessaires
            contravention_data = validated_data.get("contravention", {})
            certificat_data = validated_data.get("certificat", {})
            permis_data = validated_data.get("permis", {})
            domicile_data = validated_data.get("domicile", {})
            
            # Essayer LaTeX en premier
            if self._check_latex_availability():
                logger.info("Utilisation de LaTeX pour la génération")
                return self._generate_with_latex(
                    contravention_data, certificat_data, permis_data, 
                    domicile_data, driver_visible, task_id
                )
            
            # Fallback vers ReportLab
            if self._check_reportlab_availability():
                logger.info("Utilisation de ReportLab pour la génération")
                return self._generate_with_reportlab(
                    contravention_data, certificat_data, permis_data, 
                    domicile_data, driver_visible, task_id
                )
            
            # Fallback vers HTML/CSS
            logger.info("Utilisation du fallback HTML pour la génération")
            return self._generate_with_html(
                contravention_data, certificat_data, permis_data, 
                domicile_data, driver_visible, task_id
            )
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération du PDF: {str(e)}")
            raise PDFGenerationError(f"Impossible de générer le document: {str(e)}")

    def _generate_with_latex(self, contravention_data, certificat_data, permis_data, 
                           domicile_data, driver_visible, task_id):
        """Génération avec LaTeX (méthode originale améliorée)"""
        
        latex_content = self._generate_latex_content(
            contravention_data, certificat_data, permis_data, 
            domicile_data, driver_visible
        )
        
        return self._compile_latex_to_pdf(latex_content, task_id)

    def _extract_nom_prenom(self, permis_data, domicile_data, certificat_data):
        """Extrait nom et prénom de manière robuste depuis les données"""
        # Essayer d'abord le permis
        if permis_data and "identite" in permis_data:
            identite = permis_data["identite"]
            nom = identite.get("nom", "")
            prenom = identite.get("prenom", "")
            if nom and nom != "NONE":
                return f"{prenom} {nom}".strip()
        
        # Ensuite le domicile
        if domicile_data and "personne" in domicile_data:
            personne = domicile_data["personne"]
            nom = personne.get("nom", "")
            prenom = personne.get("prenom", "")
            if nom and nom != "NONE":
                return f"{prenom} {nom}".strip()
        
        # Enfin le certificat
        if certificat_data and "proprietaire" in certificat_data:
            proprietaire = certificat_data["proprietaire"]
            nom = proprietaire.get("nom", "")
            prenom = proprietaire.get("prenom", "")
            if nom and nom != "NONE":
                return f"{prenom} {nom}".strip()
        
        return "N/A"
    
    def _extract_adresse(self, domicile_data):
        """Extrait l'adresse depuis les données de domicile"""
        if domicile_data and "domicile" in domicile_data:
            return domicile_data["domicile"].get("adresse", "N/A")
        return "N/A"

    def _generate_with_reportlab(self, contravention_data, certificat_data, permis_data, 
                               domicile_data, driver_visible, task_id):
        """Génération avec ReportLab (améliorée)"""
        
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import cm
            from reportlab.lib import colors
            from reportlab.lib.enums import TA_CENTER, TA_RIGHT
            
            pdf_path = self.results_dir / f"contestation_{task_id}.pdf"
            
            # Configuration du document
            doc = SimpleDocTemplate(
                str(pdf_path), 
                pagesize=A4,
                leftMargin=2.5*cm, rightMargin=2.5*cm,
                topMargin=2.5*cm, bottomMargin=2.5*cm
            )
            
            styles = getSampleStyleSheet()
            
            # Styles personnalisés
            title_style = ParagraphStyle(
                'CustomTitle', 
                parent=styles['Heading1'],
                alignment=TA_CENTER, 
                spaceAfter=30,
                fontSize=16,
                textColor=colors.black
            )
            
            header_style = ParagraphStyle(
                'HeaderStyle',
                parent=styles['Normal'],
                alignment=TA_RIGHT,
                spaceAfter=12
            )
            
            bold_style = ParagraphStyle(
                'BoldStyle',
                parent=styles['Normal'],
                fontName='Helvetica-Bold',
                spaceAfter=6
            )
            
            # Construction du document
            story = []
            
            # Extraction des données avec les nouvelles méthodes robustes
            nom_prenom = self._extract_nom_prenom(permis_data, domicile_data, certificat_data)
            adresse = self._extract_adresse(domicile_data)
            
            # Extraction des autres champs nécessaires
            numero_contravention = "N/A"
            if contravention_data and "infraction" in contravention_data:
                numero_contravention = contravention_data["infraction"].get("numero_avis", "N/A")
            
            date_contravention = "N/A"
            if contravention_data and "infraction" in contravention_data:
                date_contravention = contravention_data["infraction"].get("date_heure", "N/A")
            
            lieu_contravention = "N/A"
            if contravention_data and "infraction" in contravention_data:
                lieu_contravention = contravention_data["infraction"].get("route", "N/A")
            
            immatriculation = "N/A"
            if certificat_data and "vehicule" in certificat_data:
                immatriculation = certificat_data["vehicule"].get("immatriculation", "N/A")
                
            marque_vehicule = "N/A"
            if certificat_data and "vehicule" in certificat_data:
                marque_vehicule = certificat_data["vehicule"].get("marque", "N/A")
            
            date_lettre = datetime.now().strftime("%d/%m/%Y")
            
            expediteur_text = f"""
            {nom_prenom}<br/>
            {adresse}<br/><br/>
            Le {date_lettre}
            """
            story.append(Paragraph(expediteur_text, header_style))
            story.append(Spacer(1, 1*cm))
            
            # Destinataire
            destinataire_text = """
            <b>À l'attention de :</b><br/>
            Service de Traitement des Contraventions<br/>
            Centre National de Traitement<br/>
            CS 41101<br/>
            35911 RENNES CEDEX 9
            """
            story.append(Paragraph(destinataire_text, styles['Normal']))
            story.append(Spacer(1, 1*cm))
            
            # Titre
            story.append(Paragraph("CONTESTATION DE CONTRAVENTION", title_style))
            story.append(Paragraph(f"<b>Avis de contravention n° {numero_contravention}</b>", 
                                 ParagraphStyle('SubTitle', parent=styles['Normal'], 
                                              alignment=TA_CENTER, spaceAfter=20)))
            
            # Corps de la lettre
            story.append(Paragraph("Madame, Monsieur,", styles['Normal']))
            story.append(Spacer(1, 0.5*cm))
            
            intro_text = f"""
            Je conteste par la présente l'avis de contravention mentionné en objet, 
            établi le {date_contravention} à {lieu_contravention}, concernant le véhicule 
            immatriculé {immatriculation}.
            """
            story.append(Paragraph(intro_text, styles['Normal']))
            story.append(Spacer(1, 0.5*cm))
            
            # Tableau des références
            story.append(Paragraph("<b>RÉFÉRENCES DE LA CONTRAVENTION :</b>", bold_style))
            
            # Extraction sécurisée du montant
            montant = "N/A"
            if contravention_data and "infraction" in contravention_data:
                vitesse_max = contravention_data["infraction"].get("vitesse_maximale_autorisee", 0)
                if vitesse_max and vitesse_max != "NONE":
                    # Estimation du montant selon la vitesse (simplifié)
                    if isinstance(vitesse_max, (int, float)) and vitesse_max > 0:
                        if vitesse_max <= 50:
                            montant = "135"
                        elif vitesse_max <= 90:
                            montant = "68"
                        else:
                            montant = "135"
            
            ref_data = [
                ['Numéro d\'avis :', numero_contravention],
                ['Date de l\'infraction :', date_contravention],
                ['Lieu :', lieu_contravention],
                ['Montant :', f"{montant} €"],
                ['Véhicule :', f"{marque_vehicule}"],
                ['Immatriculation :', immatriculation]
            ]
            
            ref_table = Table(ref_data, colWidths=[5*cm, 10*cm])
            ref_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            story.append(ref_table)
            story.append(Spacer(1, 0.5*cm))
            
            # Motifs de contestation
            story.append(Paragraph("<b>MOTIFS DE CONTESTATION :</b>", bold_style))
            
            motifs = self._get_motifs_text(driver_visible)
            for i, motif in enumerate(motifs, 1):
                story.append(Paragraph(f"{i}. {motif}", styles['Normal']))
                story.append(Spacer(1, 6))
            
            story.append(Spacer(1, 0.5*cm))
            
            # Conclusion
            conclusion_text = """
            En application des articles 529-2 et suivants du Code de procédure pénale, 
            je conteste formellement cette contravention et demande son annulation.
            """
            story.append(Paragraph(conclusion_text, styles['Normal']))
            story.append(Spacer(1, 0.5*cm))
            
            story.append(Paragraph(
                "Je vous prie de bien vouloir annuler cette contravention et vous remercie "
                "de l'attention que vous porterez à ma demande.", styles['Normal']
            ))
            story.append(Spacer(1, 1*cm))
            
            story.append(Paragraph(
                "Je vous prie d'agréer, Madame, Monsieur, l'expression de mes salutations distinguées.",
                styles['Normal']
            ))
            story.append(Spacer(1, 2*cm))
            
            # Signature
            signature_text = f"{nom_prenom}<br/><i>Signature</i>"
            story.append(Paragraph(signature_text, header_style))
            story.append(Spacer(1, 1*cm))
            
            # Pièces jointes
            story.append(Paragraph("<b>Pièces jointes :</b>", bold_style))
            pieces_jointes = [
                "Copie de l'avis de contravention",
                "Copie du certificat d'immatriculation",
                "Copie du permis de conduire",
                "Copie du justificatif de domicile",
                "Photo du contrôle radar (si applicable)"
            ]
            
            for piece in pieces_jointes:
                story.append(Paragraph(f"• {piece}", styles['Normal']))
            
            # Génération du PDF
            doc.build(story)
            logger.info(f"PDF généré avec ReportLab: {pdf_path}")
            return str(pdf_path)
            
        except Exception as e:
            logger.error(f"Erreur avec ReportLab: {str(e)}")
            raise

    def _generate_with_html(self, contravention_data, certificat_data, permis_data, 
                          domicile_data, driver_visible, task_id):
        """Génération avec HTML/CSS comme dernier fallback"""
        
        html_content = self._generate_html_content(
            contravention_data, certificat_data, permis_data, 
            domicile_data, driver_visible
        )
        
        html_path = self.results_dir / f"contestation_{task_id}.html"
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"Document HTML généré: {html_path}")
        return str(html_path)

    def _generate_html_content(self, contravention_data, certificat_data, permis_data, 
                             domicile_data, driver_visible):
        """Génère le contenu HTML de la lettre"""
        
        # Extraction robuste des données
        nom_prenom = self._extract_nom_prenom(permis_data, domicile_data, certificat_data)
        adresse = self._extract_adresse(domicile_data)
        
        numero_contravention = "N/A"
        if contravention_data and "infraction" in contravention_data:
            numero_contravention = contravention_data["infraction"].get("numero_avis", "N/A")
        
        date_contravention = "N/A"
        if contravention_data and "infraction" in contravention_data:
            date_contravention = contravention_data["infraction"].get("date_heure", "N/A")
        
        lieu_contravention = "N/A"
        if contravention_data and "infraction" in contravention_data:
            lieu_contravention = contravention_data["infraction"].get("route", "N/A")
        
        immatriculation = "N/A"
        if certificat_data and "vehicule" in certificat_data:
            immatriculation = certificat_data["vehicule"].get("immatriculation", "N/A")
            
        marque_vehicule = "N/A"
        if certificat_data and "vehicule" in certificat_data:
            marque_vehicule = certificat_data["vehicule"].get("marque", "N/A")
        
        # Estimation du montant
        montant = "N/A"
        if contravention_data and "infraction" in contravention_data:
            vitesse_max = contravention_data["infraction"].get("vitesse_maximale_autorisee", 0)
            if vitesse_max and vitesse_max != "NONE":
                if isinstance(vitesse_max, (int, float)) and vitesse_max > 0:
                    if vitesse_max <= 50:
                        montant = "135"
                    elif vitesse_max <= 90:
                        montant = "68"
                    else:
                        montant = "135"
        
        date_lettre = datetime.now().strftime("%d/%m/%Y")
        
        motifs = self._get_motifs_html(driver_visible)
        
        html_content = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contestation de Contravention</title>
    <style>
        @media print {{
            body {{ margin: 0; }}
            .page-break {{ page-break-before: always; }}
        }}
        
        body {{
            font-family: 'Times New Roman', serif;
            font-size: 12pt;
            line-height: 1.6;
            max-width: 21cm;
            margin: 2.5cm auto;
            padding: 0 2.5cm;
            color: #000;
        }}
        
        .header {{
            text-align: right;
            margin-bottom: 2cm;
        }}
        
        .destinataire {{
            margin-bottom: 2cm;
        }}
        
        .titre {{
            text-align: center;
            font-weight: bold;
            font-size: 14pt;
            margin: 2cm 0;
        }}
        
        .references {{
            margin: 1cm 0;
        }}
        
        .references table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        .references td:first-child {{
            font-weight: bold;
            width: 30%;
            padding: 3px 0;
        }}
        
        .motifs {{
            margin: 1cm 0;
        }}
        
        .motifs ol {{
            padding-left: 1.5cm;
        }}
        
        .motifs li {{
            margin-bottom: 0.5cm;
            text-align: justify;
        }}
        
        .signature {{
            text-align: right;
            margin-top: 3cm;
        }}
        
        .pieces-jointes {{
            margin-top: 2cm;
        }}
        
        .pieces-jointes ul {{
            padding-left: 1cm;
        }}
        
        .bold {{
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="header">
        {nom_prenom}<br>
        {adresse}<br><br>
        Le {date_lettre}
    </div>
    
    <div class="destinataire">
        <strong>À l'attention de :</strong><br>
        Service de Traitement des Contraventions<br>
        Centre National de Traitement<br>
        CS 41101<br>
        35911 RENNES CEDEX 9
    </div>
    
    <div class="titre">
        CONTESTATION DE CONTRAVENTION<br>
        <strong>Avis de contravention n° {numero_contravention}</strong>
    </div>
    
    <p>Madame, Monsieur,</p>
    
    <p>Je conteste par la présente l'avis de contravention mentionné en objet, établi le {date_contravention} à {lieu_contravention}, concernant le véhicule immatriculé {immatriculation}.</p>
    
    <div class="references">
        <p class="bold">RÉFÉRENCES DE LA CONTRAVENTION :</p>
        <table>
            <tr><td>Numéro d'avis :</td><td>{numero_contravention}</td></tr>
            <tr><td>Date de l'infraction :</td><td>{date_contravention}</td></tr>
            <tr><td>Lieu :</td><td>{lieu_contravention}</td></tr>
            <tr><td>Montant :</td><td>{montant} €</td></tr>
            <tr><td>Véhicule :</td><td>{marque_vehicule}</td></tr>
            <tr><td>Immatriculation :</td><td>{immatriculation}</td></tr>
        </table>
    </div>
    
    <div class="motifs">
        <p class="bold">MOTIFS DE CONTESTATION :</p>
        {motifs}
    </div>
    
    <p>En application des articles 529-2 et suivants du Code de procédure pénale, je conteste formellement cette contravention et demande son annulation.</p>
    
    <p>Je vous prie de bien vouloir annuler cette contravention et vous remercie de l'attention que vous porterez à ma demande.</p>
    
    <p>Je vous prie d'agréer, Madame, Monsieur, l'expression de mes salutations distinguées.</p>
    
    <div class="signature">
        {nom_prenom}<br>
        <em>Signature</em>
    </div>
    
    <div class="pieces-jointes">
        <p class="bold">Pièces jointes :</p>
        <ul>
            <li>Copie de l'avis de contravention</li>
            <li>Copie du certificat d'immatriculation</li>
            <li>Copie du permis de conduire</li>
            <li>Copie du justificatif de domicile</li>
            <li>Photo du contrôle radar (si applicable)</li>
        </ul>
    </div>
</body>
</html>
        """
        
        return html_content

    def _get_motifs_text(self, driver_visible):
        """Retourne les motifs de contestation sous forme de liste"""
        if driver_visible:
            return [
                "<b>Défaut de signalisation :</b> La signalisation du contrôle radar n'était pas conforme aux dispositions réglementaires en vigueur.",
                "<b>Conditions de circulation :</b> Les conditions de circulation au moment des faits ne permettaient pas le respect de la limitation de vitesse en toute sécurité.",
                "<b>Calibrage de l'appareil :</b> Je conteste la fiabilité de l'appareil de contrôle et demande la production du certificat de vérification périodique.",
                "<b>Erreur sur la personne :</b> Je n'étais pas le conducteur du véhicule au moment des faits reprochés.",
                "<b>Vice de procédure :</b> La procédure de constatation de l'infraction présente des irrégularités substantielles."
            ]
        else:
            return [
                "<b>Impossibilité d'identification du conducteur :</b> La photographie jointe à l'avis de contravention ne permet pas d'identifier clairement le conducteur du véhicule au moment des faits.",
                "<b>Défaut de preuve :</b> En application de l'article 529-2 du Code de procédure pénale, l'administration doit apporter la preuve de l'infraction. La photo fournie ne constitue pas une preuve suffisante de mon implication personnelle.",
                "<b>Principe de la présomption d'innocence :</b> Conformément à l'article 9 de la Déclaration des droits de l'homme et du citoyen, toute personne est présumée innocente jusqu'à ce que sa culpabilité soit établie.",
                "<b>Qualité de la photographie :</b> La qualité de l'image ne permet pas une identification formelle et certaine du conducteur, rendant impossible l'établissement de ma responsabilité.",
                "<b>Usage possible du véhicule par un tiers :</b> Le véhicule aurait pu être utilisé par une tierce personne autorisée au moment des faits reprochés."
            ]

    def _get_motifs_html(self, driver_visible):
        """Retourne les motifs formatés en HTML"""
        motifs_list = self._get_motifs_text(driver_visible)
        html_motifs = "<ol>"
        for motif in motifs_list:
            html_motifs += f"<li>{motif}</li>"
        html_motifs += "</ol>"
        return html_motifs

    def _generate_latex_content(self, contravention_data, certificat_data, permis_data, domicile_data, driver_visible):
        """Génération du contenu LaTeX pour la lettre"""
        
        # Extraction robuste des données
        nom_prenom = self._extract_nom_prenom(permis_data, domicile_data, certificat_data)
        adresse = self._extract_adresse(domicile_data)
        
        numero_contravention = "N/A"
        if contravention_data and "infraction" in contravention_data:
            numero_contravention = contravention_data["infraction"].get("numero_avis", "N/A")
        
        date_contravention = "N/A"
        if contravention_data and "infraction" in contravention_data:
            date_contravention = contravention_data["infraction"].get("date_heure", "N/A")
        
        lieu_contravention = "N/A"
        if contravention_data and "infraction" in contravention_data:
            lieu_contravention = contravention_data["infraction"].get("route", "N/A")
        
        immatriculation = "N/A"
        if certificat_data and "vehicule" in certificat_data:
            immatriculation = certificat_data["vehicule"].get("immatriculation", "N/A")
            
        marque_vehicule = "N/A"
        if certificat_data and "vehicule" in certificat_data:
            marque_vehicule = certificat_data["vehicule"].get("marque", "N/A")
        
        # Génération du contenu LaTeX avec la mise en forme professionnelle
        latex_content = f"""\\documentclass[12pt,a4paper]{{article}}
% Encodage et langue
\\usepackage[utf8]{{inputenc}}
\\usepackage[T1]{{fontenc}}
\\usepackage[french]{{babel}}
% Mise en page
\\usepackage[a4paper,top=2.5cm,bottom=2.5cm,left=2.5cm,right=2.5cm]{{geometry}}
\\usepackage{{setspace}}
\\setstretch{{1.3}} % Interligne principal
% Police Times New Roman
\\usepackage{{newtxtext,newtxmath}}
% Suppression de l'indentation et justification
\\setlength{{\\parindent}}{{0pt}}
\\setlength{{\\parskip}}{{0.6em}} % Espace entre paragraphes
\\usepackage{{ragged2e}}
\\justifying
% Date automatique au format français personnalisé
\\usepackage[french]{{datetime2}}
\\renewcommand{{\\DTMdisplaydate}}[4]{{\\number##3~\\DTMfrenchmonthname{{##2}}~##1}}
% Gestion des images
\\usepackage{{graphicx}}
% --- Variables client ---
\\newcommand{{\\nomclient}}{{{nom_prenom}}}
\\newcommand{{\\adresseclient}}{{{adresse}}}
\\newcommand{{\\numcontravention}}{{{numero_contravention}}}
\\newcommand{{\\dateinfraction}}{{{date_contravention}}}
% --- Variables avocat ---
\\newcommand{{\\nomavocat}}{{Maître Yoann LEROUGE}}
\\newcommand{{\\signaturefile}}{{signature.png}} % Nom du fichier image de signature
% --- Variables destinataire ---
\\newcommand{{\\adresseofficier}}{{CONTESTATION VITESSE\\\\CS41101\\\\35911 RENNES CEDEX 9}}
% ----------------------------
\\begin{{document}}
% En-tête avocat
\\noindent
\\textbf{{\\nomavocat}} \\\\
Cabinet YSL \\\\
74 rue du Faubourg Saint-Denis \\\\
75010 PARIS
\\vspace{{0.6cm}}
% Bloc destinataire + date dans un seul bloc décalé de 10 cm
\\noindent

\\hspace*{{10cm}}%
\\begin{{minipage}}{{7cm}}
\\textbf{{L'Officier du Ministère Public}} \\\\
\\normalsize \\adresseofficier \\\\
\\vspace{{0.4cm}} \\\\
\\textbf{{Paris,}} le \\DTMdisplaydate{{\\year}}{{\\month}}{{\\day}}{{-1}}
\\end{{minipage}}
\\vspace{{0.6cm}}
% Objet
\\noindent
\\textbf{{Objet : Contestation d'un procès-verbal pour excès de vitesse}} \\\\
\\vspace{{0.15cm}}
\\textit{{Avis de contravention n° \\numcontravention}} \\\\[0.3cm]
Madame, Monsieur l'Officier du Ministère Public, \\\\
En qualité de représentant de \\nomclient, domicilié au \\adresseclient, j'ai été mandaté pour
contester l'avis de contravention n° \\numcontravention \\ reçu en date du \\dateinfraction,
concernant un excès de vitesse supposé commis à cette occasion.
En tant que propriétaire du véhicule responsable de l'infraction, mon client a été présumé en
être le conducteur au moment des faits. Toutefois, mon client conteste être le conducteur au
moment de la réalisation de l'infraction. De plus, la photographie prise (ci-jointe) ne permet pas
d'identifier le conducteur.
En conséquence, je sollicite l'annulation de ce procès-verbal pour les raisons évoquées.
Dans l'attente de votre retour, je vous remercie pour l'examen attentif de la demande.
\\vspace{{1.2cm}}
% Bloc nom avocat + signature décalé de 10 cm
\\noindent
\\hspace*{{10cm}}%
\\begin{{minipage}}{{7cm}}
\\textbf{{\\nomavocat}} \\\\
% Note: Si signature.png n'existe pas, cette ligne sera ignorée
% \\includegraphics[width=2.5cm]{{\\signaturefile}} % Taille de la signature réduite
\\end{{minipage}}
\\end{{document}}"""
        
        return latex_content

    def _get_motifs_latex(self, driver_visible):
        """Retourne les motifs formatés pour LaTeX"""
        if driver_visible:
            return [
                "Défaut de signalisation : La signalisation du contrôle radar n'était pas conforme aux dispositions réglementaires.",
                "Conditions de circulation : Les conditions ne permettaient pas le respect de la limitation en sécurité.",
                "Calibrage de l'appareil : Je conteste la fiabilité de l'appareil de contrôle.",
                "Erreur sur la personne : Je n'étais pas le conducteur au moment des faits.",
                "Vice de procédure : La procédure présente des irrégularités substantielles."
            ]
        else:
            return [
                "Impossibilité d'identification du conducteur : La photographie ne permet pas d'identifier clairement le conducteur.",
                "Défaut de preuve : L'administration doit apporter la preuve de l'infraction selon l'article 529-2 du Code de procédure pénale.",
                "Principe de présomption d'innocence : Toute personne est présumée innocente jusqu'à établissement de sa culpabilité.",
                "Qualité de la photographie : La qualité ne permet pas une identification formelle et certaine.",
                "Usage possible par un tiers : Le véhicule aurait pu être utilisé par une tierce personne autorisée."
            ]

    def _compile_latex_to_pdf(self, latex_content, task_id):
        """Compilation du LaTeX en PDF"""
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Créer le fichier .tex
            tex_file = Path(temp_dir) / f"contestation_{task_id}.tex"
            
            with open(tex_file, 'w', encoding='utf-8') as f:
                f.write(latex_content)
            
            # Compiler avec pdflatex
            try:
                result = subprocess.run([
                    'pdflatex', 
                    '-output-directory', temp_dir,
                    '-interaction=nonstopmode',
                    str(tex_file)
                ], capture_output=True, text=True, timeout=30)
                
                if result.returncode != 0:
                    raise Exception(f"Erreur de compilation LaTeX: {result.stderr}")
                
                # Copier le PDF vers le répertoire de résultats
                pdf_source = Path(temp_dir) / f"contestation_{task_id}.pdf"
                pdf_destination = self.results_dir / f"contestation_{task_id}.pdf"
                
                if pdf_source.exists():
                    import shutil
                    shutil.copy2(pdf_source, pdf_destination)
                    logger.info(f"PDF généré avec LaTeX: {pdf_destination}")
                    return str(pdf_destination)
                else:
                    raise Exception("Le fichier PDF n'a pas été généré")
                    
            except subprocess.TimeoutExpired:
                raise Exception("Timeout lors de la compilation LaTeX")
            except FileNotFoundError:
                raise Exception("pdflatex non trouvé sur le système")

    def _check_latex_availability(self):
        """Vérifie si pdflatex est disponible"""
        try:
            result = subprocess.run(['pdflatex', '--version'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False

    def _check_reportlab_availability(self):
        """Vérifie si ReportLab est disponible"""
        try:
            from reportlab.lib.pagesizes import A4
            return True
        except ImportError:
            return False


# Usage simplifié
def generate_final_pdf(validated_data: dict, driver_visible: bool, task_id: str) -> str:
    """Interface simplifiée pour compatibilité avec le code existant"""
    generator = LetterGenerator()
    return generator.generate_final_pdf(validated_data, driver_visible, task_id)


if __name__ == "__main__":
    # Test de la fonction
    test_data = {
        "contravention": {
            "numero": "12345678901234",
            "date": "15/01/2024",
            "lieu": "Avenue des Champs-Élysées, Paris",
            "montant": "135"
        },
        "certificat": {
            "immatriculation": "AB-123-CD",
            "marque": "Peugeot",
            "modele": "308"
        },
        "permis": {
            "nom_prenom": "Jean DUPONT"
        },
        "domicile": {
            "adresse": "123 Rue de la République",
            "code_postal": "75001",
            "ville": "Paris"
        }
    }
    
    try:
        generator = LetterGenerator()
        pdf_path = generator.generate_final_pdf(test_data, False, "test_task")
        print(f"Document généré avec succès: {pdf_path}")
        
        # Afficher les capacités disponibles
        print("\nCapacités disponibles:")
        print(f"- LaTeX: {'✓' if generator._check_latex_availability() else '✗'}")
        print(f"- ReportLab: {'✓' if generator._check_reportlab_availability() else '✗'}")
        print("- HTML: ✓")
        
    except Exception as e:
        print(f"Erreur: {e}")