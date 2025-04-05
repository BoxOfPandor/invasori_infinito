#!/usr/bin/env python3

"""
Configurazioni globali del gioco
"""

import pygame

# Inizializza pygame per ottenere le informazioni sul display
pygame.init()

# Ottieni la risoluzione dello schermo
info_schermo = pygame.display.Info()

# Calcola dimensioni sicure (90% della risoluzione dello schermo)
schermo_larghezza_sicura = int(info_schermo.current_w * 0.9)
schermo_altezza_sicura = int(info_schermo.current_h * 0.9)

# Dimensioni della finestra di menu
MENU_LARGHEZZA = 1024
MENU_ALTEZZA = 768

# Dimensioni per la finestra di gioco
GIOCO_LARGHEZZA = 800
GIOCO_ALTEZZA = 600

# Mantieni queste dimensioni come riferimento
LARGHEZZA_SCHERMO = 1024
ALTEZZA_SCHERMO = 768

# Configurazioni della finestra
TITOLO_GIOCO = "Invasori Infinito"

# Configurazioni di gioco
FPS = 60
VELOCITA_GIOCATORE = 300  # pixel al secondo

# Colori
COLORE_NERO = (0, 0, 0)
COLORE_BIANCO = (255, 255, 255)
COLORE_ROSSO = (255, 0, 0)
COLORE_VERDE = (0, 255, 0)
COLORE_BLU = (0, 0, 255)

# Area di gioco
LARGHEZZA_AREA_GIOCO = min(720, GIOCO_LARGHEZZA - 40)  # Larghezza fissa dell'area di gioco
# L'altezza dell'area di gioco si adatterà in base alla proporzione
