import json


class ModelMain:
    """Classe qui s'occupe des donner en genérale 
    """

    def __init__(self, relative_path_data: str):
        """Methode constructrice 

        Args:
            relative_path_data (str): chemin relative du dossier data 
        """
        self.path_data = relative_path_data
        self.number_cutt = 150

    def write_json_dict(self, filename: str, data: dict):
        """Ecris les donnes dans un fichier json 

        Args:
            filename (str): seulement le nom du fichier
            data (dict): donne a ecrire
        """
        with open(self.path_data+filename, 'w') as f:
            json.dump(data, f)  # ecrit dans le ficher

    def cutt_list(self, filename: str, filename_ouput: str):
        """Coupe le fichier en pars, tout en gardant l'originale

        Args:
            filename (str): seulement nom du fichier
            filename_ouput (str): nom du fichier/ chemin relatife
        """
        with open(self.path_data+filename, 'r') as f:
            # NOTE on laisse le choix a l'utilisateur ou le stocker
            with open(filename_ouput, 'w') as f_two:
                for line in f.readlines()[:self.number_cutt]:
                    if line != '':
                        f_two.write(f'{line}')


class ModelExtension(ModelMain):
    """Classe qui gere les donnes des extensions 

    Args:
        ModelMain(str): chemin relative du dossier data
    """

    def __init__(self, relative_path_data: str):
        super().__init__(relative_path_data)

    def get_extension(self, filename: str):
        """Renvoie une liste d'extension

        Args:
            filename (str): nom du fichier (non le chemin relative)

        Returns:
            list : liste extension de fichier
        """
        with open(self.path_data+filename) as f:
            return [line for line in f.readlines()]
    
    
