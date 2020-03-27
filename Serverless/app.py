#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importation des librairies FLASK et C°
from flask import *

# Importation des librairies générales
from datetime import datetime
import json
import string
import os
import os.path
import sys
import path

from aws import *

app = Flask(__name__)

@app.route("/rekognition", methods=['GET', 'POST'])
def uploadFichier():

    extension = ["image/gif", "image/jpeg", "image/png", "image/jpg"]

    bucket_perso = "stockagefbsdpfilrougealan"

    if 'data_file' in request.files:

        fichier = request.files['data_file']
        typeFichier = fichier.content_type

        if typeFichier in extension:

            #######################################
            print("# Envoi vers S3 du fichier REQUEST #")
            #######################################

            nomSauvegarde = str(datetime.now()) + '__' + fichier.filename
            datafile = filetodisplay.read()
            file =  BytesIO(datafile)
            upload_file(file, bucket_perso, 'Sauvegarde/'+nomSauvegarde)

            #######################################
            print("# Récupération depuis S3 du fichier REQUEST pour travail #")
            #######################################

            output_file = download_file('fichier', bucket_perso, 'Sauvegarde/'+nomSauvegarde)

            #######################################
            print("# Métadonnées Générales #")
            #######################################

            nom_fichier = fichier.filename
            contenu = str(open(output_file,'rb').read())
            taillefichier = os.stat(output_file).st_size
            # + type_fichier

            #######################################
            print("# Métadonnées Rekognition #")
            #######################################

            try:
                if taillefichier < 5242880:
                    rekognition = detect_labels(output_file)
                else:
                    rekognition = "Taille trop grande pour API Rekognition"

            except Exception as err:
                rekognition =  "Rekognition : " + str(err)
           
            #######################################
            print("# Mise en forme, nettoyage et retour du fichier JSON #")
            #######################################

            donneesJSON = {}
            
            donneesJSON["META"] = {}            
            donneesJSON["META"]["nom_fichier"] = nom_fichier
            donneesJSON["META"]["type_fichier"] = typeFichier
            donneesJSON["META"]["taille_fichier"] = taillefichier
            donneesJSON["META"]["labels_rekognition"] = rekognition

            donneesJSON["fichier_bytes"] = contenu

            donnees = json.dump(donneesJSON, tmp, indent=4)

            return donnees
        else:
            return "L'API n'autorise que les fichiers de type gif, jpeg, jpg ou png."
    else:
        return "Aucun fichier envoyé."

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = False
    app.run(debug=True, host='0.0.0.0', port=8000)