from django.db import models

class User(models.Model):
	Artist = 'artist'
	Producer = 'producer'
	General = 'general'
	Type_Of_user_List = (
		(Artist, 'Artist'),
		(Producer, 'Producer'),
		(General, 'General'),
	)
	username = models.CharField(max_length=24, unique=True)
	date_joined = models.DateTimeField()
	first_name = models.CharField(max_length=16)
	last_name = models.CharField(max_length=16)
	password = models.CharField(max_length=16)
	is_active = models.BooleanField()
	type_of_user = modelsCharField(max_length=16, choices=Type_Of_User_list, default=General)
	listings = models.OneToManyField(Listing)
	type_of_instrument = models.CharField(max_length=16, null=True, blank=True)

class Listing(models.Model):
	title = models.Charfield(max_length=16)
	description = models.TextField(blank=True)
	creator = models.ForeinKey('User')
	date_listed = models.DateTimeField()
	available = models.BooleanField()