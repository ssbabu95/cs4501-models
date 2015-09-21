from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

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
	type_of_user = models.CharField(max_length=16, choices=Type_Of_user_List, default=General)
	type_of_instrument = models.CharField(max_length=16, null=True, blank=True)

class Listing(models.Model):
	title = models.CharField(max_length=16)
	description = models.TextField(blank=True)
	creator = models.ForeignKey(User)
	date_listed = models.DateTimeField()
	available = models.BooleanField()

class Review(models.Model):
	title = models.CharField(max_length=40)
	body = models.CharField(max_length=250)
	review_rating = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)])
	reviewer = models.ForeignKey(User)
	
