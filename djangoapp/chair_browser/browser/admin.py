from django.contrib import admin	
from browser.models import Room, Term, Reservation, Attribute

class ChoiceInline(admin.TabularInline):
	model=Term
	extra=3


class RoomAdmin(admin.ModelAdmin):
	fieldsets=[
		('Name',		{'fields': ['name']}),
		('Capacity',	{'fields': ['capacity']}),
		('Description', {'fields': ['description']}),
		('Attributes', {'fields': ['attributes']}),
	]
	inlines=[ChoiceInline]
	list_display=('name', 'capacity', 'description', 'get_attributes',)


class TermAdmin(admin.ModelAdmin):
	list_display=('room', 'booking_date', 'from_hour', 'to')
	

class ReservationAdmin(admin.ModelAdmin):
	list_display=('user_profile', 'room', 'booking_date', 'from_hour', 'to')
	 
class AttributeAdmin(admin.ModelAdmin):
	list_display=('attribute',)

admin.site.register(Room, RoomAdmin)
admin.site.register(Term, TermAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Attribute, AttributeAdmin)
