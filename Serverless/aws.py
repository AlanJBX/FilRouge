#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importation des librairies pour transfert vers AWS
import boto3
from botocore.exceptions import ClientError
from boto.s3.connection import S3Connection

def upload_file(entry_file, bucket, output_s3_file):
    """
    Téléchargement sur le bucket S3
    :param entry_file: nom de sauvegarde en local du fichier à télécharger
    :type entry_file: string
    :param bucket: nom du bucket ciblé
    :type bucket: string
    :param output_s3_file: nom du fichier à télécharger
    :type output_s3_file: string
    :return: réussite ou non
    :rtype: bool    
    """
    #######################################
    print("# Début transfert de fichier #")
    #######################################
    
    try:

        s3 = boto3.client('s3')

        #######################################
        print("# Télé..", end='')
        #######################################
        s3.upload_fileobj(entry_file, bucket, output_s3_file)
        #######################################
        print(".chargement réussi #")
        #######################################
        return "Téléchargement réussi"
    except Exception as err:
        #######################################
        print("Téléchargement sur le bucket : " + str(err))
        #######################################
        return False

def download_file(output_file, bucket, input_s3_file):
    """
    Téléchargement depuis le bucket S3
    :param output_file: nom de sauvegarde en local du fichier à télécharger
    :type output_file: string
    :param bucket: nom du bucket ciblé
    :type bucket: string
    :param input_s3_file: nom du fichier à télécharger
    :type input_s3_file: string
    :return: le fichier à télécharger depuis le bucket
    :rtype: file
    """
    #######################################
    print("# Début de téléchargement depuis le bucket #")
    #######################################

    try:

        s3 = boto3.client('s3')
        
        file_return = s3.download_file(bucket, input_s3_file, output_file)

        #######################################
        print("# Transfert du fichier depuis le bucket validé # ")
        #######################################        

        return file_return

    except Exception as err:

        #######################################
        print("Erreur dans le transfert du fichier depuis le bucket | " + str(err))
        #######################################    

        return "Erreur dans le transfert du fichier depuis le bucket | " + str(err)

def detect_labels(image):
    """
    Appel de l'API rekognition
    :param image: image à envoyer à l'API
    :type image: string
    :return: les labels déterminés par l'API
    :rtype: [string]
    """
    try:
        #######################################
        print("# Début rekognition du fichier #")
        #######################################

        reko=boto3.client('rekognition', 'eu-west-1')

        #######################################
        print("# Etude reko...", end='')
        #######################################

        imgfile = open(image, 'rb')
        imgbytes = imgfile.read()
        imgfile.close()
        response = {}
        response = reko.detect_labels(Image={'Bytes': imgbytes})
        
        response_return = []
        for k in response["Labels"]:
            response_return.append(k["Name"])

        #######################################
        print("gnition du fichier #")
        #######################################

        return response_return

    except Exception as err:
        #######################################
        print("Utilisation de rekognition : " + str(err))
        #######################################
        response_return = "Erreur dans la détection via API Rekognition"
        return response