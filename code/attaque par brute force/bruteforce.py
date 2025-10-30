import string
chars=list(string.printable)
import pyautogui
pwd=pyautogui.password("Donnez votre vote de passe")
mot_de_passe=""
import random
while mot_de_passe!=pwd:
    mot_de_passe=random.choices(chars,k=len(pwd))
    print("##########",mot_de_passe,"##########")
    if mot_de_passe==list(pwd):
        print("Votre mot de passe est ","".join(mot_de_passe))
        break

        

