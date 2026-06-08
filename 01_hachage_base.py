"""
SA4 - Script 01 : Fonctions de hachage de base
EFREI Paris — Yousfi Souheib
-------------------------------------------------
Packages requis : aucun (hashlib est intégré à Python)
"""

import hashlib

def hash_texte(texte, algorithme="sha256"):
    """Calcule le hash d'un texte avec l'algorithme choisi."""
    h = hashlib.new(algorithme)
    h.update(texte.encode("utf-8"))
    return h.hexdigest()

def afficher_comparaison(texte):
    """Affiche les différents hashes d'un texte."""
    print(f"\n{'='*60}")
    print(f"Texte : '{texte}'")
    print(f"{'='*60}")
    print(f"MD5     : {hash_texte(texte, 'md5')}")
    print(f"SHA-1   : {hash_texte(texte, 'sha1')}")
    print(f"SHA-256 : {hash_texte(texte, 'sha256')}")
    print(f"SHA-512 : {hash_texte(texte, 'sha512')}")

def demo_sensibilite():
    """Démo : un petit changement → hash totalement différent."""
    print("\n\n--- DÉMONSTRATION : Sensibilité aux modifications ---")
    texte1 = "hello"
    texte2 = "Hello"
    texte3 = "hello "  # espace en plus
    
    print(f"'{texte1}' → SHA256 : {hash_texte(texte1)}")
    print(f"'{texte2}' → SHA256 : {hash_texte(texte2)}")
    print(f"'{texte3}' → SHA256 : {hash_texte(texte3)}")
    print("\nObservation : même une majuscule ou un espace change totalement le hash !")

if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════╗")
    print("║     SA4 - Script 01 : Fonctions de Hachage      ║")
    print("╚══════════════════════════════════════════════════╝")
    
    exemples = ["monmotdepasse", "efrei2025", "P@ssw0rd!"]
    for ex in exemples:
        afficher_comparaison(ex)
    
    demo_sensibilite()
    
    print("\n\n--- LONGUEUR DES EMPREINTES ---")
    texte = "test"
    algos = ["md5", "sha1", "sha256", "sha512"]
    for algo in algos:
        h = hash_texte(texte, algo)
        print(f"{algo.upper():10} : {len(h)*4} bits  ({len(h)} caractères hex)")
