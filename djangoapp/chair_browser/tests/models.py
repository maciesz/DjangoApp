from django.test import TestCase
from browser.models import Room, Term, Reservation
from django.db.models import Q

class RoomTestCase(TestCase):

	# Cacapacity is greater or equal than 1
	def test_rooms_capacity(self):
		rows=Room.objects.count()
		valid_capacity_rows=Room.objects.filter(capacity__gte=1)

		self.assertEqual(rows, valid_capacity_rows)


class TermTestCase(TestCase):
	def setUp(self):
		rows=Term.objects.all()
	
	# Starting_time < ending_time
	def test_terms_start_ending_times(self):
		for row in rows:
			self.assertTrue(row.from_hour < row.to)	
			
	# Same room term collision
	def test_terms_time_intervals(self):
		for row in rows:
			same_room_rows=Term.objects.filter(room__name=row.name)
			self.assertEqual(
				same_room_rows.filter(
					Q(from_hour__gte=row.to) |
					Q(to__lte=row.from_hour)
				),
				same_room_rows.count()
			)


class ReservationTestCase(TestCase):

	# Starting time < ending time
	def test_reservation_start_ending_times(self):
		rows=Reservation.objects.all()
		
		for row in rows:
			self.assertTrue(row.from_hour < row.to)

