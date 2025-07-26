import { Button } from "./components/ui/button";
import { Card, CardContent } from "./components/ui/card";
import { Badge } from "./components/ui/badge";
import { CheckCircle, FileText, Zap } from "lucide-react";
import Header from './components/Header';

export default function Home() {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      {/* Hero Section */}
      <section className="relative overflow-hidden py-24 md:py-40 bg-gradient-to-br from-accent/10 to-accent/5">
        <div className="absolute inset-0 bg-grid-small-accent/10 [mask-image:linear-gradient(0deg,white,rgba(255,255,255,0.6))]" />
        <div className="container mx-auto px-6 relative">
          <div className="text-center max-w-6xl mx-auto animate-fade-in">
            <div className="inline-flex items-center gap-3 px-6 py-3 rounded-full bg-accent/20 text-accent-foreground mb-8 hover-scale">
              <CheckCircle className="h-5 w-5" />
              <span className="text-base font-medium">Solution 100% automatisée</span>
            </div>
            <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold mb-8 text-foreground leading-tight">
              Contestez votre amende.<br />
              <span className="text-accent bg-gradient-to-r from-accent to-accent/80 bg-clip-text text-transparent">Sauvez vos points.</span>
            </h1>
            <p className="text-lg md:text-xl lg:text-2xl text-muted-foreground mb-12 max-w-4xl mx-auto leading-relaxed">
              Avopoints automatise la contestation de votre amende pour excès de vitesse : 
              vous déposez votre contravention, on s&apos;occupe du reste.
            </p>
            <div className="flex flex-col sm:flex-row gap-6 justify-center items-center mb-12">
              <Badge variant="secondary" className="text-base px-8 py-4 bg-accent text-accent-foreground border-0 hover-scale shadow-medium">
                ⚡ 1 minute, 0 formulaire
              </Badge>
              <div className="relative px-8 py-4 bg-gradient-to-r from-accent/20 to-primary/20 rounded-full border-2 border-accent/30 hover-scale shadow-large">
                <div className="flex items-center gap-4">
                  <span className="text-xl font-bold text-black animate-pulse relative">
                    59€
                    <div className="absolute top-1/2 left-1/2 w-16 h-1 bg-black/50 transform -translate-x-1/2 -translate-y-1/2 -rotate-12"></div>
                  </span>
                  <span className="text-3xl font-black bg-gradient-to-r from-yellow-400 to-yellow-600 bg-clip-text text-transparent animate-scale-in drop-shadow-[0_0_10px_rgba(250,204,21,0.8)] shadow-yellow-400/50">39€</span>
                </div>
                <div className="absolute -top-2 -right-2 bg-gradient-to-r from-yellow-400 to-yellow-600 text-yellow-900 text-xs font-bold px-2 py-1 rounded-full animate-bounce shadow-md">
                  -34%
                </div>
              </div>
            </div>
            <div className="flex flex-col sm:flex-row gap-6 justify-center items-center">
              <a href="/upload">
                <Button className="text-lg px-12 py-6 bg-accent text-accent-foreground hover:bg-accent/90 transition-all duration-300 shadow-large hover-scale">
                  Je veux récupérer mes points !
                  <CheckCircle className="ml-3 h-6 w-6" />
                </Button>
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 bg-background">
        <div className="container mx-auto px-6">
          <div className="text-center mb-20 animate-fade-in">
            <h2 className="text-3xl md:text-5xl font-bold mb-6 text-foreground">
              Comment ça marche ?
            </h2>
            <p className="text-lg md:text-xl text-muted-foreground max-w-3xl mx-auto leading-relaxed">
              Un processus simple en 3 étapes pour contester votre amende efficacement
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-10 max-w-6xl mx-auto">
            <Card className="relative overflow-hidden border-0 shadow-large hover-scale transition-all duration-300 group bg-gradient-to-br from-background to-accent/5">
              <CardContent className="p-10 text-center">
                <div className="h-24 w-24 bg-accent rounded-2xl flex items-center justify-center mx-auto mb-8 transition-transform duration-300 group-hover:scale-110 shadow-medium">
                  <FileText className="h-12 w-12 text-accent-foreground" />
                </div>
                <div className="bg-accent/10 rounded-full px-4 py-2 inline-block mb-6">
                  <span className="text-accent font-bold text-sm">ÉTAPE 1</span>
                </div>
                <h3 className="text-xl md:text-2xl font-bold mb-6 text-foreground">Déposez votre contravention</h3>
                <p className="text-muted-foreground leading-relaxed text-base">
                  Téléchargez 4 documents : 
                  avis de contravention, 
                  permis de conduire, 
                  justificatif de domicile, justificatif de consignation.
                </p>
              </CardContent>
            </Card>
            
            <Card className="relative overflow-hidden border-0 shadow-large hover-scale transition-all duration-300 group bg-gradient-to-br from-background to-accent/5">
              <CardContent className="p-10 text-center">
                <div className="h-24 w-24 bg-accent rounded-2xl flex items-center justify-center mx-auto mb-8 transition-transform duration-300 group-hover:scale-110 shadow-medium">
                  <Zap className="h-12 w-12 text-accent-foreground" />
                </div>
                <div className="bg-accent/10 rounded-full px-4 py-2 inline-block mb-6">
                  <span className="text-accent font-bold text-sm">ÉTAPE 2</span>
                </div>
                <h3 className="text-xl md:text-2xl font-bold mb-6 text-foreground">Analyse automatique</h3>
                <p className="text-muted-foreground leading-relaxed text-base">Notre IA s&apos;occupe du reste.</p>
              </CardContent>
            </Card>
            
            <Card className="relative overflow-hidden border-0 shadow-large hover-scale transition-all duration-300 group bg-gradient-to-br from-background to-accent/5">
              <CardContent className="p-10 text-center">
                <div className="h-24 w-24 bg-accent rounded-2xl flex items-center justify-center mx-auto mb-8 transition-transform duration-300 group-hover:scale-110 shadow-medium">
                  <CheckCircle className="h-12 w-12 text-accent-foreground" />
                </div>
                <div className="bg-accent/10 rounded-full px-4 py-2 inline-block mb-6">
                  <span className="text-accent font-bold text-sm">ÉTAPE 3</span>
                </div>
                <h3 className="text-xl md:text-2xl font-bold mb-6 text-foreground">Envoi automatique</h3>
                <p className="text-muted-foreground leading-relaxed text-base">
                  La photo radar est demandée en ligne et votre contestation part directement à l&apos;officier du ministère public.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 bg-foreground text-background">
        <div className="container mx-auto px-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-12 text-center max-w-4xl mx-auto">
            <div className="group">
              <div className="text-4xl md:text-5xl font-bold mb-4 text-accent transition-transform duration-300 group-hover:scale-110">15k+</div>
              <p className="text-background/80 text-base md:text-lg font-medium">Contraventions traitées</p>
            </div>
            <div className="group">
              <div className="text-4xl md:text-5xl font-bold mb-4 text-accent transition-transform duration-300 group-hover:scale-110">98%</div>
              <p className="text-background/80 text-base md:text-lg font-medium">Taux de réussite</p>
            </div>
            <div className="group">
              <div className="text-4xl md:text-5xl font-bold mb-4 text-accent transition-transform duration-300 group-hover:scale-110">1min</div>
              <p className="text-background/80 text-base md:text-lg font-medium">Temps moyen</p>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials TikTok Section - Style Lovable */}
      <section className="py-20 bg-background">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4 text-foreground">
              Ils parlent de nous sur TikTok
            </h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto leading-relaxed">
              Découvrez les témoignages authentiques de nos utilisateurs
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* TikTok Video 1 */}
            <div className="relative aspect-[9/16] bg-gradient-to-br from-gray-900 to-black rounded-2xl overflow-hidden shadow-large hover-scale transition-all duration-300 group">
              <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent z-10" />
              <div className="absolute top-4 right-4 z-20">
                <div className="w-8 h-8 bg-white rounded-full flex items-center justify-center">
                  <span className="text-black font-bold text-sm">▶</span>
                </div>
              </div>
              <div className="absolute bottom-4 left-4 right-4 z-20 text-white">
                <div className="flex items-center gap-2 mb-2">
                  <div className="w-8 h-8 bg-accent rounded-full flex items-center justify-center">
                    <span className="text-accent-foreground font-bold text-sm">@</span>
                  </div>
                  <span className="font-semibold">marie_conduit</span>
                </div>
                <p className="text-sm opacity-90">&quot;Incroyable ! Mes 4 points récupérés en 3 semaines ! #avopoints #permis&quot;</p>
                <div className="flex items-center gap-4 mt-2 text-xs">
                  <span>❤️ 12.5K</span>
                  <span>💬 234</span>
                  <span>📤 89</span>
                </div>
              </div>
            </div>

            {/* TikTok Video 2 */}
            <div className="relative aspect-[9/16] bg-gradient-to-br from-purple-900 to-pink-900 rounded-2xl overflow-hidden shadow-large hover-scale transition-all duration-300 group">
              <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent z-10" />
              <div className="absolute top-4 right-4 z-20">
                <div className="w-8 h-8 bg-white rounded-full flex items-center justify-center">
                  <span className="text-black font-bold text-sm">▶</span>
                </div>
              </div>
              <div className="absolute bottom-4 left-4 right-4 z-20 text-white">
                <div className="flex items-center gap-2 mb-2">
                  <div className="w-8 h-8 bg-accent rounded-full flex items-center justify-center">
                    <span className="text-accent-foreground font-bold text-sm">@</span>
                  </div>
                  <span className="font-semibold">julien_auto</span>
                </div>
                <p className="text-sm opacity-90">&quot;Plus jamais de paperasse ! Merci @avopoints 🙏 #contestation #facile&quot;</p>
                <div className="flex items-center gap-4 mt-2 text-xs">
                  <span>❤️ 8.9K</span>
                  <span>💬 156</span>
                  <span>📤 67</span>
                </div>
              </div>
            </div>

            {/* TikTok Video 3 */}
            <div className="relative aspect-[9/16] bg-gradient-to-br from-blue-900 to-cyan-900 rounded-2xl overflow-hidden shadow-large hover-scale transition-all duration-300 group">
              <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent z-10" />
              <div className="absolute top-4 right-4 z-20">
                <div className="w-8 h-8 bg-white rounded-full flex items-center justify-center">
                  <span className="text-black font-bold text-sm">▶</span>
                </div>
              </div>
              <div className="absolute bottom-4 left-4 right-4 z-20 text-white">
                <div className="flex items-center gap-2 mb-2">
                  <div className="w-8 h-8 bg-accent rounded-full flex items-center justify-center">
                    <span className="text-accent-foreground font-bold text-sm">@</span>
                  </div>
                  <span className="font-semibold">sophie_road</span>
                </div>
                <p className="text-sm opacity-90">&quot;1 minute pour tout faire ! C&apos;est magique ✨ #tech #innovation&quot;</p>
                <div className="flex items-center gap-4 mt-2 text-xs">
                  <span>❤️ 15.2K</span>
                  <span>💬 312</span>
                  <span>📤 128</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
