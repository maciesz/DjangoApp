# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):
	
	def forwards(self, orm):
		"Write your forwards methods here."
		white_board = orm['browser.Attribute'](attribute='white_board')
		green_board = orm['browser.Attribute'](attribute='green_board')
		projector = orm['browser.Attribute'](attribute='projector')

		white_board.save()
		green_board.save()
		projector.save()
		
		import random
		bound = 15
		for room in orm['browser.Room'].objects.all():
			if room.capacity <= bound:
				room.attribute.add(white_board)
			else:
				room.attribute.add(green_board)

			decision = random.randint(0, 1)
			if random.randint(0, 1):
				room.attribute.add(projector)

			room.save()

	def backwards(self, orm):
		for room in orm['browser.Room'].objects.all():
			room.attributes
	models = {
		u'auth.group': {
			'Meta': {'object_name': 'Group'},
			u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
			'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
		},
		u'auth.permission': {
			'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
			'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
			'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
			u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
		},
		u'auth.user': {
			'Meta': {'object_name': 'User'},
			'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
			'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
			'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
			'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
			u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
			'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
			'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
			'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
			'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
			'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
			'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
			'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
		},
		u'browser.attribute': {
			'Meta': {'object_name': 'Attribute'},
			'attribute': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
			u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
		},
		u'browser.reservation': {
			'Meta': {'object_name': 'Reservation'},
			'booking_date': ('django.db.models.fields.DateField', [], {}),
			'from_hour': ('django.db.models.fields.TimeField', [], {}),
			u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'room': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['browser.Room']"}),
			'to': ('django.db.models.fields.TimeField', [], {}),
			'user_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
		},
		u'browser.room': {
			'Meta': {'object_name': 'Room'},
			'attribute': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['browser.Attribute']", 'symmetrical': 'False'}),
			'capacity': ('django.db.models.fields.IntegerField', [], {'default': '20'}),
			'description': ('django.db.models.fields.CharField', [], {'max_length': '120', 'blank': 'True'}),
			u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'name': ('django.db.models.fields.CharField', [], {'max_length': '25'})
		},
		u'browser.term': {
			'Meta': {'object_name': 'Term'},
			'booking_date': ('django.db.models.fields.DateField', [], {}),
			'from_hour': ('django.db.models.fields.TimeField', [], {}),
			u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'room': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['browser.Room']"}),
			'to': ('django.db.models.fields.TimeField', [], {})
		},
		u'browser.userprofile': {
			'Meta': {'object_name': 'UserProfile'},
			u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
			'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
		},
		u'contenttypes.contenttype': {
			'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
			'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
			u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
			'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
		}
	}

	complete_apps = ['browser']
	symmetrical = True
