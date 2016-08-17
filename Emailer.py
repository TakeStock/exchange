import sys;
from logging import Logger;
import poplib;
import email.parser;
import string;
import smtplib;
from email.mime.text import MIMEText
 
class Emailer(object):
	def __init__(s):
		logger = Logger('EmailServer'); 	

	def setup(s, username, password):
		s.username = username;
		s.password = password;

	def connect(s):
		mailbox = poplib.POP3_SSL('pop.googlemail.com');
		mailbox.user(s.username);
		mailbox.pass_(s.password);
		print('Successfully connected');
		return mailbox;
	
	def readEmail(s):
		mailbox = s.connect();
	
		(response, rawLines, bytes) = mailbox.retr(4);
		rawString = '\n'.join(str(l)[2:-1] for l in rawLines);
		mail = email.message_from_string(rawString);
	
		parts = mail.get_payload()[0]
	
		for part in mail.walk():
			if part.get_content_type() == 'text/plain':
				body = part.get_payload();
	
		return [mail['from'], mail['subject'], body];
	
	def sendEmail(s, to, subject, body):
		email = MIMEText(body);
		email['subject'] = subject;
		email['from'] = exchangeEmail;
		email['to'] = to;
	
		smtp = smtplib.SMTP('smtp.gmail.com');
		smtp.starttls();
		smtp.login(exchangeEmail, exchangePass);
		smtp.sendmail(exchangeEmail, to, email.as_string());
		smtp.quit();

args = sys.argv;
e = Emailer();
e.setup(args[0], args[1]);
e.connect();