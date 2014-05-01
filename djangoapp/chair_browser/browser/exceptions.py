from django.http import HttpResponse

class TimeIntervalException(Exception):
	""" Raised when invalid time interval was given """

	def __unicode__(self):
		return "Taking up time must be less than freeing time"


class ScheduleException(Exception):
	""" Raised when term to be insterted insult room-renting schedule """

	def __unicode__(self):
		return "Term collides with room-renting schedule"


class ArchaicDateTimeException(Exception):
	""" Raised when term is partially not available from the start """

	def __unicode__(self):
		return "Try to save term from the past"
