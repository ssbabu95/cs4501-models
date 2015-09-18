import datetime

from django.http import JsonReponse
from django.contrib.auth import hashers
from django import db

from cs4501 import models

def create_user(request):
	if request.method != 'POST':
		return _error_response(request, "Must make a POST request")
	if 'first_name' not in request.POST or 
	   'last_name' not in request.POST or
	   'password' not in request.POST or
	   'username' not in request.POST or
	   'type_of_user' not in request.POST:
	   return _error_response(request, "Missing required fields")

	user = models.User(username=request.POST['username'],
		first_name = request.POST['first_name'],
		last_name = request.POST['last_name'],
		password = hashers.makepassword(request.POST['password']),
		username = request.POST['username'],
		type_of_user = request.POST['type_of_user'],
		date_joined = datetime.datetime.now()
	)
	try:
		user.save()
	except db.Error:
		return _error_response(request, "DB error")
	return _success_response(request, {'user_id': user.pk})

def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request, user)
				return HttpResponse("Login successful")
			else:
				return HttpResponse("Login failed")
		else:
			return HttpResponse("Wrong username or password")
	else:
		return _error_response(request, "Must make a POST request")

@login_required
def user_logout(request):
	logout(request)
	return HttpResponse("Logged out") 
