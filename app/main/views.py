from . import main
from .WebhookView import WebhookView
from flask import redirect
webhookview = WebhookView.as_view("wh")
main.add_url_rule("/",view_func = webhookview,methods = ["GET","POST"])


@main.route("/g/<string:dirc>")
def reroute(dirc):
	return redirect("/gallery/" + dirc)