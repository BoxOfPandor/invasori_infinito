#!/usr/bin/env python3

"""
Gestione dei nemici che attaccano il giocatore
"""

import pygame
import random
import os

class Nemico:
    """Classe che rappresenta un nemico"""

    def __init__(self, x, y, tipo=1):
        """Inizializza un nemico"""
        self.tipo = tipo

        # Dimensioni in base al tipo
        if tipo == 1:  # Nemico piccolo
            self.larghezza = 40
            self.altezza = 30
            self.velocita = 100
            self.colore = (255, 0, 0)  # Rosso
            self.punti = 10
            self.salute = 1  # Nemico debole, muore con un colpo
        elif tipo == 2:  # Nemico medio
            self.larghezza = 50
            self.altezza = 40
            self.velocita = 80
            self.colore = (255, 100, 0)  # Arancione
            self.punti = 20
            self.salute = 2  # Nemico medio, richiede due colpi
        else:  # Nemico grande/boss
            self.larghezza = 70
            self.altezza = 50
            self.velocita = 60
            self.colore = (255, 0, 100)  # Fucsia
            self.punti = 30
            self.salute = 3  # Nemico resistente, richiede tre colpi

        # Posizione
        self.x = x
        self.y = y

        # Rect per collisioni e disegno
        self.rect = pygame.Rect(self.x, self.y, self.larghezza, self.altezza)

        # Carica immagine
        self.immagine = self.carica_immagine()

        # Flag di attività
        self.attivo = True

    def prendi_danno(self, danno=1):
        """Riduce la salute del nemico quando colpito"""
        self.salute -= danno
        if self.salute <= 0:
            self.attivo = False
            return True  # Nemico distrutto
        return False  # Nemico ancora attivo

    def carica_immagine(self):
        """Carica l'immagine del nemico o crea un placeholder"""
        try:
            percorso = os.path.join("assets", "img", f"nemico{self.tipo}.png")
            immagine = pygame.image.load(percorso).convert_alpha()
            return pygame.transform.scale(immagine, (self.larghezza, self.altezza))
        except:
            # Se l'immagine non è disponibile, crea un placeholder
            superficie = pygame.Surface((self.larghezza, self.altezza), pygame.SRCALPHA)
            pygame.draw.rect(superficie, self.colore, (0, 0, self.larghezza, self.altezza))
            return superficie

    def aggiorna(self, delta_tempo):
        """Aggiorna la posizione del nemico"""
        # Movimento verso il basso
        self.y += self.velocita * delta_tempo
        self.rect.y = int(self.y)

        # Disattiva se esce dallo schermo
        if self.y > 800:  # Usa un valore abbastanza grande per assicurarsi che sia fuori schermo
            self.attivo = False

    def disegna(self, schermo):
        """Disegna il nemico sullo schermo"""
        schermo.blit(self.immagine, self.rect)

    def collide_con(self, altro_rect):
        """Controlla se il nemico collide con un altro rettangolo"""
        return self.rect.colliderect(altro_rect)