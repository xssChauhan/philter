from flask import request
from .Messages import Postback, Message,Attachment
class BaseView():

	def messaging_events(self):
		data = request.get_json()
		event = data["entry"][0]["messaging"][0]
		print("Keys",event)
		print("Data",data)
		sender = event["sender"]["id"]
		if "postback" in event:
			print(event.get("postback"))
			print("Yielding Postback")
			yield Postback(sender = sender , payload = event.get("postback").get("payload").encode("unicode_escape"))			
		elif "attachments" in event["message"]:
			print("Yielding Attachment")
			yield Attachment(sender = sender , attachments = event.get("message").get("attachments"))
		elif "message" in event: 
			print("Messaging event",event.keys())
			yield Message(sender = sender , message = event["message"])