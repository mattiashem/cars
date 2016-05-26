from flask import Flask
from flask import render_template
from flask import request,make_response, redirect
from pymongo import MongoClient


app = Flask(__name__)

#Setup the db cnnection to the mongo database
mongo = MongoClient('db', 27017)
db = mongo.reco_database


'''
This is our page thet only display clean html to the vistitor
'''

@app.route("/")
def hello():
    return render_template('hello.html')

@app.route("/f")
def features():
    return render_template('f.html')

@app.route("/api/")
def api():
    return render_template('api.html')

@app.route("/api/action" ,methods=['GET', 'POST'])
def action():
	if request.method == 'POST':
		return storeAction()
	else:
		return getActions()

@app.route("/api/otaequipment" ,methods=['GET', 'POST'])
def otaequipment():
	if request.method == 'POST':
		return storeOtaEquipment()
	else:
		return getOtaEquipment()

@app.route("/api/drop/otaequipment" ,methods=['GET'])
def dropotaequipment():
	db.otaequipments.drop()
	return 'dropped otaequipments'

@app.route("/api/drop/action" ,methods=['GET'])
def dropaction():
	db.actions.drop()
	return 'dropped actions'

def store(aCollectionString):
	thing = request.json
	thing_id = db[aCollectionString].insert_one(thing).inserted_id
	return str(thing_id)

def get(aCollectionString):
		things_returned =""
		things = db[aCollectionString].find()
		for thing in things:
			things_returned += str(thing)+","
		return things_returned

def storeOtaEquipment():
	return store('otaequipments')

def storeAction():
	action = request.json
	answer = '';
	if db.otaequipments.find({'ota': action['ota']}).count() > 0:
		answer = '{"id":"' + store('actions') + '"}'
	else:
		answer = '{"error":"OTA Code not in our database"}'
	return answer

def getActions():
	return get('actions')

def getOtaEquipment():
	return get('otaequipments')

if __name__ == "__main__":
	app.debug = True
	app.run(host='0.0.0.0')