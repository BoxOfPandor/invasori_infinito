#!/usr/bin/env python3

"""
Gestione dei power-up che possono essere raccolti dal giocatore
"""

import pygame
import random
import os

class PowerUp:
    """Classe che rappresenta un power-up che può essere raccolto dal giocatore"""
    
    # Tipi di power-up
    TIPO_CLEAR_SCREEN = 0    # Elimina tutti i nemici
    TIPO_FIRE_RATE = 1       # Aumenta la velocità di fuoco
    TIPO_SPEED = 2           # Aumenta la velocità di movimento
    TIPO_EXTRA_LIFE = 3      # Aggiunge una vita
    
    def __init__(self, x, y):
        """Inizializza un power-up"""
        self.larghezza = 30
        self.altezza = 30
        self.x = x
        self.y = y
        self.velocita = 120  # Più lento dei nemici per dare tempo di raccoglierlo
        
        # Scegli un tipo casuale di power-up
        self.tipo = random.randint(0, 3)
        
        # Imposta il colore in base al tipo
        self.colori = {
            self.TIPO_CLEAR_SCREEN: (255, 255, 255),  # Bianco per clear screen
            self.TIPO_FIRE_RATE: (0, 191, 255),      # Azzurro per fire rate
            self.TIPO_SPEED: (124, 252, 0),          # Verde lime per velocità
            self.TIPO_EXTRA_LIFE: (255, 0, 127)      # Rosa per vita extra
        }
        self.colore = self.colori[self.tipo]
        
        # Rect per collisioni
        self.rect = pygame.Rect(self.x, self.y, self.larghezza, self.altezza)
        
        # Flag di attività
        self.attivo = True
        
        # Carica immagine
        self.immagine = self.crea_immagine()
    
    def crea_immagine(self):
        """Crea un'immagine per il power-up"""
        superficie = pygame.Surface((self.larghezza, self.altezza), pygame.SRCALPHA)
        
        # Disegna un cerchio con il colore appropriato
        pygame.draw.circle(superficie, self.colore, 
                          (self.larghezza // 2, self.altezza // 2), 
                          self.larghezza // 2)
        
        # Disegna un simbolo al centro in base al tipo
        if self.tipo == self.TIPO_CLEAR_SCREEN:
            # Disegna una X per clear screen
            pygame.draw.line(superficie, (50, 50, 50), 
                            (10, 10), (self.larghezza - 10, self.altezza - 10), 3)
            pygame.draw.line(superficie, (50, 50, 50), 
                            (10, self.altezza - 10), (self.larghezza - 10, 10), 3)
        
        elif self.tipo == self.TIPO_FIRE_RATE:
            # Disegna una freccia doppia per fire rate
            pygame.draw.polygon(superficie, (50, 50, 50), [
                (5, 15), (15, 5), (15, 12), 
                (25, 12), (25, 5), (self.larghezza - 5, 15),
                (25, 25), (25, 18), (15, 18), (15, 25)
            ])
        
        elif self.tipo == self.TIPO_SPEED:
            # Disegna freccia di velocità
            pygame.draw.polygon(superficie, (50, 50, 50), [
                (5, 15), (20, 15), (20, 7), 
                (self.larghezza - 5, self.altezza // 2),
                (20, self.altezza - 7), (20, self.altezza - 15), 
                (5, self.altezza - 15)
            ])
        
        elif self.tipo == self.TIPO_EXTRA_LIFE:
            # Disegna un cuore o un + per vita extra
            pygame.draw.rect(superficie, (50, 50, 50), 
                           (10, 5, 10, 20))
            pygame.draw.rect(superficie, (50, 50, 50), 
                           (5, 10, 20, 10))
        
        return superficie
    
    def aggiorna(self, delta_tempo):
        """Aggiorna la posizione del power-up"""
        # Movimento verso il basso
        self.y += self.velocita * delta_tempo
        self.rect.y = int(self.y)
        
        # Disattiva se esce dallo schermo
        if self.y > 800:
            self.attivo = False
    
    def disegna(self, schermo):
        """Disegna il power-up sullo schermo"""
        schermo.blit(self.immagine, self.rect)
    
    def applica_effetto(self, scena_gioco):
        """Applica l'effetto del power-up raccolto"""
        if self.tipo == self.TIPO_CLEAR_SCREEN:
            # Elimina tutti i nemici
            for nemico in scena_gioco.nemici[:]:
                nemico.attivo = False
                scena_gioco.punteggio += nemico.punti
            scena_gioco.nemici.clear()
            
        elif self.tipo == self.TIPO_FIRE_RATE:
            # Aumenta la velocità di fuoco del 10%
            scena_gioco.nave_giocatore.ritardo_sparo *= 0.9  # Riduzione del 10%
            
        elif self.tipo == self.TIPO_SPEED:
            # Aumenta la velocità di movimento del 10%
            scena_gioco.nave_giocatore.velocita *= 1.1
            
        elif self.tipo == self.TIPO_EXTRA_LIFE:
            # Aggiunge una vita (fino a un massimo di 4)
            if scena_gioco.vite < 4:
                scena_gioco.vite += 1
                # Aggiorna anche il livello di danno della nave
                scena_gioco.nave_giocatore.danno = max(0, 3 - scena_gioco.vite)
                scena_gioco.nave_giocatore.immagine = scena_gioco.nave_giocatore.immagini[scena_gioco.nave_giocatore.danno]
