#! /usr/local/bin/python3.10
from src.controllers.search_google import GoogleDork, ScrapingController 
from src.models.model import ModelMain  

google = GoogleDork(ModelMain) 
scraping = ScrapingController(ModelMain)
print(scraping.already_registered_extension()) # NOTE doit renvoyez false si le fichier est vide ou si il n'existe pas 