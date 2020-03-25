#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functions.flaskapp import *

if __name__=="__main__":
	application.secret_key = b'\xd5\x8af\xb4\x9e*1SN\xcbl\xc18\x7f\xa4\x96'
	application.run(debug=False, host='0.0.0.0', port=443, ssl_context=('certificat.crt', 'certificat.key'))