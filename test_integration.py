#!/usr/bin/env python3
"""
Test d'intégration pour vérifier la compatibilité entre les modules
"""

import sys
import traceback
from pathlib import Path

def test_imports():
    """Test l'importation de tous les modules"""
    print("=== Test des imports ===")
    
    try:
        print("[OK] Import app.py...")
        import app
        print("[OK] app.py importe avec succes")
    except Exception as e:
        print(f"[ERREUR] Erreur import app.py: {e}")
        return False
    
    try:
        print("[OK] Import scan.py...")
        import scan
        print("[OK] scan.py importe avec succes")
    except Exception as e:
        print(f"[ERREUR] Erreur import scan.py: {e}")
        return False
    
    try:
        print("[OK] Import form_filler.py...")
        import form_filler
        print("[OK] form_filler.py importe avec succes")
    except Exception as e:
        print(f"[ERREUR] Erreur import form_filler.py: {e}")
        return False
    
    try:
        print("[OK] Import generate_letter.py...")
        import generate_letter
        print("[OK] generate_letter.py importe avec succes")
    except Exception as e:
        print(f"[ERREUR] Erreur import generate_letter.py: {e}")
        return False
    
    return True

def test_function_signatures():
    """Test les signatures des fonctions principales"""
    print("\n=== Test des signatures de fonctions ===")
    
    try:
        from scan import scan_contravention, scan_permis_conduire, scan_certificat_immatriculation, scan_justificatif_domicile, validate_documents_data
        from form_filler import fill_website_form
        from generate_letter import generate_final_pdf
        
        print("[OK] Toutes les fonctions principales sont accessibles")
        
        # Test avec des données factices
        test_data = {
            "contravention": {
                "infraction": {
                    "numero_avis": "TEST123",
                    "date_heure": "01/01/2024 10:00",
                    "route": "Test Route"
                }
            },
            "certificat": {
                "vehicule": {
                    "immatriculation": "AB-123-CD",
                    "marque": "TEST"
                }
            },
            "permis": {
                "identite": {
                    "nom": "TEST",
                    "prenom": "User"
                }
            },
            "domicile": {
                "personne": {
                    "nom": "TEST",
                    "prenom": "User"
                },
                "domicile": {
                    "adresse": "123 Test Street"
                }
            }
        }
        
        # Test de validate_documents_data
        validation_result = validate_documents_data(
            contravention_data=test_data["contravention"],
            permis_data=test_data["permis"],
            certificat_data=test_data["certificat"],
            justificatif_data=test_data["domicile"]
        )
        print("[OK] validate_documents_data fonctionne")
        
        # Test de generate_final_pdf (structure de données)
        from generate_letter import LetterGenerator
        generator = LetterGenerator()
        
        # Vérifier les méthodes d'extraction
        nom_prenom = generator._extract_nom_prenom(
            test_data["permis"], 
            test_data["domicile"], 
            test_data["certificat"]
        )
        print(f"[OK] Extraction nom/prenom: {nom_prenom}")
        
        adresse = generator._extract_adresse(test_data["domicile"])
        print(f"[OK] Extraction adresse: {adresse}")
        
        return True
        
    except Exception as e:
        print(f"[ERREUR] Erreur test fonctions: {e}")
        traceback.print_exc()
        return False

def test_data_compatibility():
    """Test la compatibilité des structures de données"""
    print("\n=== Test de compatibilité des données ===")
    
    try:
        # Simuler les structures de données retournées par scan.py
        contravention_data = {
            "identité": {
                "nom": "DUPONT",
                "prenom": "Jean",
                "adresse": "123 Rue Test"
            },
            "infraction": {
                "numero_avis": "12345678901234",
                "date_heure": "15/01/2024:14h30",
                "route": "D938",
                "vitesse_maximale_autorisee": 90,
                "vitesse_mesuree": 98
            },
            "identification_vehicule": {
                "immatriculation": "AB-123-CD",
                "marque": "PEUGEOT"
            }
        }
        
        certificat_data = {
            "proprietaire": {
                "nom": "DUPONT",
                "prenom": "Jean"
            },
            "vehicule": {
                "immatriculation": "AB-123-CD",
                "marque": "PEUGEOT"
            }
        }
        
        permis_data = {
            "identite": {
                "nom": "DUPONT",
                "prenom": "Jean"
            }
        }
        
        domicile_data = {
            "personne": {
                "nom": "DUPONT",
                "prenom": "Jean"
            },
            "domicile": {
                "adresse": "123 Rue Test, 75001 Paris"
            }
        }
        
        # Test avec generate_letter
        from generate_letter import LetterGenerator
        generator = LetterGenerator()
        
        # Test HTML generation
        html_content = generator._generate_html_content(
            contravention_data, certificat_data, permis_data, domicile_data, False
        )
        
        if "DUPONT" in html_content and "AB-123-CD" in html_content:
            print("[OK] Generation HTML compatible avec les structures de donnees")
        else:
            print("[ERREUR] Probleme de compatibilite HTML")
            return False
        
        # Test LaTeX generation
        latex_content = generator._generate_latex_content(
            contravention_data, certificat_data, permis_data, domicile_data, False
        )
        
        if "DUPONT" in latex_content and "AB-123-CD" in latex_content:
            print("[OK] Generation LaTeX compatible avec les structures de donnees")
        else:
            print("[ERREUR] Probleme de compatibilite LaTeX")
            return False
        
        return True
        
    except Exception as e:
        print(f"[ERREUR] Erreur test compatibilite: {e}")
        traceback.print_exc()
        return False

def main():
    """Fonction principale des tests"""
    print("Tests d'integration et de compatibilite")
    print("=" * 50)
    
    success = True
    
    # Test 1: Imports
    if not test_imports():
        success = False
    
    # Test 2: Signatures de fonctions
    if not test_function_signatures():
        success = False
    
    # Test 3: Compatibilite des donnees
    if not test_data_compatibility():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("TOUS LES TESTS SONT PASSES!")
        print("Votre code est compatible et pret a fonctionner")
    else:
        print("DES ERREURS ONT ETE DETECTEES")
        print("Veuillez corriger les problemes signales")
        sys.exit(1)

if __name__ == "__main__":
    main()