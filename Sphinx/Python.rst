***************
Module Python
***************

Introduction
=============

Présentation générale
~~~~~~~~~~~~~~~~~~~~~~

L'application permet accepte le dépôt des fichiers dont les extensions sont les suivantes : pdf, jpeg, png, jpg, gif, bmp, txt, py, csv, ods, odt, odg, ipynb, json, docx, doc, xls, tex avec un stockage local sur le serveur et dans le cloud et de restituer un fichier JSON des fichiers envoyés enrichi des métadonnées de ces derniers.

Fonctions développées
~~~~~~~~~~~~~~~~~~~~~~

.. topic:: Python :

	- Utilisation de Python et Flask, oui

	- Dépôt d'un fichier et retour JSON, oui

	- API type RESTFull, en partie

	- Gestion des extension, oui

	- Gestion des métadonnées, oui

	- Gestion des erreurs d'extension, oui

	- Appel d'un autre API, en partie

Mise en oeuvre
~~~~~~~~~~~~~~~

Afin d'utiliser le programme, deux méthodes sont possibles :

	* Depuis l'interface graphique : 

	'https://54.246.242.159/' ou 'http://54.246.242.159/home'

	* Avec la méthode 'curl' (uniquement pour la version HTTP) :

	'http://54.246.242.159:8000/swagger/'

Il est également possible de lancer l'application sur votre ordinateur :

.. code-block:: bash

	gunicorn-3.7 --certfile=certificat.crt --keyfile=certificat.key --bind 0.0.0.0:443 __init__:application 
	# version HTTPS

	gunicorn-3.7 --bind 0.0.0.0:8000 __init__http:application 
	# version HTTP

Il suffit alors de remplacer l'adresse IP de l'instance AWS par l'adresse IP de votre machine (adresse IP externe et non le localhost)

Améliorations possibles
~~~~~~~~~~~~~~~~~~~~~~~~

Il serait envisageable d'effectuer les améliorations suivantes :

* Augmentation des extensions et métadonnées liées (pour les vidéos notamment)
* Prise en compte du MIMEType
* Gestion plus évoluée des erreurs (afin prendre en comptes les codes status)
* Passage en API RESTfull
* Mise en place de l'AutoDoc en lien avec les DocStrings rédigées
* Résolution du problème de buffer pour l'appel à une autre API

Programmation sous Python et Flask
===================================

Le programme est développé en Flask-1.1.1 et Python-3.7.3.

Python est en charge du traitement du fichier tandis que Flask est en charge du moteur web tandis que Gunicorn se charge de la mise en place du serveur.

Modules développés
~~~~~~~~~~~~~~~~~~~

* Module Auth_ : permet de gérer les authentifications/identifications, l'ajout d'un nouvel utilisateur
.. _Auth : https://pfralanjbx.readthedocs.io/Codes.html#identification-et-authentification-auth-py

* Module AWS_ : permet de gérer les appels vers et depuis le Bucket S3 ainsi que l'API Rekognition
.. _AWS : https://pfralanjbx.readthedocs.io/Codes.html#gestion-des-buckets-et-api-aws-py

* Module Extensions_ : permet de tester l'extension du fichier pris en compte et de retourner les métadonnées particulères liées
.. _Extensions : https://pfralanjbx.readthedocs.io/Codes.html#gestion-des-extensions-de-fichier-extensions-py

* Module FlaskApp_ : permet de gérer les pages WEB du serveur HTTP(S) de l'application et de faire du micro traitement de fichier
.. _FlaskApp : https://pfralanjbx.readthedocs.io/Codes.html#moteur-web-flask-pour-http-et-https-flaskapp-py-et-flaskapp-http-py

* Module Hash_ : mini programme permettant de traiter de hasher des mots de passe
.. _Hash : https://pfralanjbx.readthedocs.io/Codes.html#mini-programme-de-hash-hash-py

* Module Logger_ : permet de traiter les LOG
.. _Logger : https://pfralanjbx.readthedocs.io/Codes.html#gestion-des-logs-logger-py

* Module Swagger_ : permet d'appeler le module SWAGGER pour la génération de la documentation
.. _Swagger : https://pfralanjbx.readthedocs.io/Codes.html#generateur-swagger-swagger-py

* Module Traitement_ : permet de traiter la conversion du fichier d'origine en version JSONifié
.. _Traitement : https://pfralanjbx.readthedocs.io/Codes.html#traitement-des-fichier-a-convertir-traitement-py

* Module Serverless_ : permet de gérer l'application en version serverless
.. _Serverless : https://pfralanjbx.readthedocs.io/IAAS.html#code-serverless

* Module ViaCURL_ : permet d'appeler une autre API pour la conversion
.. _ViaCURL : https://pfralanjbx.readthedocs.io/Codes.html#appel-vers-une-autre-api-viaCurl.py

Application au format RESTFull
===============================

L'application est développée afin de correspondre qu'en partie aux propriétés RESTfull. Notament la partie 'authentification' et la partie 'liens entre les ressources'.

