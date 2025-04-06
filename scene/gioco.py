#!/usr/bin/env python3

"""
Scena del gioco principale
Gestisce il gameplay principale
"""

import pygame
import os
import random
import math  # Aggiunto import per la funzione sin
from core.scena import Scena
import config
from logic.laser import Laser
from logic.nemico import Nemico
from logic.power_up import PowerUp
from logic.boss import Boss, BossLaser, PallaDiFuoco


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
        self.power_ups = []  # Lista per i power-up attivi
        self.vite = 4  # Giocatore inizia con 4 vite
        self.game_over_status = False

        # Parametri di spawn dei nemici
        self.intervallo_spawn_base = 1500  # Intervallo base (1.5 secondi)
        self.intervallo_spawn_minimo = 300  # Intervallo minimo (0.3 secondi)
        self.tempo_ultimo_spawn = 0

        # Parametri per lo spawn dei power-up basato sul punteggio
        self.punteggio_ultimo_power_up = 0
        self.punteggio_intervallo_power_up = 500  # Spawn power-up ogni 500 punti

        # Parametri per il messaggio power-up
        self.messaggio_power_up = ""
        self.tempo_messaggio_power_up = 0
        self.durata_messaggio_power_up = 3000  # 3 secondi in millisecondi

        # Parametri per il boss
        self.boss = None
        self.laser_boss = []  # Laser sparati dal boss
        self.palle_fuoco = []  # Palle di fuoco lanciate dal boss
        self.punteggio_ultimo_boss = 0
        self.punteggio_intervallo_boss = 2500  # Boss ogni 2500 punti
        self.livello_boss = 0  # Livello del boss (aumenta ogni volta che viene sconfitto)
        self.boss_attivo = False

    def calcola_intervallo_spawn(self):
        """Calcola l'intervallo di spawn in base al punteggio"""
        # Calcola un valore di oscillazione tra 0 e 0.3 (30%) basato sul tempo
        tempo_corrente = pygame.time.get_ticks()
        oscillazione = 0.3 * (0.5 + 0.5 * math.sin(tempo_corrente / 5000))  # Oscillazione tra 0 e 0.3 con periodo di 10 secondi

        if self.punteggio <= 2000:
            # Progressione lineare fino a 2000 punti
            riduzione = min(self.punteggio / 2000 * 0.8, 0.8)  # Max 80% di riduzione a 2000 punti
        else:
            # Dopo 2000 punti, mantiene la difficoltà massima con oscillazione
            riduzione = 0.8 - oscillazione  # Oscillazione tra 50% e 80% di riduzione

        intervallo = self.intervallo_spawn_base * (1 - riduzione)

        # Assicura che l'intervallo non scenda sotto il minimo
        return max(int(intervallo), self.intervallo_spawn_minimo)

    def inizializza(self):
        """Inizializza gli elementi del gioco"""
        super().inizializza()

        # Reset game state
        self.game_over_status = False
        self.vite = 4
        self.punteggio = 0
        self.punteggio_ultimo_power_up = 0
        self.punteggio_ultimo_boss = 0
        self.livello_boss = 0
        self.boss = None
        self.boss_attivo = False
        self.laser_boss.clear()
        self.palle_fuoco.clear()
        self.lasers.clear()
        self.nemici.clear()
        self.power_ups.clear()
        self.messaggio_power_up = ""
        self.tempo_messaggio_power_up = 0

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

    def mostra_messaggio_power_up(self, tipo_power_up):
        """Mostra un messaggio che indica quale power-up è stato raccolto"""
        messaggi = {
            PowerUp.TIPO_CLEAR_SCREEN: "ELIMINA NEMICI!",
            PowerUp.TIPO_FIRE_RATE: "VELOCITÀ DI FUOCO +10%!",
            PowerUp.TIPO_SPEED: "VELOCITÀ MOVIMENTO +10%!",
            PowerUp.TIPO_EXTRA_LIFE: "VITA EXTRA!"
        }

        self.messaggio_power_up = messaggi.get(tipo_power_up, "POWER-UP!")
        self.tempo_messaggio_power_up = pygame.time.get_ticks()

    def mostra_messaggio_boss(self, sconfitto=False):
        """Mostra un messaggio che indica l'arrivo o la sconfitta del boss"""
        if sconfitto:
            self.messaggio_power_up = f"BOSS SCONFITTO! +{500 * self.livello_boss} PUNTI!"
        else:
            self.messaggio_power_up = f"BOSS LIVELLO {self.livello_boss} IN ARRIVO!"

        self.tempo_messaggio_power_up = pygame.time.get_ticks()

    def controlla_boss(self):
        """Controlla se è ora di far apparire il boss"""
        if not self.boss_attivo and self.punteggio - self.punteggio_ultimo_boss >= self.punteggio_intervallo_boss:
            self.livello_boss += 1
            self.boss = Boss(self.area_gioco, self.livello_boss)
            self.boss_attivo = True
            self.mostra_messaggio_boss(False)  # Mostra messaggio di arrivo boss
            
            # Elimina tutti i nemici rimanenti sul campo
            for nemico in self.nemici[:]:
                nemico.attivo = False
            self.nemici.clear()
            
            return True
        return False

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

        # Controlla se è ora di far apparire il boss
        self.controlla_boss()

        # Gestione del boss attivo
        if self.boss_attivo and self.boss:
            # Aggiorna il boss
            self.boss.aggiorna(delta_tempo)

            # Boss spara laser
            nuovo_laser = self.boss.spara(tempo_corrente)
            if nuovo_laser:
                self.laser_boss.append(nuovo_laser)

            # Boss lancia palle di fuoco (dal livello 2 in poi)
            if self.livello_boss >= 2:
                nuova_palla = self.boss.lancia_palla_fuoco(tempo_corrente)
                if nuova_palla:
                    self.palle_fuoco.append(nuova_palla)

            # Aggiorna tutti i laser del boss
            for laser in self.laser_boss[:]:
                laser.aggiorna(delta_tempo)

                # Controlla se il laser ha colpito il giocatore
                if laser.rect.colliderect(self.nave_giocatore.rect):
                    self.perdi_vita()
                    laser.attivo = False

                # Rimuovi laser non attivi
                if not laser.attivo:
                    self.laser_boss.remove(laser)

            # Aggiorna tutte le palle di fuoco
            for palla in self.palle_fuoco[:]:
                palla.aggiorna(delta_tempo)

                # Controlla se la palla ha colpito il giocatore
                if palla.rect.colliderect(self.nave_giocatore.rect):
                    self.perdi_vita()
                    palla.attivo = False

                # Se la palla è esplosa, crea i laser dell'esplosione
                if palla.esplosa:
                    laser_esplosione = palla.esplodi()
                    self.laser_boss.extend(laser_esplosione)

                # Rimuovi palle non attive
                if not palla.attivo:
                    self.palle_fuoco.remove(palla)

            # Controlla collisioni laser-boss
            for laser in self.lasers[:]:
                if self.boss.collide_con(laser.rect):
                    laser.attivo = False
                    if self.boss.prendi_danno(1):  # Boss sconfitto
                        self.boss_attivo = False
                        self.punteggio_ultimo_boss = self.punteggio

                        # Assegna punti per la sconfitta del boss
                        punti_boss = 500 * self.livello_boss
                        self.punteggio += punti_boss

                        # Mostra messaggio
                        self.mostra_messaggio_boss(True)  # Messaggio di boss sconfitto

                        # Pulisci i laser e le palle di fuoco del boss
                        self.laser_boss.clear()
                        self.palle_fuoco.clear()

        # Se non c'è un boss attivo, gestisci lo spawn normale dei nemici
        if not self.boss_attivo:
            # Gestione spawn nemici
            if tempo_corrente - self.tempo_ultimo_spawn > self.calcola_intervallo_spawn():
                self.spawn_nemico()
                self.tempo_ultimo_spawn = tempo_corrente

        # Controlla se è ora di spawnare un power-up basato sul punteggio
        if self.punteggio - self.punteggio_ultimo_power_up >= self.punteggio_intervallo_power_up:
            self.spawn_power_up()
            self.punteggio_ultimo_power_up = self.punteggio

        # Aggiorna tutti i power-up attivi
        for power_up in self.power_ups[:]:
            power_up.aggiorna(delta_tempo)

            # Controlla se il power-up ha colpito il giocatore
            if power_up.rect.colliderect(self.nave_giocatore.rect):
                self.mostra_messaggio_power_up(power_up.tipo)
                power_up.applica_effetto(self)
                power_up.attivo = False

            # Rimuovi power-up non attivi
            if not power_up.attivo:
                self.power_ups.remove(power_up)

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

        # Update the ship's damage level when the player loses a life
        if self.nave_giocatore:
            self.nave_giocatore.danno = 3 - self.vite  # Map life count to damage level (0-3)
            self.nave_giocatore.immagine = self.nave_giocatore.immagini[self.nave_giocatore.danno]

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

    def spawn_power_up(self):
        """Spawna un nuovo power-up in una posizione casuale"""
        # Calcola una posizione x casuale all'interno dell'area di gioco
        min_x = self.area_gioco.left + 10
        max_x = self.area_gioco.right - 40
        x_pos = random.randint(min_x, max_x)

        # Crea il power-up appena sopra lo schermo
        power_up = PowerUp(x_pos, -30)

        # Aggiungi alla lista dei power-up attivi
        self.power_ups.append(power_up)

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

        # Disegna tutti i power-up attivi
        for power_up in self.power_ups:
            power_up.disegna(schermo)

        # Disegna il boss se attivo
        if self.boss_attivo and self.boss:
            self.boss.disegna(schermo)

        # Disegna tutti i laser del boss
        for laser in self.laser_boss:
            laser.disegna(schermo)

        # Disegna tutte le palle di fuoco
        for palla in self.palle_fuoco:
            palla.disegna(schermo)

        # Disegna il punteggio e le vite
        font = pygame.font.SysFont("Arial", 24)
        testo_punteggio = font.render(f"Punti: {self.punteggio}", True, (255, 255, 255))
        schermo.blit(testo_punteggio, (self.area_gioco.left + 10, 20))

        testo_vite = font.render(f"Vite: {self.vite}", True, (255, 255, 255))
        schermo.blit(testo_vite, (self.area_gioco.right - testo_vite.get_width() - 10, 20))

        # Disegna il messaggio del power-up se è attivo
        tempo_corrente = pygame.time.get_ticks()
        if self.messaggio_power_up and tempo_corrente - self.tempo_messaggio_power_up < self.durata_messaggio_power_up:
            # Crea un font più grande per il messaggio del power-up
            font_power_up = pygame.font.SysFont("Arial", 36, bold=True)

            # Crea il rendering del testo con un colore vivace
            testo_power_up = font_power_up.render(self.messaggio_power_up, True, (255, 255, 0))

            # Posiziona il messaggio in alto al centro dello schermo
            pos_x = (config.GIOCO_LARGHEZZA - testo_power_up.get_width()) // 2
            pos_y = 60

            # Disegna un rettangolo semi-trasparente dietro il testo per migliorare la leggibilità
            sfondo_msg = pygame.Surface((testo_power_up.get_width() + 20, testo_power_up.get_height() + 10))
            sfondo_msg.set_alpha(150)  # Imposta trasparenza
            sfondo_msg.fill((0, 0, 0))  # Colore nero
            schermo.blit(sfondo_msg, (pos_x - 10, pos_y - 5))

            # Disegna il testo
            schermo.blit(testo_power_up, (pos_x, pos_y))

        # Mostra game over
        if self.game_over_status:
            font_game_over = pygame.font.SysFont("Arial", 72, bold=True)
            testo_game_over = font_game_over.render("GAME OVER", True, (255, 0, 0))
            pos_x = (self.gioco.schermo.get_width() - testo_game_over.get_width()) // 2
            pos_y = (self.gioco.schermo.get_height() - testo_game_over.get_height()) // 2
            schermo.blit(testo_game_over, (pos_x, pos_y))

    def salva_stato(self):
        """Salva lo stato attuale per il rewind"""
        stato = {
            'nave_x': self.nave_giocatore.x,
            'nave_y': self.nave_giocatore.y,
            'lasers': [(laser.x, laser.y) for laser in self.lasers],
            'punteggio': self.punteggio,
            'vite': self.vite
        }

        # Salva lo stato del boss se attivo
        if self.boss_attivo and self.boss:
            stato['boss_attivo'] = True
            stato['boss_x'] = self.boss.x
            stato['boss_y'] = self.boss.y
            stato['boss_salute'] = self.boss.salute
            stato['laser_boss'] = [(laser.x, laser.y) for laser in self.laser_boss]
            stato['palle_fuoco'] = [(palla.x, palla.y) for palla in self.palle_fuoco]
        else:
            stato['boss_attivo'] = False

        return stato

    def carica_stato(self, stato):
        """Carica uno stato salvato durante il rewind"""
        if not stato:
            return

        if 'nave_x' in stato:
            self.nave_giocatore.x = stato['nave_x']
            self.nave_giocatore.y = stato['nave_y']
            self.nave_giocatore.rect.x = int(self.nave_giocatore.x)
            self.nave_giocatore.rect.y = int(self.nave_giocatore.y)

            # Ricrea i laser nella posizione salvata
            self.lasers = []
            if 'lasers' in stato:
                for pos_laser in stato['lasers']:
                    self.lasers.append(Laser(pos_laser[0], pos_laser[1]))

            # Ripristina il punteggio e le vite
            if 'punteggio' in stato:
                self.punteggio = stato['punteggio']
            if 'vite' in stato:
                self.vite = stato['vite']
                self.nave_giocatore.danno = 3 - self.vite
                self.nave_giocatore.immagine = self.nave_giocatore.immagini[self.nave_giocatore.danno]

            # Ripristina lo stato del boss
            if 'boss_attivo' in stato:
                self.boss_attivo = stato['boss_attivo']

                if self.boss_attivo:
                    # Se il boss era attivo ma non c'è più, ricrealo
                    if not self.boss:
                        self.boss = Boss(self.area_gioco, self.livello_boss)

                    # Ripristina la posizione e la salute del boss
                    if 'boss_x' in stato and 'boss_y' in stato:
                        self.boss.x = stato['boss_x']
                        self.boss.y = stato['boss_y']
                        self.boss.rect.x = int(self.boss.x)
                        self.boss.rect.y = int(self.boss.y)

                    if 'boss_salute' in stato:
                        self.boss.salute = stato['boss_salute']

                    # Ricrea i laser del boss
                    self.laser_boss = []
                    if 'laser_boss' in stato:
                        for pos_laser in stato['laser_boss']:
                            self.laser_boss.append(BossLaser(pos_laser[0], pos_laser[1]))

                    # Ricrea le palle di fuoco
                    self.palle_fuoco = []
                    if 'palle_fuoco' in stato:
                        for pos_palla in stato['palle_fuoco']:
                            self.palle_fuoco.append(PallaDiFuoco(pos_palla[0], pos_palla[1]))
                else:
                    # Se il boss non era attivo, assicurati che sia rimosso
                    self.boss = None
                    self.laser_boss.clear()
                    self.palle_fuoco.clear()


