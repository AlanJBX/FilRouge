Lancement du serveur
=====================

Après avoir : cloné le repository, installé les librairies et fabriquer les certificats 
(voir : https://github.com/AlanJBX/FilRouge/tree/master/IP )

Lancement du serveur :
```
gunicorn-3.7 --certfile=certificat.crt --keyfile=certificat.key --bind 0.0.0.0:443 __init__:application
```

Lancement HTTPS, disponible sur https://54.246.242.159/ (ou modification de l'adresse IP par votre adresse IP)
```
gunicorn-3.7 --bind 0.0.0.0:8000 __init__http:application
```
Lancement HTTP, disponible sur http://54.246.242.159:8000/home (ou modification de l'adresse IP par votre adresse IP)