import anthropic
import dotenv
import base64
import json
from datetime import datetime
import re

dotenv.load_dotenv()

client = anthropic.Anthropic()

def scan_contravention(file_path):
    """
    Extract structured data from a French traffic violation notice (avis de contravention).
    
    Args:
        file_path (str): Path to the image or PDF file
    
    Returns:
        dict: Structured data extracted from the traffic violation notice
    
    Raises:
        Exception: If there's an error with the API call or data extraction
    """
    try:
        # Convert file to base64 and get media type
        file_data = file_to_base64(file_path)
        image_base64 = file_data["base64_data"]
        media_type = file_data["media_type"]
        
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": image_base64,
                            },
                        },
                        {
                            "type": "text",
                            "text": """Analyse cette image d'avis de contravention français et extrais les informations suivantes au format JSON strict. Si une information n'est pas disponible, utilise "NONE".

Structure JSON attendue:
{
  "identité": {
    "nom": "nom de la personne verbalisée",
    "prenom": "prénom de la personne verbalisée",
    "adresse": "adresse de la personne verbalisée (ex:)"
  },
  "infraction": {
    "numero_avis": "numéro de l'avis de contravention",
    "date_heure": "date et heure de l'infraction (format exact trouvé)",
    "format_date": "DD/MM/YYYY:HHhMM",
    "route": "nom de la route (ex: D938, A10, etc.)",
    "exces_vitesse_kmh": nombre (vitesse mesurée - vitesse autorisée),
    "vitesse_maximale_autorisee": nombre,
    "vitesse_mesuree": nombre
  },
  "identification_vehicule": {
    "immatriculation": "numéro d'immatriculation",
    "pays": "pays d'immatriculation",
    "marque": "marque du véhicule"
  },
  "appareil_controle": {
    "type": "type d'appareil de contrôle",
    "date_derniere_verification": "date de dernière vérification"
  },
  "agent_verbalisateur": {
    "agent_verbalisateur": "Numéro de l'agent verbalisateur",
    "service": "nom du service verbalisateur"
  },
  "réglements": {
      "date_15j": "date à compter de laquelle la personne doit payer dans les 15 jours",
      "adresse_demarche": "Adresse à laquelle adresser requêtes par lettre recommandée",
  }
}

Retourne UNIQUEMENT le JSON, sans commentaire ni explication. Si l'information est indisponible, return NONE."""
                        }
                    ],
                }
            ],
        )
        
        # Extract the JSON content from the response
        response_text = message.content[0].text.strip()
        
        # Try to parse as JSON
        try:
            extracted_data = json.loads(response_text)
            return extracted_data
        except json.JSONDecodeError:
            # If JSON parsing fails, try to extract JSON from the response
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                extracted_data = json.loads(json_match.group())
                return extracted_data
            else:
                raise Exception("Could not extract valid JSON from response")
        
    except Exception as e:
        raise Exception(f"Error extracting data from image: {str(e)}")

def scan_permis_conduire(file_path):
    """
    Extract structured data from a French driving license (permis de conduire).
    
    Args:
        file_path (str): Path to the image or PDF file
    
    Returns:
        dict: Structured data extracted from the driving license
    
    Raises:
        Exception: If there's an error with the API call or data extraction
    """
    try:
        # Convert file to base64 and get media type
        file_data = file_to_base64(file_path)
        image_base64 = file_data["base64_data"]
        media_type = file_data["media_type"]
        
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": image_base64,
                            },
                        },
                        {
                            "type": "text",
                            "text": """Analyse cette image de permis de conduire français et extrais les informations suivantes au format JSON strict. Si une information n'est pas disponible, utilise "NONE".

Structure JSON attendue:
{
  "identite": {
    "nom": "nom de famille",
    "prenom": "prénom(s)",
    "date_naissance": "DD/MM/YYYY",
    "lieu_naissance": "ville et pays de naissance"
  },
  "permis": {
    "numero_permis": "numéro du permis",
    "date_delivrance": "DD/MM/YYYY",
    "date_expiration": "DD/MM/YYYY",
    "autorite_delivrance": "préfecture ou autorité",
    "categories": ["B", "A1", "etc."]
  },
  "adresse": {
    "adresse_complete": "adresse complète",
    "code_postal": "code postal",
    "ville": "ville"
  }
}

Retourne UNIQUEMENT le JSON, sans commentaire ni explication."""
                        }
                    ],
                }
            ],
        )
        
        # Extract the JSON content from the response
        response_text = message.content[0].text.strip()
        
        # Try to parse as JSON
        try:
            extracted_data = json.loads(response_text)
            return extracted_data
        except json.JSONDecodeError:
            # If JSON parsing fails, try to extract JSON from the response
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                extracted_data = json.loads(json_match.group())
                return extracted_data
            else:
                raise Exception("Could not extract valid JSON from response")
        
    except Exception as e:
        raise Exception(f"Error extracting data from license: {str(e)}")

