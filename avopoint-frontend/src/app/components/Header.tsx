'use client'

export default function Header() {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <div className="flex items-center">
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center mr-3">
                <span className="text-white font-bold text-lg">A</span>
              </div>
              <h1 className="text-2xl font-bold text-gray-900">Avopoint</h1>
            </div>
            <div className="ml-4 hidden md:block">
              <span className="text-sm text-gray-500 bg-gray-100 px-2 py-1 rounded">
                Expertise Juridique IA
              </span>
            </div>
          </div>
          
          <nav className="hidden md:flex items-center space-x-6">
            <a href="#how-it-works" className="text-gray-600 hover:text-gray-900 transition-colors">
              Comment ça marche
            </a>
            <a href="#pricing" className="text-gray-600 hover:text-gray-900 transition-colors">
              Tarifs
            </a>
            <a href="#contact" className="text-gray-600 hover:text-gray-900 transition-colors">
              Contact
            </a>
          </nav>
          
          <div className="flex items-center space-x-3">
            <button className="text-gray-600 hover:text-gray-900 transition-colors">
              Connexion
            </button>
            <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
              Commencer
            </button>
          </div>
        </div>
      </div>
    </header>
  )
}