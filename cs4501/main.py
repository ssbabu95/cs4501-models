import datetime

from django.http import JsonResponse
from django.contrib.auth import hashers
from django import db

from stuff import models

# APIs for accessing Users###############################################################################################

def create_user(request):
    if request.method != 'POST':
        return _error_response(request, "must make POST request")
    if 'first_name' not in request.POST or    \
       'last_name' not in request.POST or     \
       'password' not in request.POST or      \
       'username' not in request.POST or      \
	   'type_of_user' not in request.POST or  \
       'type_of_instrument' not in request.POST or \
       'listings' not in request.POST:
            return _error_response(request, "missing required fields")

    u = models.User(username=request.POST['username'],                         \
                    first_name=request.POST['first_name'],                             \
                    last_name=request.POST['last_name'], 					           \
					type_of_user=request.POST['type_of_user'],
                    password=hashers.make_password(request.POST['password']),  \
                    type_of_instrument=request.POST['type_of_instrument'],  \
                    is_active=False,                                           \
                    date_joined=datetime.datetime.now()                        \
                    )

    try:
        u.save()
    except db.Error:
        return _error_response(request, "db error")

    return _success_response(request, {'user_id': u.pk})

def lookup_user(request, user_id):
    if request.method != 'GET':
        return _error_response(request, "must make GET request")

    try:
        u = models.User.objects.get(pk=user_id)
    except models.User.DoesNotExist:
        return _error_response(request, "user not found")

    return _success_response(request, {'username': u.username,      \
                                       'first_name': u.f_name,          \
                                       'last_name': u.l_name,          \
									   'type_of_user': u.user_type, \
                                       'is_active': u.is_active,    \
                                       'type_of_instrument': u.type_of_instrument, \
                                       'date_joined': u.date_joined \
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
        return _error_response(request, "must make GET request")

    try:
        l = models.Listing.objects.get(pk=listing_id)
    except models.User.DoesNotExist:
        return _error_response(request, "user not found")

    return _success_response(request, {'title': l.username,      \
                                       'description': l.f_name,          \
                                       'creator': l.l_name,          \
                                       'available': l.is_active,    \
                                       'date_listed': l.date_joined \
                                       })

def update_listing(request, user_id):
    if request.method != 'POST':
        return _error_response(request, "must make POST request")

    try:
        u = models.User.objects.get(pk=user_id)
    except models.User.DoesNotExist:
        return _error_response(request, "user not found")

    changed = False
    if 'title' in request.POST:
        u.f_name = request.POST['title']
        changed = True
    if 'description' in request.POST:
        u.l_name = request.POST['description']
        changed = True
    if 'creator' in request.POST:
        u.password = hashers.make_password(request.POST['creator'])
        changed = True
    if 'available' in request.POST:
        u.is_active = request.POST['available']
        changed = True

    if not changed:
        return _error_response(request, "no fields updated")

    u.save()

    return _success_response(request)

############################################################################################################################################

def leave_thing(request):
    if request.method != 'POST':
        return _error_response(request, "must make POST request")
    if 'title' not in request.POST or      \
       'giver_id' not in request.POST or   \
       'location' not in request.POST:
        return _error_response(request, "missing required fields")

    try:
        giver = models.User.objects.get(pk=request.POST['giver_id'])
    except models.User.DoesNotExist:
        return _error_response(request, "giver not found")
    
    t = models.Thing(title=request.POST['title'],                       \
                     description = request.POST.get('description', ''), \
                     giver=giver,                                       \
                     location=request.POST['location'],                 \
                     date_given=datetime.datetime.now(),                \
                     was_taken=False                                    \
                     )
    try:
        t.save()
    except db.Error:
        return _error_response(request, "db error")

    return _success_response(request, {'thing_id': t.pk})
                     
def lookup_thing(request, thing_id):
    if request.method != 'GET':
        return _error_response(request, "must make GET request")
    
    try:
        t = models.Thing.objects.get(pk=thing_id)
    except models.Thing.DoesNotExist:
        return _error_response(request, "thing not found")

    return _success_response(request, {'title': t.title,             \
                                       'description': t.description, \
                                       'giver_id': t.giver_id,       \
                                       'location': t.location,       \
                                       'date_given': t.date_given,   \
                                       'was_taken': t.was_taken,     \
                                       })

def take_thing(request, thing_id):
    if request.method != 'POST':
        return _error_response(request, "must make POST request")

    try:
        t = models.Thing.objects.get(pk=thing_id)
    except models.Thing.DoesNotExist:
        return _error_response(request, "thing not found")

    if t.was_taken:
        return _error_response(request, "thing already taken")

    t.was_taken = True

    try:
        t.save()
    except db.Error:
        return _error_response(request, "db error")

    return _success_response(request)

def _error_response(request, error_msg):
    return JsonResponse({'ok': False, 'error': error_msg})

def _success_response(request, resp=None):
    if resp:
        return JsonResponse({'ok': True, 'resp': resp})
    else:
        return JsonResponse({'ok': True})