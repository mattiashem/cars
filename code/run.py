from flask import Flask
from flask import render_template
from flask import request,make_response, redirect
from pymongo import MongoClient
from datetime import datetime, timedelta
import calendar


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

@app.route("/api/recommend/<year>/<month>" ,methods=['GET', 'POST'])
def recommend(year, month):
	if len(year) == 4 and year.isdigit() and len(month) < 3 and month.isdigit():
		things_returned =""
		try:
			things = db.actions.find({
	    		'date': {	
	        		'$gte': datetime(int(year),int(month),1,0,0,0,0),
	        		'$lt': datetime(int(year),int(month),calendar.monthrange(int(year), int(month))[1],0,0,0,0) 
	    		}
			})
			for thing in things:
				things_returned += str(thing)+","
		except ValueError:
			things_returned ='{"error":"Value error"}'
	else:
		things_returned ='{"error":"Validation error"}'
	return things_returned

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
	return '{"id":"' + store('otaequipments') + '"}'

def storeAction():
	action = request.json
	answer = '';
	try:
		action['date'] = datetime.strptime(action['date'] + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
		if db.otaequipments.find({'ota': action['ota']}).count() > 0:
			answer = '{"id":"' + store('actions') + '"}'
		else:
			answer = '{"error":"OTA Code not in our database"}'
	except ValueError:
			answer ='{"error":"Value error"}'
	return answer

def getActions():
	return get('actions')

def getOtaEquipment():
	return get('otaequipments')

if __name__ == "__main__":
	app.debug = True
	app.run(host='0.0.0.0')