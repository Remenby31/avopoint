'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from './ui/card'
import { Progress } from './ui/progress'
import { Badge } from './ui/badge'
import { Button } from './ui/button'
import { Alert, AlertDescription } from './ui/alert'
import { Spinner, LoadingDots } from './ui/spinner'

interface ProcessingStatusProps {
  taskId: string
  onComplete: () => void
  onReset: () => void
  onStatusUpdate?: (status: TaskStatus) => void
}

interface TaskStatus {
  task_id: string
  status: string
  progress: number
  message: string
  current_step?: string
  error?: string
}

const STEP_MESSAGES = {
  'UPLOADED': 'Documents reçus et vérifiés',
  'SCANNING_CONTRAVENTION': 'Extraction OCR de l\'avis de contravention',
  'SCANNING_CERTIFICAT': 'Extraction OCR du certificat d\'immatriculation',
  'SCANNING_PERMIS': 'Extraction OCR du permis de conduire',
  'SCANNING_DOMICILE': 'Extraction OCR du justificatif de domicile',
  'VALIDATING': 'Validation croisée des données extraites',
  'FILLING_FORM': 'Demande automatique d\'image radar',
  'RETRIEVING_RADAR_IMAGE': 'Récupération de l\'image du radar',
  'ANALYZING_PHOTO': 'Analyse IA de la visibilité du conducteur',
  'GENERATING_PDF': 'Génération de la lettre de contestation',
  'COMPLETED': 'Contestation prête à télécharger',
  'FAILED': 'Erreur lors du traitement'
}

