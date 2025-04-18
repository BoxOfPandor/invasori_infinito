#!/usr/bin/env python3

"""
Scena del menu principale
Gestisce l'interfaccia del menu di avvio
"""

import pygame
import os
import subprocess
from core.scena import Scena
import config

class MenuPrincipale(Scena):
    """Scena del menu principale del gioco"""

    def __init__(self, gioco):
        """Inizializza la scena del menu principale"""
        super().__init__(gioco)
        self.font_titolo = None
        self.font_pulsante = None
        self.colore_titolo = (255, 255, 0)  # Giallo
        self.colore_pulsante = (100, 100, 255)  # Blu chiaro
        self.colore_pulsante_hover = (150, 150, 255)  # Blu più chiaro quando hover
        self.pulsante_start = None
        self.mouse_su_pulsante = False
        self.immagine_sfondo = None
        
        # Konami code: ↑ ↑ ↓ ↓ ← → ← → B A Enter
        self.konami_code = [
            pygame.K_UP, pygame.K_UP,
            pygame.K_DOWN, pygame.K_DOWN,
            pygame.K_LEFT, pygame.K_RIGHT,
            pygame.K_LEFT, pygame.K_RIGHT,
            pygame.K_b, pygame.K_a,
            pygame.K_RETURN
        ]
        self.konami_index = 0
        self.konami_attivato = False
    
    def carica_e_ritaglia_immagine(self, percorso, larghezza_finale, altezza_finale):
        """Carica un'immagine e la ritaglia mantenendo la parte centrale"""
        try:
            # Carica l'immagine originale
            immagine_originale = pygame.image.load(percorso).convert()
            
            # Dimensioni originali
            larghezza_originale = immagine_originale.get_width()
            altezza_originale = immagine_originale.get_height()
            
            # Calcola il rapporto di aspetto
            rapporto_originale = larghezza_originale / altezza_originale
            rapporto_finale = larghezza_finale / altezza_finale
            
            # Determina come ritagliare l'immagine in base ai rapports
            if rapporto_originale > rapporto_finale:
                # L'immagine è troppo large, la rogniamo sur les côtés
                nuova_larghezza = int(altezza_originale * rapporto_finale)
                x_inizio = (larghezza_originale - nuova_larghezza) // 2
                y_inizio = 0
                area_ritaglio = (x_inizio, y_inizio, nuova_larghezza, altezza_originale)
            else:
                # L'immagine è troppo haute, la rogniamo en haut et en bas
                nuova_altezza = int(larghezza_originale / rapporto_finale)
                x_inizio = 0
                y_inizio = (altezza_originale - nuova_altezza) // 2
                area_ritaglio = (x_inizio, y_inizio, larghezza_originale, nuova_altezza)
            
            # Ritaglia l'immagine
            immagine_ritagliata = pygame.Surface((area_ritaglio[2], area_ritaglio[3]))
            immagine_ritagliata.blit(immagine_originale, (0, 0), area_ritaglio)
            
            # Ridimensiona al formato finale
            return pygame.transform.scale(immagine_ritagliata, (larghezza_finale, altezza_finale))
            
        except (pygame.error, FileNotFoundError) as e:
            print(f"Errore nel caricamento dell'immagine: {e}")
            # Fallback: crea una superficie vuota con la dimensione richiesta
            superficie = pygame.Surface((larghezza_finale, altezza_finale))
            superficie.fill((0, 0, 0))  # Riempi di nero
            return superficie
    
    def inizializza(self):
        """Inizializza gli elementi del menu"""
        super().inizializza()
        
        # Carica l'immagine di sfondo
        percorso_immagine = os.path.join("assets", "img", "sfondo_menu.jpg")  # Adjust as needed
        try:
            self.immagine_sfondo = self.carica_e_ritaglia_immagine(
                percorso_immagine,
                config.MENU_LARGHEZZA,  # Usa la larghezza del menu
                config.MENU_ALTEZZA     # Usa l'altezza del menu
            )
        except (pygame.error, FileNotFoundError):
            # Fallback se l'immagine non può essere caricata
            self.immagine_sfondo = pygame.Surface((config.MENU_LARGHEZZA, config.MENU_ALTEZZA))
            self.immagine_sfondo.fill((0, 0, 0))
        
        # Carica i font
        self.font_titolo = pygame.font.SysFont("Arial", 64, bold=True)
        self.font_pulsante = pygame.font.SysFont("Arial", 36)
        
        # Definisci il pulsante di start
        larghezza_pulsante = 200
        altezza_pulsante = 60
        pos_x = (config.MENU_LARGHEZZA - larghezza_pulsante) // 2
        pos_y = (config.MENU_ALTEZZA - altezza_pulsante) // 2 + 50
        
        self.pulsante_start = pygame.Rect(pos_x, pos_y, larghezza_pulsante, altezza_pulsante)
        
        # Aggiungi questo menu come osservatore degli eventi
        self.gioco.gestore_eventi.aggiungi_osservatore(self)
        
        # Reimposta l'indice Konami
        self.konami_index = 0
        self.konami_attivato = False
    
    def termina(self):
        """Pulisce le risorse quando la scena non è più attiva"""
        super().termina()
        
        # Rimuovi questo menu come osservatore degli eventi
        self.gioco.gestore_eventi.rimuovi_osservatore(self)
    
    def attiva_easter_egg(self):
        """Attiva l'easter egg quando il codice Konami è completato"""
        if not self.konami_attivato:
            self.konami_attivato = True
            print("Konami code attivato!")
            
            # Esegue il comando nel terminale
            try:
                subprocess.run(['python3', 'Uova_di_Pasqua/flame_game.py'], check=True)
                
                # Effetto visivo - cambia temporaneamente il titolo
                self.colore_titolo = (255, 0, 0)  # Rosso
                pygame.time.set_timer(pygame.USEREVENT, 2000)  # Timer per resettare dopo 2 secondi
                
            except subprocess.SubprocessError as e:
                print(f"Errore nell'esecuzione del comando: {e}")
    
    def gestisci_evento(self, evento):
        """Gestisce gli eventi del menu"""
        if evento.type == pygame.MOUSEMOTION:
            # Controlla se il mouse è sopra il pulsante
            self.mouse_su_pulsante = self.pulsante_start.collidepoint(evento.pos)
        
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1 and self.mouse_su_pulsante:  # Clic sinistro
                print("Avvio dell'introduzione")
                # Prima passa alla scena di introduzione
                self.gioco.cambia_scena("intro")
        
        elif evento.type == pygame.KEYDOWN:
            tasto_premuto = pygame.key.name(evento.key)
            
            # Verifica se il tasto premuto corrisponde al codice Konami
            if evento.key == self.konami_code[self.konami_index]:
                self.konami_index += 1
                
                # Se l'intero codice è stato inserito correttamente
                if self.konami_index == len(self.konami_code):
                    self.attiva_easter_egg()
                    self.konami_index = 0  # Reimposta per permettere di inserirlo di nuovo
            else:
                # Se viene premuto un tasto sbagliato, reimposta l'indice
                self.konami_index = 0
                
                # Ma controlla se è il primo tasto della sequenza
                if evento.key == self.konami_code[0]:
                    self.konami_index = 1
        
        elif evento.type == pygame.USEREVENT:
            # Reset del colore del titolo dopo l'attivazione dell'easter egg
            self.colore_titolo = (255, 255, 0)  # Torna al giallo originale
            pygame.time.set_timer(pygame.USEREVENT, 0)  # Disattiva il timer
    
    def aggiorna(self, delta_tempo):
        """Aggiorna la logica del menu"""
        pass
    
    def disegna(self, schermo):
        """Disegna gli elementi del menu"""
        # Disegna lo sfondo
        if self.immagine_sfondo:
            schermo.blit(self.immagine_sfondo, (0, 0))
        else:
            # Fallback se l'immagine non può essere caricata
            schermo.fill((0, 0, 0))
        
        # Disegna il titolo
        titolo_surf = self.font_titolo.render("INVASORI INFINITO", True, self.colore_titolo)
        titolo_rect = titolo_surf.get_rect(center=(config.MENU_LARGHEZZA // 2, config.MENU_ALTEZZA // 2 - 50))
        schermo.blit(titolo_surf, titolo_rect)
        
        # Disegna il pulsante di start
        colore_attuale = self.colore_pulsante_hover if self.mouse_su_pulsante else self.colore_pulsante
        pygame.draw.rect(schermo, colore_attuale, self.pulsante_start, border_radius=10)
        pygame.draw.rect(schermo, (255, 255, 255), self.pulsante_start, 2, border_radius=10)  # Bordo bianco
        
        # Testo del pulsante
        testo_start = self.font_pulsante.render("INIZIO", True, (255, 255, 255))
        testo_rect = testo_start.get_rect(center=self.pulsante_start.center)
        schermo.blit(testo_start, testo_rect)
        
        # Mostra piccole stelle per indicare il progresso del codice Konami
        if self.konami_index >= 2:  # Mostra solo dopo aver iniziato la sequenza
            font_stars = pygame.font.SysFont("Arial", 12)
            stars_text = ""
            
            # Aggiungi una stella per ogni tasto corretto inserito
            for i in range(self.konami_index):
                stars_text += "* "
            
            # Mostra stelle in basso
            stars_surf = font_stars.render(stars_text, True, (150, 150, 150))
            schermo.blit(stars_surf, (10, config.MENU_ALTEZZA - 20))
