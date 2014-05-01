from django.shortcuts import render
from browser.forms import UserForm, UserProfileForm, TermForm
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from browser.models import Room, Term, Reservation
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, Page
from browser.models import Room, Term, Reservation, RoomTable, TermTable
from django.db.models import Q
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db import IntegrityError, transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
import datetime
import time



# Based on: http://www.tangowithdjango.com/book/chapters/login.html
def register(request):
    # Get request context
    context = RequestContext(request)

    # A boolean value for telling the template
    # whether the registration was successful
    # Set to False initially.
    # Code changes value to True when registration succeeds.
    registered = False

    #If it's a HTTP POST, we're interested in processing form data
    if request.method == 'POST':
        # Attempt to grab information from the raw form information
        user_form = UserForm(data=request.POST)

        # If both forms are valid
        if user_form.is_valid():

            # Save the user's form data to the database
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we compute update the user object.
            user.set_password(user.password)
            user.save()

            # Update our variable, to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistake or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()

    # Render the template depending on the context
    return render_to_response(
        'browser/register.html',
        {'user_form': user_form,
         'registered': registered},
        context)


def user_login(request):
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have User object, the details are correct.
        # If None (Python's way of representing the absence of a value),
        # no user with matching credentials was found.
        if user is not None:
            # Is the account active? It could have been disabled.
            if user.is_active:

                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/browser/homepage')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled")
        else:
            # Bad login details were provided.
            # We cannot log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system,
        # hence the blank dictionary object...
        return render_to_response('browser/login.html', {}, context)


# Use the login_required() decorator to ensure only those logged in can access the view
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to index.
    return HttpResponseRedirect("/browser")


# Self-defined views
def index(request):
    return render_to_response('browser/index.html', RequestContext(request))


@login_required
def homepage(request):
    return render_to_response("browser/homepage.html", RequestContext(request))


@login_required
def rooms(request):
    # Remove previous choices
    if 'ids' in request.session:
        del request.session['ids']

    # By default set full room_list
    room_list = Room.objects.all()

    if request.method == 'GET':
        # Validate msg from search-box
        query = request.GET.get('query', '')
        room_list = Room.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query) | Q(capacity__icontains=query))

    # Prepare RoomTable content to display
    rooms = RoomTable(room_list, order_by=request.GET.get('sort'))

    # Set pagination
    paginator = Paginator(rooms.rows, 3)

    page = request.GET.get('page')
    try:
        pagRooms = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        pagRooms = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        pagRooms = paginator.page(paginator.num_pages)


    return render_to_response('browser/rooms.html', {'rooms': pagRooms}, RequestContext(request))


@login_required
def terms(request):
    # Initialize term_list to empty
    term_list = []
    if request.method == 'POST':
        # If user directly decided to skip room browser,
        # assume that all rooms are in his area of interests
        if 'all_ids' in request.POST:
            request.session['ids'] = list(Room.objects.values_list('id', flat=True))
        elif 'ids' not in request.session:
            request.session['ids'] = request.POST.getlist('selection', None)

        ids = request.session['ids']
        term_list = Term.objects.filter(room_id__id__in=ids)

    if request.method == 'GET':

        ids = request.session['ids']
        term_list = Term.objects.filter(Q(room_id__id__in=ids))
        form = TermForm(data=request.GET)

        # Validate term form
        if form.is_valid():
            sel_date = form.cleaned_data.get('date')
            sel_from_hour = form.cleaned_data.get('from_hour')
            sel_to = form.cleaned_data.get('to')
            term_list = term_list.filter(
                booking_date=sel_date,
                from_hour__lte=sel_from_hour,
                to__gte=sel_to
            )

            # Parse datetime to string using .isoformat()
            request.session['from'] = sel_from_hour.isoformat()
            request.session['to'] = sel_to.isoformat()

    # Construct data to be displayed
    terms = TermTable(term_list)
    paginator = Paginator(terms.rows, 3)

    page = request.GET.get('page')
    try:
        pagTerms = paginator.page(page)
    except PageNotAnInteger:
        pagTerms = paginator.page(1)
    except EmptyPage:
        pagTerms = paginator.page(paginator.num_pages)
    term_form = TermForm()

    return render_to_response('browser/terms.html', {'terms': pagTerms, 'term_form': term_form}, RequestContext(request))


@login_required
def confirmation(request):
    if request.method == 'POST':
        # By default get list of selected terms
        term_list = request.POST.getlist('selection')
        if term_list:

            # If term list is not empty pick one random request
            import random

            term_id = random.choice(term_list)

            # Get random reservation from selected
            reservation = Term.objects.filter(pk=term_id)
            request.session['term_id'] = reservation[0].id

            if 'from' not in request.session or 'to' not in request.session:
                request.session['from'] = reservation[0].from_hour.isoformat()
                request.session['to'] = reservation[0].to.isoformat()

        else:
            reservation = []

        if 'from' in request.session and 'to' in request.session:
            from_hour = request.session['from']
            to = request.session['to']

            return render_to_response('browser/confirmation.html',
                                      {'reservations': reservation, 'from': from_hour, 'to': to},
                                      RequestContext(request))

        else:
            return render_to_response('browser/confirmation.html', {'redirect_homepage': True}, RequestContext(request))


@login_required
@transaction.atomic
def commit(request):
    print "Start: %s" % time.ctime()
    time.sleep(8)
    print "End: %s" % time.ctime()

    if request.method == 'POST':
        # If user submits non-empty reservation
        # and all of necessary data saved in session
        if 'term_id' in request.session and 'from' in request.session and 'to' in request.session:

            # Get term id
            term_id = request.session.pop('term_id')

            # Create datetimer to handle string-to-datetime conversion
            datetimer = datetime.datetime.strptime

            # Convert time
            term_from = datetimer(request.session.pop('from'), "%H:%M:%S").time()
            term_to = datetimer(request.session.pop('to'), "%H:%M:%S").time()

            # Get first row, not whole QuerySet!
            terms = Term.objects.filter(id=term_id)

            # If non-empty row
            if terms:
                db_term = terms[0]
                #
                room = Room.objects.get(pk=db_term.room.id)
                # Delete reserver interval from area of interests
                room.term_set.filter(id=term_id).delete()
                # Check whether date interval can be divided from left-side
                if db_term.from_hour < term_from:
                    # If so create appropriate row
                    room.term_set.create(
                        booking_date=db_term.booking_date,
                        from_hour=db_term.from_hour,
                        to=term_from
                    )

                # Analogical situation to rhs of time interval
                if db_term.to > term_to:
                    room.term_set.create(
                        booking_date=db_term.booking_date,
                        from_hour=term_to,
                        to=db_term.to
                    )

                # Register reservation
                Reservation.objects.create(
                    user_profile=request.user,
                    room=db_term.room,
                    booking_date=db_term.booking_date,
                    from_hour=term_from,
                    to=term_to
                )

                # Add eventual intervals
                room.save()

                return render_to_response('browser/commit.html',
                                          {'transaction_msg': 'Transaction accomplished successfully'},
                                          RequestContext(request))

    return render_to_response('browser/commit.html', {'transaction_msg': 'Transaction failed. Try again!'},
                              RequestContext(request))


