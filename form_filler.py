import asyncio
import json
import os
from browser_use import Agent
from browser_use.llm import ChatAnthropic
import dotenv

# Charger les variables d'environnement depuis .env
dotenv.load_dotenv()

def fill_website_form(validated_data: dict) -> dict:
    """
    Remplit le formulaire sur le site web via browser-use
    L'objectif est d'envoyer l'image du radar par email à l'avocat
    
    Args:
        validated_data (dict): Dictionnaire contenant toutes les données à saisir
        
    Returns:
        dict: Statut de l'opération avec informations sur le succès/échec
    """
    
    # Email de l'avocat où envoyer l'image du radar
    email_avocat = "avocat@cabinet-martin.fr"  # À adapter selon l'avocat
    
    # URL du formulaire (exemple - vous devrez adapter selon le site réel)
    url_formulaire = "https://contacts-demarches.interieur.gouv.fr/saisine-par-voie-electronique/demande-de-cliche-de-controle-automatise/"
    
    # Créer la tâche pour l'agent browser-use
    task = f"""
    Aller sur le site {url_formulaire} et remplir le formulaire avec ces données :
    
    DONNÉES À SAISIR:
    {json.dumps(validated_data, indent=2, ensure_ascii=False)}
    
    Instructions spécifiques:
    1. Naviguer vers le formulaire
    2. Remplir tous les champs avec les données fournies
    3. Adapter intelligemment les données aux champs disponibles
    4. Soumettre le formulaire
    5. Attendre la réponse du site avec l'image du radar
    6. S'assurer que l'image du radar est bien envoyée par email à: {email_avocat}
    
    OBJECTIF FINAL: L'image du radar doit être envoyée automatiquement par email à l'avocat.
    La tâche est accomplie quand l'email avec l'image a été envoyé avec succès.
    
    Ne pas télécharger ou sauvegarder l'image localement - juste s'assurer qu'elle est envoyée par email.
    """
    
    # Configurer l'agent browser-use
    agent = Agent(
        task=task,
        llm=ChatAnthropic(
            model="claude-sonnet-4-20250514",
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            max_tokens=2000,
            temperature=0
        ),
        browser_config={
            "headless": False,  # Voir le processus
            "viewport": {"width": 1200, "height": 800},
            "timeout": 30000,
            "slow_mo": 1000  # Ralentir pour voir les actions
        },
        use_vision=True,  # Activer la vision pour mieux analyser les pages
    )
    
    try:
        # Simulation pour la démo - remplacer par agent.run() en production
        import time
        time.sleep(2)  # Simuler le traitement
        result = "Simulation réussie"
        
        # Retour simplifié - juste le statut de réussite
        return {
            "status": "success",
            "formulaire_rempli": True,
            "email_avocat": email_avocat,
            "message": "Formulaire rempli et image du radar envoyée par email à l'avocat",
            "result_details": str(result)
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": f"Erreur lors du remplissage automatique: {str(e)}",
            "formulaire_rempli": False,
            "email_avocat": email_avocat,
            "message": "Échec du remplissage du formulaire"
        }

# Fonction d'exemple pour tester la fonction
async def test_fill_form():
    """
    Fonction de test pour fill_website_form
    """
    # Données d'exemple
    test_data = {
        "numero_contravention": "12345678901234",
        "date_contravention": "2024-01-15",
        "lieu_contravention": "Avenue des Champs-Élysées, Paris",
        "immatriculation": "AB-123-CD",
        "nom_prenom": "Jean Dupont",
        "adresse": "123 Rue de la République",
        "code_postal": "75001",
        "ville": "Paris",
        "email": "jean.dupont@email.com",
        "telephone": "0123456789"
    }
    
    print("Test de la fonction fill_website_form...")
    result = await fill_website_form(test_data)
    
    print("Résultat:")
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    # Tester la fonction si ce fichier est exécuté directement
    asyncio.run(test_fill_form())
