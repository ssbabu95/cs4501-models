import datetime

from django.http import JsonReponse
from django.contrib.auth import hashers
from django import db
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from stuff import models

# APIs for accessing Users###############################################################################################

def create_user(request):
    if request.method != 'POST':
        return _error_response(request, "Must make a POST request")
    if 'first_name' not in request.POST or 
       'last_name' not in request.POST or
       'password' not in request.POST or
       'username' not in request.POST or
       'type_of_user' not in request.POST or:
       return _error_response(request, "Missing required fields")

    user = models.User(username=request.POST['username'],
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        password = hashers.makepassword(request.POST['password']),
        username = request.POST['username'],
        type_of_user = request.POST['type_of_user'],
        date_joined = datetime.datetime.now(),
        is_active = True,
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

    return _success_response(request, {'username': u.username,      
                                       'first_name': u.f_name,          
                                       'last_name': u.l_name,          
									   'type_of_user': u.user_type, 
                                       'is_active': u.is_active,    
                                       'type_of_instrument': u.type_of_instrument, 
                                       'date_joined': u.date_joined 
                                       'listings': u.listings
                                       'reviews': u.reviews
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
        u.f_name = request.POST['f_name']
        changed = True
    if 'last_name' in request.POST:
        u.l_name = request.POST['l_name']
        changed = True
	if 'type_of_user' in request.POST:
		u.user_type = request.POST['user_type']
		changed = True
    if 'password' in request.POST:
        u.password = hashers.make_password(request.POST['password'])
        changed = True
    if 'is_active' in request.POST:
        u.is_active = request.POST['is_active']
        changed = True
    if 'type_of_instrument' in request.POST:
        u.is_active = request.POST['type_of_instrument']
        changed = True
    if 'listings' in request.POST:
        u.is_active = request.POST['listings']
        changed = True

    if not changed:
        return _error_response(request, "no fields updated")

    u.save()

    return _success_response(request)
	
#APIs for accessing Listing################################################################################################################

def create_listing(request):
    if request.method != 'POST':
        return _error_response(request, "must make POST request")
    if 'title' not in request.POST or     \
       'description' not in request.POST or     \
       'creator' not in request.POST or   \
       'available' not in request.POST:
        return _error_response(request, "missing required fields")

    l = models.Listing(title=request.POST['title'],                         \
                    description=request.POST['description'],                             \
                    creator=request.POST['creator'],                             \
                    available=request.POST['available'],  \
                    date_listed=datetime.datetime.now()                        \
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

    return _success_response(request, {'title': l.title,      
                                       'description': l.description,          
                                       'creator': l.creator,          
                                       'available': l.available,    
                                       'date_listed': l.date_listed 
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
        u.creator = request.POST['creator']
        changed = True
    if 'available' in request.POST:
        u.available = request.POST['available']
        changed = True

    if not changed:
        return _error_response(request, "No fields updated")

    u.save()

    return _success_response(request)


def buy_listing(request, listing_id):
    if request.method != 'POST':
        return _error_response(request, "must make POST request")

    try:
        t = models.Listing.objects.get(pk=listing_id)
    except models.Listing.DoesNotExist:
        return _error_response(request, "Listing not found")

    if !t.available:
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
    if 'title' not in request.POST or     
       'body' not in request.POST or     
       'review_rating' not in request.POST or   
       'reviewer' not in request.POST:
        return _error_response(request, "missing required fields")

    r = models.Review(title=request.POST['title'],                         
                    body=request.POST['body'],                             
                    review_rating=request.POST['review_rating'],                             
                    reviewer=request.POST['reviewer']
                    )

    try:
        r.save()
    except db.Error:
        return _error_response(request, "db error")

    return _success_response(request, {'review_id': r.pk})

def update_review(request, review_id):
    if request.method != 'POST':
        return _error_response(request, "Must make POST request")

    try:
        r = models.Review.objects.get(pk=user_id)
    except models.Review.DoesNotExist:
        return _error_response(request, "Listing not found")

    changed = False
    if 'title' in request.POST:
        u.title = request.POST['title']
        changed = True
    if 'description' in request.POST:
        u.description = request.POST['description']
        changed = True
    if 'creator' in request.POST:
        u.creator = request.POST['creator']
        changed = True
    if 'available' in request.POST:
        u.available = request.POST['available']
        changed = True

    if not changed:
        return _error_response(request, "No fields updated")

    u.save()

    return _success_response(request)
