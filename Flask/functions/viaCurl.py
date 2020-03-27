#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import requests

def viaCurl(fichier):

	headers = 
	{
	    'accept': 'application/json',
	    'Content-Type': 'multipart/form-data',
	    'Authorization': 'Bearer undefined',
	}

	data = fichier

	response = requests.post('https://localhost:8243/dev/4.0/file', headers=headers, data=data)

	return_json = {}
	return_json["name"] = request.files["data_file"].filename + "_viaCurl"
	return_json["file"] = response

	return return_json