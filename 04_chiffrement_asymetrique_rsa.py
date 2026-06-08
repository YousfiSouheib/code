"""
SA4 - Script 04 : Chiffrement Asymétrique RSA
EFREI Paris — Yousfi Souheib
-------------------------------------------------
Package requis : pycryptodome
Installation   : pip install pycryptodome --break-system-packages
"""

import sys, subprocess

def installer_package(package):
    print(f"[INFO] Installation de '{package}' en cours...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package,
                           "--break-system-packages", "-q"])
    print(f"[OK] '{package}' installé.\n")

try:
    from Crypto.PublicKey import RSA
    from Crypto.Cipher import PKCS1_OAEP, AES
    from Crypto.Random import get_random_bytes
    from Crypto.Signature import pss
    from Crypto.Hash import SHA256
    from Crypto.Util.Padding import pad, unpad
except ImportError:
    installer_package("pycryptodome")
    from Crypto.PublicKey import RSA
    from Crypto.Cipher import PKCS1_OAEP, AES
    from Crypto.Random import get_random_bytes
    from Crypto.Signature import pss
    from Crypto.Hash import SHA256
    from Crypto.Util.Padding import pad, unpad

import base64

# ─────────────────────────────────────────────────────────────
#  Génération de paire de clés RSA
# ─────────────────────────────────────────────────────────────

def generer_cles_rsa(taille_bits=2048):
    """Génère une paire de clés RSA et retourne (cle_privee, cle_publique)."""
    print(f"[*] Génération d'une paire de clés RSA-{taille_bits} bits...")
    cle = RSA.generate(taille_bits)
    cle_privee = cle.export_key().decode()
    cle_publique = cle.publickey().export_key().decode()
    print("[OK] Paire de clés générée.")
    return cle_privee, cle_publique

# ─────────────────────────────────────────────────────────────
#  Chiffrement RSA (OAEP) — pour petits messages
# ─────────────────────────────────────────────────────────────

def chiffrer_rsa(message, cle_publique_pem):
    """Chiffre un message avec la clé publique RSA (OAEP)."""
    cle = RSA.import_key(cle_publique_pem)
    cipher = PKCS1_OAEP.new(cle)
    chiffre = cipher.encrypt(message.encode("utf-8"))
    return base64.b64encode(chiffre).decode()

def dechiffrer_rsa(message_chiffre_b64, cle_privee_pem):
    """Déchiffre un message avec la clé privée RSA."""
    cle = RSA.import_key(cle_privee_pem)
    cipher = PKCS1_OAEP.new(cle)
    message_chiffre = base64.b64decode(message_chiffre_b64)
    return cipher.decrypt(message_chiffre).decode("utf-8")

# ─────────────────────────────────────────────────────────────
#  Chiffrement hybride RSA + AES (pour gros fichiers/messages)
# ─────────────────────────────────────────────────────────────

def chiffrer_hybride(message, cle_publique_pem):
    """
    Chiffrement hybride :
    1. Génère une clé AES aléatoire
    2. Chiffre le message avec AES
    3. Chiffre la clé AES avec RSA (clé publique)
    Retourne un dict contenant les deux parties chiffrées.
    """
    # Étape 1 : clé de session AES aléatoire
    cle_session = get_random_bytes(32)
    
    # Étape 2 : chiffrement AES du message
    cipher_aes = AES.new(cle_session, AES.MODE_CBC)
    ciphertext = cipher_aes.encrypt(pad(message.encode(), AES.block_size))
    
    # Étape 3 : chiffrement RSA de la clé de session
    cle_pub = RSA.import_key(cle_publique_pem)
    cipher_rsa = PKCS1_OAEP.new(cle_pub)
    cle_session_chiffree = cipher_rsa.encrypt(cle_session)
    
    return {
        "cle_session_chiffree": base64.b64encode(cle_session_chiffree).decode(),
        "iv":  base64.b64encode(cipher_aes.iv).decode(),
        "message_chiffre": base64.b64encode(ciphertext).decode(),
    }

def dechiffrer_hybride(paquet, cle_privee_pem):
    """Déchiffrement hybride RSA + AES."""
    # Étape 1 : déchiffrement RSA de la clé de session
    cle_priv = RSA.import_key(cle_privee_pem)
    cipher_rsa = PKCS1_OAEP.new(cle_priv)
    cle_session = cipher_rsa.decrypt(base64.b64decode(paquet["cle_session_chiffree"]))
    
    # Étape 2 : déchiffrement AES du message
    iv = base64.b64decode(paquet["iv"])
    ciphertext = base64.b64decode(paquet["message_chiffre"])
    cipher_aes = AES.new(cle_session, AES.MODE_CBC, iv)
    return unpad(cipher_aes.decrypt(ciphertext), AES.block_size).decode()

# ─────────────────────────────────────────────────────────────
#  Signature numérique RSA-PSS
# ─────────────────────────────────────────────────────────────

def signer_message(message, cle_privee_pem):
    """Signe un message avec la clé privée (RSA-PSS + SHA-256)."""
    cle = RSA.import_key(cle_privee_pem)
    h = SHA256.new(message.encode("utf-8"))
    signature = pss.new(cle).sign(h)
    return base64.b64encode(signature).decode()

def verifier_signature(message, signature_b64, cle_publique_pem):
    """Vérifie la signature d'un message."""
    cle = RSA.import_key(cle_publique_pem)
    h = SHA256.new(message.encode("utf-8"))
    try:
        pss.new(cle).verify(h, base64.b64decode(signature_b64))
        return True
    except (ValueError, TypeError):
        return False

# ─────────────────────────────────────────────────────────────
#  Programme principal
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════╗")
    print("║     SA4 - Script 04 : Chiffrement Asymétrique RSA   ║")
    print("╚══════════════════════════════════════════════════════╝")
    
    # Génération des clés
    priv, pub = generer_cles_rsa(2048)
    print(f"\nClé publique (extrait) :\n{pub[:80]}...\n")
    
    # ── Chiffrement RSA direct ──────────────────────────────
    print("--- CHIFFREMENT RSA DIRECT ---")
    msg = "Secret EFREI"
    chiffre = chiffrer_rsa(msg, pub)
    print(f"Original  : {msg}")
    print(f"Chiffré   : {chiffre[:60]}...")
    print(f"Déchiffré : {dechiffrer_rsa(chiffre, priv)}")
    
    # ── Chiffrement hybride ─────────────────────────────────
    print("\n--- CHIFFREMENT HYBRIDE RSA + AES ---")
    long_msg = "Message long " * 50  # RSA ne peut pas chiffrer ça directement
    paquet = chiffrer_hybride(long_msg, pub)
    print(f"Clé session chiffrée (extrait) : {paquet['cle_session_chiffree'][:40]}...")
    result = dechiffrer_hybride(paquet, priv)
    print(f"Déchiffrement OK : {result[:30]}... (longueur={len(result)})")
    
    # ── Signature numérique ─────────────────────────────────
    print("\n--- SIGNATURE NUMÉRIQUE RSA-PSS ---")
    doc = "Contrat officiel EFREI — Version 1.0"
    sig = signer_message(doc, priv)
    print(f"Message   : {doc}")
    print(f"Signature : {sig[:60]}...")
    ok = verifier_signature(doc, sig, pub)
    print(f"Vérification : {'✅ Valide' if ok else '❌ Invalide'}")
    
    # Test avec message modifié
    ok2 = verifier_signature(doc + " FALSIFIÉ", sig, pub)
    print(f"Message modifié → {'✅ Valide' if ok2 else '❌ Invalide (falsification détectée)'}")
    
    print("\n✅ Démonstration terminée.")
