#!/usr/bin/env python3

"""
Sistema di gestione degli eventi
Gestisce input da tastiera, mouse e altri eventi
"""

import pygame

class GestoreEventi:
    """Classe per gestire gli eventi di input"""
    
    def __init__(self):
        """Inizializza il gestore degli eventi"""
        self.osservatori = []
    
    def aggiungi_osservatore(self, osservatore):
        """Aggiunge un osservatore che riceverà gli eventi"""
        self.osservatori.append(osservatore)
    
    def rimuovi_osservatore(self, osservatore):
        """Rimuove un osservatore dalla lista"""
        if osservatore in self.osservatori:
            self.osservatori.remove(osservatore)
    
    def processa_evento(self, evento):
        """Processa un evento e lo invia a tutti gli osservatori"""
        for osservatore in self.osservatori:
            osservatore.gestisci_evento(evento)

    def controlla_tasto_premuto(self, tasto):
        """Controlla se un tasto specifico è premuto"""
        return pygame.key.get_pressed()[tasto]
    
    def controlla_mouse_premuto(self):
        """Restituisce lo stato dei pulsanti del mouse"""
        return pygame.mouse.get_pressed()
    
    def ottieni_posizione_mouse(self):
        """Restituisce la posizione corrente del mouse"""
        return pygame.mouse.get_pos()
