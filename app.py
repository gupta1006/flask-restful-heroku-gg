#import packages

from flask import Flask 
from flask_restful import Resource, reqparse, Api

#instantiate flask object 
app = Flask(__name__)

#instantiate Api boject 
api = Api(app)

#setting the location for the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
#adding the DB configurations 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

#import classes from base.py
from base import Movies, db
#link the app object to the movies db 
db.init_app(app)
app.app_context().push()
#create the db 
db.create_all()


#Creating a class to create get, post, put & delete methods
class Movies_List(Resource):      
#Instantiating a parser object to hold data from message payload
	parser = reqparse.RequestParser()                      
	parser.add_argument('director', type=str, required=False, help='Director of the movie')    
	parser.add_argument('genre', type=str, required=False, help='Genre of the movie')    
	parser.add_argument('collection', type=int, required=True, help='Gross collection of the movie') 
	#GET METHOD
	def get(self, movie):
		item = Movies.find_by_title(movie)
		if item:
				return item.json()
		else:
			return {'Message': 'Movie is not found'}
	#POST METHOD
	def post(self, movie):
		if Movies.find_by_title(movie):
			return{'Message': 'Movie with the title {} already exists'.format(movie)}
		else: 
			args = Movies_List.parser.parse_args()
			item = Movies(movie, args['director'],args['genre'],args['collection'])

			item.save_to()
			return item.json()
	#PUT METHOD 
	
	#Creating the put method
    	def put(self, movie):        
		args = Movies_List.parser.parse_args()        
		item = Movies.find_by_title(movie)        
		if item:            
		    item.collection = args['collection']            
		    item.save_to()            
		    return {'Movie': item.json()}        
		item = Movies(movie, args['director'], args['genre'], args['collection'])        
		item.save_to()        
		return item.json()
	#DELETE METHOD 
	def delete(self, movie):
		args = Movies.find_by_title(movie)
		if item: 
			item.delete_()
			return {'Message': '{} has been deleted from records'.format(movie)}
		else: 
			return {'Message': '{} no such movie exist in our records'.format()}
	#creating a class to get all the movies from the db 
class All_Movies(Resource):
#defining the get method 
	def get(self):
		return {'Movies':list(map(lambda x: x.json(),Movies.query.all()))}
#adding the URIs to the API
api.add_resource(All_Movies,'/')
api.add_resource(Movies_List, '/<string:movie>')

if __name__== '__main__':
	app.run()

