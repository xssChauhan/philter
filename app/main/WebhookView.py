from app.Adapters.Views import BaseView
from flask.views import MethodView
from flask import request, g
from app.credentials import PAGE_ACCESS_TOKEN, VERIFY_TOKEN
from app.models import UserStatus, UserData
from app import db
import requests
from flask import render_template


class WebhookView(MethodView, BaseView):
    def createNewStatus(self, fbid, status):
        us = UserStatus(fbid=fbid, status=status)
        db.session.add(us)
        db.session.commit()

    def isPage(self):
        return g.data.get("object") == "page"

    def post(self):
        print("Calling post")
        for e in self.messaging_events():
            e.reply()
        return "ok"

    def get(self):
        # Verification for webhook
        print("Calling %$$$$$$$$$$")
        if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
            if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
                return "Verification token mismath", 403
            return request.args["hub.challenge"], 200
        # return "Hello world", 200

        return "Hello"
