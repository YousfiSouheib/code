"""
SA4 - Script 02 : Encodage (Base64, Hex, Base32, ROT13)
EFREI Paris — Yousfi Souheib
-------------------------------------------------
Packages requis : aucun (base64, codecs sont intégrés à Python)
"""

import base64
import codecs

def encoder_base64(texte):
    encoded = base64.b64encode(texte.encode("utf-8"))
    return encoded.decode("utf-8")

def decoder_base64(texte_encode):
    decoded = base64.b64decode(texte_encode.encode("utf-8"))
    return decoded.decode("utf-8")

def encoder_hex(texte):
    return texte.encode("utf-8").hex()

def decoder_hex(texte_hex):
    return bytes.fromhex(texte_hex).decode("utf-8")

def encoder_base32(texte):
    encoded = base64.b32encode(texte.encode("utf-8"))
    return encoded.decode("utf-8")

def decoder_base32(texte_encode):
    decoded = base64.b32decode(texte_encode.encode("utf-8"))
    return decoded.decode("utf-8")

def encoder_rot13(texte):
    return codecs.encode(texte, 'rot_13')

def demo_encodage(texte):
    print(f"\n{'='*60}")
    print(f"Texte original : '{texte}'")
    print(f"{'='*60}")
    
    b64 = encoder_base64(texte)
    print(f"\nBase64 :")
    print(f"  Encodé  : {b64}")
    print(f"  Décodé  : {decoder_base64(b64)}")
    
    hexval = encoder_hex(texte)
    print(f"\nHexadécimal :")
    print(f"  Encodé  : {hexval}")
    print(f"  Décodé  : {decoder_hex(hexval)}")
    
    b32 = encoder_base32(texte)
    print(f"\nBase32 :")
    print(f"  Encodé  : {b32}")
    print(f"  Décodé  : {decoder_base32(b32)}")
    
    rot = encoder_rot13(texte)
    print(f"\nROT-13 (décalage de 13) :")
    print(f"  Encodé  : {rot}")
    print(f"  Décodé  : {encoder_rot13(rot)}  (ROT-13 appliqué deux fois)")
    
    print(f"\n⚠️  L'encodage N'EST PAS du chiffrement — il est réversible sans clé !")

if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════╗")
    print("║         SA4 - Script 02 : Encodage              ║")
    print("╚══════════════════════════════════════════════════╝")
    
    textes = ["Hello EFREI!", "Bonjour les étudiants", "P@ssw0rd123"]
    for t in textes:
        demo_encodage(t)