class Nave:
    """Classe che rappresenta la nave del giocatore"""

    def __init__(self, area_gioco):
        """Inizializza la nave del giocatore"""
        self.area_gioco = area_gioco
        self.larghezza = 50  # Modificato da 40
        self.altezza = 50    # Modificato da 40
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

        # Livello di danno (0 = nessun danno, 3 = massimo danno)
        self.danno = 0

        # Immagini per i diversi stati di danno
        self.immagini = self.carica_immagini()
        self.immagine = self.immagini[self.danno]

    def carica_immagini(self):
        """Carica le immagini della nave per i diversi livelli di danno"""
        immagini = []
        nomi_file = [
            "Main Ship - Base - Full health.png",  # Nave intatta
            "Main Ship - Base - Slight damage.png",  # Danno leggero
            "Main Ship - Base - Damaged.png",  # Danno medio
            "Main Ship - Base - Very damaged.png"  # Danno grave
        ]

        for nome_file in nomi_file:
            try:
                # Fix the path to match the actual directory structure
                percorso = os.path.join("entita", "Nave", nome_file)
                immagine = pygame.image.load(percorso).convert_alpha()
                immagini.append(pygame.transform.scale(immagine, (self.larghezza, self.altezza)))
            except Exception as e:
                print(f"Errore nel caricamento dell'immagine {nome_file}: {e}")
                # Create a placeholder with different color based on damage level
                superficie = pygame.Surface((self.larghezza, self.altezza), pygame.SRCALPHA)
                colore = (
                    (0, 255, 0) if len(immagini) == 0 else  # Verde per nave intatta
                    (255, 255, 0) if len(immagini) == 1 else  # Giallo per danno leggero
                    (255, 165, 0) if len(immagini) == 2 else  # Arancione per danno medio
                    (255, 0, 0)  # Rosso per danno grave
                )
                pygame.draw.rect(superficie, colore, (0, 0, self.larghezza, self.altezza))
                immagini.append(superficie)

        return immagini

    def aumenta_danno(self):
        """Aumenta il livello di danno della nave e aggiorna l'immagine"""
        self.danno = min(self.danno + 1, 3)  # Massimo 3 livelli di danno
        self.immagine = self.immagini[self.danno]
        return self.danno

    def carica_immagine(self):
        """Funzione di compatibilità per il codice esistente"""
        return self.immagini[0]

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