#!/usr/bin/env python3

"""
Gestione dei laser sparati dalla nave del giocatore
"""

import pygame

class Laser:
    """Classe che rappresenta un laser sparato dalla nave del giocatore"""

    def __init__(self, x, y, velocita=400):
        """Inizializza un laser"""
        self.larghezza = 4
        self.altezza = 15
        self.x = x
        self.y = y
        self.velocita = velocita
        self.colore = (0, 255, 0)  # Verde
        self.rect = pygame.Rect(self.x, self.y, self.larghezza, self.altezza)
        self.attivo = True

    def aggiorna(self, delta_tempo):
        """Aggiorna la posizione del laser"""
        self.y -= self.velocita * delta_tempo
        self.rect.y = int(self.y)

        # Disattiva il laser se esce dallo schermo
        if self.y < 0:
            self.attivo = False

    def disegna(self, schermo):
        """Disegna il laser sullo schermo"""
        pygame.draw.rect(schermo, self.colore, self.rect)