#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functions.logger import logger

from yaml import load, Loader
from flask_swagger_ui import get_swaggerui_blueprint

def toSwagger(application):
	"""
	Gestion de l'export du Swagger
	:param application: application à exporter en swagger
	:type application: string
	:return: réussite ou non
	:rtype: bool
	"""	

	try :

		SWAGGER_URL = '/swagger'
		API_URL = './static/swagger.yml'
		swagger_yml = load(open(API_URL, 'r'), Loader=Loader)
		swaggerui_blueprint = get_swaggerui_blueprint(
			SWAGGER_URL,API_URL,
			config={
				'app_name': "ConvertToJSON",
				'spec':swagger_yml
				}
		)
		application.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
		return True


	except Exception as err:

		logger.warning("Erreur dans le chargement du swagger")
		return False