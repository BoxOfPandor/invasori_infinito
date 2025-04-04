#!/usr/bin/env python3

"""
Modulo del motore di gioco principale
Gestisce il loop di gioco, il rendering e l'aggiornamento
"""

import pygame
import time
from core.eventi import GestoreEventi
from core.scena import GestoreScene

class Gioco:
    """Classe principale che gestisce il gioco"""
    
    def __init__(self, titolo, larghezza, altezza, fps):
        """Inizializza il gioco"""
        self.titolo = titolo
        self.larghezza = larghezza
        self.altezza = altezza
        self.fps = fps
        
        # Creazione della finestra
        self.schermo = pygame.display.set_mode((larghezza, altezza))
        pygame.display.set_caption(titolo)
        
        # Orologio per controllare gli FPS
        self.orologio = pygame.time.Clock()
        
        # Gestore di eventi
        self.gestore_eventi = GestoreEventi()
        
        # Gestore delle scene
        self.gestore_scene = GestoreScene(self)
        
        # Stato del gioco
        self.in_esecuzione = False
        self.tempo_attuale = 0
        self.tempo_precedente = 0
        self.delta_tempo = 0
        
        # Flag per il rewind
        self.modalita_rewind = False
    
    def esegui(self):
        """Avvia il loop principale del gioco"""
        self.in_esecuzione = True
        self.tempo_precedente = time.time()
        
        while self.in_esecuzione:
            # Calcolo del delta tempo
            self.tempo_attuale = time.time()
            self.delta_tempo = self.tempo_attuale - self.tempo_precedente
            self.tempo_precedente = self.tempo_attuale
            
            # Gestione eventi
            self.elabora_eventi()
            
            # Aggiornamento logica
            self.aggiorna()
            
            # Rendering
            self.disegna()
            
            # Controllo FPS
            self.orologio.tick(self.fps)
    
    def elabora_eventi(self):
        """Elabora tutti gli eventi di input"""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.in_esecuzione = False
            
            # Passa l'evento al gestore
            self.gestore_eventi.processa_evento(evento)
    
    def aggiorna(self):
        """Aggiorna la logica del gioco"""
        if self.modalita_rewind:
            self.gestore_scene.rewind(self.delta_tempo)
        else:
            self.gestore_scene.aggiorna(self.delta_tempo)
    
    def disegna(self):
        """Disegna gli elementi sullo schermo"""
        # Pulisci lo schermo
        self.schermo.fill((0, 0, 0))
        
        # Disegna la scena corrente
        self.gestore_scene.disegna(self.schermo)
        
        # Aggiorna lo schermo
        pygame.display.flip()
    
    def cambia_scena(self, nome_scena):
        """Cambia la scena corrente"""
        self.gestore_scene.cambia_scena(nome_scena)
    
    def attiva_rewind(self):
        """Attiva la modalità rewind"""
        self.modalita_rewind = True
    
    def disattiva_rewind(self):
        """Disattiva la modalità rewind"""
        self.modalita_rewind = False
    
    def termina(self):
        """Termina il gioco"""
        self.in_esecuzione = False
