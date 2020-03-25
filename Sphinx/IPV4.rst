.. _IPV4:
*************
Module IPv4
*************

.. _IPV4INTRO:
Introduction
=============

Présentation générale
----------------------

Le serveur est hébergé via RosettaHub dans le Cloud d'Amazon. Une instance EC2 avec un OS de type FreeBSD relié à un bucket S3 permet le traitement et le stockage des fichiers envoyés par un utilisateur dans le cadre de l'API développée.

Fonctions développées
-----------------------

.. topic:: IPV4 :

	- Instance EC2 et bucket S3, oui

	- OS FreeBSD, oui

	- Usage de PacketFilter, oui

	- Connexion SSH via clé et id/mdp, oui

	- Connexion à l'application, oui

	- Protocole HTTPS, oui

	- Identification, oui

Accès à l'instance
--------------------

Afin de vous connecter à l'instance :

.. code-block:: bash

	ssh ec2-user@54.246.242.159

.. _IPV4AWS:
Infrastructure du serveur
===========================

Le serveur se décompose en deux entitées :

* un bucket S3 AWS 'stockagefbsdpfilrougealan' composé comme suit :

stockagefbsdpfilrougealan

|- Sauvegarde/

|- StockageJSON/

* une instance EC2 AWS sous FreeBSD 11.3-STABLE-amd64-2020-02-20.

.. _IPV4ACS:
Accès au service
==================

Il est possible de se connecter à l'application aux adresses suivantes :

* Lien vers l'application développée en HTTPS avec identification et authentification. 
.. centered:: https://54.246.242.159/

* Lien vers l'application développée en HTTP sans identification et authentification ainsi que sa documentation SWAGGER. 
.. centered::  http://54.246.242.159:8000/home
.. centered::  http://54.246.242.159:8000/swagger

Afin de gérer le serveur, deux connexions SSH sont disponibles :

* avec une clef :
 
.. code-block:: sh
	
	ssh -i ~/Desktop/PFR/keyPFilRougeAlan.pem ec2-user@54.246.242.159 
	# clef que je garde sur mon ordinateur

* avec un identification/authentification :

.. code-block:: sh
	
	ssh ec2-user@54.246.242.159

.. _IPV4PFL:
Packet Filter
===============

Malgré la présence d'un packet filter disponible via la gestion AWS de l'instance, un PF a néanmoins été développé pour le test.

.. code-block:: sh

	ip_ext="54.246.242.159"
	ip_sio="138.195.237.216"

	webports = "{http, https}"
	int_tcp_services = "{domain, ntp, smtp, www, https, ftp, ssh}"
	int_udp_services = "{domain, ntp}"

	# Ne pas filtrer lo0 et xn0
	pass quick on lo0
	pass quick on xn0

	# Par défaut tout est bloqué, les règles suivantes ouvrent quelques portes.
	block return in log all
	block all

	# Trafic TCP entrant sur le port 22 pour ip_sio
	pass in quick on $ip_ext inet proto tcp from $ip_sio port >=49152 to $ip_ext port 22

	# Trafic ping pour admin
	pass inet proto icmp icmp-type echoreq

	# Trafic complet entrant pour ip_sio
	pass in quick on $ip_ext inet proto {udp, icmp, tcp} from $ip_sio to $ip_ext

	# Trafic TCP entrant sur le port 80 et 443 pour tous
	pass in quick on $ip_ext inet proto tcp from any to $ip_ext port $webports

	# Trafic sortant
	pass out quick on $ip_ext proto tcp to any port $int_tcp_services
	pass out quick on $ip_ext proto udp to any port $int_udp_services
	#_EOT_#

Néanmoins, par précaution et afin de pouvoir accéder à l'instance depuis différents ordinateurs, il n'a pas été activé de manière permanente. Seul le PF d'AWS est activé.

Un point d'amélioration du service serait la mise en place complète et totale d'un PF au sein de l'instance.

.. _IPV4HTTPS:
Protocole HTTP & HTTPS
========================

Vous trouverez l'ensemble des informations relatives à la sécurité de l'application sur la page dédiée à l'IPv6 et la SSI : 

:ref:`Module SSI`