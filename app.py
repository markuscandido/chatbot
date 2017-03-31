#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/', methods=['GET'])
def root():
	res = "Aqui o Sistema eh Bruto e Sistematico"
	r = make_response(res)
	r.headers['Content-Type'] = 'text/plain; charset=utf-8'
	return r

@app.route('/webhook', methods=['GET'])
def getWebhook():
	res = "GET /webhook"
	r = make_response(res)
	r.headers['Content-Type'] = 'text/plain; charset=utf-8'
	return r

@app.route('/webhook', methods=['POST'])
def webhook():
	req = request.get_json(silent=True, force=True)
	#print("Request >>>")
	#print(json.dumps(req, indent=4))
	res = makeWebhookResult(req)
	res = json.dumps(res, indent=4)
	#print("<<< Response:")
	#print(res)
	r = make_response(res)
	r.headers['Content-Type'] = 'application/json; charset=utf-8'
	return r

def makeWebhookResult(req):
	result = req.get("result")
	action = result.get("action")
	if action != "curso.valor": return {}
	if action == "curso.valor" : return actionCursoValor(result)

def actionCursoValor(result):
	cursos = {'R':100, 'Python':200, 'Machine Learning': 300, 'AI':400 }
	actionIncomplete = result.get("actionIncomplete")
	if(actionIncomplete):
		speech = "Qual curso? Escolha entre " + str(cursos.keys())
		return monta_retorno(speech)
	parameters = result.get("parameters")
	curso = parameters.get("curso")
	if not curso :
		speech = "Nenhum curso selecionado. Escolha entre " + str(cursos.keys())
		return monta_retorno(speech)
	try:
		speech = "O valor do curso " + curso + " eh " + str(cursos[curso]) + " reais."
	except Exception as e:
		speech = "O curso " + curso + " eh invalido. Escolha entre " + str(cursos.keys())
	finally:
		return monta_retorno(speech)

def monta_retorno(speech):
    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print ("Starting app on port %d" % port)
    app.run(debug=True, port=port, host='0.0.0.0')