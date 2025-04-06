#!/usr/bin/env python3

"""
Gestione del boss nemico che appare ogni 2500 punti
"""

import pygame
import random
import os
import math
from logic.laser import Laser

class BossLaser(Laser):
    """Classe che rappresenta un laser sparato dal boss"""
    
    def __init__(self, x, y, velocita=200, colore=(255, 0, 0)):
        """Inizializza un laser del boss"""
        super().__init__(x, y, velocita)
        self.colore = colore  # Rosso per i laser del boss
        
        # Aggiorna la direzione: verso il basso
        self.direzione = 1  # 1 = giù, -1 = su
        
        # Velocità direzionali per lasers delle esplosioni
        self.velocita_x = 0
        self.velocita_y = velocita
        self.direzione_personalizzata = False
        
        # Carica immagine del laser del boss
        self.immagine = self.carica_immagine()
    
    def carica_immagine(self):
        """Carica l'immagine del laser o crea un placeholder"""
        try:
            # Modifié pour utiliser le chemin correct
            percorso = os.path.join("entita", "laser_boss.png")  # ou utiliser un laser générique
            immagine = pygame.image.load(percorso).convert_alpha()
            return pygame.transform.scale(immagine, (self.larghezza, self.altezza))
        except Exception as e:
            print(f"Errore nel caricamento dell'immagine del laser del boss: {e}")
            # Si l'image n'est pas disponible, créer un placeholder
            superficie = pygame.Surface((self.larghezza, self.altezza), pygame.SRCALPHA)
            pygame.draw.rect(superficie, self.colore, (0, 0, self.larghezza, self.altezza))
            return superficie
    
    def aggiorna(self, delta_tempo):
        """Aggiorna la posizione del laser"""
        if self.direzione_personalizzata:
            # Movimento direzionale per i laser delle esplosioni
            self.x += self.velocita_x * delta_tempo
            self.y += self.velocita_y * delta_tempo
            self.rect.x = int(self.x)
            self.rect.y = int(self.y)
        else:
            # Movimento standard verso il basso
            self.y += self.velocita * delta_tempo * self.direzione
            self.rect.y = int(self.y)
        
        # Disattiva il laser se esce dallo schermo
        if self.y > 800 or self.y < 0 or self.x < 0 or self.x > 1200:
            self.attivo = False

