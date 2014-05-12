from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.db import models
from django.db.models import Q
#from browser.exceptions import TimeIntervalException, ScheduleException, ArchaicDateTimeException
from django.contrib.auth.models import User
import django_tables2 as tables
from datetime import datetime, date
from django.utils import timezone


class Attribute(models.Model):
	"""Attribute that can be involved in Room object"""
	attribute=models.CharField(max_length=30)

	def __unicode__(self):
		return self.attribute

class Room(models.Model):
	"""Room model that contains name, capacity and optional descripiton"""
	name=models.CharField(max_length=25)
	capacity=models.IntegerField(default=20)
	description=models.CharField(max_length=120, blank=True)
	attributes=models.ManyToManyField(Attribute)

	def get_attributes(self):
		separator = ", "
		return separator.join([item.attribute for item in self.attributes.all()])
	get_attributes.short_description = "Set of attributes"

	def __unicode__(self):
		return self.name

class RoomTable(tables.Table):
	name=tables.Column(orderable=True)
	capacity=tables.Column(orderable=True)
	description=tables.Column(orderable=False)

	class Meta:
		#model=Room
		attrs={"class": "paleblue", "width": "300%"}

	selection = tables.CheckBoxColumn(accessor='pk')

class Term(models.Model):
    """ Term model. Involves info about booking term for concrete room """
    booking_date=models.DateField()
    from_hour=models.TimeField('from')
    to=models.TimeField()
    room=models.ForeignKey(Room)


    def __unicode__(self):
		return "Date: " + str(self.booking_date) + " From: " + str(self.from_hour) + " To: " + str(self.to)

class TermTable(tables.Table):
	id=tables.Column()
	booking_date=tables.Column()
	from_hour=tables.Column('from')
	to=tables.Column()
	room=tables.Column(Room, 'room')
	class Meta:
		orderable=True

	selection = tables.CheckBoxColumn(accessor="pk")

class UserProfile(models.Model):
	""" User profile model overriding User model with additional photo opiton """
	user=models.OneToOneField(User)
	photo=models.ImageField(upload_to="profile_images", blank=True)
	
	def __unicode__(self):
		return self.user.username


class Reservation(models.Model):
	""" Reservation model related with user and term of renting room """
	user_profile=models.ForeignKey(User, verbose_name='user')
	room=models.ForeignKey(Room)
	booking_date=models.DateField()
	from_hour=models.TimeField()
	to=models.TimeField()
	
	def __unicode__(self):
		return "User: " + str(self.user_profile) + ", Room" + str(self.room) + ", " + str(self.booking_date)
