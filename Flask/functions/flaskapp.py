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
from functions.aws import *
from functions.auth import *
from functions.traitement import *
from functions.logger import logger

application = Flask(__name__,template_folder='../templates')
application.secret_key = b'\xd5\x8af\xb4\x9e*1SN\xcbl\xc18\x7f\xa4\x96'

# Déclaration du bucket de travail
bucket_perso = 'stockagefbsdpfilrougealan'

@application.route("/")
def login():
	"""
	Page d'accueil
	"""
	logger.info("Ouverture de la page de connexion")
	return render_template('entree.html')

@application.route("/login", methods=['POST'])
def check_login():
	"""
	Gestion des utilisateurs enregistrés avec différenciation admin / other
	"""
	logger.info("Début identification")

	usr = load_users()
	psw = hash_mdp(request.form['password'])

	try :
		if request.form['username'] not in usr:

			logger.warning("Identifiant incorrect")
			flash("Identifiant incorrect")
			return redirect(url_for('login'))

		else:

			if usr[request.form['username']] == psw:

				session['logged_in'] = True

				if request.form['username'] == 'admin':

					session['admin'] = True

				else :

					session['admin'] = False

				session['name'] = request.form['username']
				logger.info(session['name'] + " | Identification réussie")
				return redirect(url_for('home'))

			else:

				logger.warning("Mot de passe incorrect")
				flash("Mot de passe incorrect")
				return redirect(url_for('login'))

	except Exception as err:
		
		logger.error("Erreur dans l'identification | " + str(err))
		flash("Erreur dans l'identification")
		return redirect(url_for('login'))

@application.route("/register", methods=['POST'])
def register():
	"""
	Page d'enregistrement
	"""
	logger.info("Ouverture de la page d'enregistrement")
	return render_template('enregistrer.html')

@application.route("/register/add_user", methods=['POST'])
def add_user():
	"""
	Gestion d'un nouvel utilisateur
	"""

	logger.info("Début enregistrement d'un nouvel utilisateur")

	retour_test = test_new_users(request.form['new_username'], request.form['new_password'], request.form['new_email'])

	if retour_test[0]:

		new_user(request.form['new_username'],request.form['new_password'])

		session['logged_in'] = True
		session['admin'] = False
		session['name'] = request.form['new_username']

		message = 'Un nouvel utilisateur : ' + request.form['new_username'] + ' souhaite accéder au service. Son mail : ' + request.form['new_email']
		send_mail(str(message))

		logger.info(session['name'] + " | Nouvel utilisateur enregistré")
		flash("Nouvel utilisateur enregistré")
		return redirect(url_for('home'))

	else:
		logger.error("Erreur dans l'enregistrement du nouvel utilisateur | " + str(retour_test[1]))
		flash(retour_test[1])
		return render_template('enregistrer.html')

		DPP_from_png_to_JSON__1584647357.json

@application.route("/logout", methods=["POST"])
def logout():
	"""
	Gestion de la déconnexion.
	"""

	session['logged_in'] = False

	logger.info(session['name'] + " | Déconnexion réussie")
	flash("Déconnexion réussie")
	return redirect(url_for('login'))

@application.route("/login/home")
def home():
	"""
	Page principale du service
	"""

	if session.get('logged_in'):

		if session.get('admin'):

			logger.info(session['name'] + " | Page admin")	

		else:

			logger.info(session['name'] + " | Page utilisateur")
		
		return render_template('menu.html')

	else:

		logger.info("Déconnexion automatique")
		flash("Déconnexion automatique")
		return redirect(url_for('logout'))

@application.route("/login/home/s3/list_bucket")
def list_bucket():	
	"""
	Méthode : retourner des fichiers présents sur le bucket
	"""

	if session.get('logged_in'):

		try:

			with open('./tmp', 'w') as tmp:
				for file in files_bucket(bucket_perso):
					tmp.write(str(file)+'\n')
			
			logger.info(session['name'] + " | Retour de la liste des fichiers du bucket")
			return send_file('../tmp', as_attachment = True, attachment_filename = 'liste_fichiers.txt')

		except Exception as err:

			logger.error(session['name'] + " | Erreur dans le retour du bucket")
			return redirect(url_for('home'))
	else:

		logger.info("Déconnexion automatique")
		flash("Déconnexion automatique")
		return redirect(url_for('logout'))

@application.route("/login/home/s3/del_file", methods=["POST"])
def del_file():	
	"""
	Méthode : supprimer le fichier du bucket
	"""

	if session.get('logged_in') and session['admin']:

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

@application.route("/login/home/s3/get_file", methods=['POST'])
def get_file():	
	"""
	Méthode : récupérer le fichier sur le bucket
	"""
	
	try :
		
		if session.get('logged_in') and session['admin']:
			
			
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


@application.route("/login/home/convert", methods=["POST"])
def convert():
	"""
	Page de conversion
	"""
	try:

		if session.get('logged_in'):

			logger.info(session['name'] + " | Page convertisseur")
			return render_template('convertisseur.html')

		else:

			logger.info("Déconnexion automatique")
			flash("Déconnexion automatique")
			return redirect(url_for('logout'))

	except Exception as err:

			logger.error(session['name'] + " | Erreur dans l'afficage du convertisseur | " + str(err))
			flash("Erreur dans l'affichage du convertisseur")
			return redirect(url_for('logout'))

@application.route("/login/home/convert/fichierJSON", methods=["POST"])
def JSONify():
	"""
	Méthode : conversion en JSON du fichier
	"""
	logger.info(session['name'] + " | Début conversion")

	if session.get('logged_in'):

		try:
			return_json = toJSON(request.files["data_file"],bucket_perso) # Conversion du fichier
			return send_file(return_json["file"], as_attachment = True, attachment_filename = return_json["name"])

		except Exception as err:

			logger.error(session['name'] + " | Erreur dans la conversion | " + str(err))
			return redirect(url_for('convert'))

	else:

		logger.info("Déconnexion automatique")
		flash("Déconnexion automatique")
		return redirect(url_for('logout'))