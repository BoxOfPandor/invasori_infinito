#!/usr/bin/env python3

"""
Scena del gioco principale
Gestisce il gameplay principale
"""

import pygame
import os
from core.scena import Scena

class ScenaGioco(Scena):
    """Scena principale del gioco"""
    
    def __init__(self, gioco):
        """Inizializza la scena di gioco"""
        super().__init__(gioco)
        self.sfondo = None
        self.area_gioco = None
        self.margine_laterale = 200  # Margine su ciascun lato
        
    def inizializza(self):
        """Inizializza gli elementi del gioco"""
        super().inizializza()
        
        # Carica l'immagine di sfondo
        percorso_sfondo = os.path.join("assets", "img", "sfondo_gioco.jpg")
        try:
            self.sfondo = pygame.image.load(percorso_sfondo).convert()
            self.sfondo = pygame.transform.scale(self.sfondo, (self.gioco.larghezza, self.gioco.altezza))
        except pygame.error:
            # Fallback se l'immagine non può essere caricata
            self.sfondo = pygame.Surface((self.gioco.larghezza, self.gioco.altezza))
            self.sfondo.fill((0, 0, 0))  # Sfondo nero
        
        # Definisci l'area di gioco esattamente di 720 pixel di larghezza
        larghezza_area_gioco = 720
        self.margine_laterale = (self.gioco.larghezza - larghezza_area_gioco) // 2
        self.area_gioco = pygame.Rect(
            self.margine_laterale,
            0,
            larghezza_area_gioco,
            self.gioco.altezza
        )
    
    def termina(self):
        """Pulisce le risorse quando la scena non è più attiva"""
        super().termina()
        
        # Rimuovi questa scena come osservatore degli eventi
        self.gioco.gestore_eventi.rimuovi_osservatore(self)
    
    def gestisci_evento(self, evento):
        """Gestisce gli eventi di gioco"""
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                # Torna al menu principale
                self.gioco.cambia_scena("menu")
    
    def aggiorna(self, delta_tempo):
        """Aggiorna la logica del gioco"""
        pass
    
    def disegna(self, schermo):
        """Disegna gli elementi del gioco"""
        # Disegna lo sfondo su tutto lo schermo
        schermo.blit(self.sfondo, (0, 0))
        
        # Disegna un bordo per l'area di gioco per renderla visibile
        pygame.draw.rect(schermo, (100, 100, 100), self.area_gioco, 2)
        
        # Puoi aggiungere qui del testo o elementi dell'interfaccia per i test
        font = pygame.font.SysFont("Arial", 24)
        testo = font.render("Area di Gioco", True, (255, 255, 255))
        pos_testo = (self.area_gioco.centerx - testo.get_width() // 2, 20)
        schermo.blit(testo, pos_testo)
    
    def salva_stato(self):
        """Salva lo stato attuale per il rewind"""
        return {}
    
    def carica_stato(self, stato):
        """Carica uno stato salvato durante il rewind"""
        pass