import UploadForm from './components/UploadForm'
import Header from './components/Header'

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <Header />
      <main className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              Contestez vos contraventions en toute simplicité
            </h1>
            <p className="text-xl text-gray-600 mb-8">
              Notre IA analyse vos documents et génère automatiquement votre lettre de contestation
            </p>
            <div className="flex justify-center space-x-8 text-sm text-gray-500">
              <div className="flex items-center">
                <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
                100% Automatisé
              </div>
              <div className="flex items-center">
                <div className="w-3 h-3 bg-blue-500 rounded-full mr-2"></div>
                Avocat Expert
              </div>
              <div className="flex items-center">
                <div className="w-3 h-3 bg-purple-500 rounded-full mr-2"></div>
                Conforme Légalement
              </div>
            </div>
          </div>
          
          <UploadForm />
        </div>
      </main>
    </div>
  )
}
