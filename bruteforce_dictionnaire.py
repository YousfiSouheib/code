"""
SA5 - Script 01 : Attaques par Dictionnaire & Brute Force (Hash SHA-256)
EFREI Paris — Yousfi Souheib
-------------------------------------------------
Packages requis : aucun
⚠️  Usage pédagogique uniquement — environnements autorisés seulement
"""

import hashlib
import itertools
import string
import time
import sys

# ─────────────────────────────────────────────────────────────
#  Utilitaires
# ─────────────────────────────────────────────────────────────

def sha256(texte):
    return hashlib.sha256(texte.encode("utf-8")).hexdigest()

def md5(texte):
    return hashlib.md5(texte.encode("utf-8")).hexdigest()

def afficher_barre(tentatives, debut, largeur=40):
    """Affiche les tentatives en cours sans spammer le terminal."""
    if tentatives % 100000 == 0:
        elapsed = time.time() - debut
        vitesse = tentatives / elapsed if elapsed > 0 else 0
        print(f"\r[*] Tentatives : {tentatives:,} | Vitesse : {vitesse:,.0f} h/s", end="", flush=True)

# ─────────────────────────────────────────────────────────────
#  Attaque par dictionnaire
# ─────────────────────────────────────────────────────────────

def attaque_dictionnaire(hash_cible, fichier_wordlist, algo="sha256"):
    """
    Tente de retrouver le mot de passe correspondant au hash cible
    en testant chaque mot du fichier wordlist.
    """
    hasher = sha256 if algo == "sha256" else md5
    
    print(f"\n{'='*60}")
    print(f"[*] Attaque par DICTIONNAIRE")
    print(f"    Hash cible : {hash_cible}")
    print(f"    Algorithme : {algo.upper()}")
    print(f"    Wordlist   : {fichier_wordlist}")
    print(f"{'='*60}")
    
    debut = time.time()
    tentatives = 0
    
    try:
        with open(fichier_wordlist, "r", encoding="utf-8", errors="ignore") as f:
            for ligne in f:
                mot = ligne.strip()
                if not mot:
                    continue
                tentatives += 1
                if hasher(mot) == hash_cible:
                    elapsed = time.time() - debut
                    print(f"\n[✅] MOT DE PASSE TROUVÉ : '{mot}'")
                    print(f"    Tentatives : {tentatives:,}")
                    print(f"    Temps      : {elapsed:.3f}s")
                    return mot
                if tentatives % 10000 == 0:
                    print(f"\r[*] Tentatives : {tentatives:,}", end="", flush=True)
    except FileNotFoundError:
        print(f"[ERREUR] Fichier '{fichier_wordlist}' introuvable.")
        print("  Créez-le avec : cat > wordlist.txt << EOF")
        print("  password\n  123456\n  monmotdepasse\n  EOF")
        return None
    
    elapsed = time.time() - debut
    print(f"\n[❌] Mot de passe non trouvé dans la wordlist.")
    print(f"    Mots testés : {tentatives:,} en {elapsed:.3f}s")
    return None

# ─────────────────────────────────────────────────────────────
#  Attaque par brute force (charset personnalisable)
# ─────────────────────────────────────────────────────────────

