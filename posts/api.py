import json

from flask import request, Response, url_for
from jsonschema import validate, ValidationError

from . import models
from . import decorators
from posts import app
from .database import session

@app.route("/api/posts", methods=["GET"])
@decorators.accept("application/json")
def posts_get():
	""" Get a list of posts """
	# Get the querystring arguments
	title_like = request.args.get("title_like")
	
	# Get and filter the posts from the database
	posts = session.query(models.Post)
	if title_like:
		posts = posts.filter(models.Post.title.contains(title_like))
	posts = posts.order_by(models.Post.id)
	
	# Convert the posts to JSOM and return a response
	data = json.dumps([post.as_dictionary() for post in posts])
	return Response(data, 200, mimetype="application/json")

@app.route("/api/posts/<int:id>", methods=["GET"])
@decorators.accept("application/json")
def post_get(id):
	""" Single post endpoint """
	# Get the post from the database
	post = session.query(models.Post).get(id)
	
	# Check whether the post exists
	# If not return a 404 with a helpful message
	if not post:
		message = "Could not find post with id {}".format(id)
		data = json.dumps({"message": message})
		return Response(data, 404, mimetype="application/json")
	
	# Return the post as JSON
	data = json.dumps(post.as_dictionary())
	return Response(data, 200, mimetype="application/json")

@app.route("/api/posts/<int:id>", methods=["DELETE"])
@decorators.accept("application/json")
def post_delete(id):
	""" Delete single post """
	# Get the post from the database
	post = session.query(models.Post).get(id)
	
	# Check whether the post exists
	# If not return a 404 with a helpful message
	if not post:
		message = "Could not find post with id {}".format(id)
		data = json.dumps({"message": message})
		return Response(data, 404, mimetype="application/json")
	
	session.delete(post)
	
	# Confirm deletion by response
	message = "Post #{} successfully deleted".format(id)
	data = json.dumps({"message": message})
	return Response(data, 200, mimetype="application/json")
