'use client'

import { useState, useEffect } from 'react'
import FileUpload from './FileUpload'
import ProcessingStatus from './ProcessingStatus'

interface TaskStatus {
  task_id: string
  status: string
  progress: number
  message: string
  current_step?: string
  error?: string
}

export default function UploadForm() {
  const [currentStep, setCurrentStep] = useState<'upload' | 'processing' | 'completed'>('upload')
  const [taskId, setTaskId] = useState<string | null>(null)
  const [taskStatus, setTaskStatus] = useState<TaskStatus | null>(null)

  const handleFilesUploaded = (newTaskId: string) => {
    console.log('[UploadForm] Files uploaded, taskId:', newTaskId)
    setTaskId(newTaskId)
    setCurrentStep('processing')
  }

  const handleProcessingComplete = () => {
    setCurrentStep('completed')
  }

  const handleStatusUpdate = (status: TaskStatus) => {
    console.log('[UploadForm] Status update received:', status)
    setTaskStatus(status)
  }

  const resetForm = () => {
    setCurrentStep('upload')
    setTaskId(null)
    setTaskStatus(null)
  }

  // Le polling est géré par ProcessingStatus, on supprime la redondance ici

  return (
    <div className="bg-white rounded-xl shadow-lg p-8">
      <div className="mb-8">
        <div className="flex items-center justify-center space-x-4 mb-6">
          <div className="flex flex-col items-center">
            <div className={`flex items-center justify-center w-10 h-10 rounded-full text-sm font-medium transition-all duration-300 ${
              currentStep === 'upload' ? 'bg-blue-600 text-white shadow-lg' : 
              currentStep === 'processing' || currentStep === 'completed' ? 'bg-green-500 text-white' : 
              'bg-gray-200 text-gray-600'
            }`}>
              {currentStep === 'upload' ? '📄' : '✓'}
            </div>
            <span className="text-xs text-gray-600 mt-1">Documents</span>
          </div>
          <div className={`h-1 w-16 transition-all duration-500 ${
            currentStep === 'processing' || currentStep === 'completed' ? 'bg-green-500' : 'bg-gray-200'
          }`}></div>
          <div className="flex flex-col items-center">
            <div className={`flex items-center justify-center w-10 h-10 rounded-full text-sm font-medium transition-all duration-300 ${
              currentStep === 'processing' ? 'bg-blue-600 text-white shadow-lg animate-pulse' : 
              currentStep === 'completed' ? 'bg-green-500 text-white' : 
              'bg-gray-200 text-gray-600'
            }`}>
              {currentStep === 'processing' ? '⚡' : currentStep === 'completed' ? '✓' : '⚙️'}
            </div>
            <span className="text-xs text-gray-600 mt-1">Analyse</span>
          </div>
          <div className={`h-1 w-16 transition-all duration-500 ${
            currentStep === 'completed' ? 'bg-green-500' : 'bg-gray-200'
          }`}></div>
          <div className="flex flex-col items-center">
            <div className={`flex items-center justify-center w-10 h-10 rounded-full text-sm font-medium transition-all duration-300 ${
              currentStep === 'completed' ? 'bg-green-500 text-white shadow-lg' : 'bg-gray-200 text-gray-600'
            }`}>
              {currentStep === 'completed' ? '🎉' : '📝'}
            </div>
            <span className="text-xs text-gray-600 mt-1">Résultat</span>
          </div>
        </div>
        
        <div className="text-center">
          {currentStep === 'upload' && (
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Téléchargez vos documents</h2>
              <p className="text-gray-600">Ajoutez vos 4 documents pour commencer l&apos;analyse</p>
            </div>
          )}
          {currentStep === 'processing' && (
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Traitement en cours</h2>
              {taskStatus ? (
                <div className="space-y-2">
                  <p className="text-blue-600 font-medium">
                    {taskStatus.message}
                  </p>
                  <div className="w-full bg-gray-200 rounded-full h-2 max-w-md mx-auto">
                    <div 
                      className="bg-blue-600 h-2 rounded-full transition-all duration-500 ease-out"
                      style={{ width: `${Math.max(0, Math.min(100, taskStatus.progress))}%` }}
                    ></div>
                  </div>
                  <p className="text-sm text-gray-500">
                    {Math.max(0, Math.min(100, taskStatus.progress))}% terminé
                  </p>
                </div>
              ) : (
                <p className="text-gray-600">Connexion au serveur...</p>
              )}
            </div>
          )}
          {currentStep === 'completed' && (
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Contestation prête !</h2>
              <p className="text-gray-600">Votre lettre de contestation a été générée avec succès</p>
            </div>
          )}
        </div>
      </div>

      {currentStep === 'upload' && (
        <FileUpload onFilesUploaded={handleFilesUploaded} />
      )}
      
      {currentStep === 'processing' && taskId && (
        <ProcessingStatus 
          taskId={taskId} 
          onComplete={handleProcessingComplete}
          onReset={resetForm}
          onStatusUpdate={handleStatusUpdate}
        />
      )}
      
      {currentStep === 'completed' && taskId && (
        <div className="text-center">
          <div className="mb-6">
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Votre contestation est prête !
            </h3>
            <p className="text-gray-600 mb-6">
              Téléchargez votre lettre de contestation personnalisée et envoyez-la par courrier recommandé.
            </p>
          </div>
          
          <div className="flex justify-center space-x-4">
            <a
              href={`http://localhost:8000/api/v1/task/${taskId}/result`}
              target="_blank"
              rel="noopener noreferrer"
              className="bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors"
            >
              Télécharger la lettre PDF
            </a>
            <button
              onClick={resetForm}
              className="bg-gray-100 text-gray-700 px-6 py-3 rounded-lg font-medium hover:bg-gray-200 transition-colors"
            >
              Nouvelle contestation
            </button>
          </div>
        </div>
      )}
    </div>
  )
}