def attaque_brute_force(hash_cible, longueur_max=4, charset=None, algo="sha256"):
    """
    Génère toutes les combinaisons possibles jusqu'à longueur_max
    et compare leur hash au hash cible.
    ⚠️  Très lent au-delà de 5-6 caractères — pédagogique uniquement.
    """
    if charset is None:
        charset = string.ascii_lowercase + string.digits  # a-z + 0-9
    
    hasher = sha256 if algo == "sha256" else md5
    
    print(f"\n{'='*60}")
    print(f"[*] Attaque par BRUTE FORCE")
    print(f"    Hash cible     : {hash_cible}")
    print(f"    Algorithme     : {algo.upper()}")
    print(f"    Longueur max   : {longueur_max}")
    print(f"    Charset        : {charset[:20]}... ({len(charset)} caractères)")
    print(f"    Combinaisons   : ~{sum(len(charset)**i for i in range(1, longueur_max+1)):,}")
    print(f"{'='*60}")
    
    debut = time.time()
    tentatives = 0
    
    for longueur in range(1, longueur_max + 1):
        print(f"\n[*] Test longueur {longueur}...")
        for combo in itertools.product(charset, repeat=longueur):
            mot = "".join(combo)
            tentatives += 1
            
            afficher_barre(tentatives, debut)
            
            if hasher(mot) == hash_cible:
                elapsed = time.time() - debut
                print(f"\n[✅] MOT DE PASSE TROUVÉ : '{mot}'")
                print(f"    Tentatives : {tentatives:,}")
                print(f"    Temps      : {elapsed:.3f}s")
                print(f"    Vitesse    : {tentatives/elapsed:,.0f} hash/s")
                return mot
    
    elapsed = time.time() - debut
    print(f"\n[❌] Non trouvé en {tentatives:,} tentatives ({elapsed:.2f}s)")
    return None

# ─────────────────────────────────────────────────────────────
#  Démonstration des Rainbow Tables (concept)
# ─────────────────────────────────────────────────────────────

def demo_rainbow_table():
    """
    Simule une attaque par rainbow table :
    pré-calcule un dictionnaire de hashes.
    """
    print(f"\n{'='*60}")
    print("[*] DÉMONSTRATION : Rainbow Table (concept)")
    print(f"{'='*60}")
    
    mots_communs = ["password", "123456", "qwerty", "admin", "letmein",
                    "welcome", "monkey", "dragon", "master", "efrei2025"]
    
    # Construction de la table
    rainbow = {sha256(m): m for m in mots_communs}
    print(f"[*] Table pré-calculée ({len(rainbow)} entrées) :")
    for h, m in list(rainbow.items())[:3]:
        print(f"    {h[:32]}... → '{m}'")
    
    # Simulation d'une attaque
    hash_a_casser = sha256("admin")
    print(f"\n[*] Hash à casser : {hash_a_casser}")
    
    debut = time.time()
    if hash_a_casser in rainbow:
        print(f"[✅] Trouvé instantanément → '{rainbow[hash_a_casser]}'")
        print(f"    Temps : {(time.time()-debut)*1000:.3f}ms  (pré-calcul = avantage !!)")
    
    print("\n⚠️  Protection : le SALT rend les rainbow tables inutiles !")

# ─────────────────────────────────────────────────────────────
#  Programme principal
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════╗")
    print("║  SA5 - Script 01 : Attaques Dictionnaire & BF       ║")
    print("╚══════════════════════════════════════════════════════╝")
    
    # ── Cible de démonstration ──────────────────────────────
    MOT_DE_PASSE_CIBLE = "abc"
    HASH_CIBLE = sha256(MOT_DE_PASSE_CIBLE)
    print(f"\n[INFO] Mot de passe cible (pour la démo) : '{MOT_DE_PASSE_CIBLE}'")
    print(f"[INFO] Hash SHA-256 : {HASH_CIBLE}")
    
    # ── Attaque par dictionnaire ────────────────────────────
    import os
    # Création d'une wordlist de démo si inexistante
    if not os.path.exists("wordlist.txt"):
        with open("wordlist.txt", "w") as f:
            mots = ["password", "123456", "qwerty", "admin", "abc",
                    "letmein", "efrei", "master", "test", "root"]
            f.write("\n".join(mots))
        print("\n[INFO] wordlist.txt créée avec des mots de démo.")
    
    attaque_dictionnaire(HASH_CIBLE, "wordlist.txt")
    
    # ── Attaque brute force ─────────────────────────────────
    attaque_brute_force(HASH_CIBLE, longueur_max=3,
                        charset=string.ascii_lowercase)
    
    # ── Rainbow table ────────────────────────────────────────
    demo_rainbow_table()
    
    print("\n✅ Fin de la démonstration.")
    print("💡 Conseil : utilisez bcrypt/Argon2 + salt pour protéger vos mots de passe !")
