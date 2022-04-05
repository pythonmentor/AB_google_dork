#!/usr/local/bin/python3.10
# utiliser le spammeur est envoyer un message, si il leve une execptions alors l'email existse pas

import Controllers.emails.spammeur as spam 
from  smtplib import SMTPSenderRefused
import time 

spam.FILENAME_DICT = '/home/ayoub/email_list/mail_list_mail_russia.dict' # chemin complet du fichier dictionnaire
email_hd = spam.EmailHandling()
email_hd.connect()

for emails in spam.cutt_mail_part(spam.FILENAME_DICT):
    for email in emails: 
        try: 
            email_hd.send_msg(email.strip())
        except SMTPSenderRefused:
            print('Le serveur nous a bloquer, une pause de 15 seconde est neccaissaire')
            time.sleep(15)             