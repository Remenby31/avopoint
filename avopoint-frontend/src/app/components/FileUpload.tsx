'use client'

import { useState } from 'react'

interface FileUploadProps {
  onFilesUploaded: (taskId: string) => void
}

interface UploadedFile {
  file: File
  preview?: string
}

interface FileState {
  contravention: UploadedFile | null
  certificat: UploadedFile | null
  permis: UploadedFile | null
  domicile: UploadedFile | null
}

export default function FileUpload({ onFilesUploaded }: FileUploadProps) {
  const [files, setFiles] = useState<FileState>({
    contravention: null,
    certificat: null,
    permis: null,
    domicile: null
  })
  const [isUploading, setIsUploading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleFileSelect = (type: keyof FileState, file: File) => {
    const reader = new FileReader()
    reader.onload = (e) => {
      setFiles(prev => ({
        ...prev,
        [type]: {
          file,
          preview: e.target?.result as string
        }
      }))
    }
    reader.readAsDataURL(file)
    setError(null)
  }

  const removeFile = (type: keyof FileState) => {
    setFiles(prev => ({
      ...prev,
      [type]: null
    }))
  }

  const handleSubmit = async () => {
    if (!files.contravention || !files.certificat || !files.permis || !files.domicile) {
      setError('Veuillez télécharger les 4 documents requis')
      return
    }

    setIsUploading(true)
    setError(null)

    try {
      const formData = new FormData()
      formData.append('contravention', files.contravention.file)
      formData.append('certificat', files.certificat.file)
      formData.append('permis', files.permis.file)
      formData.append('domicile', files.domicile.file)

      const response = await fetch('http://localhost:8000/api/v1/process-documents', {
        method: 'POST',
        body: formData
      })

      if (!response.ok) {
        throw new Error('Erreur lors de l\'upload des fichiers')
      }

      const result = await response.json()
      onFilesUploaded(result.task_id)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Une erreur est survenue')
    } finally {
      setIsUploading(false)
    }
  }

  const isAllFilesUploaded = files.contravention && files.certificat && files.permis && files.domicile

  const fileTypes = [
    {
      key: 'contravention' as const,
      label: 'Avis de contravention',
      description: 'Le document officiel de votre contravention',
      icon: '📄'
    },
    {
      key: 'certificat' as const,
      label: 'Certificat d\'immatriculation',
      description: 'Carte grise de votre véhicule',
      icon: '🚗'
    },
    {
      key: 'permis' as const,
      label: 'Permis de conduire',
      description: 'Votre permis de conduire en cours de validité',
      icon: '🪪'
    },
    {
      key: 'domicile' as const,
      label: 'Justificatif de domicile',
      description: 'Facture récente (moins de 3 mois)',
      icon: '🏠'
    }
  ]

  return (
    <div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        {fileTypes.map((fileType) => (
          <div key={fileType.key} className="border-2 border-dashed border-gray-300 rounded-lg p-6 hover:border-blue-400 transition-colors">
            <div className="text-center">
              <div className="text-4xl mb-2">{fileType.icon}</div>
              <h3 className="font-medium text-gray-900 mb-1">{fileType.label}</h3>
              <p className="text-sm text-gray-500 mb-4">{fileType.description}</p>
              
              {files[fileType.key] ? (
                <div className="space-y-3">
                  <div className="flex items-center justify-center space-x-2 text-green-600">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    <span className="text-sm font-medium">{files[fileType.key]!.file.name}</span>
                  </div>
                  <button
                    onClick={() => removeFile(fileType.key)}
                    className="text-red-600 hover:text-red-700 text-sm"
                  >
                    Supprimer
                  </button>
                </div>
              ) : (
                <div>
                  <input
                    type="file"
                    accept="image/*,.pdf"
                    onChange={(e) => {
                      const file = e.target.files?.[0]
                      if (file) handleFileSelect(fileType.key, file)
                    }}
                    className="hidden"
                    id={`file-${fileType.key}`}
                  />
                  <label
                    htmlFor={`file-${fileType.key}`}
                    className="cursor-pointer inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-blue-600 bg-blue-50 hover:bg-blue-100 transition-colors"
                  >
                    Choisir un fichier
                  </label>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <div className="flex items-center">
            <svg className="w-5 h-5 text-red-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span className="text-red-800">{error}</span>
          </div>
        </div>
      )}

      <div className="text-center">
        <button
          onClick={handleSubmit}
          disabled={!isAllFilesUploaded || isUploading}
          className={`px-8 py-3 rounded-lg font-medium transition-colors ${
            isAllFilesUploaded && !isUploading
              ? 'bg-blue-600 text-white hover:bg-blue-700'
              : 'bg-gray-300 text-gray-500 cursor-not-allowed'
          }`}
        >
          {isUploading ? (
            <div className="flex items-center space-x-2">
              <svg className="w-5 h-5 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              <span>Traitement en cours...</span>
            </div>
          ) : (
            'Lancer l\'analyse'
          )}
        </button>
        
        {!isAllFilesUploaded && (
          <p className="text-sm text-gray-500 mt-2">
            Téléchargez les 4 documents pour continuer
          </p>
        )}
      </div>
    </div>
  )
}