from dajaxice.decorators import dajaxice_register
from forms import ContactForm
from django.utils import simplejson
from models import Attribute, Term, Room
from dajax.core import Dajax

@dajaxice_register
def send_message(request, form):
    f = ContactForm(form)
    if f.is_valid():
        #Use mail_admin or sth to send off the data like you normally would
        return simplejson.dumps({'status': 'Success!'})
    return simplejson.dumps({'status': f.errors})


@dajaxice_register
def get_attribute(request, pk):
    dajax = Dajax()
    attr = Attribute.objects.get(pk=pk)
    if attr:
        pass
        dajax.assign('#attrName', 'innerHTML', attr.attribute)
        #tabl = 'Yes' if attr.icontains('tablica') else 'No'
        #dajax.assign('#isTable', 'innerHTML', tabl)
    dajax.script("cur = %d;" % pk)
    return dajax.json()


@dajaxice_register
def say_hello(request):
    dajax = Dajax()
    dajax.alert("Hello world!")
    return dajax.json()


@dajaxice_register
def execute(request, name):
    dajax = Dajax()
    namer = 'Bialy Dom'
    date_list = Term.objects.all()
    #if not date_list:
      #  string = "<p>" + "Ala ma kota" + "</p>"
      #  dajax.assign('#data_modal', 'innerHTML', '%s' % string)
      #  return dajax.json()
    stak = ''
    if date_list:
        for date in date_list:
            stak.append(dateroom__name)
        #stak.append('ddd', 'aaaa', 'llda') #.booking_date)
            #dajax.append('#data_modal', 'innerHTML', "<p>Cokolwiek do cholery jasnej</p>")
            #dajax.append('#data_modal', 'innerHTML', '<p>Django dziala mi na nerwy</p>')
            #dajax.append('#data_modal', 'innerHTML', date_list.attribute)
            #dajax.append('#data_modal', 'innerHTML', "<li>" + date_list + "</li>")

        dajax.append('#data_modal', 'innerHTML', stak)

    return dajax.json()


@dajaxice_register
def blabla(request, name):
    return simplejson.dumps({'status': 'aaa'})
    #date_list = ['Bialy Dom',] #Term.objects.filter(room__name=name).values('booking_date')
    #return simplejson.dumps({'dates': date_list})