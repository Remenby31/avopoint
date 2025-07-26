import UploadForm from '../components/UploadForm'
import Header from '../components/Header'
import { Badge } from '../components/ui/badge'
import { CheckCircle, Shield, Zap, FileText, Clock, Award } from 'lucide-react'

export default function UploadPage() {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      {/* Hero Section avec gradient et animations */}
      <section className="relative overflow-hidden py-16 md:py-24 bg-gradient-to-br from-accent/10 to-accent/5">
        <div className="absolute inset-0 bg-grid-small-accent/10 [mask-image:linear-gradient(0deg,white,rgba(255,255,255,0.6))]" />
        <div className="container mx-auto px-6 relative">
          <div className="text-center max-w-4xl mx-auto animate-fade-in">
            <div className="inline-flex items-center gap-3 px-6 py-3 rounded-full bg-accent/20 text-accent-foreground mb-8 hover-scale">
              <FileText className="h-5 w-5" />
              <span className="text-base font-medium">Téléchargement sécurisé</span>
            </div>
            
            <h1 className="text-3xl md:text-5xl lg:text-6xl font-bold mb-6 text-foreground leading-tight">
              Déposez vos documents.<br />
              <span className="text-accent bg-gradient-to-r from-accent to-accent/80 bg-clip-text text-transparent">
                On s&apos;occupe du reste.
              </span>
            </h1>
            
            <p className="text-lg md:text-xl text-muted-foreground mb-8 max-w-3xl mx-auto leading-relaxed">
              Notre IA analyse vos documents en temps réel et génère automatiquement votre lettre de contestation personnalisée
            </p>
            
            {/* Badges de confiance */}
            <div className="flex flex-wrap justify-center gap-4 mb-12">
              <Badge variant="secondary" className="text-sm px-4 py-2 bg-accent/10 text-accent-foreground border-0 hover-scale">
                <Shield className="w-4 h-4 mr-2" />
                Données sécurisées
              </Badge>
              <Badge variant="secondary" className="text-sm px-4 py-2 bg-accent/10 text-accent-foreground border-0 hover-scale">
                <Zap className="w-4 h-4 mr-2" />
                Traitement instantané
              </Badge>
              <Badge variant="secondary" className="text-sm px-4 py-2 bg-accent/10 text-accent-foreground border-0 hover-scale">
                <Award className="w-4 h-4 mr-2" />
                Conforme légalement
              </Badge>
            </div>
          </div>
        </div>
      </section>

      {/* Section principale avec le formulaire */}
      <main className="container mx-auto px-4 py-16">
        <div className="max-w-5xl mx-auto">
          
          {/* Guide rapide */}
          <div className="mb-12">
            <div className="text-center mb-8">
              <h2 className="text-2xl md:text-3xl font-bold text-foreground mb-4">
                Documents requis
              </h2>
              <p className="text-muted-foreground">
                Préparez ces 4 documents pour une analyse optimale
              </p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
              <div className="text-center p-6 rounded-2xl bg-gradient-to-br from-background to-accent/5 border border-accent/20 hover-scale transition-all duration-300">
                <div className="w-16 h-16 bg-accent/20 rounded-full flex items-center justify-center mx-auto mb-4">
                  <FileText className="w-8 h-8 text-accent" />
                </div>
                <h3 className="font-semibold text-foreground mb-2">Avis de contravention</h3>
                <p className="text-sm text-muted-foreground">Document officiel reçu</p>
              </div>
              
              <div className="text-center p-6 rounded-2xl bg-gradient-to-br from-background to-accent/5 border border-accent/20 hover-scale transition-all duration-300">
                <div className="w-16 h-16 bg-accent/20 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Shield className="w-8 h-8 text-accent" />
                </div>
                <h3 className="font-semibold text-foreground mb-2">Permis de conduire</h3>
                <p className="text-sm text-muted-foreground">Recto et verso</p>
              </div>
              
              <div className="text-center p-6 rounded-2xl bg-gradient-to-br from-background to-accent/5 border border-accent/20 hover-scale transition-all duration-300">
                <div className="w-16 h-16 bg-accent/20 rounded-full flex items-center justify-center mx-auto mb-4">
                  <FileText className="w-8 h-8 text-accent" />
                </div>
                <h3 className="font-semibold text-foreground mb-2">Justificatif domicile</h3>
                <p className="text-sm text-muted-foreground">Facture récente</p>
              </div>
              
              <div className="text-center p-6 rounded-2xl bg-gradient-to-br from-background to-accent/5 border border-accent/20 hover-scale transition-all duration-300">
                <div className="w-16 h-16 bg-accent/20 rounded-full flex items-center justify-center mx-auto mb-4">
                  <CheckCircle className="w-8 h-8 text-accent" />
                </div>
                <h3 className="font-semibold text-foreground mb-2">Justificatif consignation</h3>
                <p className="text-sm text-muted-foreground">Preuve de paiement</p>
              </div>
            </div>
          </div>

          {/* Formulaire principal avec design amélioré */}
          <div className="relative">
            <div className="absolute inset-0 bg-gradient-to-r from-accent/5 to-primary/5 rounded-3xl blur-3xl -z-10"></div>
            <UploadForm />
          </div>
          
          {/* Section informative */}
          <div className="mt-16 text-center">
            <div className="inline-flex items-center gap-2 px-6 py-3 rounded-full bg-muted/50 text-muted-foreground">
              <Clock className="w-4 h-4" />
              <span className="text-sm">Temps de traitement moyen : 2-3 minutes</span>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}