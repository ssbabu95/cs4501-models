from django.http import JsonResponse, HttpResponse
from django.contrib.auth import hashers
from django import db
#from django.contrib.auth.decorators.csrf import csrf_exempt
import datetime, json, os, base64

from cs4501 import models

# APIs for accessing Users###############################################################################################

def create_user(request):
    if request.method != 'POST':
        return _error_response(request, "Must make a POST request")
    if 'first_name' not in request.POST or    \
       'last_name' not in request.POST or     \
       'password' not in request.POST or      \
       'username' not in request.POST or      \
       'type_of_user' not in request.POST:
       return _error_response(request, "Missing required fields")

    user = models.User(
        username=request.POST['username'],                         \
        first_name = request.POST['first_name'],                   \
        last_name = request.POST['last_name'],                     \
        password = hashers.make_password(request.POST['password']), \
        type_of_user = request.POST['type_of_user'],               \
        date_joined = datetime.datetime.now(),                     \
        is_active = True,                                          \
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
        user = authenticate(user=username, pas=password)  
        if user is not None:
            return JsonResponse({'authenticator': user.authenticator, 'user_id': user.user_id, 'date_created': user.date_created})
        else:
            return _error_response(request, "Wrong username or password")
    else:
        return _error_response(request, "Must make a POST request")

def authenticate(user=None, pas=None):
	try:
		usr = models.User.objects.get(username=user)
		if hashers.check_password(pas, usr.password):
			a = models.Authenticator(date_created=datetime.datetime.now(), user_id = usr.id, authenticator=base64.b64encode(os.urandom(32)).decode('utf-8'))
			a.save()
			return a
		else:
			return None 
	except models.User.DoesNotExist:
		return None
		
def user_logout(request):
	if request.method == 'POST':
		uid = request.POST.get('u_id')
		models.Authenticator.objects.filter(user_id=uid).delete()
		return _success_response(request, "Successfully logged out")
	else:
		return _error_response(request, "Must make a POST request")

def _error_response(request, error_msg):
    return JsonResponse({'ok': False, 'error': error_msg})

def _success_response(request, resp=None):
    if resp:
        return JsonResponse({'ok': True, 'resp': resp})
    else:
        return JsonResponse({'ok': True}) 

def lookup_user(request, user_id):
    if request.method != 'GET':
        return _error_response(request, "must make GET request")

    try:
        u = models.User.objects.get(pk=user_id)
    except models.User.DoesNotExist:
        return _error_response(request, "User not found")

    return _success_response(request, {'username': u.username,      \
                                       'first_name': u.first_name,  \
                                       'last_name': u.last_name,    \
                                       'type_of_user': u.type_of_user, \
                                       'is_active': u.is_active,    \
                       'type_of_instrument': u.type_of_instrument,  \
                                       'date_joined': u.date_joined \
                                      # 'listings': u.listings,      \
                                      # 'reviews': u.reviews         \
                                       })

def update_user(request, user_id):
    if request.method != 'POST':
        return _error_response(request, "must make POST request")

    try:
        u = models.User.objects.get(pk=user_id)
    except models.User.DoesNotExist:
        return _error_response(request, "user not found")

    changed = False
    if 'first_name' in request.POST:
        u.first_name = request.POST['first_name']
        changed = True
    if 'last_name' in request.POST:
        u.last_name = request.POST['last_name']
        changed = True
    if 'type_of_user' in request.POST:
        u.type_of_user = request.POST['type_of_user']
        changed = True
    if 'password' in request.POST:
        u.password = hashers.make_password(request.POST['password'])
        changed = True
    if 'is_active' in request.POST:
        u.is_active = request.POST['is_active']
        changed = True
    if 'type_of_instrument' in request.POST:
        u.type_of_instrument = request.POST['type_of_instrument']
        changed = True

    if not changed:
        return _error_response(request, "no fields updated")

    u.save()

    return _success_response(request)
	
#APIs for accessing Listing################################################################################################################

def create_listing(request):
	if request.method != 'POST':
		return _error_response(request, "must make POST request")
	try:
		place = models.Authenticator.objects.get(user_id=request.POST['u_id'])
	except models.Authenticator.DoesNotExist:
		return _error_response(request, "You are not logged in")

	if 'title' not in request.POST or             \
       'description' not in request.POST or       \
       'creator' not in request.POST or           \
       'available' not in request.POST:         
		return _error_response(request, "missing required fields")

	l = models.Listing(title=request.POST['title'],            \
		    description=request.POST['description'],   \
		    creator=models.User.objects.get(pk=request.POST['creator']),           \
		    available=request.POST['available'],       \
		    date_listed=datetime.datetime.now()        \
		    )

	try:
		l.save()
	except db.Error:
		return _error_response(request, "db error")

	return _success_response(request, {'listing_id': l.pk})

def lookup_listing(request, listing_id):
    if request.method != 'GET':
        return _error_response(request, "Must make GET request")

    try:
        l = models.Listing.objects.get(pk=listing_id)
    except models.Listing.DoesNotExist:
        return _error_response(request, "Listing not found")

    return _success_response(request, {'title': l.title,                \
                                       'description': l.description,    \
                                       'creator': l.creator.username,            \
                                       'available': l.available,        \
                                       'date_listed': l.date_listed,     \
				       'listing_id': l.pk		\
                                       })

def update_listing(request, listing_id):
    if request.method != 'POST':
        return _error_response(request, "Must make POST request")

    try:
        u = models.Listing.objects.get(pk=listing_id)
    except models.Listing.DoesNotExist:
        return _error_response(request, "Listing not found")

    changed = False
    if 'title' in request.POST:
        u.title = request.POST['title']
        changed = True
    if 'description' in request.POST:
        u.description = request.POST['description']
        changed = True
    if 'creator' in request.POST:
        u.creator = models.User.objects.get(pk=request.POST['creator'])
        changed = True
    if 'available' in request.POST:
        u.available = request.POST['available']
        changed = True

    if not changed:
        return _error_response(request, "No fields updated")

    u.save()

    return _success_response(request)


def buy_listing(request, listing_id):
    if request.method != 'GET':
        return _error_response(request, "must make GET request")

    try:
        t = models.Listing.objects.get(pk=listing_id)
    except models.Listing.DoesNotExist:
        return _error_response(request, "Listing not found")

    if not t.available:
        return _error_response(request, "Listing not available")

    t.available = False

    try:
        t.save()
    except db.Error:
        return _error_response(request, "db error")

    return _success_response(request)

def create_review(request):
    if request.method != 'POST':
        return _error_response(request, "must make POST request")
    if 'title' not in request.POST or           \
       'body' not in request.POST or            \
       'review_rating' not in request.POST or   \
       'reviewer' not in request.POST:
        return _error_response(request, "missing required fields")

    r = models.Review(title=request.POST['title'],                \
                    body=request.POST['body'],                    \
                    review_rating=request.POST['review_rating'],  \
                    reviewer=models.User.objects.get(pk=request.POST['reviewer'])             \
                    )

    try:
        r.save()
    except db.Error:
        return _error_response(request, "db error")

    return _success_response(request, {'review_id': r.pk})

def lookup_review(request, review_id):
	if request.method != 'GET':
		return _error_response(request, "Must make GET request")
	
	try:
		l = models.Review.objects.get(pk=review_id)
	except models.Review.DoesNotExist:
		return _error_response(request, "Review not found")

	return _success_response(request, {'title': l.title,                \
                                       'body': l.body,    \
                                       'reviewer': l.reviewer.username,            \
                                       'review_rating': l.review_rating        \
                                       })


def update_review(request, review_id):
    if request.method != 'POST':
        return _error_response(request, "Must make POST request")

    try:
        r = models.Review.objects.get(pk=review_id)
    except models.Review.DoesNotExist:
        return _error_response(request, "Listing not found")

    changed = False
    if 'title' in request.POST:
        r.title = request.POST['title']
        changed = True
    if 'body' in request.POST:
        r.body = request.POST['body']
        changed = True
    if 'reviewer' in request.POST:
        r.reviewer = models.User.objects.get(pk=request.POST['reviewer'])
        changed = True
    if 'review_rating' in request.POST:
        r.review_rating = request.POST['review_rating']
        changed = True

    if not changed:
        return _error_response(request, "No fields updated")

    r.save()

    return _success_response(request)

def most_recent(request):
	if request.method != 'GET':
		return _error_response(request, "Must make a GET request")
	try:
		l = models.Listing.objects.latest('date_listed')
	except models.Listing.DoesNotExist:
		return _error_response(request, "Listing not found")

	return _success_response(request, {'title': l.title,                \
                                       'description': l.description,    \
                                       'creator': l.creator.username,            \
                                       'available': l.available,        \
                                       'date_listed': l.date_listed,     \
				       'listing_id': l.pk,		\
                                       })