def scan_certificat_immatriculation(file_path):
    """
    Extract structured data from a French vehicle registration certificate (certificat d'immatriculation).
    
    Args:
        file_path (str): Path to the image or PDF file
    
    Returns:
        dict: Structured data extracted from the registration certificate
    
    Raises:
        Exception: If there's an error with the API call or data extraction
    """
    try:
        # Convert file to base64 and get media type
        file_data = file_to_base64(file_path)
        image_base64 = file_data["base64_data"]
        media_type = file_data["media_type"]
        
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": image_base64,
                            },
                        },
                        {
                            "type": "text",
                            "text": """Analyse cette image de certificat d'immatriculation français (carte grise) et extrais UNIQUEMENT les informations suivantes au format JSON strict. Si une information n'est pas disponible, utilise "NONE".

Structure JSON attendue:
{
  "proprietaire": {
    "nom": "nom de famille du propriétaire",
    "prenom": "prénom du propriétaire"
  },
  "vehicule": {
    "immatriculation": "numéro d'immatriculation au format XX-123-XX",
    "marque": "marque du véhicule uniquement"
  }
}

IMPORTANT: 
- Pour l'immatriculation, cherche le format XX-123-XX (2 lettres, 3 chiffres, 2 lettres)
- Pour la marque, donne uniquement la marque (ex: PEUGEOT, RENAULT, etc.)
- Ne pas inclure le modèle, juste la marque

Retourne UNIQUEMENT le JSON, sans commentaire ni explication."""
                        }
                    ],
                }
            ],
        )
        
        # Extract the JSON content from the response
        response_text = message.content[0].text.strip()
        
        # Try to parse as JSON
        try:
            extracted_data = json.loads(response_text)
            return extracted_data
        except json.JSONDecodeError:
            # If JSON parsing fails, try to extract JSON from the response
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                extracted_data = json.loads(json_match.group())
                return extracted_data
            else:
                raise Exception("Could not extract valid JSON from response")
        
    except Exception as e:
        raise Exception(f"Error extracting data from registration certificate: {str(e)}")

def scan_justificatif_domicile(file_path):
    """
    Extract structured data from a French proof of residence document (justificatif de domicile).
    
    Args:
        file_path (str): Path to the image or PDF file
    
    Returns:
        dict: Structured data extracted from the proof of residence document
    
    Raises:
        Exception: If there's an error with the API call or data extraction
    """
    try:
        # Convert file to base64 and get media type
        file_data = file_to_base64(file_path)
        image_base64 = file_data["base64_data"]
        media_type = file_data["media_type"]
        
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": image_base64,
                            },
                        },
                        {
                            "type": "text",
                            "text": """Analyse cette image de justificatif de domicile français (facture, attestation, etc.) et extrais UNIQUEMENT les informations suivantes au format JSON strict. Si une information n'est pas disponible, utilise "NONE".

Structure JSON attendue:
{
  "personne": {
    "nom": "nom de famille de la personne",
    "prenom": "prénom de la personne"
  },
  "domicile": {
    "adresse": "adresse complète du domicile",
    "date_justificatif": "date du justificatif (convertis au format: DD-MM-YYYY)"
  }
}

IMPORTANT: 
- Cherche le nom et prénom du titulaire/destinataire du document
- Pour l'adresse, donne l'adresse complète (rue, code postal, ville)
- Pour la date, utilise le format exact trouvé sur le document (peut être une date de facture, d'émission, etc.)

Retourne UNIQUEMENT le JSON, sans commentaire ni explication."""
                        }
                    ],
                }
            ],
        )
        
        # Extract the JSON content from the response
        response_text = message.content[0].text.strip()
        
        # Try to parse as JSON
        try:
            extracted_data = json.loads(response_text)
            return extracted_data
        except json.JSONDecodeError:
            # If JSON parsing fails, try to extract JSON from the response
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                extracted_data = json.loads(json_match.group())
                return extracted_data
            else:
                raise Exception("Could not extract valid JSON from response")
        
    except Exception as e:
        raise Exception(f"Error extracting data from proof of residence: {str(e)}")

