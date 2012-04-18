from django.db import models
from django.contrib.auth.models import User



class UserProfile(models.Model):
	phone_number = models.CharField(max_length=255)
	user = models.ForeignKey(User, unique=True)
	def __unicode__(self):
		return self.username

class Sow(models.Model):
	project = models.CharField(max_length=255)
	client = models.CharField(max_length=255)
	pub_date = models.DateTimeField('date published')
	author = models.ForeignKey(User)

	def __unicode__(self):
		return self.project

class Content(models.Model):
	sow = models.ForeignKey(Sow)
	sectionID = models.IntegerField(editable=True)
	sectiontitle = models.CharField(max_length=255)
	sectioncontent = models.TextField()
	
	def __unicode__(self):
		return self.sectiontitle
		


