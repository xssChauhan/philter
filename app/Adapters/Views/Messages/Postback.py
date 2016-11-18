from .Base import Base
from app.Resources import Messages
from app.models import *
from app import db
from flask import json
commands = {
	b"style-davehilleffect" : "./freddy/davehilleffect %s output/%s-davehill.png",
	b"style-popart" : './freddy/popart -r 1 -c 1 -g 0 -i bilinear -c1 "red yellow yellow yellow" %s output/%s-popart.png',
	b"style-cartoon" : "./freddy/cartoon %s output/%s-cartoon.png",
	b"style-kmeans" : "./freddy/cartoon %s output/%s-cartoon.png",
	b"style-sketch" : "./freddy/kmeans %s output/%s-kmeans.png",
	b"style-popart1" : './freddy/popart -r 1 -c 1 -g 0 -i bilinear -c1 "red yellow green purple" %s output/%s-popart1.png',
	b"style-popart2" : './freddy/popart -r 1 -c 1 -g 0 -i bilinear -c1 "#FF9C00 white" %s output/%s-popart2.png',
	b'style-popart4' : './freddy/popart -r 1 -c 1 -g 0 -i bilinear -c1 "#00FF20 white" %s output/%s-popart4.png',
	b'style-popart5' : './freddy/popart -r 1 -c 1 -g 0 -i bilinear -c1 "#00FFE8 white" %s output/%s-popart5.png',
	b'style-popartr1' : './freddy/popart -r 1 -c 1 -g 0 -i bilinear -c1 "#$(openssl rand -hex 3) white" %s output/%s-popartr1.png',
	b'style-popartr3' : './freddy/popart -r 1 -c 1 -g 0 -i bilinear -c1 "#$(openssl rand -hex 3) white" %s output/%s-popartr3.png',
	b'style-popartr4' : './freddy/popart -r 1 -c 1 -g 0 -i bilinear -c1 "#$(openssl rand -hex 3) white" %s output/%s-popartr4.png',
	b'style-popartr5' : './freddy/popart -r 1 -c 1 -g 0 -i bilinear -c1 "#$(openssl rand -hex 3) white" %s output/%s-popartr5.png'
}
class Postback(Base):

	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.type = "postback"

	def reply(self):
		payload = self.payload
		filter = payload.decode("utf8").split("-")[1]
		print("postback reply" , payload)

		if payload.startswith(b"style"):
			print("Making profile picture and Replying profile video")
			#Add to database
			u = UserImages(fbid = self.sender , image = self.user.data.get("profile_pic") , primitive = filter , step = 159753)
			db.session.add(u)
			db.session.commit()
			self.setStatus(status = "second")
			#self.saveAttachment(self.user.data.get("profile_pic"),name="%s.jpg"%(self.user.fbid))
			# self.processImage(commands.get(payload) , filter = filter)
			# self.send_image(image = self.replyUrl)
			# self.buttons(2 , self.user.get("first_name"))
			self.send_style_quick_reply()
			self.send_message(Messages.picture)
		
		elif payload == b"profile-video":
			print("Replying picture-upload")
			print("Message",Messages.before_upload)
			self.send_message(Messages.before_upload)
			u = UserVideos(fbid = self.sender)
			db.session.add(u)
			db.session.commit()