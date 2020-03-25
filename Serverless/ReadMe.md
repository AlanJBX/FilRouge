Lancement du Serverless
========================

Après avoir téléchargé le repository et vérifié les credentials keys et les droits d'accès à l'API Rekognition

Mise en place de l'environnement virtuel
```
bash script_venv.sh
```

Lanncement de l'environnement virtuel
```
source venv/bin/activate
```

Mise en place des librairies
```
bash script_lib.sh
```

Déploiement du serverless
```
sls deploy
```

Test de l'application
```
curl -X POST "http://@IPv4:8000/rekognition" -F "data_file=@~FilRouge/Testeurs/Ville.jpg" > Ville_from_JPEG_to_JSON.json
```
Attention à la mise à jour de l'adresse IP ainsi que le chemin d'accès au fichier test.