from .Base import Base
from app.Resources import Messages
import os,requests,shutil

class Attachment(Base):
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.type = "attachment"


	def reply(self):
		for e in self.attachments:
			self.saveAttachment(e.get('payload').get('url'),"primitive1.png")
		self.send_message(Messages.after_upload)
		self.setStatus(status = "third")
