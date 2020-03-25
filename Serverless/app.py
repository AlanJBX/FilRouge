#!/usr/bin/env python
# -*- coding: utf-8 -*-

#curl -X POST "http://54.246.242.159:8000/rekognition" -F "data_file=@Ville.jpg" > ../../sortie.json

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

        print(type(fichier))

        if typeFichier in extension:

            #######################################
            print("# Envoi vers S3 du fichier REQUEST #")
            #######################################

            nomSauvegarde = str(datetime.now()) + '__' + fichier.filename
            fichier.save(os.path.join('./', nomSauvegarde))
            cheminSauvegarde = './' + nomSauvegarde

            upload_file(cheminSauvegarde, bucket_perso, 'Sauvegarde/'+nomSauvegarde)

            #######################################
            print("# Récupération depuis S3 du fichier REQUEST pour travail #")
            #######################################

            #download_file(cheminSauvegarde, bucket_perso, 'Sauvegarde/'+nomSauvegarde)

            #######################################
            print("# Métadonnées Générales #")
            #######################################

            nom_fichier = fichier.filename
            contenu = str(fichier.read())
            taillefichier = os.stat(cheminSauvegarde).st_size
            # + type_fichier

            #######################################
            print("# Métadonnées Rekognition #")
            #######################################

            try:
                if taillefichier < 5242880:
                    rekognition = detect_labels(cheminSauvegarde)
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

            objet = open(cheminSauvegarde,'rb')
            donneesJSON["fichier_bytes"] = str(objet.read())
            objet.close()
            

            fichierNomJSON = nomSauvegarde + '_to_JSON.json'

            print(donneesJSON["META"])

            with open("file_send", 'w') as tmp:
                json.dump(donneesJSON, tmp, indent=4)

            os.remove(cheminSauvegarde)

            return send_file("./file_send", as_attachment = True, attachment_filename = fichierNomJSON)
        else:
            return "L'API n'autorise que les fichiers de type gif, jpeg, jpg ou png."
    else:
        return "Aucun fichier envoyé."

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = False
    app.run(debug=True, host='0.0.0.0', port=8000)