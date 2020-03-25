#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functions.logger import logger

# Importation des librairies pour métadonnées
import mimetypes
from exif import Image
import PIL.Image 
from PIL.ExifTags import *
import PyPDF2

# Importation de la libraire AWS
from functions.aws import detect_labels

def test_extension(fichierNom, listeExtensions):
	"""
	Vérification de la prise en compte de l'extension
	:param fichierNom: nom du fichier à tester
	:type fichierNom: string
	:param listeExtensions: liste des extensions prises en compte
	:type listeExtensions: [string]	
	:return: réussite ou non et extension du fichier
	:rtype: [bool, string]	
	"""

	logger.info("Etude de l'extension")

	try:

		retour = {}
		extension = "".join(reversed("".join(reversed(fichierNom))[0:"".join(reversed(fichierNom)).find('.')].lower() + "."))

		logger.info("Test du l'extension")

		if extension not in listeExtensions :

			retour["resultat"] = False
			logger.warning("Extension non prise en compte")
			return retour

		else:

			retour["resultat"] = True
			retour["extension"] = extension
			logger.info("Extension prise en compte")
			return retour

	except Exception as err:

		retour["resultat"] = False
		logger.error("Erreur dans le test de l'extension | " + str(err))
		return retour

def meta_image(cheminSauvegarde,metadonnees):
	"""
	Traitement des métadonnées des fichiers IMG
	:param cheminSauvegarde: fichier à traiter
	:type cheminSauvegarde: string
	:param metadonnees: métadonnées du fichier
	:type metadonnees: dict
	:return: métadonnées du fichier
	:rtype: dict
	"""

	logger.info("Métadonnées IMG")

	try:

		image = PIL.Image.open(cheminSauvegarde)

		try:

			for k, v in image._getexif().items():
				if k in PIL.ExifTags.TAGS:
					metadonnees["metaExifIMG"] = {PIL.ExifTags.TAGS[k]: v}

		except Exception as err:

			logger.error("Erreur dans les métadonnées EXIF | " + str(err))
			metadonnees["metaExifIMG"] = "Erreur, vérifier présence de métadonnées ou extension"
			return metadonnees

		try:

			if metadonnees["taille"] < 5242880 and metadonnees["extension"] in ['.jpeg','.jpg','.png']:
				metadonnees["metaRekoIMG"] = detect_labels(cheminSauvegarde)

			else:
				logger.warning("Fichier non valide pour API Rekognition")
				metadonnees["metaRekoIMG"] = "Fichier non valide pour API Rekognition"

		except Exception as err:

		 	logger.error("Erreur dans les métadonnées REKO | " + str(err))
		 	metadonnees["metaRekoIMG"] = "Erreur dans les métadonnées REKO"
		 	return metadonnees

		logger.info("Retour des métadonnées IMG")
		return metadonnees

	except Exception as err:

		logger.warning("Erreur dans les métadonnées IMG | " + str(err))
		return metadonnees

def meta_pdf(cheminSauvegarde,metadonnees):
	"""
	Traitement des métadonnées des fichiers PDF
	:param cheminSauvegarde: fichier à traiter
	:type cheminSauvegarde: string
	:param metadonnees: métadonnées du fichier
	:type metadonnees: dict
	:return: métadonnées du fichier
	:rtype: dict
	"""

	logger.info("Métadonnées PDF")

	try:

		pdf = PyPDF2.PdfFileReader(cheminSauvegarde)
		metadonnees["metaPyPDFxmp"] = pdf.getXmpMetadata()
		metadonnees["metaPyPDFdoc"] = pdf.getDocumentInfo()
		metadonnees["metaPyPDFnumpage"] = pdf.getNumPages()
		metadonnees["metaPyPDFfields"] = pdf.getFields()
		logger.info("Retour des métadonnées PDF")
		return metadonnees

	except Exception as err:

		logger.warning("Erreur dans les métadonnées PDF | " + str(err))
		metadonnees["metaPDF"] = "Erreur, vérifier présence de métadonnées ou extension"
		return metadonnees