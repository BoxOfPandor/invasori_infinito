#!/usr/bin/env python3

"""
Scena dell'introduzione
Mostra l'introduzione come un brief militare su un vecchio computer
"""

import pygame
import math
import os
import time
from core.scena import Scena
import config

class ScenaIntroduzione(Scena):
    """Scena di introduzione che mostra il brief della missione"""
    
    def __init__(self, gioco):
        """Inizializza la scena di introduzione"""
        super().__init__(gioco)
        self.sfondo = None
        self.font_titolo = None
        self.font_testo = None
        
        # Nuovo testo del brief
        self.testo_brief = [
            "BRIEF DE MISSIONE — CLASSIFICAZIONE OMEGA-RED",
            "",
            "Data: 17 ottobre 3147",
            "Destinazione: Nucleo Solare",
            "Operatore: Comandante Lupo Bruni",
            "Progetto: AURORA",
            "",
            "\"Comandante Bruni, questo messaggio è probabilmente l'ultimo che riceverà dall'umanità.\"",
            "",
            "La Terra è in agonia. Gli oceani sono morti, i cieli avvelenati. Ciò che resta",
            "della nostra specie vive sottoterra, in rifugi sempre più silenziosi. Gli",
            "scienziati del programma Aurora hanno identificato un'unica possibilità di",
            "resettare il ciclo stellare: innescare una reazione a catena nel cuore del Sole.",
            "Una rinascita... o l'oblio totale.",
            "",
            "La sua missione: pilotare la sonda Helios-9 fino al cuore del Sole. La carica",
            "a bordo deve essere attivata manualmente. Nessun ritorno previsto. Nessuna gloria.",
            "Solo la fine. O un nuovo inizio.",
            "",
            "Ma avvicinandosi alla stella, forme di vita sconosciute — antiche, colossali,",
            "ostili — l'hanno intercettata. Il contatto è perso. Lei fallisce... e si risveglia.",
            "Ancora.",
            "",
            "Qualcosa ha spezzato il corso del tempo. Lei è intrappolato in un ciclo,",
            "un eterno ricominciare.",
            "",
            "E poi, durante il suo ultimo attraversamento, Il Fenice è apparso: una creatura",
            "di fuoco e luce, nata dalle ceneri del Sole stesso. È una guida? Un'arma?",
            "Un'illusione?",
            "",
            "Lei è solo, Comandante. Ancora e ancora.",
            "",
            "Ma questa volta... potrebbe essere l'ultima."
        ]
        
        # Impostazioni di visualizzazione
        self.linee_mostrate = []            # Linee già completamente mostrate
        self.linea_corrente = ""            # Linea attualmente in fase di digitazione
        self.indice_linea = 0               # Indice della linea corrente nel testo
        self.indice_carattere = 0           # Indice del carattere corrente nella linea
        self.tempo_ultimo_carattere = 0     # Per il controllo della velocità di digitazione
        self.velocita_carattere = 15        # Millisecondi tra un carattere e l'altro
        self.velocita_linea_vuota = 300     # Millisecondi di pausa per le linee vuote
        self.tempo_pausa_dopo_linea = 100   # Pausa dopo che una linea è completa
        self.tempo_completamento_linea = 0  # Quando una linea è stata completata
        self.linea_completata = False       # Flag per indicare se la linea corrente è completa
        self.max_linee_visibili = 15        # Numero massimo di linee visibili contemporaneamente
        self.tempo_skip = 0
        self.tempo_inizio = 0
        
        # Colori e stile
        self.colore_sfondo = (0, 0, 0)      # Nero
        self.colore_testo = (0, 255, 0)     # Verde terminale
        self.colore_titolo = (255, 255, 0)  # Giallo per il titolo
        
        # Flag di completamento
        self.intro_completata = False
    
    def inizializza(self):
        """Inizializza gli elementi dell'introduzione"""
        super().inizializza()
        
        # Crea uno sfondo nero con effetto CRT
        self.sfondo = pygame.Surface((self.gioco.larghezza, self.gioco.altezza))
        self.sfondo.fill(self.colore_sfondo)
        
        # Prepara i font (monospace per effetto terminale) - simplifié
        try:
            self.font_titolo = pygame.font.SysFont("Arial", 28, bold=True)
            self.font_testo = pygame.font.SysFont("Arial", 20)
        except Exception as e:
            print(f"Errore nel caricare i font: {e}")
            # Fallback con font di sistema
            self.font_titolo = pygame.font.Font(None, 32)
            self.font_testo = pygame.font.Font(None, 24)
        
        # Memorizza il tempo di inizio
        self.tempo_inizio = pygame.time.get_ticks()
        self.tempo_ultimo_carattere = self.tempo_inizio  # Inizializza anche questo
        
        # Aggiungi questa scena come osservatore degli eventi
        self.gioco.gestore_eventi.aggiungi_osservatore(self)
        
        # Imposta timer per quando il tasto skip diventa disponibile
        self.tempo_skip = pygame.time.get_ticks() + 2000  # 2 secondi prima di poter saltare
    
    def termina(self):
        """Pulisce le risorse quando la scena non è più attiva"""
        super().termina()
        
        # Rimuovi questa scena come osservatore degli eventi
        self.gioco.gestore_eventi.rimuovi_osservatore(self)
    
    def gestisci_evento(self, evento):
        """Gestisce gli eventi di input"""
        # Usa ESC per saltare l'introduzione
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            print("Brief saltato con ESC")
            self.gioco.cambia_scena("gioco")
    
    def aggiorna(self, delta_tempo):
        """Aggiorna l'animazione dell'introduzione"""
        # Ottieni il tempo corrente
        tempo_corrente = pygame.time.get_ticks()
        
        # Se tutte le linee sono state mostrate, attendi un po' e poi passa al gioco
        if self.intro_completata:
            if tempo_corrente - self.tempo_completamento_linea > 3000:  # 3 secondi di attesa
                self.gioco.cambia_scena("gioco")
            return
        
        # Se abbiamo finito tutte le linee, segna l'intro come completata
        if self.indice_linea >= len(self.testo_brief):
            self.intro_completata = True
            self.tempo_completamento_linea = tempo_corrente
            return
        
        # Se la linea corrente è completata, attendi un po' prima di passare alla prossima
        if self.linea_completata:
            if tempo_corrente - self.tempo_completamento_linea > self.tempo_pausa_dopo_linea:
                self.linee_mostrate.append(self.linea_corrente)
                # Limita il numero di linee visibili
                if len(self.linee_mostrate) > self.max_linee_visibili:
                    self.linee_mostrate.pop(0)
                self.linea_corrente = ""
                self.indice_linea += 1
                self.indice_carattere = 0
                self.linea_completata = False
            return
        
        # Se siamo su una linea vuota, aspetta meno tempo e segnala come completata
        if self.indice_linea < len(self.testo_brief) and self.testo_brief[self.indice_linea] == "":
            if tempo_corrente - self.tempo_ultimo_carattere > self.velocita_linea_vuota:
                self.linea_completata = True
                self.tempo_completamento_linea = tempo_corrente
                self.tempo_ultimo_carattere = tempo_corrente
            return
        
        # Aggiunge progressivamente i caratteri alla linea corrente
        if self.indice_carattere < len(self.testo_brief[self.indice_linea]):
            if tempo_corrente - self.tempo_ultimo_carattere > self.velocita_carattere:
                self.linea_corrente += self.testo_brief[self.indice_linea][self.indice_carattere]
                self.indice_carattere += 1
                self.tempo_ultimo_carattere = tempo_corrente
                
                # Effetto sonoro di digitazione (opzionale)
                # pygame.mixer.Sound("assets/audio/type.wav").play()
        else:
            # La linea è stata completamente scritta
            self.linea_completata = True
            self.tempo_completamento_linea = tempo_corrente
    
    def disegna(self, schermo):
        """Disegna l'introduzione sullo schermo"""
        # Disegna lo sfondo (nero)
        schermo.fill((0, 0, 0))  # Remplissage complet en noir
        
        # Aggiungi effetto CRT (griglia sottile)
        self.disegna_effetto_crt(schermo)
        
        # Calcola il margine laterale sicuro - usa un valore fisso più petit
        margine_laterale = 30
        
        # Position fixe en haut de l'écran
        y_base = 50
        
        # Disegna le linee già mostrate - avec une couleur très visible
        for i, linea in enumerate(self.linee_mostrate):
            # Il titolo ha un colore diverso
            colore = (255, 255, 0) if i == 0 else (0, 255, 0)  # Jaune pour le titre, vert vif pour le texte
            font = self.font_titolo if i == 0 else self.font_testo
            
            # Rendu du texte
            try:
                surf_linea = font.render(linea, True, colore)
                schermo.blit(surf_linea, (margine_laterale, y_base + i * 30))
            except Exception as e:
                print(f"Errore nel rendering della linea {i}: {e}")
        
        # Disegna la linea corrente (che sta venendo digitata)
        colore_corrente = (255, 255, 0) if self.indice_linea == 0 else (0, 255, 0)
        font_corrente = self.font_titolo if self.indice_linea == 0 else self.font_testo
        
        # Rendu de la ligne courante
        try:
            surf_corrente = font_corrente.render(self.linea_corrente, True, colore_corrente)
            schermo.blit(surf_corrente, (margine_laterale, y_base + len(self.linee_mostrate) * 30))
        except Exception as e:
            print(f"Errore nel rendering della linea corrente: {e}")
        
        # Disegna il cursore lampeggiante
        if not self.linea_completata and (pygame.time.get_ticks() // 500) % 2 == 0:
            try:
                larghezza_testo = font_corrente.size(self.linea_corrente)[0]
                pygame.draw.rect(schermo, colore_corrente, 
                                (margine_laterale + larghezza_testo, y_base + len(self.linee_mostrate) * 30,
                                8, font_corrente.get_height()))
            except Exception as e:
                print(f"Errore nel disegnare il cursore: {e}")
        
        # Mostra suggerimento per saltare l'introduzione con ESC - position fixe en bas
        try:
            font_hint = pygame.font.SysFont("Courier New", 18)  # Police plus grande
            hint_text = font_hint.render("Premi ESC per saltare", True, (200, 200, 200))  # Couleur plus claire
            pos_x = 20
            pos_y = self.gioco.altezza - hint_text.get_height() - 20
            schermo.blit(hint_text, (pos_x, pos_y))
        except Exception as e:
            print(f"Errore nel rendering del suggerimento: {e}")
        
        # Dessinez une ligne de test juste pour vérifier que le rendu fonctionne
        pygame.draw.line(schermo, (255, 0, 0), (10, 10), (100, 10), 2)
    
    def disegna_effetto_crt(self, schermo):
        """Disegna un effetto CRT sul terminale"""
        # Recupera le dimensioni effettive dello schermo
        larghezza_schermo = schermo.get_width()
        altezza_schermo = schermo.get_height()
        
        # Assicurati che il bordo non sia fuori dallo schermo
        margine = 10
        larghezza_bordo = larghezza_schermo - 2 * margine
        altezza_bordo = altezza_schermo - 2 * margine
        
        # Disegna righe orizzontali leggermente più scure (effetto scanline)
        for y in range(0, altezza_schermo, 2):
            pygame.draw.line(schermo, (10, 10, 10), (0, y), (larghezza_schermo, y))
        
        # Disegna una sottile cornice verde come i vecchi monitor
        pygame.draw.rect(schermo, (0, 60, 0), (margine, margine, larghezza_bordo, altezza_bordo), 2)
        
        # Aggiungi un leggero bagliore verde al centro dello schermo
        bagliore = pygame.Surface((larghezza_schermo, altezza_schermo), pygame.SRCALPHA)
        pygame.draw.circle(bagliore, (0, 40, 0, 50), 
                          (larghezza_schermo // 2, altezza_schermo // 2), 
                          min(larghezza_schermo, altezza_schermo) // 3)
        schermo.blit(bagliore, (0, 0))