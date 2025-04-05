#!/usr/bin/env python3

"""
Configurazioni globali del gioco
"""

import pygame

# Inizializza pygame per ottenere le informazioni sul display
pygame.init()

# Ottieni la risoluzione dello schermo
info_schermo = pygame.display.Info()
LARGHEZZA_SCHERMO = info_schermo.current_w
ALTEZZA_SCHERMO = info_schermo.current_h

# Configurazioni della finestra
TITOLO_GIOCO = "Invasori Infinito"

# Se si desidera utilizzare una percentuale della risoluzione dello schermo
# LARGHEZZA_SCHERMO = int(info_schermo.current_w * 0.8)  # 80% della larghezza
# ALTEZZA_SCHERMO = int(info_schermo.current_h * 0.8)    # 80% dell'altezza

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
LARGHEZZA_AREA_GIOCO = 720  # Larghezza fissa dell'area di gioco
# L'altezza dell'area di gioco si adatterà in base alla proporzione