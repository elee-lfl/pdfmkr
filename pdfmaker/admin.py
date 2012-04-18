from pdfmaker.models import Sow, Content
from django.contrib import admin
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import makepdf

class ContentInline(admin.TabularInline):
	model = Content
	extra = 3


class SowAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['author']}),
		(None, {'fields': ['project']}),
		(None, {'fields': ['client']}),
		('Date published', {'fields': ['pub_date']})
	]
	inlines = [ContentInline]
	actions = ['publish_pdf']
	def publish_pdf(self,request,queryset):
		for sow in queryset:
			sectionset = sow.content_set.all()
			makepdf.printpdf(sow,sectionset)
	publish_pdf.short_description = "Publish this as a .pdf"
	
class CommonMedia:
  js = (
    'https://ajax.googleapis.com/ajax/libs/dojo/1.6.0/dojo/dojo.xd.js',
    'http://some-antics.com/emma/appmedia/admin/js/editor.js',
  )
  css = {
    'all': ('http://some-antics.com/emma/appmedia/admin/css/editor.css',),
  }	
	
admin.site.register(Sow, SowAdmin, Media=CommonMedia)