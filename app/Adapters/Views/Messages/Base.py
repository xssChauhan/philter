from app import db
from app.Resources import Images
from app.models import UserData , UserStatus , UserImages
from app.credentials import PAGE_ACCESS_TOKEN
from flask import json
from datetime import datetime
import requests,os,shutil
import boto3 , uuid , subprocess
s3 = boto3.resource("s3")
S3Base = "https://s3-us-west-2.amazonaws.com/pyramid-ai/pyramid/%s"

class Base():

	picturesDir = os.path.join(os.path.expanduser("~"),"Documents/pyramid/pyramid-apex/picture/")
	outputDir = os.path.join(os.path.expanduser("~"),"Documents/pyramid/pyramid-apex/picture/output")
	videoDir = os.path.join(os.path.expanduser("~") , "Documents/pyramid/fast-neural-style")
	def __init__(self,*args,**kwargs):
		for i,e in kwargs.items():
			setattr(self,i,e)
		self.dir = os.getcwd()
		self.getUser()
		self.getStatus()

	def getFBData(self):
		r = requests.get("https://graph.facebook.com/v2.6/"+str(self.sender)+"?access_token="+PAGE_ACCESS_TOKEN).json()
		return r

	def getUser(self):
		user = UserData.get(self.sender)
		if user is not None:
			self.user = user
		else:
			self.setUser() 
		
	def setUser(self):
		data = self.getFBData()
		user = UserData(fbid = self.sender , data = data)
		try:
			db.session.add(user)
			db.session.commit()
		except Exception as e:
			db.session.rollback()
		else:
			self.user = user
			os.makedirs(os.path.join(self.dir ,"apex" ,"pictures",self.sender))

	def getStatus(self):
		status = UserStatus.getLastStep(self.sender)
		if status is not None:
			self.status = status
		else:
			print("Status is None")
			self.setStatus(status = "first")

	def setStatus(self,status):
		status = UserStatus(fbid = self.sender , status = status , time = datetime.now())
		try:
			db.session.add(status)
			db.session.commit()
		except Exception as e:
			print(e)
			db.session.rollback()
		else:
			self.status = status

	def buttons(self,n,name):
		params = {
			"access_token": PAGE_ACCESS_TOKEN
		}
		headers = {
			"Content-Type": "application/json"
		}
		recipient_id = str(self.sender)
		print("User ID is" , recipient_id)
		#Hi! I am 0nline bot
		data1 = json.dumps({
			"recipient": {
				"id": recipient_id
			},
			"message":{
				"attachment":{
					"type":"template",
					"payload":{
						"template_type":"generic",
						"elements" : [
							{
								"title" : "HoneyDew",
								"image_url":"https://s3-us-west-2.amazonaws.com/pyramid-ai/pyramid/lenna/78d68651-3c5c-46f7-9b19-b36cd22c4829.png",
								"subtitle":"Soft white cotton t-shirt is back in style",
								"buttons":[
									{
										"type":"postback",
										"title":"HoneyDew",
										"payload":"style-popart1"
									}

								]
							},
							{
								"title" : "Electric Forest",
								"image_url" : "https://s3-us-west-2.amazonaws.com/pyramid-ai/pyramid/lenna/2ae7b05e-68ee-4505-b9c4-74c65b31b76d.png",
								"subtitle" : "Soft white cotton t-shirt is back in style",
								"buttons":[
									{
										"type":"postback",
										"title":"Electric Forest",
										"payload":"style-popart"
									}

								]
							},
							{
								"title" : "SpringGreen",
								"image_url":"https://s3-us-west-2.amazonaws.com/pyramid-ai/pyramid/lenna/a35ff454-0d66-4c81-93f1-7eabe2d39b58.png",
								"subtitle":"Soft white cotton t-shirt is back in style",
								"buttons":[
									{
										"type":"postback",
										"title":"SpringGreen",
										"payload":"style-popart2"
									}

								]
							},
							{
								"title" : "ChartReuse",
								"image_url":"https://s3-us-west-2.amazonaws.com/pyramid-ai/pyramid/lenna/d8149fdc-ee9b-4cc5-9ba7-b74e33994de9.png",
								"subtitle":"Soft white cotton t-shirt is back in style",
								"buttons":[
									{
										"type":"postback",
										"title":"ChartReuse",
										"payload":"style-popart4"
									}

								]
							},
							{
								"title" : "Turquoise",
								"image_url":"https://s3-us-west-2.amazonaws.com/pyramid-ai/pyramid/lenna/67561684-ec22-478e-8af0-ddf35abed2b1.png",
								"subtitle":"Soft white cotton t-shirt is back in style",
								"buttons":[
									{
										"type":"postback",
										"title":"TURQUOISE",
										"payload":"style-popartr3"
									}

								]
							},
							{
								"title" : "Classic White Image",
								"image_url":"https://s3-us-west-2.amazonaws.com/pyramid-ai/pyramid/lenna/72c72d9d-6c3f-4b22-9e11-c150d90edc42.png",
								"subtitle":"Soft white cotton t-shirt is back in style",
								"buttons":[
									{
										"type":"postback",
										"title":"RoyalBlue",
										"payload":"style-popartr4"
									}

								]
							},
							{
								"title" : "Astroboy",
								"image_url":"https://s3-us-west-2.amazonaws.com/pyramid-ai/pyramid/lenna/e6f8f325-4ad3-4bbc-9ea3-05347dc48c47.png",
								"subtitle":"Soft white cotton t-shirt is back in style",
								"buttons":[
									{
										"type":"postback",
										"title":"Astroboy",
										"payload":"style-popart5"
									}

								]
							},
							{
								"title" : "Eastwood",
								"image_url":"https://s3-us-west-2.amazonaws.com/pyramid-ai/pyramid/lenna/a94df3c3-0d6c-4630-a422-fda6eb3b19ca.png",
								"subtitle":"Soft white cotton t-shirt is back in style",
								"buttons":[
									{
										"type":"postback",
										"title":"Eastwood",
										"payload":"style-popartr1"
									}

								]
							},
						],

					}
				}
			}
		})
		data2  = json.dumps({
		  "recipient":{
		    "id": recipient_id
		  },
		  "message":{
		    "attachment":{
		      "type":"template",
		      "payload":{
		        "template_type":"generic",
		        "elements":[
		          {
		            "title":"Get an awesome profile video",
		            "image_url":"https://media.giphy.com/media/PzY2K7SaqIEyA/giphy.gif",
		            "buttons":[
		              {
		                "type":"postback",
		                "payload":"profile-video",
		                "title":"Profile Video"
		              }           
		            ]
		          }
		        ]
		      }
		    }
		  }
		})


		print("N!!!!! = " , n)
		if n==1:
			r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data1)
			print(data1)
			print(r.status_code)
			print(r.json())
		if n == 2:
			r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data2)
			print(data2)
			print(params)
			print(headers)
			print(r.status_code)
			print(r.url)
			print(r.json())

	def send_image(self,image = Images.upload):
		print("Sending image" , image)
		params = {
			"access_token" : PAGE_ACCESS_TOKEN
		}
		headers = {
			"Content-Type" : "application/json"
		}
		data = json.dumps({
				"recipient" : {
					"id" : str(self.sender)
				},
				"message" : {
					"attachment" : {
						"type" : "image",
						"payload" : {
							"url" : image
						}
					}
				}
			})
		try:
			r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
		except Exception as e:
			print("Error",e)
		finally:
			print(r.json())

	def send_message(self, message_text):

		params = {
			"access_token": PAGE_ACCESS_TOKEN
		}
		headers = {
			"Content-Type": "application/json"
		}
		data = json.dumps({
			"recipient": {
				"id": self.sender
			},
			"message": {
				"text": message_text
			},
			"postback":{
				"payload":"initial"
			}
		})
		r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)

	def savingFolder(self):
		path = self.getUserDir()
		folders = os.listdir(path)
		maxdir = max([int(e) for e in folders]) if folders else 0
		save = os.path.join(path,str(maxdir + 1))
		os.mkdir(save)
		return save

	def getUserDir(self):
		return os.path.join(self.dir ,"apex" ,"pictures",self.sender)

	def saveAttachment(self,url,name):
		self.name = name
		step = UserImages.getUserLastStep(self.sender)
		step = 0 if step is None else step.step
		u = UserImages(fbid = self.sender , image = url , step = step + 1 , primitive = name)
		try:
			db.session.add(u)
			db.session.commit()
		except Exception as e:
			raise(e)
			db.session.rollback()
		dirToSave = "/tmp"
		file = os.path.join(dirToSave , name)
		print("File name" , file)
		self.image = file
		print("File is ++++",file)
		r = requests.get(url , stream = True)
		if r.status_code == 200:
			with open(file , "wb") as f:
				r.raw.decode_content = True
				shutil.copyfileobj(r.raw,f)

	def uploadToS3(self , file):
		key = str(uuid.uuid4())
		ext = os.path.splitext(os.path.basename(file))[1]
		s3.Object( "pyramid-ai" , ("pyramid/%s")%(key + ext )).put( Body = open(file , "rb") , ACL = "public-read" , ContentType=  "image/png" )
		self.replyUrl = S3Base%(key+ext)
		print(self.replyUrl)
		return self.replyUrl

	def processImage(self , command , filter):
		'''
		Implementing the image using subprocess.call
		Define the proper command here from the directories
		'''
		self.key = self.name.split()[0]
		self.filter = filter
		command = command%(self.image , self.key.split(".")[0])
		print(command)
		subprocess.call("cd %s && %s"%(self.picturesDir , command ),shell = True)
		test = os.path.join(self.outputDir , self.key.split(".")[0] + "-" + filter + ".png")
		print("Output file to search is " , test)
		print(os.listdir(self.outputDir))
		self.uploadToS3(test)
		return

	def processVideo(self):
		video_command = "cd %s && bash profile-video.sh %s"%(self.videoDir , self.image)
		subprocess.call(video_command , shell = True)
		test = os.path.join(self.videoDir , "output" , self.name.split(".")[0] + "-000.mp4")
		print("Output file to search is " , test)
		return

	def send_style_quick_reply(self):
		params = {
			"access_token": PAGE_ACCESS_TOKEN
		}
		print("PARAMS ---------------", params)
		headers = {
			"Content-Type": "application/json"
		}
		data = 	json.dumps({
			  		"recipient":{
			    		"id": self.sender
			  		},
			  		"message":{
				    	"text":"Pick a color:",
				    	"quick_replies":[
					      	{
					        	"content_type":"text",
					        	"title":"Red",
					        	"payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_RED"
					      	},
					      	{
					        	"content_type":"text",
					        	"title":"Green",
					        	"payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_GREEN"
					      	}
				    	]
			  		}
				})
		r = requests.post("https://graph.facebook.com/v2.6/me/messages" , params = params , data = data , headers = headers)
		print(r.json())

