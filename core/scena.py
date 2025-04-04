#!/usr/bin/env python3

"""
Sistema di gestione delle scene del gioco
Gestisce transizioni tra menu, gameplay, game over, ecc.
"""

class Scena:
    """Classe base per tutte le scene del gioco"""
    
    def __init__(self, gioco):
        """Inizializza la scena"""
        self.gioco = gioco
        self.attivo = False
    
    def inizializza(self):
        """Inizializza la scena quando diventa attiva"""
        self.attivo = True
    
    def termina(self):
        """Pulisce la scena quando non è più attiva"""
        self.attivo = False
    
    def gestisci_evento(self, evento):
        """Gestisce gli eventi specifici della scena"""
        pass
    
    def aggiorna(self, delta_tempo):
        """Aggiorna la logica della scena"""
        pass
    
    def disegna(self, schermo):
        """Disegna la scena sullo schermo"""
        pass
    
    def salva_stato(self):
        """Salva lo stato attuale per il rewind"""
        return {}
    
    def carica_stato(self, stato):
        """Carica uno stato salvato durante il rewind"""
        pass


class GestoreScene:
    """Gestisce le scene e le transizioni tra di esse"""
    
    def __init__(self, gioco):
        """Inizializza il gestore delle scene"""
        self.gioco = gioco
        self.scene = {}
        self.scena_corrente = None
        self.storia_stati = []
    
    def aggiungi_scena(self, nome, scena):
        """Aggiunge una scena al gestore"""
        self.scene[nome] = scena
    
    def cambia_scena(self, nome):
        """Cambia la scena corrente"""
        if nome in self.scene:
            if self.scena_corrente:
                self.scena_corrente.termina()
            
            self.scena_corrente = self.scene[nome]
            self.scena_corrente.inizializza()
    
    def aggiorna(self, delta_tempo):
        """Aggiorna la scena corrente"""
        if self.scena_corrente:
            # Salva lo stato corrente per il rewind
            stato = self.scena_corrente.salva_stato()
            self.storia_stati.append(stato)
            
            # Limita la dimensione della storia
            if len(self.storia_stati) > 1000:
                self.storia_stati.pop(0)
            
            # Aggiorna la scena
            self.scena_corrente.aggiorna(delta_tempo)
    
    def disegna(self, schermo):
        """Disegna la scena corrente"""
        if self.scena_corrente:
            self.scena_corrente.disegna(schermo)
    
    def rewind(self, delta_tempo):
        """Esegue il rewind se ci sono stati salvati"""
        if self.storia_stati and self.scena_corrente:
            stato = self.storia_stati.pop()
            self.scena_corrente.carica_stato(stato)
