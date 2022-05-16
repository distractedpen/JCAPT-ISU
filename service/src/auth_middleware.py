# Modified tutorial from 
# https://www.loginradius.com/blog/engineering/guest-post/securing-flask-api-with-jwt/

from functools import wraps
import jwt
from flask import request, abort
from flask import current_app
from UserHandler import UserHandler

def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = None
		if "Authorization" in request.headers:
			token = request.headers["Authorization"].split(" ")[1]
		if not token:
			return {
				"message": "Authentication Token is missing!",
				"data": None,
				"error": "Unauthorized"
			}, 401
		try:
			data=jwt.decode(token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"])
			current_user=UserHandler.get_by_id(data["user_id"])
			if current_user is None:
				return {
					"message": "Invalid Authentication token!",
					"data": None,
					"error": "Unauthorized"
				}, 401
			if not current_user["active"]:
				abort(403)
		except Exception as e:
			return {
				"message": "Something went wrong",
				"data": None,
				"error": str(e)
			}, 500

		return f(current_user, *args, **kwargs)

	return decorated

