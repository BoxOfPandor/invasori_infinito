#!/usr/bin/env python3

"""
Scena del gioco principale
Gestisce il gameplay principale
"""

import pygame
import os
from core.scena import Scena
import config

class ScenaGioco(Scena):
    """Scena principale del gioco"""

    def __init__(self, gioco):
        """Inizializza la scena di gioco"""
        super().__init__(gioco)
        self.sfondo = None
        self.area_gioco = None
        self.margine_laterale = 0

    def inizializza(self):
        """Inizializza gli elementi del gioco"""
        super().inizializza()
        
        # Carica l'immagine di sfondo
        percorso_sfondo = os.path.join("assets", "img", "sfondo_gioco.jpg")
        try:
            self.sfondo = self.carica_e_ritaglia_immagine(
                percorso_sfondo,
                config.GIOCO_LARGHEZZA,
                config.GIOCO_ALTEZZA
            )
        except Exception as e:
            print(f"Errore nel caricamento dello sfondo: {e}")
            # Fallback se l'immagine non può essere caricata
            self.sfondo = pygame.Surface((config.GIOCO_LARGHEZZA, config.GIOCO_ALTEZZA))
            self.sfondo.fill((0, 0, 0))  # Sfondo nero

        # Definisci l'area di gioco con larghezza proporzionata
        # Usiamo l'80% della larghezza della finestra, ma non più di 720 pixel
        larghezza_area_gioco = min(int(config.GIOCO_LARGHEZZA * 0.9), 720)
        self.margine_laterale = (config.GIOCO_LARGHEZZA - larghezza_area_gioco) // 2
        self.area_gioco = pygame.Rect(
            self.margine_laterale,
            0,
            larghezza_area_gioco,
            config.GIOCO_ALTEZZA
        )

        # Aggiungi questa scena come osservatore degli eventi
        self.gioco.gestore_eventi.aggiungi_osservatore(self)
        
    def carica_e_ritaglia_immagine(self, percorso, larghezza_finale, altezza_finale):
        """Carica un'immagine e la ritaglia mantenendo la parte centrale"""
        try:
            # Carica l'immagine originale
            immagine_originale = pygame.image.load(percorso).convert()
            
            # Dimensioni originali
            larghezza_originale = immagine_originale.get_width()
            altezza_originale = immagine_originale.get_height()
            
            # Calcola il rapporto di aspetto
            rapporto_originale = larghezza_originale / altezza_originale
            rapporto_finale = larghezza_finale / altezza_finale
            
            # Determina come ritagliare l'immagine in base ai rapports
            if rapporto_originale > rapporto_finale:
                # L'immagine è troppo large, la rogniamo sur les côtés
                nuova_larghezza = int(altezza_originale * rapporto_finale)
                x_inizio = (larghezza_originale - nuova_larghezza) // 2
                y_inizio = 0
                area_ritaglio = (x_inizio, y_inizio, nuova_larghezza, altezza_originale)
            else:
                # L'immagine è troppo haute, la rogniamo en haut et en bas
                nuova_altezza = int(larghezza_originale / rapporto_finale)
                x_inizio = 0
                y_inizio = (altezza_originale - nuova_altezza) // 2
                area_ritaglio = (x_inizio, y_inizio, larghezza_originale, nuova_altezza)
            
            # Ritaglia l'immagine
            immagine_ritagliata = pygame.Surface((area_ritaglio[2], area_ritaglio[3]))
            immagine_ritagliata.blit(immagine_originale, (0, 0), area_ritaglio)
            
            # Ridimensiona al formato finale
            return pygame.transform.scale(immagine_ritagliata, (larghezza_finale, altezza_finale))
        
        except (pygame.error, FileNotFoundError) as e:
            print(f"Errore nel caricamento dell'immagine: {e}")
            # Fallback: crea una superficie vuota con la dimensione richiesta
            superficie = pygame.Surface((larghezza_finale, altezza_finale))
            superficie.fill((0, 0, 0))  # Riempi di nero
            return superficie

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