#####################################
f1	=	open('doc.txt',	'r')
import hashlib
import pyautogui
TK_SILENCE_DEPRECATION=1
pwd = pyautogui.password("Tapez le mot de passe : ")
pwd1=hashlib.md5(pwd.encode()).hexdigest()
def	reading_data(f):
    while	True:
        data	=	f.readline().strip()
        if	(data	==	'')	or	(data	==	None):
            break
        if hashlib.md5(data.encode()).hexdigest() == pwd1 :
            print(f"The hash of your Password : {hashlib.md5(data.encode()).hexdigest()} "
                  f"\n was Cracked,  \n your password : {pwd}")
            break
    if not data:
        print("Password not found :( ")
reading_data(f1)