export default function ProcessingStatus({ taskId, onComplete, onReset, onStatusUpdate }: ProcessingStatusProps) {
  const [status, setStatus] = useState<TaskStatus | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let interval: NodeJS.Timeout | null = null
    let isActive = true

    const pollStatus = async () => {
      if (!isActive) return
      
      try {
        console.log(`[ProcessingStatus] Polling status for task: ${taskId}`)
        const response = await fetch(`http://localhost:8000/api/v1/task/${taskId}/status`)
        if (!response.ok) {
          throw new Error(`Erreur HTTP ${response.status}: ${response.statusText}`)
        }
        
        const statusData: TaskStatus = await response.json()
        console.log('[ProcessingStatus] Status received:', statusData)
        
        if (!isActive) return // Check again before updating state
        
        setStatus(statusData)
        
        // Notify parent component of status update
        if (onStatusUpdate) {
          onStatusUpdate(statusData)
        }
        
        if (statusData.status === 'COMPLETED') {
          console.log('[ProcessingStatus] Task completed, calling onComplete')
          onComplete()
          return // Stop polling
        } else if (statusData.status === 'FAILED') {
          console.log('[ProcessingStatus] Task failed:', statusData.error)
          setError(statusData.error || 'Une erreur est survenue lors du traitement')
          return // Stop polling
        }
      } catch (err) {
        console.error('[ProcessingStatus] Polling error:', err)
        if (!isActive) return
        setError(err instanceof Error ? err.message : 'Erreur de connexion')
        return // Stop polling on error
      }
    }

    // Initial call
    pollStatus()
    
    // Set up interval only if not already completed/failed
    interval = setInterval(pollStatus, 1000)

    return () => {
      isActive = false
      if (interval) {
        clearInterval(interval)
      }
    }
  }, [taskId, onComplete, onStatusUpdate])

  if (error) {
    return (
      <Card className="w-full max-w-2xl mx-auto">
        <CardHeader className="text-center">
          <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg className="w-8 h-8 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </div>
          <CardTitle className="text-xl text-gray-900 mb-2">
            Erreur de traitement
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <Alert variant="destructive">
            <AlertDescription>
              {error}
            </AlertDescription>
          </Alert>
          <div className="flex justify-center">
            <Button onClick={onReset} className="px-6">
              Recommencer
            </Button>
          </div>
        </CardContent>
      </Card>
    )
  }

  if (!status) {
    return (
      <Card className="w-full max-w-2xl mx-auto">
        <CardHeader className="text-center">
          <div className="relative w-24 h-24 mx-auto mb-6">
            {/* Pulsing outer ring */}
            <div className="absolute inset-0 bg-blue-200 rounded-full animate-ping"></div>
            <div className="absolute inset-2 bg-blue-100 rounded-full animate-pulse"></div>
            <div className="absolute inset-4 bg-white rounded-full flex items-center justify-center shadow-lg">
              <Spinner size="lg" className="text-blue-500" />
            </div>
          </div>
          <CardTitle className="text-xl text-gray-900 mb-2">
            Initialisation
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <Alert>
            <AlertDescription>
              <div className="flex items-center justify-center space-x-2">
                <LoadingDots />
                <span className="text-blue-700 font-medium">Connexion au serveur...</span>
              </div>
            </AlertDescription>
          </Alert>
          <p className="text-sm text-gray-500 text-center">Préparation du traitement de vos documents</p>
        </CardContent>
      </Card>
    )
  }

  const progressPercentage = Math.max(0, Math.min(100, status.progress))
  const currentMessage = STEP_MESSAGES[status.current_step as keyof typeof STEP_MESSAGES] || status.message

  return (
    <Card className="w-full max-w-4xl mx-auto">
      <CardHeader className="text-center">
        {/* Animated processing icon */}
        <div className="relative w-32 h-32 mx-auto mb-6">
          <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full animate-pulse"></div>
          <div className="absolute inset-2 bg-white rounded-full flex items-center justify-center">
            <div className="relative">
              <Spinner size="lg" className="w-16 h-16 text-blue-500" />
              <div className="absolute -top-1 -right-1 w-4 h-4 bg-green-500 rounded-full animate-bounce"></div>
            </div>
          </div>
        </div>
        
        <CardTitle className="text-2xl font-bold text-gray-900 animate-fade-in mb-4">
          Traitement en cours
        </CardTitle>
        
        <Alert className="mb-6">
          <AlertDescription>
            <p className="text-blue-800 font-medium text-lg animate-pulse">
              {currentMessage}
            </p>
          </AlertDescription>
        </Alert>
        
        <div className="flex items-center justify-center space-x-2 text-sm text-gray-600 mb-6">
          <div className="w-2 h-2 bg-blue-500 rounded-full animate-ping"></div>
          <span>Étape actuelle: </span>
          <Badge variant="outline">{status.current_step || status.status}</Badge>
        </div>
      </CardHeader>
      
      <CardContent className="space-y-6">
        {/* Enhanced progress bar */}
        <div className="space-y-3">
          <Progress value={progressPercentage} className="h-4" />
          
          <div className="flex justify-between items-center text-sm">
            <span className="text-gray-600 font-medium">Progression globale</span>
            <div className="flex items-center space-x-2">
              <Badge variant="secondary" className="text-lg font-bold">
                {progressPercentage}%
              </Badge>
              <div className="w-3 h-3 bg-blue-500 rounded-full animate-bounce"></div>
            </div>
          </div>
        </div>
        
        {/* Enhanced steps timeline */}
        <Card className="bg-gray-50">
          <CardHeader>
            <CardTitle className="text-lg text-gray-800 text-center">
              Étapes du traitement
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
          {[
            { threshold: 5, label: 'Réception et vérification des documents', icon: '📄' },
            { threshold: 15, label: 'Extraction OCR avis de contravention', icon: '🔍' },
            { threshold: 25, label: 'Extraction OCR certificat d\'immatriculation', icon: '🚗' },
            { threshold: 35, label: 'Extraction OCR permis de conduire', icon: '🪪' },
            { threshold: 45, label: 'Extraction OCR justificatif de domicile', icon: '🏠' },
            { threshold: 55, label: 'Validation croisée des données', icon: '✅' },
            { threshold: 65, label: 'Demande d\'image radar gouvernementale', icon: '📡' },
            { threshold: 75, label: 'Récupération de l\'image du radar', icon: '📧' },
            { threshold: 85, label: 'Analyse IA de la visibilité du conducteur', icon: '🤖' },
            { threshold: 95, label: 'Génération de la lettre de contestation', icon: '📝' },
            { threshold: 100, label: 'Contestation prête à télécharger', icon: '🎉' }
          ].map((step, index) => {
            const isCompleted = progressPercentage >= step.threshold
            const isActive = progressPercentage >= step.threshold - 10 && progressPercentage < step.threshold
            const isCurrent = progressPercentage >= step.threshold - 10 && progressPercentage < step.threshold + 10
            
            return (
              <div key={index} className={`flex items-center p-3 rounded-lg transition-all duration-500 ${
                isCompleted ? 'bg-green-50 border border-green-200 animate-fade-in' :
                isActive ? 'bg-blue-50 border border-blue-200 shadow-sm animate-slide-in-right' :
                'bg-white border border-gray-200'
              }`}>
                <div className={`relative w-8 h-8 rounded-full mr-4 flex items-center justify-center transition-all duration-500 ${
                  isCompleted ? 'bg-green-500 shadow-lg' : 
                  isActive ? 'bg-blue-500 animate-pulse shadow-md' : 'bg-gray-300'
                }`}>
                  {isCompleted ? (
                    <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                    </svg>
                  ) : isActive ? (
                    <div className="w-3 h-3 bg-white rounded-full animate-ping"></div>
                  ) : (
                    <div className="w-2 h-2 bg-white rounded-full"></div>
                  )}
                </div>
                <div className="flex items-center flex-1">
                  <span className={`text-2xl mr-3 transition-transform duration-300 ${
                    isCurrent ? 'animate-bounce' : ''
                  }`}>{step.icon}</span>
                  <span className={`text-sm font-medium transition-colors duration-300 ${
                    isCompleted ? 'text-green-700' : 
                    isActive ? 'text-blue-700' : 'text-gray-600'
                  }`}>
                    {step.label}
                  </span>
                </div>
                {isCompleted && (
                  <div className="ml-auto">
                    <Badge variant="success" className="text-xs">
                      Terminé ✓
                    </Badge>
                  </div>
                )}
                {isActive && (
                  <div className="ml-auto">
                    <Badge variant="default" className="text-xs">
                      <LoadingDots className="mr-1" />
                      En cours...
                    </Badge>
                  </div>
                )}
              </div>
            )
          })}
            </div>
          </CardContent>
        </Card>
        
        <div className="flex justify-center mt-6">
          <Button variant="ghost" onClick={onReset} className="text-gray-500 hover:text-gray-700">
            Annuler le traitement
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}