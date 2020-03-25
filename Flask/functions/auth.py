#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functions.logger import logger

# Gestion des mails
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Gestion des hashs
import hashlib

def send_mail(message):
	"""
	Fonction permettant d'avertir de l'ajout d'un utilisateur
	:param message: message à envoyer
	:type message: string
	:return: réussite ou non
	:rtype: bool
	"""
	
	try :
		msg = MIMEMultipart()
		msg['From'] = 'filRougeAlan@gmail.com'
		msg['To'] = 'alan.joubioux@student-cs.fr'
		msg['Subject'] = "Ajout d'un utilisateur" 
		msg.attach(MIMEText(message))
		mailserver = smtplib.SMTP('smtp.gmail.com', 587)
		mailserver.ehlo()
		mailserver.starttls()
		mailserver.ehlo()
		mailserver.login('filRougeAlan@gmail.com', 'promo2019')
		mailserver.sendmail('filRougeAlan@gmail.com', 'alan.joubioux@student-cs.fr', msg.as_string())
		mailserver.quit()

		logger.info("Mail envoyé ")
		return True

	except Exception as err:

		logger.error("Erreur dans l'envoi du mail | " + str(err))
		return False

def hash_mdp(password):
	"""
	Hashage du mot de passe
	:param password: mot de passe à hasher
	:type password: string
	:return: hash du mot de passe
	:rtype: string
	"""

	try :

		return hashlib.sha256(str(password).encode('utf-8')).hexdigest()

	except Exception as err:

		logger.error("Erreur dans le hash | " + str(err))
		return None

def new_user(user, password):
	"""
	Gestion du nouvel utilisateur
	:param user: nom d'utilisateur à ajouter
	:type user: string
	:param password: mot de passe à ajouter
	:type password: string
	:return: réussite ou non
	:rtype: bool
	"""

	try :
		couple = {}
		couple['user']= user
		couple['mdp']= hash_mdp(password) # On hashe directement le mot de passe.

		with open('./users.txt', 'a') as tmp:
			tmp.write(str(couple['user'])+","+str(couple['mdp'])+"\n")

		logger.info("Ajout du nouvel utilisateur ")
		return True

	except Exception as err:

		logger.error("Erreur dans l'ajout d'un nouvel utilisateur | " + str(err))
		return False

def load_users():
	"""
	Liste des utilisateurs enregistrés
	:return: liste des utilisateurs enregistrés
	:rtype: [string]
	"""

	try:

		users = {}
		with open("./users.txt") as file:
			for log in file:
				usr, psw = log.split(',')
				users[usr] = psw[:-1]

		logger.info("Chargement des utilisateurs ")
		return users

	except Exception as err:

		logger.error("Erreur dans le chargement des utilisateurs | " + str(err))
		return None

def test_new_users(new_username, new_password, new_mail):
	"""
	Vérification des identifiants et mails du nouvel utilisateur (existance, taille, forme)
	:param new_username: nom d'utilisateur à ajouter
	:type new_username: string
	:param new_password: mot de passe à ajouter
	:type new_password: string
	:param new_mail: mail de l'utilisateur à ajouter
	:type new_mail: string
	:return: réussite ou non
	:rtype: bool
	"""

	users = load_users()

	try:

		if new_username not in users:

			if test_identification("Nom utilisateur", new_username, 10, 3):

				if test_identification("Mot de passe", new_password, 15, 5):

					if test_mail(new_mail):
						return [True, "Identifiants corrects"]

					else:
						return [False, "Email incorrect"]

				else:
					return [False, "Mot de passe incorrect (entre 5 et 15 caractères)"]

			else:
				return [False, "Nom utilisateur incorrect (entre 3 et 10 caractères)"]
		else:

			logger.warning("Utilisateur déjà enregistré")
			return [False, "Utilisateur déjà enregistré"]
	
	except Exception as err:

		logger.error("Erreur dans le traitement du nouvel utilisateur | " + str(err))
		return False
		

def test_identification(categorie, identifiant, length_max, length_min):
	"""
	Vérification de la taille du nom utilisateur ou du mot de passe
	:param categorie: type de la variable à tester
	:type categorie: string
	:param identifiant: variable à tester
	:type identifiant: string	:param length_max: taille max de la variable	:type length_max: int	:param length_min: taille min de la variable	:type length_min: int	:return: réussite ou non	:rtype: bool
	"""

	try :

		if len(identifiant) < length_min:

			logger.warning(str(categorie) + " trop court")
			return False

		elif len(identifiant) > length_max:

			logger.warning(str(categorie) + " trop long")
			return False

		else:
				logger.info(str(categorie) + " accepté")
				return True

	except Exception as err:

		logger.error("Erreur dans le traitement du" + str(categorie) + " | " + str(err))
		return False

def test_mail(email):
	"""
	Vérification du format de l'adresse mail	
	:param email: adresse mail à tester	
	:type email: string	
	:return: réussite ou non	
	:rtype: bool
	"""

	try :

		nom, domaine = email.split('@')

		if len(nom) < 2:
			return False

		else:

			corps, extension = domaine.split('.')

			if len(corps) < 2:
				return False

			elif len(extension) < 2 or len(extension) > 4:
				return False

			else:
				return True

	except Exception as err:

		logger.error("Erreur dans le traitement de l'adresse mail | " + str(err))
		return False



