import requests
import urllib3

from pathlib import Path
from bs4 import BeautifulSoup


# desactive le message d'attention ( comme on a mis a false a la verification de certification)
urllib3.disable_warnings()
RELATIVE_PATH_DATA = str(Path.cwd()) + '/data/'
extension_suffixe = {
                    'bdd': 'https://www.file-extension.info/fr/fichiers-de-base-de-donnes/',
                     'system': 'https://www.file-extension.info/fr/fichiers-systme',
                     'compresse': 'https://www.file-extension.info/fr/fichiers-compresss',
                     'texte': 'https://www.file-extension.info/fr/fichiers-text'
                    }


class GoogleDork:
    """Objet qui 
    """
    def __init__(self, model):
        self.page = 1
        # calculating start, (page=2) => (start=11), (page=3) => (start=21)
        self.start = (self.page - 1) * 10 + 1

        self.__model = model(RELATIVE_PATH_DATA)

        self.__api_key = ''
        self.__search_engine_id = ''
        self.url_base = f'https://www.googleapis.com/customsearch/v1?key={self.__api_key}&cx={self.__search_engine_id}'

        """
STEP 1: Recuperer les extension enregistrer, si elle le sont pas on les enregistre
STEP 2: ajouter le fyle type a la requete de base est recuperer les liens est en les enregistre 
( pourquoi ? , parce que'il faut pas allez dans le meme lien a chaque fois pour plus de chance de ne pas avoir la meme list)
        """

    def __requests_uri(self, params: dict): 
        """_summary_

        Args:
            params (dict): _description_

        Returns:
            _type_: _description_
        """
        return requests.get(self.url_base, params=params)
    
    def fyle_type(self, extensions: list): 
        for extension in extensions: 
            result = self.__requests_uri({'fileType': extension})
            if result.ok: 
                yield result.json()
                 
            
        
         
        

class ScrapingController:
    def __init__(self, model):
        self.namefile_extension = 'extension.json'
        self.model = model()

        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv :98.0) Gecko/20100101 Firefox/98.0", }

    def scrap_extension(self, url: str):
        """Capture les extension, cette methode marche que sur le site https://www.file-extension.info/fr/

        Args:
            url (str): lien de l'url

        Returns:
            list : liste d'extensions 
        """
        extension = []
        # NOTE Non verife certificat  SSL
        resp = requests.get(url, headers=self.headers, verify=False)
        if resp.ok:
            soup = BeautifulSoup(resp.text, 'lxml')
            for column in soup.find_all('td'):

                try:
                    extension.append(column.a['title'].lower()[1:])
                except TypeError:
                    pass

        return extension

    def save_suffix_extension(self, data: dict):
        """Enregistre les extension dans un fichier json 

        Args:
            data (dict) : donne a enregistrer, la clef contient le type
                                d'extension est la valeur l'url (qui seras remplacer)
        """
        for keys in data.keys():
            # NOTE met a la place de l'url, la liste d'extension
            data[keys] = self.scrap_extension(keys)

        # NOTE ecrit les donner dans un fichier json
        self.model.write_json_dict(self.namefile_extension, data)

    def already_registered_extension(self):
        """Methode qui verifie si les extensions sont deja enregistrer

        Returns:
            bool : vrai si le fichier est deja enregistrer avec une contenue, faux s'il n'existe pas ou qu'il  est vide
        """

        file = Path('data/'+self.namefile_extension)
        if file.exists():
            if file.read_text() != '':
                return True
        return False
