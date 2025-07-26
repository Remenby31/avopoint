# AvoPoint - Contestation Automatisée de Contraventions

AvoPoint est une application web qui automatise le processus de contestation des contraventions routières en utilisant l'OCR et l'intelligence artificielle pour traiter les documents et générer automatiquement les lettres de contestation.

## Architecture du Projet

Le projet est composé de deux parties principales :
- **Backend** : API FastAPI (Python) pour le traitement des documents
- **Frontend** : Application Next.js (React/TypeScript) pour l'interface utilisateur

## Technologies Utilisées

### Backend
- **FastAPI** : Framework web moderne et performant
- **Python 3.x** : Langage de programmation principal
- **OCR** : Extraction de données depuis les documents PDF/images
- **ReportLab** : Génération de documents PDF
- **Pillow & pdf2image** : Traitement d'images
- **Uvicorn** : Serveur ASGI

### Frontend
- **Next.js 15** : Framework React avec rendu hybride
- **React 19** : Bibliothèque d'interface utilisateur
- **TypeScript** : Typage statique
- **Tailwind CSS** : Framework CSS utility-first
- **Lucide React** : Icônes

## Installation

### Prérequis
- Python 3.8+
- Node.js 18+
- npm ou yarn

### Installation du Backend

1. Naviguez vers le répertoire racine du projet :
```bash
cd avopoint
```

2. Créez un environnement virtuel Python :
```bash
python -m venv venv
```

3. Activez l'environnement virtuel :
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Installez les dépendances Python :
```bash
pip install -r requirements.txt
```

### Installation du Frontend

1. Naviguez vers le répertoire frontend :
```bash
cd avopoint-frontend
```

2. Installez les dépendances Node.js :
```bash
npm install
```

## Lancement de l'Application

### Démarrage du Backend

1. Assurez-vous que l'environnement virtuel est activé
2. Depuis le répertoire racine, lancez l'API :
```bash
python app.py
```

L'API sera accessible sur : `http://localhost:8000`

Documentation API interactive : `http://localhost:8000/docs`

### Démarrage du Frontend

1. Dans un nouveau terminal, naviguez vers le répertoire frontend :
```bash
cd avopoint-frontend
```

2. Lancez l'application en mode développement :
```bash
npm run dev
```

L'application sera accessible sur : `http://localhost:3000`

## Fonctionnalités

- **Upload de documents** : Avis de contravention, certificat d'immatriculation, permis de conduire, justificatif de domicile
- **Extraction OCR** : Analyse automatique des documents uploadés
- **Validation croisée** : Vérification de la cohérence des données extraites
- **Remplissage automatique** : Soumission automatique des formulaires web
- **Analyse IA** : Détection de la visibilité du conducteur sur les photos radar
- **Génération PDF** : Création automatique de la lettre de contestation
- **Suivi en temps réel** : Interface de progression du traitement

## Structure des Répertoires

```
avopoint/
├── app.py                  # Point d'entrée de l'API FastAPI
├── requirements.txt        # Dépendances Python
├── scan.py                # Fonctions OCR
├── form_filler.py         # Remplissage automatique des formulaires
├── generate_letter.py     # Génération des lettres PDF
├── uploads/               # Stockage temporaire des fichiers uploadés
├── results/               # Résultats générés (lettres PDF)
├── temp/                  # Fichiers temporaires
└── avopoint-frontend/     # Application Next.js
    ├── package.json
    ├── src/
    │   └── app/
    │       ├── components/    # Composants React
    │       ├── page.tsx      # Page d'accueil
    │       └── upload/       # Page d'upload
    └── public/           # Assets statiques
```

## API Endpoints

- `GET /api/v1/health` : Vérification de l'état du service
- `POST /api/v1/process-documents` : Upload et traitement des documents
- `GET /api/v1/task/{task_id}/status` : Suivi de l'avancement
- `GET /api/v1/task/{task_id}/result` : Téléchargement du résultat
- `DELETE /api/v1/task/{task_id}` : Suppression d'une tâche

## Scripts Disponibles

### Backend
```bash
python app.py              # Lancer le serveur de développement
```

### Frontend
```bash
npm run dev                # Serveur de développement
npm run build              # Build de production
npm run start              # Serveur de production
npm run lint               # Vérification du code
```

## Contribution

1. Fork le projet
2. Créez une branche pour votre fonctionnalité
3. Committez vos changements
4. Poussez vers la branche
5. Ouvrez une Pull Request