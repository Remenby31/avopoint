'use client'

import { useState } from 'react'
import FileUpload from './FileUpload'
import ProcessingStatus from './ProcessingStatus'
import { Card, CardContent, CardHeader, CardTitle } from './ui/card'
import { Badge } from './ui/badge'
import { Button } from './ui/button'
import { Progress } from './ui/progress'

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
    <Card className="w-full">
      <CardHeader>
        {/* Progress Steps */}
        <div className="flex items-center justify-center space-x-4 mb-6">
          <div className="flex flex-col items-center">
            <div className={`flex items-center justify-center w-12 h-12 rounded-full text-lg font-medium transition-all duration-300 ${
              currentStep === 'upload' ? 'bg-blue-600 text-white shadow-lg' : 
              currentStep === 'processing' || currentStep === 'completed' ? 'bg-green-500 text-white' : 
              'bg-gray-200 text-gray-600'
            }`}>
              {currentStep === 'upload' ? '📄' : '✓'}
            </div>
            <Badge variant={currentStep !== 'upload' ? 'success' : 'secondary'} className="mt-2 text-xs">
              Documents
            </Badge>
          </div>
          <div className={`h-2 w-16 rounded-full transition-all duration-500 ${
            currentStep === 'processing' || currentStep === 'completed' ? 'bg-green-500' : 'bg-gray-200'
          }`}></div>
          <div className="flex flex-col items-center">
            <div className={`flex items-center justify-center w-12 h-12 rounded-full text-lg font-medium transition-all duration-300 ${
              currentStep === 'processing' ? 'bg-blue-600 text-white shadow-lg animate-pulse' : 
              currentStep === 'completed' ? 'bg-green-500 text-white' : 
              'bg-gray-200 text-gray-600'
            }`}>
              {currentStep === 'processing' ? '⚡' : currentStep === 'completed' ? '✓' : '⚙️'}
            </div>
            <Badge variant={currentStep === 'completed' ? 'success' : currentStep === 'processing' ? 'default' : 'secondary'} className="mt-2 text-xs">
              Analyse
            </Badge>
          </div>
          <div className={`h-2 w-16 rounded-full transition-all duration-500 ${
            currentStep === 'completed' ? 'bg-green-500' : 'bg-gray-200'
          }`}></div>
          <div className="flex flex-col items-center">
            <div className={`flex items-center justify-center w-12 h-12 rounded-full text-lg font-medium transition-all duration-300 ${
              currentStep === 'completed' ? 'bg-green-500 text-white shadow-lg' : 'bg-gray-200 text-gray-600'
            }`}>
              {currentStep === 'completed' ? '🎉' : '📝'}
            </div>
            <Badge variant={currentStep === 'completed' ? 'success' : 'secondary'} className="mt-2 text-xs">
              Résultat
            </Badge>
          </div>
        </div>
        
        {/* Step Content */}
        {currentStep === 'upload' && (
          <div className="text-center">
            <CardTitle className="text-2xl text-gray-900 mb-2">
              Téléchargez vos documents
            </CardTitle>
            <p className="text-gray-600">Ajoutez vos 4 documents pour commencer l&apos;analyse</p>
          </div>
        )}
        {currentStep === 'processing' && (
          <div className="text-center">
            <CardTitle className="text-2xl text-gray-900 mb-4">
              Traitement en cours
            </CardTitle>
            {taskStatus ? (
              <div className="space-y-4 max-w-md mx-auto">
                <Badge variant="default" className="text-sm px-4 py-2">
                  {taskStatus.message}
                </Badge>
                <Progress value={Math.max(0, Math.min(100, taskStatus.progress))} className="h-3" />
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
          <div className="text-center">
            <CardTitle className="text-2xl text-gray-900 mb-2">
              Contestation prête ! 🎉
            </CardTitle>
            <p className="text-gray-600">Votre lettre de contestation a été générée avec succès</p>
          </div>
        )}
      </CardHeader>

      <CardContent>
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
          <div className="text-center space-y-6">
            <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto">
              <svg className="w-10 h-10 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            
            <div>
              <CardTitle className="text-xl text-gray-900 mb-2">
                Votre contestation est prête !
              </CardTitle>
              <p className="text-gray-600 mb-6">
                Téléchargez votre lettre de contestation personnalisée et envoyez-la par courrier recommandé.
              </p>
            </div>
            
            <div className="flex justify-center space-x-4">
              <a
                href={`http://localhost:8000/api/v1/task/${taskId}/result`}
                target="_blank"
                rel="noopener noreferrer"
              >
                <Button className="px-6">
                  Télécharger la lettre PDF
                </Button>
              </a>
              <Button variant="outline" onClick={resetForm} className="px-6">
                Nouvelle contestation
              </Button>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  )
}