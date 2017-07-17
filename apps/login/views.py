from __future__ import unicode_literals
from django.shortcuts import render, redirect 
from .models import User
from django.contrib import messages


def index(request):
	if request.session.get('id'):
		return render(request, 'login/success.html')
	return render(request, 'login/index.html')

def register(request):
	logged = User.objects.registerValidation(request.POST)
	if not logged['status']:
		for error in logged['errors']:
			messages.error(request, error)
		return redirect('/')
	request.session['id'] = logged['user'].id
	return redirect('/success')

def login(request):
	logged = User.objects.loginValidation(request.POST)
	if not logged['status']:
		for error in logged['errors']:
			messages.error(request, error)
		return redirect('/')
	else:
		user = User.objects.get(id=logged['user'])
		request.session['id'] = user.id
	return redirect('/success')

def success(request):
	user = User.objects.get(id=request.session['id'])
	context = {
		'user': user
	}
	
	return render(request, 'login/success.html', context)