#! /usr/local/bin/python3.10
import faker
import requests
from bs4 import BeautifulSoup
""" https://www.pages-annuaire.net/res/search?q=Ayoub&w=Colmar"""
URL_BASE = 'https://www.pages-annuaire.net/res/search?q=Ayoub&w=Colmar'  # url de base
NUMBER_MAX = 150


HEADER = {
    # "User-Agent" : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv :98.0) Gecko/20100101 Firefox/98.0",
    # "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    # "Accept-Language" : "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
    # "Accept-Encoding" : "gzip, deflate",
    # "Content-Type" : "application/x-www-form-urlencoded",
    # "Content-Length" : "4210",
    # "Upgrade-Insecure-Requests" : "1",
    # "Sec-Fetch-Dest" : "document",
    # "Sec-Fetch-Mode" : "navigate",
    # "Sec-Fetch-Site" : "same-origin",
    # "Sec-Fetch-User" : "?1",
    # "Cache-Control" : "max-age=0",
    # "Te" : "trailers"
    }

fake = faker.Faker('fr_FR')
# NOTE recuperer un nombre  nom français
names = [fake.unique.name() for _ in range(NUMBER_MAX)]
# NOTE recuperer un nombre de departements
departements = [fake.department() for _ in range(NUMBER_MAX)]

# NOTE classe mere des piquer numero
class PickNum:
    def __init__(self):
        self.file_write = open('nl.dict', 'w')

        self.params_required = {}  # NOTE les paramatres obligatoire
        self.url = self.format_url()

    def format_url(self):
        return URL_BASE.split('?')[0]
        # NOTE recupere l'url sans les parametres (si jamais y' en a)

    def get_page_content(self):  # NOTE retourner le contenue de la page
        return requests.post(self.url, headers=HEADER, params=self.params_required).text
        

    def __del__(self):
        self.file_write.close()

class PageJaunesNum(PickNum):
    def __init__(self):
        super().__init__()
        self.params_required['quoiqui'] = 'ab'
        self.params_required['ou'] = 'Alsace'
        self.params_required['univers'] = "pagesjaunes"

    def get_numbers(self):
        resp = self.get_page_content()
        return resp
        soup = BeautifulSoup(resp.text, 'lxml')
        return [num for num in soup.find_all('span')]


if __name__ == '__main__':
    pg = PageJaunesNum()
    print(pg.get_numbers())
    
