import requests 
import re  

class PickMain: 
    def __init__(self, url: str, view):
        self.view = view() # NOTE objet de la vue 
        self.namefile = ''
        self.file_write = open(self.namefile, 'w')
        
        self.params_required = {}
        self.headers = {"User-Agent" : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv :98.0) Gecko/20100101 Firefox/98.0"}
        
        self.url_base = self.__format_url_base(url)
        
    def __format_url_base(self, url: str): 
        """Methode privée qui enleve les parametres de l'url  

        Args:
            url (str): url donner 

        Returns:
            str:url de base sans paramtre 
        """
        return url.split('?')[0]
    
    
    def get_page_content(self): 
        """Execute une requete en POST pour recuperer le contenue de la page.
            Elle doit etre utliser apres avoir specifier les paramatre requis 

        Returns:
            str: contenue de la page
        """
        return requests.post(self.url_base, headers=self.headers, params=self.params_required).text
            
    
    def __del__(self): 
        """Ferme le fichier 
        """
        self.file_write.close()
        
    

class PickEmail(PickMain): 
    """ 
    Mode 1: email:password
    mode 2: email (simple)
    """
    def __init__(self, url: str, view):
        super().__init__(url, view)
        self.namefile = 'email_list.dict'
        
    
    def mode_one(self, content_page: str): # NOTE example  https://xn--e1alhsoq4c.xn--p1ai/base/Mail.txt 
        """Cette methode utilise le mode 1, c'est a dire que le contenue de la page est formatter de cette façon email:password.
        recuperer l'email est l'ecri dans le fichier 

        Args:
            content_page (str): _description_
        """
        for element_one, element_two in zip(content_page.split(':'), content_page.split('\n')): 
            try: 
                email_probality_one =  element_one.split('\n')[1] # l'email propable 
                email_probality_two =  element_two.split(':')[0]
            
            except IndexError:
                pass 
            
            else: 
                if re.search('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$',email_probality_one):  # expression regulierer pour voir si c'est un email 
                    self.file_write.write(f'{email_probality_one}\n') # write email uniquement 
            
                elif re.search('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$',email_probality_two): 
                    self.file_write.write(f'{email_probality_two}\n') # write email uniquement 
             
    
    def mode_two(self): 
        pass 
    
    def __del__(self):
        return super().__del__()
    
    
class PickNum(PickMain): 
    def __init__(self, url: str, view):
            super().__init__(url, view)
        
        
    
    def __del__(self):
        return super().__del__()
    