"""
SA4 - Script 05 : Hachage avec Salt et Stockage Sécurisé
EFREI Paris — Yousfi Souheib
-------------------------------------------------
Package requis : bcrypt
Installation   : pip install bcrypt --break-system-packages
"""

import sys, subprocess, hashlib, os, json, time

def installer_package(package):
    print(f"[INFO] Installation de '{package}' en cours...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package,
                           "--break-system-packages", "-q"])
    print(f"[OK] '{package}' installé.\n")

try:
    import bcrypt
except ImportError:
    installer_package("bcrypt")
    import bcrypt

# ─────────────────────────────────────────────────────────────
#  Hachage avec salt manuel (SHA-256)
# ─────────────────────────────────────────────────────────────

def hasher_avec_salt(mot_de_passe, salt=None):
    """
    Hache un mot de passe avec un salt.
    Si salt=None, génère un salt aléatoire de 16 octets.
    Retourne (hash_hex, salt_hex).
    """
    if salt is None:
        salt = os.urandom(16)
    elif isinstance(salt, str):
        salt = bytes.fromhex(salt)
    
    hache = hashlib.sha256(salt + mot_de_passe.encode("utf-8")).hexdigest()
    return hache, salt.hex()

def verifier_mot_de_passe_salt(mot_de_passe, hash_stocke, salt_hex):
    """Vérifie un mot de passe en recalculant le hash avec le même salt."""
    hache_calc, _ = hasher_avec_salt(mot_de_passe, salt=salt_hex)
    return hache_calc == hash_stocke

# ─────────────────────────────────────────────────────────────
#  Hachage avec bcrypt (recommandé en production)
# ─────────────────────────────────────────────────────────────

def hasher_bcrypt(mot_de_passe, rounds=12):
    """Hache avec bcrypt (salt intégré, résistant aux GPU)."""
    return bcrypt.hashpw(mot_de_passe.encode("utf-8"), bcrypt.gensalt(rounds=rounds)).decode()

def verifier_bcrypt(mot_de_passe, hash_stocke):
    """Vérifie un mot de passe bcrypt."""
    return bcrypt.checkpw(mot_de_passe.encode("utf-8"), hash_stocke.encode("utf-8"))

# ─────────────────────────────────────────────────────────────
#  Base de données simplifiée de mots de passe
# ─────────────────────────────────────────────────────────────

DB_FILE = "users_db.json"

def creer_utilisateur(nom, mot_de_passe):
    """Ajoute un utilisateur dans la base avec un hash bcrypt."""
    try:
        with open(DB_FILE, "r") as f:
            db = json.load(f)
    except FileNotFoundError:
        db = {}
    
    db[nom] = hasher_bcrypt(mot_de_passe)
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=2)
    print(f"[OK] Utilisateur '{nom}' créé.")

def authentifier(nom, mot_de_passe):
    """Tente d'authentifier un utilisateur."""
    try:
        with open(DB_FILE, "r") as f:
            db = json.load(f)
    except FileNotFoundError:
        print("[ERREUR] Base de données introuvable.")
        return False
    
    if nom not in db:
        print(f"[ERREUR] Utilisateur '{nom}' inexistant.")
        return False
    
    return verifier_bcrypt(mot_de_passe, db[nom])

# ─────────────────────────────────────────────────────────────
#  Programme principal
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════╗")
    print("║    SA4 - Script 05 : Hachage avec Salt & Bcrypt     ║")
    print("╚══════════════════════════════════════════════════════╝")
    
    # ── Démonstration du salt ───────────────────────────────
    print("\n--- POURQUOI LE SALT ? ---")
    pwd = "password123"
    h1, s1 = hasher_avec_salt(pwd)
    h2, s2 = hasher_avec_salt(pwd)
    print(f"Même mot de passe '{pwd}' hashé deux fois :")
    print(f"  Hash 1 (salt={s1[:16]}...) : {h1}")
    print(f"  Hash 2 (salt={s2[:16]}...) : {h2}")
    print("  → Les hashes sont DIFFÉRENTS grâce au salt !")
    
    print("\n--- VÉRIFICATION AVEC SALT ---")
    print(f"  Bon mdp    : {'✅' if verifier_mot_de_passe_salt(pwd, h1, s1) else '❌'}")
    print(f"  Mauvais mdp: {'✅' if verifier_mot_de_passe_salt('mauvais', h1, s1) else '❌'}")
    
    # ── Démonstration bcrypt ────────────────────────────────
    print("\n--- HACHAGE BCRYPT (recommandé en production) ---")
    pwd_b = "MonSuperMotDePasse!"
    
    t0 = time.time()
    hb = hasher_bcrypt(pwd_b, rounds=10)
    t1 = time.time()
    
    print(f"Hash bcrypt : {hb}")
    print(f"Temps de calcul (rounds=10) : {(t1-t0)*1000:.0f} ms  ← intentionnellement lent !")
    print(f"Vérification OK : {'✅' if verifier_bcrypt(pwd_b, hb) else '❌'}")
    
    # ── Base de données simplifiée ──────────────────────────
    print("\n--- SIMULATION BASE DE DONNÉES UTILISATEURS ---")
    creer_utilisateur("alice", "alice2025!")
    creer_utilisateur("bob",   "P@ssw0rd")
    
    print(f"\nConnexion alice / alice2025! → {'✅ Succès' if authentifier('alice', 'alice2025!') else '❌ Échec'}")
    print(f"Connexion alice / mauvais    → {'✅ Succès' if authentifier('alice', 'mauvais') else '❌ Échec'}")
    
    print("\n✅ Démonstration terminée. Fichier users_db.json créé.")
