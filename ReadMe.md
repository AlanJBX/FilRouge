Introduction
==============

### Prise en main

Dans un premier temps afin de découvrir l'outil conçu, je vous invite à vous rendre sur les liens suivant :

* Lien vers l'application développée en HTTPS avec identification et authentification.
https://54.246.242.159/


* Lien vers l'application développée en HTTP sans identification et authentification ainsi que sa documentation SWAGGER.
http://54.246.242.159:8000/home  &  http://54.246.242.159:8000/swagger/

Vous trouverez les quatres fonctionnalités suivantes :
- Convertisseur de fichier : convertit un fichier donné en un fichier au format JSON : {métadonnées, fichier_binaire}
- Liste des fichiers : liste des fichiers JSONifiés présents sur le bucket de stockage
- Suppression d'un fichier : supprime un fichier JSONifié donné du bucket de stockage
- Récupération d'un fichier : récupère un fichier JSONifié donné du bucket de stockage

Afin d'accéder à l'ensemble de la documentation de ce projet, vous pouvez soit lire le PDF présent à la racine du repository ou vous rendre sur le lien suivant : https://PFRAlanJBX.readthedocs.io/

### Présentation du GIT

Vous trouverez dans ce repository les dossiers suivant :

- Dossier IP : l'ensemble des fichiers et scripts permettant la mise en place de l'instance et la création du certificat HTTPS
https://github.com/AlanJBX/FilRouge/tree/master/IP

- Dossier Flask : l'ensemble des fichiers permettant la mise en place des serveurs HTTP, HTTPS en python.
https://github.com/AlanJBX/FilRouge/tree/master/Flask

- Dossier Serverless : l'ensemble des fichiers permettant le déploiement d'une application serverless.
https://github.com/AlanJBX/FilRouge/tree/master/Serverless

- Dossier Sphinx : l'ensemble des fichiers sources permettant la génération de la documentation.
https://github.com/AlanJBX/FilRouge/tree/master/Sphinx

- Dossier Testeurs : l'ensemble des fichiers utilisés pour tester l'application. Certains fichiers vides (non pris en compte par GitHub) ne sont pas présents. Je vous invite à les créer en local afin de mettre à l'épreuve l'application.
https://github.com/AlanJBX/FilRouge/tree/master/Testeurs


### Briques développées :

IPv4 : 
* Instance EC2 et bucket S3, oui
* OS FreeBSD, oui
* Usage de PacketFilter, oui
* Connexion SSH via clé et id/mdp, oui
* Connexion à l'application, oui
* Protocole HTTPS, oui
* Identification, oui

Python :
* Utilisation de Python et Flask, oui
* Dépôt d'un fichier et retour JSON, oui
* API type RESTFull, en partie
* Gestion des extension, oui
* Gestion des métadonnées, oui
* Gestion des erreurs d'extension, oui

SSI :
* Connexion SSH via clé et id/mdp, oui
* Protocole HTTPS, oui
* Connexion avec id/mdp à l'application, oui
* Gestion d'un nouvel utilisateur, oui

AWS / IAAS :
* Serverless, en partie
* Gestion des métadonnées, oui
* Utilisation d'un bucket S3, oui
* Fichier test et commande de requête, oui
* Utilisation AWS Rekognition, oui

SOA : 
* Interface graphique, oui
* Commande CURL, oui
* API Manager, oui
* API Limitation requête, oui
* API Sécurisation, oui
* API Interconnectée, oui
* API Documentation, oui

### Difficultés rencontrées

De petites difficultés ont rencontrées sur l'ensemble du projet et sur l'ensembl des briques développées. Elles ont été de deux natures différentes :
- Automatisation : afin d'avoir un code propre et facilement debuggable, j'ai tenté d'automatisé le plus possible de chose. Il reste néanmoins de nombreuses choses à effectuer. Cette difficulté a eu pour principal effet de me faire perdre beaucoup de temps pour des gains marginaux.
- Spécificité et compatibilités : afin de faire correspondre mon idée de mon programme aux capacités de chaque technologie, il m'a fallut chercher les méthodes spécifiques à chacune d'entre elle. Cette difficulté a eu pour effet principal de rendre le code plus efficace et de me faire montée en compétence.

### Améliorations potentielles

IPv4 :
- Mise en place d'un Packet Filter complète et totale d'un PF au sein de l'instance.

Python :
- Augmentation des extensions et métadonnées liées (pour les vidéos notamment)
- Prise en compte du MIMEType
- Gestion plus évoluées des erreurs (afin prendre en comptes les codes status)
- Passage en API RESTfull
- Mise en place de l'AutoDoc en lien avec les DocStrings rédigées

SSI :
- Générateur de mot de passe aléatoire

AWS / IAAS :
- Mise en place complète de ServerLess
- Automatisation de la création et de la gestion du bucket à partir d'un programme/script.

SOA :
- Génération des requêtes CURL prenant en compte la spécificité de mon programme HTTPS avec id/auth.

### SAV

Dans le cas d'un problème technique, vous pouvez me joindre à mon adresse mail @student-cs.fr.
Notament dans le cadre de la gestion de l'API Rekognition qui nécessite une autorisation préalable et temporaire sur RosettaHub depuis mon compte personnel afin d'être utilisée.