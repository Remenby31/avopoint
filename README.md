# AvoPoint - Automated Traffic Violation Contest

AvoPoint is a web application that automates the process of contesting traffic violations by using OCR and artificial intelligence to process documents and automatically generate contest letters.

## Project Architecture

The project consists of two main parts:
- **Backend**: FastAPI (Python) API for document processing
- **Frontend**: Next.js (React/TypeScript) application for user interface

## Technologies Used

### Backend
- **FastAPI**: Modern and performant web framework
- **Python 3.x**: Main programming language
- **OCR**: Data extraction from PDF/image documents
- **ReportLab**: PDF document generation
- **Pillow & pdf2image**: Image processing
- **Uvicorn**: ASGI server

### Frontend
- **Next.js 15**: React framework with hybrid rendering
- **React 19**: User interface library
- **TypeScript**: Static typing
- **Tailwind CSS**: Utility-first CSS framework
- **Lucide React**: Icons

## Installation

### Prerequisites
- Python 3.8+
- Node.js 18+
- npm or yarn

### Backend Installation

1. Navigate to the project root directory:
```bash
cd avopoint
```

2. Create a Python virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Install Python dependencies:
```bash
pip install -r requirements.txt
```

### Frontend Installation

1. Navigate to the frontend directory:
```bash
cd avopoint-frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

## Running the Application

### Starting the Backend

1. Make sure the virtual environment is activated
2. From the root directory, launch the API:
```bash
python app.py
```

The API will be accessible at: `http://localhost:8000`

Interactive API documentation: `http://localhost:8000/docs`

### Starting the Frontend

1. In a new terminal, navigate to the frontend directory:
```bash
cd avopoint-frontend
```

2. Launch the application in development mode:
```bash
npm run dev
```

The application will be accessible at: `http://localhost:3000`

## Features

- **Document upload**: Traffic violation notice, vehicle registration certificate, driver's license, proof of residence
- **OCR extraction**: Automatic analysis of uploaded documents
- **Cross-validation**: Verification of extracted data consistency
- **Automatic form filling**: Automated web form submission
- **AI analysis**: Detection of driver visibility in radar photos
- **PDF generation**: Automatic creation of contest letters
- **Real-time tracking**: Processing progress interface

## Directory Structure

```
avopoint/
├── app.py                  # FastAPI API entry point
├── requirements.txt        # Python dependencies
├── scan.py                # OCR functions
├── form_filler.py         # Automatic form filling
├── generate_letter.py     # PDF letter generation
├── uploads/               # Temporary file storage
├── results/               # Generated results (PDF letters)
├── temp/                  # Temporary files
└── avopoint-frontend/     # Next.js application
    ├── package.json
    ├── src/
    │   └── app/
    │       ├── components/    # React components
    │       ├── page.tsx      # Home page
    │       └── upload/       # Upload page
    └── public/           # Static assets
```

## API Endpoints

- `GET /api/v1/health`: Service health check
- `POST /api/v1/process-documents`: Document upload and processing
- `GET /api/v1/task/{task_id}/status`: Progress tracking
- `GET /api/v1/task/{task_id}/result`: Result download
- `DELETE /api/v1/task/{task_id}`: Task deletion

## Available Scripts

### Backend
```bash
python app.py              # Start development server
```

### Frontend
```bash
npm run dev                # Development server
npm run build              # Production build
npm run start              # Production server
npm run lint               # Code linting
```

## Contributing

1. Fork the project
2. Create a branch for your feature
3. Commit your changes
4. Push to the branch
5. Open a Pull Request