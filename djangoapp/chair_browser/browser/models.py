from django.db import models
from django.db.models import Q
from browser.exceptions import TimeIntervalException, ScheduleException, ArchaicDateTimeException
from django.contrib.auth.models import User
import django_tables2 as tables
from datetime import datetime, date
from django.utils import timezone


class Room(models.Model):
	"""Room model that contains name, capacity and optional descripiton"""
	name=models.CharField(max_length=25)
	capacity=models.IntegerField(default=20)
	description=models.CharField(max_length=120, blank=True)
	
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
	
	def save(self, *args, **kwargs):
		if self.booking_date < date.today():
			raise ArchaicDateTimeException()
		if self.booking_date == date.today():
			if self.from_hour.hour < timezone.now().hour:
				raise ArchaicDateTimeException()
			if self.from_hour.minute < timezone.now().minute:
				raise ArchaicDateTimeException()
		# Check time interval format
		if self.from_hour >= self.to:
			raise TimeIntervalException()
		
		# If call has been made in case of time interval distribution
		if kwargs.pop('parameter', None):
			super(Term, self).save(self, *args, **kwargs)
		
		# Check whether exists term collision for particular room
		try:
			term = Term.objects.get(
						Q(room__name=self.room.name),
						Q(booking_date=self.booking_date),
						~Q(from_hour__gte=self.to),
						~Q(to__lte=self.from_hour),
					)
		except Term.MultipleObjectsReturned:
			raise ScheduleException()
		except Term.DoesNotExist:
			super(Term, self).save(self, *args, **kwargs)
		else:
			if term:
				raise ScheduleException()
			else:
				super(Term, self).save(self, *args, **kwargs)
		
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
