from .Base import Base
from app.Resources import Messages
import os,requests,shutil
import uuid
import pprint

pp = pprint.PrettyPrinter(indent = 4)
class Attachment(Base):
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.type = "attachment"


	def reply(self):
		pp.pprint(self.attachments)
		for e in self.attachments:
			name = str(uuid.uuid4())[:10]
			# self.saveAttachment(e.get('payload').get('url'), name + ".png")
			print("Type" , e.get("type"))
			if e.get("type") == "image":
				self.send_message("Choose a style ❤ ")
				print(e.get("payload").get("url"))
				self.send_image_postback(e.get("payload").get("url"))
			if e.get("type") == "location":
				self.send_multiple_images()
		self.setStatus(status = "third")
