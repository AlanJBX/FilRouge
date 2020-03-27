#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importation des librairies FLASK et C°
from werkzeug.utils import secure_filename
from flask import *
from flask_session import Session

# Importation des librairies générales
import string
import os
import os.path
import sys
import path

# Importation des fonctions
from functions.swagger import *
from functions.aws import *
from functions.traitement import *
from functions.logger import logger

application = Flask(__name__,template_folder='../templates')
application.secret_key = b'\xd5\x8af\xb4\x9e*1SN\xcbl\xc18\x7f\xa4\x96'

toSwagger(application)

# Déclaration du bucket de travail
bucket_perso = 'stockagefbsdpfilrougealan'

@application.route("/home")
def home():
	"""
	Page principale du service
	"""

	if True:

		if True:

			logger.info("HTTP : Page principale")	

		else:

			logger.info("HTTP : Page utilisateur")
		
		return render_template('menu_http.html')

	else:

		logger.info("Déconnexion automatique")
		flash("Déconnexion automatique")
		return redirect(url_for('logout'))

@application.route("/home/s3/list_bucket", methods=["GET"])
def list_bucket():	
	"""
	Méthode : retour des fichiers présents sur le bucket
	"""

	if True:

		try:

			with open('./tmp', 'w') as tmp:
				for file in files_bucket(bucket_perso):
					tmp.write(str(file)+'\n')
			
			logger.info("HTTP : Retour de la liste des fichiers du bucket")
			return send_file('../tmp', as_attachment = True, attachment_filename = 'liste_fichiers.txt')

		except Exception as err:

			logger.error("HTTP : Erreur dans le retour du bucket")
			return redirect(url_for('home'))
	else:

		logger.info("Déconnexion automatique")
		flash("Déconnexion automatique")
		return redirect(url_for('logout'))

@application.route("/home/s3/del_file", methods=["POST"])
def del_file():	
	"""
	Méthode : supprimer le fichier du bucket
	"""

	if True and True:

		if delete_file(bucket_perso,'StockageJSON/'+ str(request.form["file_del"])):

			logger.info("Suppression du fichier")
			flash("Suppression du fichier")
			return redirect(url_for('home'))

		else:

			logger.warning("Erreur dans la suppression du fichier")
			flash("Erreur dans la suppression du fichier")
			return redirect(url_for('home'))

	else:

		logger.warning("Pas les autorisations")
		flash("Vous n'avez pas les droits pour cette fonction")
		return redirect(url_for('home'))

@application.route("/home/s3/get_file", methods=["POST"])
def get_file():	
	"""
	Méthode : récupérer le fichier sur le bucket
	"""
	
	try :
		
		if True and True:
			
			
			return_file = download_file(request.form["file_get"], bucket_perso, 'StockageJSON/'+ str(request.form["file_get"]))
			
			if return_file["success"]:
				
				with open('./tmp', 'w') as tmp:
					json.dump(return_file["file"], tmp, indent=4)
				
				return send_file('../tmp', as_attachment = True, attachment_filename = request.form["file_get"])	

			else:
						
				logger.error("Erreur dans le téléchargement | " + str(return_file["file"]))
				flash("Erreur dans le téléchargement")
				return redirect(url_for('home'))
		
		else:

			logger.info("Pas les autorisations")
			flash("Vous n'avez pas les droits pour cette fonction")
			return redirect(url_for('home'))

	except Exception as err:

		logger.error("Erreur dans le téléchargement depuis le bucket | " + str(err))
		flash("Erreur dans le téléchargement depuis le bucket")
		return redirect(url_for('home'))


@application.route("/home/convert", methods=["GET"])
def convert():
	"""
	Page de conversion
	"""
	try:

		if True:

			logger.info("HTTP : Page convertisseur")
			return render_template('convertisseur_http.html')

		else:

			logger.info("Déconnexion automatique")
			flash("Déconnexion automatique")
			return redirect(url_for('logout'))

	except Exception as err:

			logger.error("HTTP : Erreur dans l'afficage du convertisseur | " + str(err))
			flash("Erreur dans l'affichage du convertisseur")
			return redirect(url_for('logout'))

@application.route("/home/convert/fichierJSON", methods=["POST"])
def JSONify():
	"""
	Méthode : conversion en JSON du fichier
	"""
	logger.info("HTTP : Début conversion")

	if True:

		try:

			return_json = toJSON(request.files["data_file"],bucket_perso) # Conversion du fichier

			return send_file(return_json["file"], as_attachment = True, attachment_filename = return_json["name"])
		
		except Exception as err:

			logger.error("HTTP : Erreur dans la conversion | " + str(err))
			return redirect(url_for('convert'))

	else:

		logger.info("Déconnexion automatique")
		flash("Déconnexion automatique")
		return redirect(url_for('logout'))
