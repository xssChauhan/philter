from .Base import Base
from app.Resources import Messages, Images

class Message(Base):
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.type = "message"
		print("Message is " , self.message)

	def isEcho(self):
		return self.message.get("is_echo")

	def reply(self):
		print("STATUS" , self.status.status)

		if self.status.status == "first":
			print("replying message first")
			self.buttons(1,self.user.get("first_name"))
			self.setStatus(status = "second")

		elif self.status.status == "second":
			print("replying third")
			self.send_image()
	
		elif self.status.status == "third":
			print("replying message second")
			self.send_message(Messages.final)
	
		else:
			print("oops")
			self.send_message("Fuck")
