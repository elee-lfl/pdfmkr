from django.db import models
from django.contrib.auth.models import User
from adminsortable.models import Sortable, SortableForeignKey


class Sow(Sortable):
	class Meta:
		pass
	project = models.CharField(max_length=255)
	client = models.CharField(max_length=255)
	pub_date = models.DateTimeField('date published')
	author = models.ForeignKey(User)
	
	def __unicode__(self):
		return self.project

class Content(Sortable):
	class Meta(Sortable.Meta):
		pass
	sow = models.ForeignKey(Sow)
	sectiontitle = models.CharField(max_length=255)
	sectioncontent = models.TextField()		
		
	def __unicode__(self):
		return self.sectiontitle



