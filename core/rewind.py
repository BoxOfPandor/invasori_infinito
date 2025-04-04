#!/usr/bin/env python3

"""
Sistema di rewind temporale
Permette di tornare indietro nel tempo durante il gioco
"""

class GestoreRewind:
    """Gestisce la funzionalità di rewind temporale"""
    
    def __init__(self, capacita_massima=600):  # 10 secondi a 60 FPS
        """Inizializza il gestore di rewind"""
        self.capacita_massima = capacita_massima
        self.stati = []
        self.indice_corrente = -1
    
    def salva_stato(self, stato):
        """Salva uno stato per il rewind"""
        # Se siamo in mezzo alla storia (dopo un rewind), tronca la storia
        if self.indice_corrente < len(self.stati) - 1:
            self.stati = self.stati[:self.indice_corrente + 1]
        
        # Aggiungi il nuovo stato
        self.stati.append(stato)
        self.indice_corrente = len(self.stati) - 1
        
        # Limita la dimensione della storia
        if len(self.stati) > self.capacita_massima:
            self.stati.pop(0)
            self.indice_corrente -= 1
    
    def ottieni_stato_precedente(self):
        """Ottiene lo stato precedente per il rewind"""
        if self.indice_corrente > 0:
            self.indice_corrente -= 1
            return self.stati[self.indice_corrente]
        return None
    
    def ottieni_stato_successivo(self):
        """Ottiene lo stato successivo (avanzamento dopo rewind)"""
        if self.indice_corrente < len(self.stati) - 1:
            self.indice_corrente += 1
            return self.stati[self.indice_corrente]
        return None
    
    def cancella_storia(self):
        """Cancella la storia degli stati"""
        self.stati = []
        self.indice_corrente = -1
    
    def puo_tornare_indietro(self):
        """Verifica se è possibile tornare indietro"""
        return self.indice_corrente > 0
    
    def puo_andare_avanti(self):
        """Verifica se è possibile andare avanti"""
        return self.indice_corrente < len(self.stati) - 1
