from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, Optional, List
import asyncio
import uuid
import os
import shutil
from pathlib import Path
import logging
from datetime import datetime
import json

# Import des fonctions de scan OCR
from scan import (
    scan_contravention, 
    scan_certificat_immatriculation, 
    scan_permis_conduire, 
    scan_justificatif_domicile,
    validate_documents_data
)
from form_filler import fill_website_form
# from your_modules.image_analysis import detect_clear_driver
from generate_letter import generate_final_pdf

# Configuration
app = FastAPI(
    title="API Traitement Contraventions",
    description="API pour le traitement automatisé des contraventions",
    version="1.0.0"
)

# Configuration des logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Répertoires de travail
UPLOAD_DIR = Path("uploads")
TEMP_DIR = Path("temp")
RESULTS_DIR = Path("results")

# Créer les répertoires s'ils n'existent pas
for directory in [UPLOAD_DIR, TEMP_DIR, RESULTS_DIR]:
    directory.mkdir(exist_ok=True)

# Stockage des tâches en mémoire (en production, utiliser Redis ou une BDD)
tasks_storage: Dict[str, dict] = {}

# Modèles Pydantic
class TaskStatus(BaseModel):
    task_id: str
    status: str
    progress: int
    message: str
    current_step: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    error: Optional[str] = None

class TaskResponse(BaseModel):
    task_id: str
    status: str
    message: str

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str

# États possibles des tâches avec plus de détails
TASK_STATUS = {
    "UPLOADED": {"progress": 0, "message": "Documents reçus"},
    "SCANNING_CONTRAVENTION": {"progress": 10, "message": "Extraction des données de contravention"},
    "SCANNING_CERTIFICAT": {"progress": 15, "message": "Extraction des données du certificat d'immatriculation"},
    "SCANNING_PERMIS": {"progress": 20, "message": "Extraction des données du permis de conduire"},
    "SCANNING_DOMICILE": {"progress": 25, "message": "Extraction des données du justificatif de domicile"},
    "VALIDATING": {"progress": 40, "message": "Validation des données"},
    "FILLING_FORM": {"progress": 60, "message": "Remplissage du formulaire web"},
    "ANALYZING_PHOTO": {"progress": 80, "message": "Analyse de la photo"},
    "GENERATING_PDF": {"progress": 90, "message": "Génération du PDF"},
    "COMPLETED": {"progress": 100, "message": "Traitement terminé"},
    "FAILED": {"progress": -1, "message": "Erreur lors du traitement"}
}

# Fonctions de gestion des tâches
def create_task(task_id: str, user_files: dict) -> None:
    """Crée une nouvelle tâche de traitement"""
    tasks_storage[task_id] = {
        "task_id": task_id,
        "status": "UPLOADED",
        "progress": 0,
        "message": "Documents reçus et traitement démarré",
        "current_step": "UPLOADED",
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "files": user_files,
        "error": None,
        "result_file": None
    }
    logger.info(f"Tâche {task_id} créée")

def update_task_status(task_id: str, status: str, message: str = None, error: str = None) -> None:
    """Met à jour le statut d'une tâche"""
    if task_id not in tasks_storage:
        return
    
    task = tasks_storage[task_id]
    task["status"] = status
    task["current_step"] = status
    task["progress"] = TASK_STATUS.get(status, {}).get("progress", task["progress"])
    task["message"] = message or TASK_STATUS.get(status, {}).get("message", "")
    task["updated_at"] = datetime.now()
    
    if error:
        task["error"] = error
        task["status"] = "FAILED"
        task["progress"] = -1
    
    logger.info(f"Tâche {task_id} mise à jour: {status}")

def get_task_status(task_id: str) -> Optional[dict]:
    """Récupère le statut actuel d'une tâche"""
    return tasks_storage.get(task_id)

