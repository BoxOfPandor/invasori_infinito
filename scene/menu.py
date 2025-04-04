#!/usr/bin/env python3

"""
Scena del menu principale
Gestisce l'interfaccia del menu di avvio
"""

import pygame
import os
from core.scena import Scena

class MenuPrincipale(Scena):
    """Scena del menu principale del gioco"""
    
    def __init__(self, gioco):
        """Inizializza la scena del menu principale"""
        super().__init__(gioco)
        self.font_titolo = None
        self.font_pulsante = None
        self.colore_titolo = (255, 255, 0)  # Giallo
        self.colore_pulsante = (100, 100, 255)  # Blu chiaro
        self.colore_pulsante_hover = (150, 150, 255)  # Blu più chiaro quando hover
        self.pulsante_start = None
        self.mouse_su_pulsante = False
        self.immagine_sfondo = None
    
    def carica_e_ritaglia_immagine(self, percorso, larghezza_finale, altezza_finale):
        """Carica un'immagine e la ritaglia mantenendo la parte centrale"""
        # Carica l'immagine originale
        immagine_originale = pygame.image.load(percorso).convert()
        
        # Dimensioni originali
        larghezza_originale = immagine_originale.get_width()
        altezza_originale = immagine_originale.get_height()
        
        # Calcola le coordinate per ritagliare (prende il centro dell'immagine)
        x_inizio = (larghezza_originale - larghezza_finale) // 2
        y_inizio = (altezza_originale - altezza_finale) // 2
        
        # Ritaglia l'immagine
        immagine_ritagliata = pygame.Surface((larghezza_finale, altezza_finale))
        immagine_ritagliata.blit(immagine_originale, (0, 0), 
                                (x_inizio, y_inizio, x_inizio + larghezza_finale, y_inizio + altezza_finale))
        
        return immagine_ritagliata
    
    def inizializza(self):
        """Inizializza gli elementi del menu"""
        super().inizializza()
        
        # Carica l'immagine di sfondo
        percorso_immagine = os.path.join("assets", "img", "sfondo_menu.jpg")  # Adjust as needed
        self.immagine_sfondo = self.carica_e_ritaglia_immagine(
            percorso_immagine,
            self.gioco.larghezza,
            self.gioco.altezza
        )
        
        # Carica i font
        self.font_titolo = pygame.font.SysFont("Arial", 64, bold=True)
        self.font_pulsante = pygame.font.SysFont("Arial", 36)
        
        # Definisci il pulsante di start
        larghezza_pulsante = 200
        altezza_pulsante = 60
        pos_x = (self.gioco.larghezza - larghezza_pulsante) // 2
        pos_y = (self.gioco.altezza - altezza_pulsante) // 2 + 50
        
        self.pulsante_start = pygame.Rect(pos_x, pos_y, larghezza_pulsante, altezza_pulsante)
        
        # Aggiungi questo menu come osservatore degli eventi
        self.gioco.gestore_eventi.aggiungi_osservatore(self)
    
    def termina(self):
        """Pulisce le risorse quando la scena non è più attiva"""
        super().termina()
        
        # Rimuovi questo menu come osservatore degli eventi
        self.gioco.gestore_eventi.rimuovi_osservatore(self)
    
    def gestisci_evento(self, evento):
        """Gestisce gli eventi del menu"""
        if evento.type == pygame.MOUSEMOTION:
            # Controlla se il mouse è sopra il pulsante
            self.mouse_su_pulsante = self.pulsante_start.collidepoint(evento.pos)
        
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1 and self.mouse_su_pulsante:  # Clic sinistro
                print("game launch")
                # Qui potresti passare alla scena di gioco effettiva
                # self.gioco.cambia_scena("gioco")
    
    def aggiorna(self, delta_tempo):
        """Aggiorna la logica del menu"""
        pass
    
    def disegna(self, schermo):
        """Disegna gli elementi del menu"""
        # Disegna lo sfondo
        if self.immagine_sfondo:
            schermo.blit(self.immagine_sfondo, (0, 0))
        else:
            # Fallback se l'immagine non può essere caricata
            schermo.fill((0, 0, 0))
        
        # Disegna il titolo
        titolo_surf = self.font_titolo.render("INVASORI INFINITO", True, self.colore_titolo)
        titolo_rect = titolo_surf.get_rect(center=(self.gioco.larghezza // 2, self.gioco.altezza // 2 - 50))
        schermo.blit(titolo_surf, titolo_rect)
        
        # Disegna il pulsante di start
        colore_attuale = self.colore_pulsante_hover if self.mouse_su_pulsante else self.colore_pulsante
        pygame.draw.rect(schermo, colore_attuale, self.pulsante_start, border_radius=10)
        pygame.draw.rect(schermo, (255, 255, 255), self.pulsante_start, 2, border_radius=10)  # Bordo bianco
        
        # Testo del pulsante
        testo_start = self.font_pulsante.render("START", True, (255, 255, 255))
        testo_rect = testo_start.get_rect(center=self.pulsante_start.center)
        schermo.blit(testo_start, testo_rect)
