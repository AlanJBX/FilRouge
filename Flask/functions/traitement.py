#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importation des librairies FLASK et C°
from werkzeug.utils import secure_filename
from flask import *

# Importation des librairies générales
import string
import os
import os.path
import sys
import path
import json
from datetime import datetime

# Importation des fonctions
from functions.extensions import *
from functions.aws import *
from functions.logger import logger

def toJSON(fichier, bucket_perso):
	"""
	Fonction de convertisseur :
	Etape 1.0 : récupérer le fichier et déterminer son extension
	Etape 1.1 : tester l'extension
	Etape 2 : sauvegarde du fichier REQUEST en local de l'instance
	Etape 3.0 : récupération des métadonnées générales
	Etape 3.1 : si possible, récupérations des métadonnées particuliètes
	Etape 3.2 : stockage des métadonnées et du fichier en binaire dans un fichier JSON
	Etape 4.0 : sauvegarde du fichier JSONify en local de l'instance
	Etude 4.1 : envoi sur S3 du fichier REQUEST et JSONify
	Etade 5.0 : retour du fichier JSONify à l'utilisateur
	:param fichier: nom du fichier à traiter
	:type fichier: string
	:param bucket_perso: nom du bucket support
	:type bucket_perso: string
	:return: fichier traité
	:rtype: {string, string}
	"""

	logger.info("Initialisation des extensions prises en compte")

	listePDF = ['.pdf']
	listeIMG = ['.jpeg','.png','.jpg','.gif','.bmp']
	listeAutre = ['.txt', '.csv','.py', '.ods', '.odt', '.odg', '.ipynb', '.json', '.docx', '.doc', '.xls', '.tex']
	listeExtensions = listePDF + listeIMG + listeAutre

	logger.info("Récupération du fichier source")

	fichierType= fichier.content_type
	fichierNom = str(fichier.filename.replace(" ",""))

	extension = test_extension(fichierNom, listeExtensions)

	if not extension["resultat"]:

		logger.warning("Extension non prise en compte")
		return "Extension non prise en compte"

	else :

		logger.info("Stockage en local du fichier source")

		nomSauvegarde = str(datetime.now()) + '__' + fichierNom
		fichier.save(os.path.join('./Sauvegarde', nomSauvegarde))
		cheminSauvegarde = './Sauvegarde/' + nomSauvegarde

		try:
	 
			logger.info("Initialisation des variables JSON de travail")

			donneesJSON = {}
			metadonnees = {}
			
			donneesJSON["META"] = metadonnees
			donneesJSON["fichier_bytes"] = {}

			logger.info("Métadonnées générales")

			metadonnees["fichiernom"] = fichierNom
			metadonnees["type"] = fichierType
			metadonnees["taille"] = os.stat(cheminSauvegarde).st_size
			metadonnees["extension"] = extension["extension"]

			logger.info("Métadonnées particulières")

			if extension["extension"] in listeIMG:

				metadonnees = meta_image(cheminSauvegarde,metadonnees)
			
			elif extension["extension"] in listePDF :

				metadonnees = meta_pdf(cheminSauvegarde,metadonnees)

			logger.info("Remplissage des variables JSON")

			objet = open(cheminSauvegarde,'rb')
			donneesJSON["fichier_bytes"] = str(objet.read())

			Nomfichier = fichierNom[0:fichierNom.find('.')] + '_from_' + extension["extension"][1:]
			fichierNomJSON = Nomfichier + '_to_JSON__' + str(int(os.stat(cheminSauvegarde).st_birthtime)) + '.json'
			fichierJSON = './StockageJSON/' + fichierNomJSON

			objet.close()

			logger.info("Stockage en local du fichier JSON")

			with open(fichierJSON, 'w') as tmp:
				json.dump(donneesJSON, tmp, indent=4)

			logger.info("Envoi du fichier source vers S3")

			upload_file(cheminSauvegarde, bucket_perso, 'Sauvegarde/'+nomSauvegarde)

			logger.info("Envoi du fichier JSON vers S3")

			upload_file(fichierJSON, bucket_perso, 'StockageJSON/'+str(fichierNomJSON))

			logger.info("Retour du fichier JSON")

			# Pour restituer correctement le fichier à retourner.
			fichierJSON = '../StockageJSON/' + fichierNomJSON

			reponse = {}
			reponse["file"] = fichierJSON
			reponse["name"] = fichierNomJSON

			return reponse

		except Exception as err:
			
			logger.error("Erreur dans le traitement du fichier | " + str(err))
			return False