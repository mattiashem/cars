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
def fetures():
    return render_template('f.html')



'''
API this route handle the API Calls. Here we get the correct url example /api/item/ we check what kind of reqest and issues the correct function aginst the db
'''
@app.route("/api/item" ,methods=['GET', 'POST'])
def item():
	'''
	If reqest is post we add the item to the db
	If the request is get we show all the items in the db

	Here we dont use and templates only clean json text

	'''
	if request.method == 'POST':
		'''
		Adding item to the db
		'''
		#Setting up the item test with http POST localhost:5000/api/item
		#
		# As now we dont recive any data from the client we use the data that is generated
		item = {"name":"mattias","text":"En massa bra text", "tags": ["matte","mattias"] }
		   
		#Chossing where in db and colelction items
		item_store = db.items
		#Saving the data and retrving the id
		item_id = item_store.insert_one(item).inserted_id
		#returning the id to the client make it a string from object
		return str(item_id) 

	else:
		#Getting all te items from the db test with http GET localhost:5000/api/item

		#String to hold the items and display
		items_returnd =""

		#Chossing where in db and colelction items
		item_store = db.items
		#Retriving all the docs
		items = item_store.find()
		for item in items:
			items_returnd += str(item)+","


		return items_returnd

if __name__ == "__main__":
	app.debug = True
	app.run(host='0.0.0.0')