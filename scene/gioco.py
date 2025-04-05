#!/usr/bin/env python3

"""
Scena del gioco principale
Gestisce il gameplay principale
"""

import pygame
import os
import random  # Add this import
from core.scena import Scena
import config
from logic.laser import Laser
from logic.nemico import Nemico


class ScenaGioco(Scena):
    """Scena principale del gioco"""

    def __init__(self, gioco):
        """Inizializza la scena di gioco"""
        super().__init__(gioco)
        self.sfondo = None
        self.area_gioco = None
        self.margine_laterale = 0
        self.nave_giocatore = None
        self.lasers = []  # Lista per tenere traccia dei laser attivi
        self.nemici = []
        self.vite = 5  # Giocatore inizia con 5 vite
        self.game_over_status = False

        # Parametri di spawn dei nemici
        self.intervallo_spawn_base = 1500  # Intervallo base (1.5 secondi)
        self.intervallo_spawn_minimo = 300  # Intervallo minimo (0.3 secondi)
        self.tempo_ultimo_spawn = 0

    def calcola_intervallo_spawn(self):
        """Calcola l'intervallo di spawn in base al punteggio"""
        # Formula: ogni 100 punti, diminuisce l'intervallo del 10%
        # fino a raggiungere l'intervallo minimo
        riduzione = min(self.punteggio // 100 * 0.1, 0.8)  # Max 80% di riduzione
        intervallo = self.intervallo_spawn_base * (1 - riduzione)

        # Assicura che l'intervallo non scenda sotto il minimo
        return max(int(intervallo), self.intervallo_spawn_minimo)

    def inizializza(self):
        """Inizializza gli elementi del gioco"""
        super().inizializza()

        # Carica l'immagine di sfondo
        percorso_sfondo = os.path.join("assets", "img", "sfondo_gioco.jpg")
        try:
            self.sfondo = self.carica_e_ritaglia_immagine(
                percorso_sfondo,
                config.GIOCO_LARGHEZZA,
                config.GIOCO_ALTEZZA
            )
        except Exception as e:
            print(f"Errore nel caricamento dello sfondo: {e}")
            # Fallback se l'immagine non può essere caricata
            self.sfondo = pygame.Surface((config.GIOCO_LARGHEZZA, config.GIOCO_ALTEZZA))
            self.sfondo.fill((0, 0, 0))  # Sfondo nero

        # Definisci l'area di gioco con larghezza proporzionata
        larghezza_area_gioco = min(int(config.GIOCO_LARGHEZZA * 0.9), 720)
        self.margine_laterale = (config.GIOCO_LARGHEZZA - larghezza_area_gioco) // 2
        self.area_gioco = pygame.Rect(
            self.margine_laterale,
            0,
            larghezza_area_gioco,
            config.GIOCO_ALTEZZA
        )

        # Crea la nave del giocatore
        self.nave_giocatore = Nave(self.area_gioco)

        # Aggiungi questa scena come osservatore degli eventi
        self.gioco.gestore_eventi.aggiungi_osservatore(self)

        # Inizializza lista nemici e timing
        self.nemici = []
        self.tempo_ultimo_spawn = pygame.time.get_ticks()
        self.intervallo_spawn = 1500  # 1.5 secondi tra gli spawn
        self.punteggio = 0

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
                # L'immagine è troppo larga, la ritaglia sui lati
                nuova_larghezza = int(altezza_originale * rapporto_finale)
                x_inizio = (larghezza_originale - nuova_larghezza) // 2
                y_inizio = 0
                area_ritaglio = (x_inizio, y_inizio, nuova_larghezza, altezza_originale)
            else:
                # L'immagine è troppo alta, la ritaglia in alto e in basso
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

    def termina(self):
        """Pulisce le risorse quando la scena non è più attiva"""
        super().termina()

        # Rimuovi questa scena come osservatore degli eventi
        self.gioco.gestore_eventi.rimuovi_osservatore(self)

    def gestisci_evento(self, evento):
        """Gestisce gli eventi di input"""
        if evento.type == pygame.USEREVENT:
            # Timer per il game over
            pygame.time.set_timer(pygame.USEREVENT, 0)  # Disattiva il timer
            self.gioco.cambia_scena("menu")
            return

        if self.game_over_status:
            return

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                self.nave_giocatore.movimento_sinistra = True
            elif evento.key == pygame.K_RIGHT:
                self.nave_giocatore.movimento_destra = True
            elif evento.key == pygame.K_UP:
                self.nave_giocatore.sparo_attivo = True

        elif evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT:
                self.nave_giocatore.movimento_sinistra = False
            elif evento.key == pygame.K_RIGHT:
                self.nave_giocatore.movimento_destra = False
            elif evento.key == pygame.K_UP:
                self.nave_giocatore.sparo_attivo = False

    def aggiorna(self, delta_tempo):
        """Aggiorna la logica del gioco"""
        # Controlla se game over
        if self.game_over_status:
            return

        # Aggiorna la nave del giocatore
        self.nave_giocatore.aggiorna(delta_tempo)

        # Gestione sparo continuo
        tempo_corrente = pygame.time.get_ticks()
        if self.nave_giocatore.sparo_attivo:
            nuovo_laser = self.nave_giocatore.spara(tempo_corrente)
            if nuovo_laser:
                self.lasers.append(nuovo_laser)

        # Aggiorna tutti i laser attivi
        for laser in self.lasers[:]:
            laser.aggiorna(delta_tempo)
            if not laser.attivo:
                self.lasers.remove(laser)

        # Nel metodo aggiorna, sostituisci:
        # if tempo_corrente - self.tempo_ultimo_spawn > self.intervallo_spawn:
        # con:
        if tempo_corrente - self.tempo_ultimo_spawn > self.calcola_intervallo_spawn():
            self.spawn_nemico()
            self.tempo_ultimo_spawn = tempo_corrente

        # Aggiorna tutti i nemici attivi e controlla collisioni con giocatore
        for nemico in self.nemici[:]:
            nemico.aggiorna(delta_tempo)

            # Controlla se il nemico ha toccato il fondo
            if nemico.rect.bottom >= self.nave_giocatore.rect.top:
                self.perdi_vita()
                nemico.attivo = False

            # Controlla se il nemico ha colpito il giocatore
            elif nemico.collide_con(self.nave_giocatore.rect):
                self.perdi_vita()
                nemico.attivo = False

            # Rimuovi nemici non attivi
            if not nemico.attivo:
                self.nemici.remove(nemico)

        # Controlla collisioni laser-nemico
        for laser in self.lasers[:]:
            for nemico in self.nemici[:]:
                if nemico.collide_con(laser.rect):
                    laser.attivo = False
                    if nemico.prendi_danno(1):  # Nemico distrutto
                        self.punteggio += nemico.punti
                    break

    def perdi_vita(self):
        """Gestisce la perdita di una vita"""
        self.vite -= 1
        # Controlla se il gioco è finito
        if self.vite <= 0:
            self.game_over()

    def game_over(self):
        """Gestisce la fine del gioco"""
        self.game_over_status = True
        print("Game Over!")
        # Torna al menu dopo un breve ritardo
        pygame.time.set_timer(pygame.USEREVENT, 2000)  # 2 secondi di attesa

    def spawn_nemico(self):
        """Spawna un nuovo nemico in una posizione casuale"""
        # Calcola una posizione x casuale all'interno dell'area di gioco
        min_x = self.area_gioco.left + 10
        max_x = self.area_gioco.right - 70
        x_pos = random.randint(min_x, max_x)

        # Tipo di nemico casuale (1, 2 o 3)
        tipo = random.randint(1, 3)

        # Crea il nemico appena sopra lo schermo
        nemico = Nemico(x_pos, -50, tipo)

        # Aggiungi alla lista dei nemici attivi
        self.nemici.append(nemico)

    def disegna(self, schermo):
        """Disegna gli elementi del gioco"""
        # Disegna lo sfondo su tutto lo schermo
        schermo.blit(self.sfondo, (0, 0))

        # Disegna un bordo per l'area di gioco
        pygame.draw.rect(schermo, (100, 100, 100), self.area_gioco, 2)

        # Disegna la nave del giocatore
        self.nave_giocatore.disegna(schermo)

        # Disegna tutti i laser attivi
        for laser in self.lasers:
            laser.disegna(schermo)

        # Disegna tutti i nemici attivi
        for nemico in self.nemici:
            nemico.disegna(schermo)

        # Disegna il punteggio e le vite
        font = pygame.font.SysFont("Arial", 24)
        testo_punteggio = font.render(f"Punti: {self.punteggio}", True, (255, 255, 255))
        schermo.blit(testo_punteggio, (self.area_gioco.left + 10, 20))

        testo_vite = font.render(f"Vite: {self.vite}", True, (255, 255, 255))
        schermo.blit(testo_vite, (self.area_gioco.right - testo_vite.get_width() - 10, 20))

        # Mostra game over
        if self.game_over_status:
            font_game_over = pygame.font.SysFont("Arial", 72, bold=True)
            testo_game_over = font_game_over.render("GAME OVER", True, (255, 0, 0))
            pos_x = (self.gioco.schermo.get_width() - testo_game_over.get_width()) // 2
            pos_y = (self.gioco.schermo.get_height() - testo_game_over.get_height()) // 2
            schermo.blit(testo_game_over, (pos_x, pos_y))

    def salva_stato(self):
        """Salva lo stato attuale per il rewind"""
        return {
            'nave_x': self.nave_giocatore.x,
            'nave_y': self.nave_giocatore.y,
            'lasers': [(laser.x, laser.y) for laser in self.lasers]
        }

    def carica_stato(self, stato):
        """Carica uno stato salvato durante il rewind"""
        if stato and 'nave_x' in stato:
            self.nave_giocatore.x = stato['nave_x']
            self.nave_giocatore.y = stato['nave_y']
            self.nave_giocatore.rect.x = int(self.nave_giocatore.x)
            self.nave_giocatore.rect.y = int(self.nave_giocatore.y)

            # Ricrea i laser nella posizione salvata
            self.lasers = []
            if 'lasers' in stato:
                for pos_laser in stato['lasers']:
                    self.lasers.append(Laser(pos_laser[0], pos_laser[1]))


class Nave:
    """Classe che rappresenta la nave del giocatore"""

    def __init__(self, area_gioco):
        """Inizializza la nave del giocatore"""
        self.area_gioco = area_gioco
        self.larghezza = 40
        self.altezza = 40
        self.x = area_gioco.centerx - self.larghezza // 2
        self.y = area_gioco.bottom - self.altezza - 10

        # Rect per collisioni e disegno
        self.rect = pygame.Rect(self.x, self.y, self.larghezza, self.altezza)

        # Movimento
        self.velocita = config.VELOCITA_GIOCATORE
        self.movimento_sinistra = False
        self.movimento_destra = False

        # Sparo
        self.sparo_attivo = False
        self.ritardo_sparo = 150  # Millisecondi tra uno sparo e l'altro
        self.tempo_ultimo_sparo = 0

        # Carica l'immagine
        self.immagine = self.carica_immagine()

    def carica_immagine(self):
        """Carica l'immagine della nave o crea un placeholder"""
        try:
            percorso = os.path.join("assets", "img", "nave.png")
            immagine = pygame.image.load(percorso).convert_alpha()
            return pygame.transform.scale(immagine, (self.larghezza, self.altezza))
        except:
            # Se l'immagine non è disponibile, crea un placeholder
            superficie = pygame.Surface((self.larghezza, self.altezza), pygame.SRCALPHA)
            pygame.draw.polygon(superficie, (0, 255, 0), [
                (self.larghezza // 2, 0),
                (0, self.altezza),
                (self.larghezza, self.altezza)
            ])
            return superficie

    def aggiorna(self, delta_tempo):
        """Aggiorna la posizione della nave"""
        if self.movimento_sinistra and not self.movimento_destra:
            self.x -= self.velocita * delta_tempo
        if self.movimento_destra and not self.movimento_sinistra:
            self.x += self.velocita * delta_tempo

        # Controlla i limiti dell'area di gioco
        if self.x < self.area_gioco.left:
            self.x = self.area_gioco.left
        elif self.x + self.larghezza > self.area_gioco.right:
            self.x = self.area_gioco.right - self.larghezza

        # Aggiorna il rettangolo di collisione
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def spara(self, tempo_corrente):
        """Spara un laser se è possibile"""
        # Verifica che sia passato abbastanza tempo dall'ultimo sparo
        if tempo_corrente - self.tempo_ultimo_sparo < self.ritardo_sparo:
            return None

        # Crea un nuovo laser al centro della nave
        x_laser = self.x + (self.larghezza // 2) - 2  # 2 è metà della larghezza del laser
        y_laser = self.y - 5  # Poco sopra la nave

        self.tempo_ultimo_sparo = tempo_corrente
        return Laser(x_laser, y_laser)

    def disegna(self, schermo):
        """Disegna la nave sullo schermo"""
        schermo.blit(self.immagine, self.rect)