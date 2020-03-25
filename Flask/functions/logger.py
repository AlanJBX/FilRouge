#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from logging.handlers import RotatingFileHandler

# Création de l'objet logger qui va nous servir à écrire dans les logs
logger = logging.getLogger()
# On met le niveau minium du logger à DEBUG
logger.setLevel(logging.DEBUG)

# Création d'un formateur qui va ajouter le temps et le niveau de chaque message quand on écrira un message dans le log
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

#  Création d'un handler qui va rediriger une écriture du log vers un fichier en mode 'append', avec 1 backup et une taille max de 10Mo
file_handler_general = RotatingFileHandler('activity.log', 'a', 10000000, 1)

# On lui met le niveau minimum sur DEBUG, on lui dit qu'il doit utiliser le formateur créé précédement et on ajoute ce handler au logger
file_handler_general.setLevel(logging.DEBUG)
file_handler_general.setFormatter(formatter)
logger.addHandler(file_handler_general)

# Création d'un nouvel handler avec le niveau minimum sur WARNING
file_handler_error = RotatingFileHandler('error.log', 'a', 1000000, 1)
file_handler_error.setLevel(logging.WARNING)
file_handler_error.setFormatter(formatter)
logger.addHandler(file_handler_error)

# Création d'un troisième handler qui va rediriger chaque écriture de log de niveau minimum INFO sur la console
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)