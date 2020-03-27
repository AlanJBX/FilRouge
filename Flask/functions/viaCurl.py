#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import requests
import os
import json

def viaCurl(fichier):
	"""
	Requête CURL vers une autre API
	:param fichier: fichier à envoyer en requête
	:return: retour de l'API appellée
	:rtype: {string, string}
	"""
	nomSauvegarde = "viaCURL_" + fichier.filename 
	fichier.save(os.path.join('./Sauvegarde', nomSauvegarde))
	cheminSauvegarde = './Sauvegarde/' + nomSauvegarde

	objet = open(cheminSauvegarde,'rb')

	url = "http://54.246.242.159:8000/home/convert/fichierJSON"
	files = {'data_file' : objet}

	response = requests.post(url, files=files)

	fichierNomCURL = nomSauvegarde + '_to_JSON__' + str(int(os.stat(cheminSauvegarde).st_birthtime)) + '.json'
	fichierCURL = './StockageJSON/' + fichierNomCURL

	with open(fichierCURL, 'w') as tmp:
		json.dump(response.text, tmp, indent=4)

	fichierCURL = '../StockageJSON/' + fichierNomCURL

	return_json = {}
	return_json["file"] = fichierCURL
	return_json["name"] = fichierNomCURL

	return return_json