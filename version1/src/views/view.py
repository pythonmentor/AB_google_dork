

class ViewMain: 
    def init(self): 
        print("""
              
              
              """)

class ViewPick:
    def __init__(self):
        self.choice = 0 
        
        
    def choice_mode(self): 
        print("""
            Mode 1: email:password
            Mode 2: email       
        """)
        self.choice =  input('Veuillez choisir un mode: ') # FIXME verifier si c'est un nombre 