* **URI comme identifiant** : chaque ressource de l'API est défini par une URI propre et hiérarchisée

* **Verbes HTTP en identification des opérations** : utilisation des opérations POST et GET

* **Réponses HTTP en représentation des ressources** : utilisation de la réponse GET

* **Liens entre les ressources** : non mis en oeuvre
* **Paramètre comme jeton d’authentification** : non mis en oeuvre


Restitution d'un fichier sous format JSON
==========================================

La restitution du fichier s'effectue en trois phases :

.. topic:: Phase 1, récupération des métadonnées

	* Analyse de l'extension du fichier et stockage en local si extension pris en compte
	* Récupération des métadonnées générales et particulières, en fonction de l'extension, sous forme d'un dictionnaire :ref: `PythonMETA`

.. topic:: Phase 2, transformation json du fichier

	* Ouverture du fichier d'origine au format binaire
	* Stockage du fichier binaire dans un dictionnaire
	* Fusion du dictionnaire des métadonnées et du binaire

.. topic:: Phase 3, restitution

	* Le fichier original est stocké sur le cloud
	* Le fichier JSON est stocké en local et sur le cloud
	* Restitution du fichier JSON à l'utilisateur via une fenêtre graphique de téléchargement (si utilisation d'un navigateur)

Le fichier JSON retourné a alors la structure suivante : 

.. code-block:: yaml

	{
	    "META": {
	        "fichiernom": "string",
	        "type": "MIMEType",
	        "taille": "int",
	        "extension": ".string",
	        "metaparticulière": "{string}"
	        },
	    "fichier_bytes": "binaire"
	}


Gestion des extensions
=======================

La gestion des extensions s'est révélée relativement basique. Le stockage du fichier en JSON se faisant sur la base d'une lecture binaire de ce dernier, la limite d'utilisation du programme est sa capacité à gérer les métadonnées générales.

Le choix a été fait de traiter les extensions depuis leur nom que depuis leur MIMIType pour une plus grande flexibilité de traitement.

Les améliorations possibles du programme seraient d'augmenter la liste des extensions disponibles et un traitement à partir du MIMEType.

Le choix arbitraire de ne pas traiter les formats vidéos a été fait car il correspond de manière similaire à la gestion des images.


Gestion des métadonnées
========================

La gestion des métadonnées va dépendre principalement de l'extension du fichier. On distingue trois catégories principales :
	* Les images
	* Les PDF
	* Les autres format

.. topic:: Gestion des métadonnées générales

	Les métadonnées suivantes sont générées pour l'ensemble des extensions prises en compte.
		- nom du fichier
		- MIMEType du fichier
		- taille du fichier
		- nom de l'extension

.. topic:: Gestion des images (.jpeg, .png, .jpg, .gif, .bmp)

	Les librairies utilisées pour extraire les métadonnées des images sont : 
		- Pillow : permet d'ouvrir l'image en tant qu'une image et non comme un fichier *lambda*
		- Exif : permet d'extraire les métadonnées si elles sont présentes. La nature principale de ces métadonnées coorespond au caractéristique de l'appareil photo ayant pris la photo.

.. topic:: AWS Rekognition
	
	Si l'image correspond à une extension donnée et une taille minimum, elle est envoyée à l'API Amazon Rekognition qui est chargée de déterminer les éléments présents dans l'image. Les métadonnées déterminées sont alors ajoutées au fichier JSON. Plus d'informations : Rekognition_.

	.. _Rekognition : https://pfralanjbx.readthedocs.io/IAAS.html#aws-rekognition


.. topic:: Gestion des pdf

	La lecture des métadonnées des PDF s'appuie sur la librairie PyPDF2. Cette librairie permet d'obtenir les informations de quatre natures différentes :
		- DocumentInformation, pour obtenir les informations générales du PDF
		- XMPInformation, pour obtenir les information XMP disponible
		- getFields, pour obtenir les champs présents dans le PDF
		- getNumPages, pour obtenir le nombre de page

	Vous trouverez toutes les informations disponibles au lien suivant : 'https://pythonhosted.org/PyPDF2/Other%20Classes.html'

Appel vers une autre API
==========================

Un module_ permettant d'appeller une autre API a été développé. Il permet d'appeller l'API sur le serveur HTTP pour convertir un fiche "text/plain".
Si l'appel et la conversion fonctionnent parfaitement quand l'API est en route, cela n'est plus le cas lorsque l'API HTTP est éteinte. En effet, un problème sur le buffer du 'request.files' n'a pas pu être géré. Le buffer lit entièrement le fichier à convertir lors de l'appel à l'API et se retrouve en bout de fichier lorsqu'il passe à l'API HTTPS en cas d'échec de la première.

.. _module : https://pfralanjbx.readthedocs.io/Codes.html#appel-vers-une-autre-api-viaCurl.py

Code source de l'application
=============================

Vous trouverez en lien le codesource_ de l'application.

.. _codesource : https://pfralanjbx.readthedocs.io/Codes.html