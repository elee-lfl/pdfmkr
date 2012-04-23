import re

from xhtml2pdf import pisa, context, document
from xhtml2pdf.context import pisaContext
from xhtml2pdf.parser import pisaParser

from reportlab.pdfgen import canvas, textobject, pathobject
from reportlab.lib.pagesizes import letter


import reportlab.rl_config
reportlab.rl_config.warnOnMissingFontGlyphs = 0
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from reportlab.lib.colors import grey, CMYKColor, PCMYKColor
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Frame, FrameBreak, PageTemplate, BaseDocTemplate, NextPageTemplate, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.rl_config import defaultPageSize
PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]
styles = getSampleStyleSheet()

# define greys as cmyk=60%
linegrey = CMYKColor(0,0,0,0.3)
numgrey = CMYKColor(0,0,0,0.6)

# sets path for registerFont to find fonts in right place 
reportlab.rl_config.TTFSearchPath.append("/Users/etc/reportlab-2.5/src/reportlab/fonts")

# building fonts
pdfmetrics.registerFont(TTFont('Akkurat-Reg','Akkurat_Reg.ttf'))
pdfmetrics.registerFont(TTFont('Akkurat-Light','Akkurat_Light.ttf'))
pdfmetrics.registerFont(TTFont('Gridnik','Gridnik.ttf'))

# margin and padding definitions
sectionLeft = 0 
sectionRight = 24
sectionTop = 39
sectionBottom = 36

mainTextMargin = 190

# frames
frameLaterPagesSide = Frame(x1=0,y1=0,width=mainTextMargin,height=792,topPadding=39.4,bottomPadding=36,rightPadding=0)
frameLaterPagesMain = Frame(x1=mainTextMargin,y1=0,width=612-mainTextMargin,height=792,topPadding=39.4,bottomPadding=36,rightPadding=24)
frameFirstPageSide = Frame(x1=0,y1=0,width=mainTextMargin,height=792,topPadding=0,leftPadding=0)
frameFirstPageMain = Frame(x1=mainTextMargin,y1=0,width=612-mainTextMargin,height=792,topPadding=218,leftPadding=0)

def lfleft(canvas):
	textobject = canvas.beginText()
	textobject.setTextOrigin(51.2,749)
	textobject.setFont('Gridnik',25)
	textobject.textLines('''
	LEFT 
	FIELD 
	LABS
	''')
	canvas.drawText(textobject)
	
def contactleftFirstPage(canvas):
	textobject = canvas.beginText()
	textobject.setTextOrigin(51.2,57)
	textobject.setFont('Akkurat-Light',9)
	textobject.textLines('''
	510 Victoria Ave
	Venice CA 90291
	www.leftfieldlabs.com
	''')
	canvas.drawText(textobject)

def contactleftLaterPages(canvas):
	textobject = canvas.beginText()
	textobject.setTextOrigin(51.2,57)
	textobject.setFont('Akkurat-Light',9)
	textobject.textLines('''
	510 Victoria Ave
	Venice CA 90291
	www.leftfieldlabs.com
	''')
	canvas.drawText(textobject)
	
def firstPage(canvas, doc):
	canvas.saveState()
	canvas.drawImage('http://some-antics.com/emma/appmedia/side.jpg',0,0,width=mainTextMargin-12,height=792)
	lfleft(canvas)
	contactleftFirstPage(canvas)
	canvas.restoreState()

def laterPages(canvas, doc):
	canvas.saveState()
	canvas.drawImage('http://some-antics.com/emma/appmedia/side.jpg',0,0,width=mainTextMargin-12,height=792)
	contactleftLaterPages(canvas)
	canvas.restoreState()

	
# hacked tabbing
def tab(left,right,tabamt):
	data = [['{}'.format(left),'{}'.format(right)]]
	t = Table(data)
	t.hAlign = 'LEFT'
	t.setStyle(TableStyle([('LEFTPADDING',(0,0),(1,0),0)]))
	t.setStyle(TableStyle([('TOPPADDING',(0,0),(1,0),0)]))
	t.setStyle(TableStyle([('BOTTOMPADDING',(0,0),(1,0),0)]))
	t.setStyle(TableStyle([('ALIGN',(0,0),(1,0),'LEFT')]))
	t._argW[0]=tabamt
	return t
	
def projectInfo(sow,story):
	statementofwork = Paragraph("<para spaceAfter=20><font face='Akkurat-Reg' size=16>// STATEMENT OF WORK<br/></font></para>",styles['Normal'])
	project = tab('PROJECT:',sow.project,83)
	client = tab('CLIENT:',sow.client,83)
	date = tab('DATE:',prettyDateTime(sow.pub_date),83)
	author = tab('CONTACT:',sow.author,83)
	project.setStyle(TableStyle([('FACE',(0,0),(1,0),'Akkurat-Light'),
							('SIZE',(0,0),(1,0),10),
							('TEXTCOLOR',(0,0),(0,0),numgrey)]))
	client.setStyle(TableStyle([('FACE',(0,0),(1,0),'Akkurat-Light'),
							('SIZE',(0,0),(1,0),10),
							('TEXTCOLOR',(0,0),(0,0),numgrey)]))							
	date.setStyle(TableStyle([('FACE',(0,0),(1,0),'Akkurat-Light'),
							('SIZE',(0,0),(1,0),10),
							('TEXTCOLOR',(0,0),(0,0),numgrey)]))
	author.setStyle(TableStyle([('FACE',(0,0),(1,0),'Akkurat-Light'),
							('SIZE',(0,0),(1,0),10),
							('TEXTCOLOR',(0,0),(0,0),numgrey)]))
	story.append(statementofwork)
	story.append(project)
	story.append(client)
	story.append(date)
	story.append(author)
	
	
