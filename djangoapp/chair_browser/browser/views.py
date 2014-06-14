from datetime import datetime
from django.shortcuts import render
from browser.forms import UserForm, TermForm, ContactForm
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, Page
from browser.models import Room, Term, Reservation, Attribute, RoomTable, TermTable
from django.db.models import Q
from django.db import IntegrityError, transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from collections import defaultdict
import json
import datetime
import time

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
    page = request.GET.get('page')
    #room_list = Room.objects.all()

    if not 'minCap' in request.session:
        request.session['minCap'] = 10
        request.session['maxCap'] = 30

    if request.method == 'GET':
        # Validate msg from search-box
        query = request.GET.get('query', '')
        capRange = request.GET.get('capacity', '10-10')
        minCap, maxCap = capRange.split('-')

        if minCap == maxCap:
            minCap = request.session['minCap']
            maxCap = request.session['maxCap']
        else:
            request.session['minCap'] = minCap
            request.session['maxCap'] = maxCap

        room_list = Room.objects.all();
        attribs = Attribute.objects.all()
        for attr in attribs:
            parameter = str(attr)
            if request.GET.get(parameter):
                att = attribs.filter(attribute=parameter)
                room_list = room_list.filter(attributes__contains=att)

        room_list = room_list.filter(
            (Q(capacity__gte=minCap) & Q(capacity__lte=maxCap)) &
            (
                Q(capacity__icontains=query) |
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )
        )

    # Prepare RoomTable content to display
    rooms = RoomTable(room_list, order_by=request.GET.get('sort'))

    # Set pagination
    paginator = Paginator(rooms.rows, 4)
    try:
        paginated_rooms = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paginated_rooms = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        paginated_rooms = paginator.page(paginator.num_pages)

    attribute_list = Attribute.objects.all()
    return render_to_response(
        'browser/rooms.html', {'rooms': paginated_rooms, 'attribute_list': attribute_list}, RequestContext(request))


@login_required
def terms(request):
    # Initialize term_list to empty
    term_list = []
    if request.method == 'POST':
        # If user directly decided to skip room browser,
        # assume that all rooms are in his area of interests
        if 'all_ids' in request.POST:
            request.session['ids'] = list(Room.objects.values_list('id', flat=True))
        if 'ids' not in request.session:
            request.session['ids'] = request.POST.getlist('selection', None)
            #name = request.POST.get('name', None)
            #if name:
             #   request.session['ids'] = Room.objects.filter(name__=name).values('pk')[0]


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


def contact_form(request):
    return render_to_response('browser/rooms.html', {'form': ContactForm()}, RequestContext(request))


def main(request):
    return render_to_response('ajaxexample.html', context_instance=RequestContext(request))

@login_required
def load_db_content(request):
    if request.GET:
        # By default set date and time to current.
        default_date = datetime.datetime.now().date()
        default_time = datetime.datetime.now().time()
        # Read concrete parametres from request.
        date_str = request.GET.get('date')
        time_str = request.GET.get('time')
        # Parse data.
        if date_str:
            # Format has been set by JS-caller.
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        else:
            # By default set current one.
            date = default_date
        # Parsowanie czasu.
        if time_str:
            time = datetime.datetime.strptime(time_str, "%H:%M").time()
        else:
            time = default_time

        # Initialize dictionary.
        dictionary = defaultdict(list)

        # Load all attributes from database.
        attribute_list = Attribute.objects.values_list('attribute', flat=True)
        final_attr_list = []
        for attr in attribute_list:
            final_attr_list.append(attr)
        # Load all room objects and slightly modify content.
        room_list = []
        for room in Room.objects.all():
            parameter_list = []
            parameter_list.extend([room.name, room.capacity, room.description])
            room_attr_list = \
                room.attributes.all().values_list('attribute', flat=True)
            final_room_attr_list = []
            for attr in room_attr_list:
                final_room_attr_list.append(attr)
            parameter_list.append(
                final_room_attr_list
            )
            room_list.append(parameter_list)

        # Filter terms by date and time.
        terms = Term.objects.filter(
            (Q(booking_date__gt=date)) |
            (Q(booking_date=date) & Q(from_hour__gte=time))
        )
        # Behave analogously to rooms.
        term_list = []
        for term in terms:
            parameter_list = []
            parameter_list.append(term.room.name)
            parameter_list.append(term.booking_date.strftime("%Y-%m-%d"))
            parameter_list.append(term.from_hour.strftime("%H:%M"))
            parameter_list.append(term.to.strftime("%H:%M"))

            term_list.append(parameter_list)

        # Fulfull dictionary with proper data.
        dictionary['Attribute'] = final_attr_list
        dictionary['Room'] = room_list
        dictionary['Term'] = term_list

        # Parse data and send it over HttpResponse.
        response_data = json.dumps(dictionary)
        return HttpResponse(response_data, mimetype='application/json')

