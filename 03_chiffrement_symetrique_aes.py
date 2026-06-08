"""
SA4 - Script 03 : Chiffrement Symétrique AES
EFREI Paris — Yousfi Souheib
-------------------------------------------------
Package requis : pycryptodome
Installation   : pip install pycryptodome --break-system-packages
"""

# ─────────────────────────────────────────────────────────────
#  Vérification et installation automatique du package requis
# ─────────────────────────────────────────────────────────────
import sys, subprocess

def installer_package(package):
    print(f"[INFO] Installation de '{package}' en cours...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package,
                           "--break-system-packages", "-q"])
    print(f"[OK] '{package}' installé avec succès.\n")

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
#  Fonctions de chiffrement / déchiffrement AES-CBC
# ─────────────────────────────────────────────────────────────

def chiffrer_aes(texte, cle_bytes):
    """
    Chiffrement AES en mode CBC.
    La clé doit faire 16, 24 ou 32 octets (AES-128, 192 ou 256).
    Un IV aléatoire est généré à chaque appel.
    """
    iv = get_random_bytes(16)
    cipher = AES.new(cle_bytes, AES.MODE_CBC, iv)
    texte_padded = pad(texte.encode("utf-8"), AES.block_size)
    ciphertext = cipher.encrypt(texte_padded)
    # On concatène IV + ciphertext puis on encode en base64 pour l'affichage
    result = base64.b64encode(iv + ciphertext).decode("utf-8")
    return result

def dechiffrer_aes(texte_chiffre_b64, cle_bytes):
    """Déchiffrement AES-CBC."""
    data = base64.b64decode(texte_chiffre_b64.encode("utf-8"))
    iv = data[:16]
    ciphertext = data[16:]
    cipher = AES.new(cle_bytes, AES.MODE_CBC, iv)
    texte_padded = cipher.decrypt(ciphertext)
    return unpad(texte_padded, AES.block_size).decode("utf-8")

# ─────────────────────────────────────────────────────────────
#  Fonctions de chiffrement / déchiffrement AES-GCM
#  (mode authentifié — recommandé en production)
# ─────────────────────────────────────────────────────────────

def chiffrer_aes_gcm(texte, cle_bytes):
    """Chiffrement AES-GCM avec authentification intégrée."""
    cipher = AES.new(cle_bytes, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(texte.encode("utf-8"))
    result = {
        "nonce": base64.b64encode(cipher.nonce).decode(),
        "tag":   base64.b64encode(tag).decode(),
        "data":  base64.b64encode(ciphertext).decode(),
    }
    return result

def dechiffrer_aes_gcm(paquet, cle_bytes):
    """Déchiffrement AES-GCM avec vérification d'authenticité."""
    nonce = base64.b64decode(paquet["nonce"])
    tag   = base64.b64decode(paquet["tag"])
    data  = base64.b64decode(paquet["data"])
    cipher = AES.new(cle_bytes, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(data, tag).decode("utf-8")

# ─────────────────────────────────────────────────────────────
#  Démonstration principale
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════╗")
    print("║     SA4 - Script 03 : Chiffrement Symétrique AES    ║")
    print("╚══════════════════════════════════════════════════════╝")
    
    message = "Message confidentiel EFREI — Ne pas divulguer !"
    
    print("\n--- MODE AES-CBC (128 bits) ---")
    cle_128 = get_random_bytes(16)  # 128 bits
    print(f"Clé (hex) : {cle_128.hex()}")
    
    chiffre = chiffrer_aes(message, cle_128)
    print(f"Texte clair   : {message}")
    print(f"Texte chiffré : {chiffre}")
    dechiffre = dechiffrer_aes(chiffre, cle_128)
    print(f"Texte déchiffré : {dechiffre}")
    
    print("\n--- MODE AES-CBC (256 bits) ---")
    cle_256 = get_random_bytes(32)  # 256 bits
    print(f"Clé (hex) : {cle_256.hex()}")
    chiffre_256 = chiffrer_aes(message, cle_256)
    print(f"Texte chiffré : {chiffre_256}")
    print(f"Texte déchiffré : {dechiffrer_aes(chiffre_256, cle_256)}")
    
    print("\n--- MODE AES-GCM (mode authentifié, recommandé) ---")
    cle_gcm = get_random_bytes(32)
    paquet = chiffrer_aes_gcm(message, cle_gcm)
    print(f"Nonce : {paquet['nonce']}")
    print(f"Tag   : {paquet['tag']}")
    print(f"Data  : {paquet['data']}")
    print(f"Texte déchiffré : {dechiffrer_aes_gcm(paquet, cle_gcm)}")
    
    print("\n--- TEST AVEC MAUVAISE CLÉ ---")
    mauvaise_cle = get_random_bytes(16)
    try:
        dechiffrer_aes(chiffre, mauvaise_cle)
    except Exception as e:
        print(f"[ERREUR ATTENDUE] Mauvaise clé → {type(e).__name__}: {e}")
    
    print("\n✅ Démonstration terminée.")