async def save_uploaded_files(task_id: str, files: dict) -> dict:
    """Sauvegarde les fichiers uploadés et retourne leurs chemins"""
    file_paths = {}
    task_dir = UPLOAD_DIR / task_id
    task_dir.mkdir(exist_ok=True)
    
    for file_type, file in files.items():
        if file:
            file_path = task_dir / f"{file_type}_{file.filename}"
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            file_paths[file_type] = str(file_path)
            logger.info(f"Fichier {file_type} sauvegardé: {file_path}")
    
    return file_paths

def cleanup_files(task_id: str) -> None:
    """Nettoie les fichiers temporaires d'une tâche"""
    task_dir = UPLOAD_DIR / task_id
    if task_dir.exists():
        shutil.rmtree(task_dir)
        logger.info(f"Fichiers temporaires de la tâche {task_id} supprimés")

# Fonction principale de traitement asynchrone
async def process_documents_async(task_id: str, file_paths: dict) -> None:
    """Fonction asynchrone principale de traitement"""
    try:
        logger.info(f"Début du traitement de la tâche {task_id}")
        
        # =========================================================================
        # ÉTAPE 1: EXTRACTION DES DONNÉES PAR OCR DE TOUS LES DOCUMENTS
        # =========================================================================
        extracted_data = {}
        
        # --- 1.1: SCAN DE L'AVIS DE CONTRAVENTION ---
        if "contravention" in file_paths:
            update_task_status(task_id, "SCANNING_CONTRAVENTION", "Extraction des données de l'avis de contravention...")
            try:
                extracted_data["contravention"] = scan_contravention(file_paths["contravention"])
                logger.info(f"Contravention scannée avec succès pour la tâche {task_id}")
            except Exception as e:
                logger.error(f"Erreur scan contravention {task_id}: {str(e)}")
                update_task_status(task_id, "FAILED", error=f"Erreur lors de l'extraction de la contravention: {str(e)}")
                return
        
        # --- 1.2: SCAN DU CERTIFICAT D'IMMATRICULATION ---
        if "certificat" in file_paths:
            update_task_status(task_id, "SCANNING_CERTIFICAT", "Extraction des données du certificat d'immatriculation...")
            try:
                extracted_data["certificat"] = scan_certificat_immatriculation(file_paths["certificat"])
                logger.info(f"Certificat scanné avec succès pour la tâche {task_id}")
            except Exception as e:
                logger.error(f"Erreur scan certificat {task_id}: {str(e)}")
                update_task_status(task_id, "FAILED", error=f"Erreur lors de l'extraction du certificat: {str(e)}")
                return
        
        # --- 1.3: SCAN DU PERMIS DE CONDUIRE ---
        if "permis" in file_paths:
            update_task_status(task_id, "SCANNING_PERMIS", "Extraction des données du permis de conduire...")
            try:
                extracted_data["permis"] = scan_permis_conduire(file_paths["permis"])
                logger.info(f"Permis scanné avec succès pour la tâche {task_id}")
            except Exception as e:
                logger.error(f"Erreur scan permis {task_id}: {str(e)}")
                update_task_status(task_id, "FAILED", error=f"Erreur lors de l'extraction du permis: {str(e)}")
                return
        
        # --- 1.4: SCAN DU JUSTIFICATIF DE DOMICILE ---
        if "domicile" in file_paths:
            update_task_status(task_id, "SCANNING_DOMICILE", "Extraction des données du justificatif de domicile...")
            try:
                extracted_data["domicile"] = scan_justificatif_domicile(file_paths["domicile"])
                logger.info(f"Justificatif de domicile scanné avec succès pour la tâche {task_id}")
            except Exception as e:
                logger.error(f"Erreur scan domicile {task_id}: {str(e)}")
                update_task_status(task_id, "FAILED", error=f"Erreur lors de l'extraction du justificatif: {str(e)}")
                return
        
        # =========================================================================
        # ÉTAPE 2: VALIDATION ET VÉRIFICATION DE LA COHÉRENCE DES DONNÉES
        # =========================================================================
        update_task_status(task_id, "VALIDATING", "Validation de la cohérence des données extraites...")
        try:
            validation_result = validate_documents_data(
                contravention_data=extracted_data.get("contravention"),
                permis_data=extracted_data.get("permis"),
                certificat_data=extracted_data.get("certificat"),
                justificatif_data=extracted_data.get("domicile")
            )
            logger.info(f"Validation terminée pour la tâche {task_id}: {validation_result.get('validation_status')}")
            
            # Stocker les résultats de validation
            tasks_storage[task_id]["validation_result"] = validation_result
            tasks_storage[task_id]["extracted_data"] = extracted_data
            
        except Exception as e:
            logger.error(f"Erreur validation {task_id}: {str(e)}")
            update_task_status(task_id, "FAILED", error=f"Erreur lors de la validation: {str(e)}")
            return
        
        # =========================================================================
        # ÉTAPE 3: REMPLISSAGE AUTOMATIQUE DU FORMULAIRE WEB GOUVERNEMENTAL
        # =========================================================================
        update_task_status(task_id, "FILLING_FORM", "Remplissage automatique du formulaire web...")
        try:
            form_result = fill_website_form(extracted_data)
            logger.info(f"Formulaire rempli avec succès pour la tâche {task_id}")
            tasks_storage[task_id]["form_result"] = form_result
        except Exception as e:
            logger.error(f"Erreur remplissage formulaire {task_id}: {str(e)}")
            update_task_status(task_id, "FAILED", error=f"Erreur lors du remplissage du formulaire: {str(e)}")
            return

        # =========================================================================
        # ÉTAPE 4: RÉCUPÉRATION DE L'IMAGE DU RADAR DEPUIS LES EMAILS
        # =========================================================================
        update_task_status(task_id, "FILLING_FORM", "Récupération de l'image du radar depuis les emails...")
        
        # TODO: Implémenter la fonction de vérification des emails
        # try:
        #     photo_path = check_email_for_radar_image()
        #     tasks_storage[task_id]["radar_photo"] = photo_path
        # except Exception as e:
        #     logger.warning(f"Impossible de récupérer l'image radar {task_id}: {str(e)}")
        
        # =========================================================================
        # ÉTAPE 5: ANALYSE INTELLIGENTE DE LA PHOTO DU RADAR
        # =========================================================================
        update_task_status(task_id, "ANALYZING_PHOTO", "Analyse de la visibilité du conducteur...")
        try:
            # TODO: Remplacer par la vraie fonction d'analyse IA
            # driver_visible = detect_clear_driver(form_result.get("photo_path"))
            driver_visible = False  # Simulation pour la démo
            tasks_storage[task_id]["driver_visible"] = driver_visible
            logger.info(f"Analyse photo terminée pour la tâche {task_id}: conducteur visible = {driver_visible}")
        except Exception as e:
            logger.error(f"Erreur analyse photo {task_id}: {str(e)}")
            update_task_status(task_id, "FAILED", error=f"Erreur lors de l'analyse de la photo: {str(e)}")
            return

        # =========================================================================
        # ÉTAPE 6: GÉNÉRATION DU DOCUMENT FINAL DE CONTESTATION
        # =========================================================================
        update_task_status(task_id, "GENERATING_PDF", "Génération du document de contestation...")
        try:
            pdf_path = generate_final_pdf(extracted_data, driver_visible, task_id)
            tasks_storage[task_id]["result_file"] = pdf_path
            logger.info(f"PDF généré avec succès pour la tâche {task_id}: {pdf_path}")
        except Exception as e:
            logger.error(f"Erreur génération PDF {task_id}: {str(e)}")
            update_task_status(task_id, "FAILED", error=f"Erreur lors de la génération du PDF: {str(e)}")
            return
        
        # =========================================================================
        # FINALISATION: MARQUAGE DE LA TÂCHE COMME TERMINÉE
        # =========================================================================
        update_task_status(task_id, "COMPLETED", "Traitement terminé avec succès")
        logger.info(f"Traitement de la tâche {task_id} terminé avec succès")
        
    except Exception as e:
        error_msg = f"Erreur inattendue lors du traitement: {str(e)}"
        logger.error(f"Erreur critique tâche {task_id}: {error_msg}")
        update_task_status(task_id, "FAILED", error=error_msg)

