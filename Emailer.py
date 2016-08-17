import smtplib
from email.mime.text import MIMEText
import datetime

global server
server = 'takestockcmd@gmail.com'
global DEBUG
DEBUG = True

class Emailer(object):

	def send_email(self, to, subject, body):
		if (self.isSetup == False):
			print 'Need to setup first'
			return
	
		#construct message
		msg=MIMEText(body)
		msg['Subject']=subject
		msg['From']=self.username[0:-8]
		msg['To']=to
		
		#connect to gmail
		s=smtplib.SMTP('smtp.gmail.com')
		s.starttls()
		s.login(self.username, self.password)
			
		#send message
		s.sendmail(self.username,to,msg.as_string())
		s.quit()
		print 'Sent %s @ %s' % (subject + ':' + body, datetime.datetime.now())
	
	def send_command(self, command, details):
		self.send_email(server, command, details)
	
	def read_email(self):
		print 'something'
	
	def setup(self, new_username, new_password):
		self.username = new_username
		self.password = new_password
		self.isSetup = True
