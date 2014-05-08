from dajaxice.decorators import dajaxice_register
from forms import ContactForm
from django.utils import simplejson

@dajaxice_register
def send_message(request, form):
    f = ContactForm(form)
    if f.is_valid():
        #Use mail_admin or sth to send off the data like you normally would
        return simplejson.dumps({'status': 'Success!'})
    return simplejson.dumps({'status': f.errors})