def validate_documents_data(contravention_data=None, permis_data=None, certificat_data=None, justificatif_data=None):
    """
    Validate consistency between extracted document data using LLM analysis.
    
    Args:
        contravention_data (dict): JSON data from traffic violation notice
        permis_data (dict): JSON data from driving license
        certificat_data (dict): JSON data from vehicle registration
        justificatif_data (dict): JSON data from proof of residence
    
    Returns:
        dict: Validation results with status and details
    """
    try:
        # Get current date
        current_date = datetime.now().strftime("%d/%m/%Y")
        
        # Prepare data summary for LLM
        data_summary = f"Date du jour: {current_date}\n\nDonnées extraites des documents:\n"
        
        found_names = []
        justificatif_date = None
        
        if contravention_data and "identité" in contravention_data:
            identite = contravention_data["identité"]
            if identite.get("nom") and identite.get("nom") != "NONE":
                name = f"{identite.get('nom', '')} {identite.get('prenom', '')}"
                found_names.append(f"Contravention: {name}")
                data_summary += f"- Contravention: {name}\n"
        
        if permis_data and "identite" in permis_data:
            identite = permis_data["identite"]
            if identite.get("nom") and identite.get("nom") != "NONE":
                name = f"{identite.get('nom', '')} {identite.get('prenom', '')}"
                found_names.append(f"Permis: {name}")
                data_summary += f"- Permis de conduire: {name}\n"
        
        if certificat_data and "proprietaire" in certificat_data:
            proprietaire = certificat_data["proprietaire"]
            if proprietaire.get("nom") and proprietaire.get("nom") != "NONE":
                name = f"{proprietaire.get('nom', '')} {proprietaire.get('prenom', '')}"
                found_names.append(f"Certificat: {name}")
                data_summary += f"- Certificat d'immatriculation: {name}\n"
        
        if justificatif_data and "personne" in justificatif_data:
            personne = justificatif_data["personne"]
            domicile = justificatif_data.get("domicile", {})
            if personne.get("nom") and personne.get("nom") != "NONE":
                name = f"{personne.get('nom', '')} {personne.get('prenom', '')}"
                found_names.append(f"Justificatif: {name}")
                justificatif_date = domicile.get("date_justificatif")
                data_summary += f"- Justificatif de domicile: {name}"
                if justificatif_date and justificatif_date != "NONE":
                    data_summary += f", date: {justificatif_date}"
                data_summary += "\n"
        
        # Create LLM prompt
        prompt = f"""{data_summary}

Analyse ces données et vérifie:
1. Les noms/prénoms sont-ils cohérents entre tous les documents (même personne) ?
2. Si il y a un justificatif de domicile avec une date, cette date fait-elle moins de 3 mois par rapport à aujourd'hui ?

Réponds UNIQUEMENT au format JSON strict:
{{
  "names_consistent": true/false,
  "names_explanation": "explication détaillée de l'analyse des noms",
  "names_found": {json.dumps(found_names, ensure_ascii=False)},
  "date_valid": true/false/null,
  "date_explanation": "explication de la vérification de date (null si pas de date)",
  "date_found": "{justificatif_date if justificatif_date else 'null'}",
  "overall_status": "VALID/INVALID/WARNING",
  "summary": "résumé avec emojis"
}}

Notes importantes:
- Pour les noms, considère les variations normales (majuscules/minuscules, tirets, espaces)
- Pour la date, accepte tous les formats français courants
- Si pas de justificatif de domicile, date_valid = null
- Si moins de 2 noms trouvés, names_consistent = null"""

        # Call LLM
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        response_text = message.content[0].text.strip()
        
        # Parse LLM response
        try:
            llm_result = json.loads(response_text)
        except json.JSONDecodeError:
            # Try to extract JSON from response if it's wrapped
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                llm_result = json.loads(json_match.group())
            else:
                raise Exception("Could not parse LLM response as JSON")
        
        # Format result in expected structure
        validation_result = {
            "validation_status": llm_result.get("overall_status", "WARNING"),
            "checks": {
                "names_consistency": {
                    "status": "VALID" if llm_result.get("names_consistent") == True else 
                             "INVALID" if llm_result.get("names_consistent") == False else "NOT_CHECKED",
                    "details": llm_result.get("names_explanation", ""),
                    "found_names": llm_result.get("names_found", found_names)
                },
                "justificatif_date": {
                    "status": "VALID" if llm_result.get("date_valid") == True else 
                             "INVALID" if llm_result.get("date_valid") == False else "NOT_CHECKED",
                    "date_found": llm_result.get("date_found"),
                    "details": llm_result.get("date_explanation", "")
                }
            },
            "summary": llm_result.get("summary", "Validation effectuée")
        }
        
        return validation_result
        
    except Exception as e:
        return {
            "validation_status": "ERROR",
            "checks": {
                "names_consistency": {
                    "status": "ERROR",
                    "details": f"Erreur lors de la validation: {str(e)}",
                    "found_names": []
                },
                "justificatif_date": {
                    "status": "ERROR",
                    "date_found": None,
                    "details": f"Erreur lors de la validation: {str(e)}"
                }
            },
            "summary": f"❌ Erreur de validation: {str(e)}"
        }

def file_to_base64(file_path):
    """
    Convert an image or PDF file to base64 encoding with media type detection.
    
    Args:
        file_path (str): Path to the image or PDF file
    
    Returns:
        dict: {
            "base64_data": str,
            "media_type": str
        }
    
    Raises:
        Exception: If file format is not supported or file cannot be read
    """
    import os
    
    # Get file extension
    _, ext = os.path.splitext(file_path.lower())
    
    # Supported formats and their media types
    media_type_mapping = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.webp': 'image/webp',
        '.bmp': 'image/bmp',
        '.pdf': 'application/pdf'
    }
    
    # Validate file format
    if ext not in media_type_mapping:
        supported_formats = list(media_type_mapping.keys())
        raise Exception(f"Unsupported file format: {ext}. Supported formats: {', '.join(sorted(supported_formats))}")
    
    try:
        with open(file_path, "rb") as file:
            base64_data = base64.b64encode(file.read()).decode('utf-8')
            media_type = media_type_mapping[ext]
            
            return {
                "base64_data": base64_data,
                "media_type": media_type
            }
    except Exception as e:
        raise Exception(f"Error reading file: {str(e)}")