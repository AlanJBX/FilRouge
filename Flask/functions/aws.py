#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functions.logger import logger

# Importation des librairies pour transfert vers AWS
import boto3
from botocore.exceptions import ClientError
from boto.s3.connection import S3Connection

def files_bucket(bucket):
	"""
	Liste des objets sur le bucket
	:param bucket: nom du bucket ciblé
	:type bucket: string
	:return: liste des fichiers présents sur le bucket
	:rtype: [string]
	"""

	logger.info("Début de chargement du bucket")

	try:

		s3 = boto3.client('s3')
		
		list_files = []
		for file in s3.list_objects(Bucket=bucket)['Contents']:
			if file['Key'][:len('StockageJSON/')] == 'StockageJSON/':
				list_files.append(file['Key'][len('StockageJSON/'):])

		logger.info("Liste des fichiers du bucket validé")
		return list_files

	except Exception as err:

		logger.error("Erreur dans le chargement du bucket | " +str(err))
		return False

def delete_file(bucket, s3_file):
	"""
	Supprimer un fichier du bucket S3
	:param bucket: nom du bucket ciblé
	:type bucket: string
	:param s3_file: nom du fichier à supprimer
	:type s3_file: string
	:return: réussite ou non
	:rtype: bool
	"""

	logger.info("Début de suppression du fichier du bucket")

	try:

		s3 = boto3.client('s3')
		s3.delete_object(Bucket= bucket, Key=s3_file)

		logger.info("Suppression du fichier du bucket validé")
		return True

	except Exception as err:

		logger.error("Erreur dans la suppression du fichier du bucket | " +str(err))
		return False

def download_file(local_file, bucket, s3_file):
	"""
	Téléchargement depuis le bucket S3
	:param local_file: nom de sauvegarde en local du fichier à télécharger
	:type local_file: string
	:param bucket: nom du bucket ciblé
	:type bucket: string
	:param s3_file: nom du fichier à télécharger
	:type s3_file: string
	:return: le fichier à télécharger deuis le bucket
	:rtype: [bool, file]
	"""
	logger.info("Début de téléchargement du fichier JSON")

	try:

		s3 = boto3.client('s3')
		
		s3.download_file(bucket, s3_file, local_file)
		file = (str(open(local_file,'r').read()))

		logger.info("Transfert du fichier depuis le bucket validé ")
		return_file = {}
		return_file["success"] = True
		return_file["file"] = file
		return return_file

	except Exception as err:

		logger.error("Erreur dans le transfert du fichier depuis le bucket | " + str(err))
		return_file = {}
		return_file["success"] = False
		return_file["file"] = err
		return return_file


def upload_file(local_file, bucket, s3_file):
	"""
	Téléchargement sur le bucket S3
	:param local_file: nom de sauvegarde en local du fichier à télécharger
	:type local_file: string
	:param bucket: nom du bucket ciblé
	:type bucket: string
	:param s3_file: nom du fichier à télécharger
	:type s3_file: string
	:return: réussite ou non
	:rtype: bool	
	"""

	logger.info("Début de transfert vers le bucket ")
	
	try:

		s3 = boto3.client('s3')

		s3.upload_file(local_file, bucket, s3_file)

		logger.info("Transfert du fichier vers le bucket validé ")
		return True

	except Exception as err:
		
		logger.error("Erreur dans le transfert du fichier vers le bucket | " + str(err))
		return False

def detect_labels(image):
	"""
	Appel de l'API rekognition
	:param image: image à envoyer à l'API
	:type image: string
	:return: les labels déterminés par l'API
	:rtype: [string]
	"""

	logger.info("Début de transfert vers API Rekognition ")

	try:

		reko=boto3.client('rekognition', 'eu-west-1')

		imgfile = open(image, 'rb')
		imgbytes = imgfile.read()
		imgfile.close() 
		response = reko.detect_labels(Image={'Bytes': imgbytes})

		response_return = []
		for k in response["Labels"]:
			response_return.append(k["Name"])

		logger.info("Appel de l'API Rekognition validé ")
		return response_return

	except Exception as err:

		logger.error("Erreur dans l'appel de l'API Rekognition | " + str(err))
		return False