@login_required
def ajax(request):
    if request.GET:
        room_name = request.GET.get('room_name', '3440')
        current_date = datetime.datetime.today()
        dates = Term.objects.filter(
            Q(room__name=room_name) &
            Q(booking_date__gte=current_date)
        ).values_list('booking_date', flat = True).distinct()
        to_json = []
        dictionary = defaultdict(list)
        for date in dates:
            d = date.strftime("%Y-%m-%d")
            time_list = \
                Term.objects.filter(
                    Q(room__name=room_name) &
                    Q(booking_date=date)
                ).values_list('from_hour', 'to').order_by('from_hour', 'to')

            #time_list.order_by('-from_hour')

            first_elt = True
            result_time_list = []
            previous_from, previous_to = None, None
            for time in time_list:
                time_from = time[0]
                time_to = time[1]
                if first_elt:
                    previous_from = time_from
                    previous_to = time_to
                    lst = [previous_from, previous_to]
                    result_time_list.append(lst)
                    first_elt = False
                else:
                    curr_from = time_from
                    curr_to = time_to
                    if previous_to == curr_from:
                        result_time_list[-1][-1] = curr_to
                        previous_to = curr_to
                    else:
                        previous_from = curr_from
                        previous_to = curr_to
                        lst = [curr_from, curr_to]
                        result_time_list.append(lst)#curr_from, curr_to)

            dict_list = []
            for time in result_time_list:
                time_from = time[0].strftime("%H:%M")
                time_to = time[-1].strftime("%H:%M")
                tup = (time_from, time_to)
                dict_list.append(tup)
            dictionary[d] = dict_list
            to_json.append(d)
        #data = serializers.serialize(format, dates)
        response_data = json.dumps(dictionary)#[str(obj) for obj in to_json])
        return HttpResponse(response_data, mimetype='application/json')

    #return render(request, 'ajaxexample_json.html', {'aa': 'aa'})#json.dumps([str(obj) for obj in dates])) #, RequestContext(request)) #response_dict))

@login_required
@transaction.atomic
def rent(request):
    completed = False

    if request.GET:
        try:
            try:
                room_name = request.GET.get('room_name')
                date = datetime.datetime.strptime(request.GET.get('date'), "%Y.%m.%d")
                from_hour = datetime.datetime.strptime(request.GET.get('from_hour'), "%I:%M %p").time()
                to_hour = datetime.datetime.strptime(request.GET.get('to_hour'), "%I:%M %p").time()

                try:
                    try:
                        terms = Term.objects.filter(
                            Q(room__name=room_name) &
                            Q(booking_date=date)
                        ).order_by('from_hour', 'to')

                        is_first = True
                        last_term = None
                        previous_to = None
                        to_be_added = []
                        for term in terms:
                            if is_first:
                                last_term = term
                                previous_to = term.to
                                is_first = False
                            else:
                                if term.from_hour == previous_to:
                                    last_term.to = term.to
                                    last_term.save()
                                    term.delete()
                                else:
                                    last_term = term
                                    previous_to = term.to

                    except Exception as e:
                        return HttpResponse(json.dumps(str(e)), mimetype='application/json')

                    reservations = Term.objects.filter(
                        Q(room__name=room_name) &
                        Q(booking_date=date) &
                        Q(from_hour__lte=from_hour) &
                        Q(to__gte=to_hour)
                    )
                    try:
                        if not reservations:
                            #dict = defaultdict(list)
                            list = []
                            #conv_date = date.strftime("%Y.%m.%d")
                            #conv_from_time = from_hour.strftime("%I:%M %p")
                            #conv_to_time = to_hour.strftime("%I:%M %p")
                            #list = [room_name, conv_date, conv_from_time, conv_to_time,]
                            #dict['values'] = list
                            #dict['komunikat'] = 'Nie istnieje tak sparametryzowany obiekt w bazie'
                            return HttpResponse(json.dumps('No rooms with such preferences are available'), mimetype='application/json')

                        reservation = reservations[0]
                        room = Room.objects.filter(pk=reservation.room.id)[0]
                        if room:
                            if reservation.from_hour < from_hour:
                                room.term_set.create(
                                    booking_date=reservation.booking_date,
                                    from_hour=reservation.from_hour,
                                    to=from_hour
                                )

                            # Analogical situation to rhs of time interval
                            if reservation.to > to_hour:
                                room.term_set.create(
                                    booking_date=reservation.booking_date,
                                    from_hour=to_hour,
                                    to=reservation.to
                                )

                            # Register reservation
                            Reservation.objects.create(
                                user_profile=request.user,
                                room=reservation.room,
                                booking_date=reservation.booking_date,
                                from_hour=from_hour,
                                to=to_hour
                            )

                            # Delete original term
                            room.term_set.filter(id=reservation.id).delete()

                            # Add eventual intervals
                            room.save()

                            #Mark operation as completed
                            completed = True

                        data = json.dumps(completed)
                        return HttpResponse(data, mimetype='application/json')
                    except:
                        return HttpResponse(json.dumps('Error in reservation service'), mimetype='application/json')
                except:
                    return HttpResponse(json.dumps('No rooms with such preferences are available'), mimetype='application/json')
            except:
                #response = defaultdict(list)
                #list = [room_name, date, from_hour, to_hour]
                #response['dane'] = list
                #response['komunikat'] = 'Blad podczas odczytywania danych GETem'
                return HttpResponse(json.dumps('Invalid data format'), mimetype='application/json')
        except:
            return HttpResponse(json.dumps('Error in GET method'), mimetype='application/json')
    else:
        return HttpResponse(json.dumps('Any of GET/SET methods has been set'), mimetype='application/json')