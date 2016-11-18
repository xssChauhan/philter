from app import db
from sqlalchemy.dialects.postgresql import JSON
import os

class UserStatus(db.Model):
	__tablename__ = "user_status"
	id = db.Column(db.Integer,primary_key = True)
	fbid = db.Column(db.String(64))
	status = db.Column(db.String)
	time = db.Column(db.DateTime)

	@classmethod
	def getLastStep(self,id):
		'''Returns the last step by the user'''
		return self.query.filter(self.fbid == id).order_by(self.id.desc()).first()

	@classmethod
	def getFb(self,id):
		return self.query.filter(self.fbid == id).first()

	@classmethod
	def get(self,id):
		'''Simple wrapper for accessing the user through ID'''
		return self.query.get(id)

class UserData(db.Model):
	__tablename__ = "user_data"
	id = db.Column(db.Integer,primary_key = True)
	fbid = db.Column(db.Integer,primary_key = True)
	data = db.Column(JSON)

	@classmethod
	def get(self,fbid):
		return self.query.filter(self.fbid == fbid).first()

	def getDir(self):
		return os.path.join(os.getcwd() ,"apex" ,"pictures",self.fbid)

class UserImages(db.Model):
	__tablename__  = "user_images"
	id = db.Column(db.Integer,primary_key = True)
	fbid = db.Column(db.String,primary_key = True)
	image = db.Column(db.Text())
	primitive = db.Column(db.Text())
	step = db.Column(db.Integer)

	@classmethod
	def getUserLastStep(self,fbid):
		return self.query.filter(self.fbid == fbid).order_by(self.id.desc()).first()

	@classmethod
	def getUserSteps(self,fbid):
		return [e.step for e in self.query.filter(self.fbid  == fbid).all()]


class UserVideos(db.Model):
	__tablename__ = "user_videos"
	id = db.Column(db.Integer,primary_key = True)
	fbid = db.Column(db.String)

	@classmethod
	def getFb(self,id):
		return self.query.filter(self.fbid == id).order_by(self.id.desc()).first()

class XDashboardImages():
	pass
	'''
	Implement the database layer for dashboard for investors
	'''