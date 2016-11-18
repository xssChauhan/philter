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
		self.payload = self.payload.decode("utf-8")

	def reply(self):
		payload = self.payload
		print(payload)
		try:
			filter = self.payload.split("\\")[2]
		except Exception as e:
			print(e)
		print("postback reply" , payload)

		if payload.startswith("style"):
			print("Making profile picture and Replying profile video")
			#Add to database
			u = UserImages.create(fbid = self.sender , image = self.user.data.get("profile_pic") , primitive = filter , step = 159753)
			self.setStatus(status = "second")
			#self.saveAttachment(self.user.data.get("profile_pic"),name="%s.jpg"%(self.user.fbid))
			# self.processImage(commands.get(payload) , filter = filter)
			# self.send_image(image = self.replyUrl)
			# self.buttons(2 , self.user.get("first_name"))
			self.send_message(Messages.picture)
		
		elif payload == "profile-video":
			print("Replying picture-upload")
			print("Message",Messages.before_upload)
			self.send_message(Messages.before_upload)
			u = UserVideos.create(fbid = self.sender)
			
		elif payload.startswith("picture"):
			image = payload.split("\\")[4]
			print(payload.split("\\"))
			u = UserImages.create(fbid = self.sender , image = image , primitive = filter , step = 159753)
			self.send_message(Messages.picture)

		elif payload == "menu-image":
			self.buttons(1,self.user.get("first_name"))

		elif payload.startswith("share"):
			self.shareToWall(payload)

		elif payload.startswith("videoshare"):
			self.shareVideoToWall(payload)

		elif payload == "reaction-menu":
			self.sendReactionMenu()
			
		elif payload.startswith("reactionfilter"):
			print("Sending reaction")
			self.sendReaction(payload)
