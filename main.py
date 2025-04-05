#!/usr/bin/env python3

"""
Alien Invader - Gioco principale
Un clone del classico Space Invaders creato per la Game JAM
"""

import pygame
import sys
from core.gioco import Gioco
import config
from scene.menu import MenuPrincipale
from scene.gioco import ScenaGioco
from scene.introduzione import ScenaIntroduzione

def main():
    """Funzione principale che avvia il gioco"""
    
    # Inizializzazione di pygame
    pygame.init()
    pygame.mixer.init()
    
    # Creazione del gioco
    alieno_invader = Gioco(
        titolo=config.TITOLO_GIOCO,
        larghezza=config.LARGHEZZA_SCHERMO,
        altezza=config.ALTEZZA_SCHERMO,
        fps=config.FPS
    )
    
    # Aggiungi le scene al gioco
    introduzione = ScenaIntroduzione(alieno_invader)
    menu_principale = MenuPrincipale(alieno_invader)
    scena_gioco = ScenaGioco(alieno_invader)
    
    alieno_invader.gestore_scene.aggiungi_scena("intro", introduzione)
    alieno_invader.gestore_scene.aggiungi_scena("menu", menu_principale)
    alieno_invader.gestore_scene.aggiungi_scena("gioco", scena_gioco)
    
    # Imposta la scena iniziale come il menu
    alieno_invader.gestore_scene.cambia_scena("menu")
    
    # Esecuzione del gioco
    try:
        alieno_invader.esegui()
    except Exception as errore:
        print(f"Errore durante l'esecuzione del gioco: {errore}")
    finally:
        # Pulizia e uscita
        pygame.quit()
        sys.exit(0)

if __name__ == "__main__":
    main()