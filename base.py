#importing sqlalchemy

from flask_sqlalchemy import SQLAlchemy
#instantiating sqlalchemy object
db = SQLAlchemy()

class Movies (db.Model): 

#creating fields/columns of the database as class variables 
	id = db.Column(db.Integer, primary_key=True)

	title = db.Column(db.String(30), unique=True, nullable=False)

	director = db.Column(db.String(30),unique=False, nullable=False)

	genre = db.Column(db.String(30),unique=False, nullable=False)

	collection = db.Column(db.Integer, unique=False, nullable=False)

	def __init__(self,title,director,genre,collection):
		self.title=title
		self.director = director
		self.genre = genre
		self.collection = collection

#method to show data as dictionary object
	def json(self):
		return {'Title': self.title, 'Director':self.director, 
		'Genre':self.genre,'Collection':self.collection}

#method to find if the queried movie exists or not 
	@classmethod
	def find_by_title(cls,title):
		return cls.query.filter_by(title=title).first()

#method to save data to database
	def save_to(self):
		db.session.add(self)
		db.session.commit()

#method to delete data from db
	def delete_(self):
		db.session.delete(self)
		db.session.commit()