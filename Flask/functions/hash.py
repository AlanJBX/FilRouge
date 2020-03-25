#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import hashlib

def read_arguments():
	"""
	Création et lecture de l'arguement
	:return: arguments rentrés en paramètres
	:rtype: args
	"""
	parser = argparse.ArgumentParser()
	parser.add_argument("-usr", type=str, help="permet de spécifier l'utilisateur")
	parser.add_argument("-mdp", type=str, help="permet de spécifier le mot de passe")
	return parser.parse_args()


def hash_mdp(mdp):
	"""
	Hashage du mot de passe
	:param password: mot de passe à hasher
	:type password: string
	:return: hash du mot de passe
	:rtype: string
	"""
	return hashlib.sha256(str(mdp).encode('utf-8')).hexdigest()

arguments = read_arguments()
couple = {}
couple['user']= arguments.usr
couple['mdp']= hash_mdp(arguments.mdp) # On hashe directement le mot de passe.

with open('./users.txt', 'a') as tmp:
	tmp.write(str(couple['user'])+","+str(couple['mdp'])+"\n")