def buildIndex(sow,story):
	index = tab('//','INDEX',22)
	index.setStyle(TableStyle([('FACE',(0,0),(1,0),'Akkurat-Reg'),
							('SIZE',(0,0),(1,0),10),
							('TOPPADDING',(0,0),(1,0),20)]))
	sectionset = sow.content_set.all()
	story.append(index)
	for content in sectionset:
		sectionid = addZero(content.sectionID)
		sectiontitle = content.sectiontitle
		section_print = tab('{}'.format(sectionid),'{}'.format(sectiontitle),22)	
		section_print.setStyle(TableStyle([('FACE',(0,0),(1,0),'Akkurat-Light'),
								('SIZE',(0,0),(1,0),10),
								('TEXTCOLOR',(0,0),(0,0),numgrey)]))
		story.append(section_print)
	
def sectionHeaders(sectionid,sectiontitle):
	sectionhead = tab(sectionid,sectiontitle.upper(),22)
	sectionhead.setStyle(TableStyle([('FACE',(0,0),(1,0),'Akkurat-Reg'),
							('SIZE',(0,0),(1,0),14),
							('TEXTCOLOR',(0,0),(0,0),numgrey),
							('LINEBELOW',(0,0),(1,0),1,linegrey),
							('BOTTOMPADDING',(0,0),(1,0),15),
							('RIGHTPADDING',(0,0),(0,0),0)]))
	sectionhead._argW[1] = 500
	return sectionhead

def sectionContent(Story,sectionset):
	Story.append(FrameBreak())
	for content in sectionset:
		sectionid = addZero(content.sectionID)
		sectiontitle = content.sectiontitle
		sectioncontent = content.sectioncontent
		Story.append(sectionHeaders(sectionid,sectiontitle))
		#Story.append(Paragraph("<para spaceAfter=40 spaceBefore=10><font face='Akkurat-Light' size=9>{}</font></para>".format(sectioncontent), styles['Normal']))
		marginparse(sectioncontent,Story)
		
	
def prettyDateTime(datetime):
	month = datetime.strftime('%B')
	day = datetime.day
	year = datetime.year
	return "{} {}, {}".format(month, day, year)
	

def addZero(num):
	if num < 10:
		sectionid = '0'
		sectionid += str(num)
		return sectionid
	else:
		sectionid = num	
		return sectionid


def marginparse(html,story):
	st = html.replace("\n","")
	f = st.replace("<br>","<br/>")
	string = f.replace("&nbsp;","")
	match_obj=re.match('^.*<div style="margin-left: (.*?)px;">(.*?)</div>(.*?)',string)
	if match_obj:
		for m in re.finditer('(.*)\s*<div style="margin-left: (.*?)px;">\s*(.*?)\s*</div>(.*)',string):
			pretext = m.group(1)
			tabamt = m.group(2)
			text = m.group(3)
			moretext = m.group(4)
			pre = Paragraph("<para spaceAfter=0 spaceBefore=10><font face='Akkurat-Light' size=9>{}</font></para>".format(pretext),styles['Normal'])
			t = tab('',text,int(tabamt)/2)
			t.setStyle(TableStyle([('FACE',(0,0),(1,0),'Akkurat-Light'),
									('SIZE',(0,0),(1,0),9),
									('TOPPADDING',(0,0),(1,0),0),
									('BOTTOMPADDING',(0,0),(1,0),0)]))
			p = Paragraph("<para spaceAfter=0 spaceBefore=10><font face='Akkurat-Light' size=9>{}</font></para>".format(moretext),styles['Normal'])
			story.append(pre)
			story.append(t)
			story.append(p)
	else:
		story.append(Paragraph("<para spaceAfter=40 spaceBefore=10><font face='Akkurat-Light' size=9>{}</font></para>".format(string),styles['Normal']))


def printpdf(sow,sectionset):
	filename = "{}.pdf".format(sow.project)
	pageOne = PageTemplate(id='FirstPage',frames=[frameFirstPageSide,frameFirstPageMain],onPage=firstPage)
	mainPages = PageTemplate(id='Sections',frames=[frameLaterPagesSide,frameLaterPagesMain],onPage=laterPages)
	doc = BaseDocTemplate(filename.format(filename),pagesize=letter,pageTemplates=[pageOne,mainPages])
	Story = []
	c = canvas.Canvas(filename)
	style = styles['Normal']
	
	#firstpage client details and index
	Story.append(FrameBreak())
	projectInfo(sow,Story)
	buildIndex(sow,Story)	
	
	#rest of pages
	Story.append(NextPageTemplate('Sections'))
	Story.append(PageBreak())
		
	#main text content
	sectionContent(Story,sectionset)
	
	
	doc.build(Story)

	



