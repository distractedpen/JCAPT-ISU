import json
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

with open("../users/users.json") as fd:
	users = json.loads(fd.read())


def save_data():
	with open("../users/users/json") as fd:
		fd.write(json.dumps(users))

class UserHandler:

	def __init__(self):
		return

	def create(self, name="", email="", password=""):
		user = self.get_by_email(self, email)
		if user:
			return
		new_id = uuid.uuid4()
		new_user = {
			"name": name,
			"email": email,
			"password": self.encrypt_password(password),
			"active": True
		}
		users[new_id] = new_user
		save_data()
		return self.get_by_id(new_id)

	def get_all(self):
		return [{**users[id]} for id in users]

	def get_by_id(self, user_id):
		try:
			user = users[user_id]
		except KeyError:
			return
		user.pop("password")
		return user

	def get_by_email(self, email):
		for id in users:
			if users[id]["email"] == email:
				return users[id]
		return

	def delete(self, user_id):
		del users[user_id]
		save_data()

	def encrypt_password(self, password):
		return generate_password_hash(password)

	def login(self, email, password):
		user = self.get_by_email(email)
		if not user or not check_password_hash(user["password"], password):
			return
		user.pop("password")
		return user