# Endpoints

@app.get("/api/v1/health", response_model=HealthResponse)
async def health_check():
    """Endpoint de vérification de l'état du service"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version="1.0.0"
    )

@app.post("/api/v1/process-documents", response_model=TaskResponse)
async def process_documents(
    background_tasks: BackgroundTasks,
    contravention: UploadFile = File(..., description="Avis de contravention"),
    certificat: UploadFile = File(..., description="Certificat d'immatriculation"),
    permis: UploadFile = File(..., description="Permis de conduire"),
    domicile: UploadFile = File(..., description="Justificatif de domicile")
):
    """Endpoint principal pour traiter les documents"""
    
    # Validation des types de fichiers
    allowed_types = ["image/jpeg", "image/png", "application/pdf"]
    files = {"contravention": contravention, "certificat": certificat, "permis": permis, "domicile": domicile}
    
    for file_type, file in files.items():
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"Type de fichier non supporté pour {file_type}: {file.content_type}"
            )
    
    # Création de la tâche
    task_id = str(uuid.uuid4())
    
    try:
        # Sauvegarde des fichiers
        file_paths = await save_uploaded_files(task_id, files)
        
        # Création de la tâche
        create_task(task_id, file_paths)
        
        # Lancement du traitement en arrière-plan
        background_tasks.add_task(process_documents_async, task_id, file_paths)
        
        return TaskResponse(
            task_id=task_id,
            status="processing",
            message="Documents reçus et traitement démarré"
        )
        
    except Exception as e:
        logger.error(f"Erreur lors de la création de la tâche: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

@app.get("/api/v1/task/{task_id}/status", response_model=TaskStatus)
async def get_task_status_endpoint(task_id: str):
    """Endpoint de suivi de l'avancement d'une tâche"""
    task = get_task_status(task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    
    # Ajouter des informations supplémentaires selon l'état
    status_response = TaskStatus(**task)
    
    # Enrichir avec des détails selon l'état
    if task["status"] == "COMPLETED" and "validation_result" in task:
        validation = task["validation_result"]
        status_response.message += f" - Validation: {validation.get('validation_status', 'UNKNOWN')}"
    
    return status_response

@app.get("/api/v1/task/{task_id}/result")
async def get_task_result(task_id: str):
    """Endpoint de récupération du résultat final"""
    task = get_task_status(task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    
    if task["status"] != "COMPLETED":
        raise HTTPException(
            status_code=400,
            detail=f"Tâche pas encore terminée. Statut actuel: {task['status']}"
        )
    
    result_file = task.get("result_file")
    if not result_file or not os.path.exists(result_file):
        raise HTTPException(status_code=404, detail="Fichier résultat non trouvé")
    
    return FileResponse(
        path=result_file,
        filename=f"contravention_result_{task_id}.pdf",
        media_type="application/pdf"
    )

@app.delete("/api/v1/task/{task_id}")
async def delete_task(task_id: str):
    """Endpoint pour supprimer/annuler une tâche"""
    task = get_task_status(task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    
    # Nettoyage des fichiers
    cleanup_files(task_id)
    
    # Suppression de la tâche
    del tasks_storage[task_id]
    
    return {"message": f"Tâche {task_id} supprimée avec succès"}

@app.get("/api/v1/tasks")
async def list_tasks():
    """Endpoint pour lister toutes les tâches (utile pour le debug)"""
    return {
        "tasks": [
            {
                "task_id": task_id,
                "status": task["status"],
                "progress": task["progress"],
                "created_at": task["created_at"]
            }
            for task_id, task in tasks_storage.items()
        ]
    }

# Point d'entrée pour lancer l'application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)