class PallaDiFuoco:
    """Classe che rappresenta una palla di fuoco lanciata dal boss che esplode in più laser"""
    
    def __init__(self, x, y, velocita=150):
        """Inizializza una palla di fuoco"""
        self.larghezza = 20
        self.altezza = 20
        self.x = x
        self.y = y
        self.velocita = velocita
        self.colore = (255, 165, 0)  # Arancione
        self.rect = pygame.Rect(self.x, self.y, self.larghezza, self.altezza)
        self.attivo = True
        self.esplosa = False
        self.tempo_esplosione = random.uniform(0.5, 1.5)  # Esplode dopo un tempo casuale
        self.tempo_accumulato = 0
        
        # Carica immagine
        self.immagine = self.carica_immagine()
    
    def carica_immagine(self):
        """Carica l'immagine della palla di fuoco o crea un placeholder"""
        try:
            # Utiliser un chemin plus générique pour la palla di fuoco
            percorso = os.path.join("entita", "fireball.png") 
            immagine = pygame.image.load(percorso).convert_alpha()
            return pygame.transform.scale(immagine, (self.larghezza, self.altezza))
        except Exception as e:
            print(f"Errore nel caricamento dell'immagine della palla di fuoco: {e}")
            # Si l'image n'est pas disponible, créer un placeholder
            superficie = pygame.Surface((self.larghezza, self.altezza), pygame.SRCALPHA)
            pygame.draw.circle(superficie, self.colore, 
                             (self.larghezza // 2, self.altezza // 2),
                             self.larghezza // 2)
            return superficie
    
    def aggiorna(self, delta_tempo):
        """Aggiorna la posizione della palla di fuoco e controlla se deve esplodere"""
        self.y += self.velocita * delta_tempo
        self.rect.y = int(self.y)
        
        # Aggiorna il tempo accumulato
        self.tempo_accumulato += delta_tempo
        
        # Verifica se è ora di esplodere
        if self.tempo_accumulato >= self.tempo_esplosione:
            self.esplosa = True
            self.attivo = False
        
        # Disattiva se esce dallo schermo
        if self.y > 800:
            self.attivo = False
    
    def esplodi(self):
        """Crea i laser dell'esplosione"""
        laser_esplosione = []
        
        # Crea 8 laser in direzioni diverse
        for i in range(8):
            angolo = i * 45  # Angoli: 0, 45, 90, 135, 180, 225, 270, 315
            radianti = math.radians(angolo)
            
            # Calcola la direzione in base all'angolo
            dx = math.cos(radianti)
            dy = math.sin(radianti)
            
            # Crea un nuovo laser nella posizione della palla di fuoco
            laser = BossLaser(self.x + (self.larghezza / 2), self.y + (self.altezza / 2))
            
            # Imposta la velocità in base alla direzione
            laser.velocita_x = dx * 150
            laser.velocita_y = dy * 150
            laser.direzione_personalizzata = True  # Indica che ha una direzione personalizzata
            
            laser_esplosione.append(laser)
        
        return laser_esplosione
    
    def disegna(self, schermo):
        """Disegna la palla di fuoco sullo schermo"""
        schermo.blit(self.immagine, self.rect)


class Boss:
    """Classe che rappresenta il boss nemico"""
    
    def __init__(self, area_gioco, livello=1):
        """Inizializza il boss"""
        self.area_gioco = area_gioco
        self.livello = livello  # Livello del boss, aumenta la difficoltà
        self.larghezza = 100
        self.altezza = 80
        
        # Posizione: centra il boss nella parte superiore dell'area di gioco
        self.x = area_gioco.centerx - self.larghezza // 2
        self.y = 50  # Distanza dall'alto
        
        # Velocità e movimento
        self.velocita_base = 80
        self.velocita = self.velocita_base + (self.livello * 10)  # Aumenta con il livello
        self.direzione = random.choice([-1, 1])  # -1 = sinistra, 1 = destra
        self.tempo_cambio_direzione = random.uniform(1.5, 3.0)  # Secondi prima di cambiare direzione
        self.tempo_accumulato = 0
        
        # Stato del boss
        self.attivo = True
        self.sconfitto = False
        
        # Salute
        self.salute_massima = 10 + (self.livello * 5)  # Aumenta con il livello
        self.salute = self.salute_massima
        
        # Tiro
        self.ritardo_tiro_base = 2.0  # Secondi tra un tiro e l'altro
        self.ritardo_tiro = max(0.5, self.ritardo_tiro_base - (self.livello * 0.2))  # Diminuisce con il livello
        self.tempo_ultimo_tiro = 0
        
        # Lancio palle di fuoco (dal livello 2 in poi)
        self.usa_palle_fuoco = livello >= 2
        self.ritardo_palla_fuoco = max(3.0, 5.0 - (self.livello * 0.5))
        self.tempo_ultima_palla_fuoco = 0
        
        # Rettangolo di collisione
        self.rect = pygame.Rect(self.x, self.y, self.larghezza, self.altezza)
        
        # Carica l'immagine
        self.immagine = self.carica_immagine()
        
        # Barra della salute
        self.colore_barra_salute = (255, 0, 0)  # Rosso
        self.colore_sfondo_barra = (50, 50, 50)  # Grigio scuro
    
    def carica_immagine(self):
        """Carica l'immagine del boss"""
        try:
            # Utiliser le chemin indiqué dans les commentaires
            percorso = os.path.join("entita", "boss.png")
            immagine = pygame.image.load(percorso).convert_alpha()
            return pygame.transform.scale(immagine, (self.larghezza, self.altezza))
        except Exception as e:
            print(f"Errore nel caricamento dell'immagine del boss: {e}")
            # Si l'image n'est pas disponible, créer un placeholder
            superficie = pygame.Surface((self.larghezza, self.altezza), pygame.SRCALPHA)
            pygame.draw.rect(superficie, (255, 0, 0), (0, 0, self.larghezza, self.altezza))
            return superficie
    
    def aggiorna(self, delta_tempo):
        """Aggiorna la posizione e il comportamento del boss"""
        # Aggiorna il tempo accumulato
        self.tempo_accumulato += delta_tempo
        
        # Cambia direzione dopo un certo tempo
        if self.tempo_accumulato >= self.tempo_cambio_direzione:
            self.direzione = random.choice([-1, 1])
            self.tempo_cambio_direzione = random.uniform(1.5, 3.0)
            self.tempo_accumulato = 0
        
        # Aggiorna la posizione
        self.x += self.velocita * delta_tempo * self.direzione
        
        # Controlla i limiti dell'area di gioco
        if self.x < self.area_gioco.left:
            self.x = self.area_gioco.left
            self.direzione *= -1  # Cambia direzione
        elif self.x + self.larghezza > self.area_gioco.right:
            self.x = self.area_gioco.right - self.larghezza
            self.direzione *= -1  # Cambia direzione
        
        # Aggiorna il rettangolo di collisione
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
    
    def spara(self, tempo_corrente):
        """Verifica se il boss deve sparare e crea un laser se necessario"""
        # Verifica se è passato abbastanza tempo dall'ultimo tiro
        if tempo_corrente - self.tempo_ultimo_tiro >= self.ritardo_tiro * 1000:  # Converti in millisecondi
            self.tempo_ultimo_tiro = tempo_corrente
            
            # Crea un laser al centro inferiore del boss
            x_laser = self.x + (self.larghezza // 2) - 4  # 4 è metà della larghezza del laser
            y_laser = self.y + self.altezza + 5  # Poco sotto il boss
            
            return BossLaser(x_laser, y_laser)
        
        return None
    
    def lancia_palla_fuoco(self, tempo_corrente):
        """Verifica se il boss deve lanciare una palla di fuoco"""
        # Verifica se il boss può lanciare palle di fuoco e se è passato abbastanza tempo
        if self.usa_palle_fuoco and tempo_corrente - self.tempo_ultima_palla_fuoco >= self.ritardo_palla_fuoco * 1000:
            self.tempo_ultima_palla_fuoco = tempo_corrente
            
            # Crea una palla di fuoco in posizione casuale sotto il boss
            x_palla = self.x + random.randint(0, self.larghezza - 20)
            y_palla = self.y + self.altezza + 10
            
            return PallaDiFuoco(x_palla, y_palla)
        
        return None
    
    def prendi_danno(self, danno=1):
        """Riduce la salute del boss quando colpito"""
        self.salute -= danno
        
        # Controlla se il boss è stato sconfitto
        if self.salute <= 0:
            self.attivo = False
            self.sconfitto = True
            return True  # Boss sconfitto
        
        return False  # Boss ancora attivo
    
    def disegna(self, schermo):
        """Disegna il boss e la barra della salute"""
        # Disegna il boss
        schermo.blit(self.immagine, self.rect)
        
        # Disegna la barra della salute
        larghezza_barra = 100
        altezza_barra = 10
        x_barra = self.x
        y_barra = self.y - 20
        
        # Sfondo della barra
        pygame.draw.rect(schermo, self.colore_sfondo_barra, (x_barra, y_barra, larghezza_barra, altezza_barra))
        
        # Barra della salute
        percentuale_salute = self.salute / self.salute_massima
        larghezza_attuale = larghezza_barra * percentuale_salute
        pygame.draw.rect(schermo, self.colore_barra_salute, (x_barra, y_barra, larghezza_attuale, altezza_barra))
    
    def collide_con(self, altro_rect):
        """Controlla se il boss collide con un altro rettangolo"""
        return self.rect.colliderect(altro_rect)
