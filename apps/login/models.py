from __future__ import unicode_literals
import re
import bcrypt
from django.db import models

# Create your models here.
class UserManager(models.Manager):
	def registerValidation(request, postData):
		logged = {'status': True, 'errors':[], 'user': None}
		if not postData['first_name'] or len(postData['first_name']) < 2:
			logged['status'] = False
			logged['errors'].append('First name must be longer than 2 characters')
		if not postData['last_name'] or len(postData['last_name']) < 2:
			logged['status'] = False
			logged['errors'].append('Last name must be longer than 2 characters')
		# if postData['email'] != re.match(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9]+\.[a-zA-Z0-9-.]+$'):
		# 	logged['logged'] = False
		# 	logged['errors'].append('Invalid email')
		if not postData['password'] or len(postData['password']) < 8:
			logged['status'] = False
			logged['errors'].append('Password must be at least 8 characters long')
		if postData['confirm_password'] != postData['password']:
			logged['status'] = False
			logged['errors'].append('Passwords to not match')
		if logged['status'] is False:
			return logged
		
		user = User.objects.filter(first_name = postData['first_name'])

		if user:
			logged['status'] = False
			logged['errors'].append('Failed to register, please try again and DO NOT mess it up this time')
		
		if logged['status']:
			password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
			user = User.objects.create(
				first_name = postData['first_name'],
				last_name = postData['last_name'],
				email = postData['email'],
				password = password
				)
			
			logged['user'] = user
		return logged

	def loginValidation(self, postData):
		logged = {'status':True, 'errors': [], 'user': None}
		user = User.objects.filter(first_name=postData['first_name'])
		try:
			user[0]
		except IndexError:
			logged['status'] = False
			logged['errors'].append('No Account found with the information provided. GO REGISTER')

		if user[0]:
			if user[0].password != bcryp.hashpw(postData['password'].encode(), user[0].password.encode()):
				logged['status'] = False
				logged['errors'].append('Password is WRONG')
			else:
				logged['user'] = user[0].id
		else:
			logged['status'] = False
		return logged


class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	confirm_password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at	= models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.id) + ", " + self.first_name

	objects  = UserManager()