'use client'

import { Button } from "./ui/button";

export default function Header() {
  return (
    <header className="sticky top-0 z-50 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 border-b border-border">
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-accent rounded-lg flex items-center justify-center">
            <span className="text-accent-foreground font-bold text-xl">A</span>
          </div>
          <span className="text-xl font-semibold text-foreground">
            Avopoints
          </span>
        </div>
        
        <nav className="hidden md:flex items-center space-x-6">
          <a href="#accueil" className="text-muted-foreground hover:text-foreground transition-colors">
            Accueil
          </a>
          <a href="#comment-ca-marche" className="text-muted-foreground hover:text-foreground transition-colors">
            Comment ça marche
          </a>
          <a href="#tarifs" className="text-muted-foreground hover:text-foreground transition-colors">
            Tarifs
          </a>
          <a href="#contact" className="text-muted-foreground hover:text-foreground transition-colors">
            Contact
          </a>
        </nav>

        <div className="flex items-center space-x-4">
          <Button variant="ghost">
            Connexion
          </Button>
          <a href="/upload">
            <Button className="bg-accent text-accent-foreground hover:bg-accent/90 transition-colors">
              Je veux récupérer mes points !
            </Button>
          </a>
        </div>
      </div>
    </header>
  )
}