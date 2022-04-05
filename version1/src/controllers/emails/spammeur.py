#!/usr/local/bin/python3.10
import concurrent.futures as th
import email.mime.multipart
import email.mime.text
import smtplib
from pathlib import Path

SENDER = 'ardis.hotel68@gmail.com'  # email du spammuer
PASSWD = 'azertyuiop123789*'  # mot de passe du compte du spammeur
SERVER = 'smtp.gmail.com'  # serveur smtp

NUMBER_CUTT = 100  # nombre d'element qui seront couper
SERVER_PORT = 587  # port su serveur smtp
WORKER_THREAD = 150  # nombre de travailler qui seront utiliser


BODY = ''  # contenue du message
SUBJECT = ''  # object de l'email

FILENAME_DICT = ''  # chemin complet du dictionnaire


class EmailHandling:
    def __init__(self):
        """Instancie l'object SMTP est MIMEMutipar est ouvre une connexion en tls au serveur smtp 
        """
        self.smtp = smtplib.SMTP(SERVER, SERVER_PORT)
        self.msg = email.mime.multipart.MIMEMultipart()
        self.msg["Subject"] = SUBJECT
        self.msg["From"] = SENDER
        self.smtp.starttls()

    def connect(self):
        """Se connecte au serveur smtp, si les identification sont fausse il arrete le programme
        """
        try:
            self.smtp.login(SENDER, PASSWD)
        except smtplib.SMTPAuthenticationError:
            exit('Veuillez verifier vos identification')

    def send_msg(self, recipient: str):
        """Cette méthode prepare le message, ajoute le receveur est envoie le message  

        Args:
            recipient (str): receveur de l'email 
        """
        self.msg["To"] = recipient

        msgBody = email.mime.text.MIMEText(BODY)
        self.msg.attach(msgBody)

        self.smtp.sendmail(SENDER, recipient, self.msg.as_string()) # envoye le message

    def __del__(self):
        self.smtp.close()


def cutt_mail_part(filename: str):
    """Cette Methode determine a couper en combien le fichier.
    Il utilise la longeur de la mail list pour calculer les part a couper, elle n'oublie aucune ligne est fiable 100%
    Elle seras utiliser avec les thread pour etre plus rapide

    Args:
        filename (str): chemin entier de la mail liste

    Yields:
        list: liste du contenue du fichier
    """
    global NUMBER_CUTT
    file = Path(filename)
    if file.exists():
        if file.is_file():
            contents = []
            with open(filename, 'r', encoding='ISO-8859-1') as f:
                contents = [content for content in f.readlines()]
            lenght_contents = len(contents)

            cutt_part = round(lenght_contents / 100)

            if lenght_contents > 1000000:  # 1 million
                NUMBER_CUTT = 1000

            start = 0
            while start < lenght_contents:
                yield contents[start:cutt_part]
                start += NUMBER_CUTT
                cutt_part += NUMBER_CUTT

            # regarde si tout le contenue du fichier est utiliser
            if (start-NUMBER_CUTT) < lenght_contents:
                yield contents[start-NUMBER_CUTT: lenght_contents]


if __name__ == '__main__':
    import time
    
    start = time.perf_counter()
    email_hd = EmailHandling()
    email_hd.connect()
    for element in cutt_mail_part(FILENAME_DICT):
        with th.ThreadPoolExecutor(max_workers=WORKER_THREAD) as executor:
            executor.map(email_hd.send_msg, element)

    print(time.perf_counter() - start) # chronometre 
