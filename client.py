import poplib;
import email.parser;
import string;
import smtplib;
import sys;
from email.mime.text import MIMEText

class Client(object):
	def connect(user, password):
		mailbox = poplib.POP3_SSL('pop.googlemail.com');
		mailbox.user(user);
		mailbox.pass_(password);
		print('Successfully connected');
		return mailbox;
	
	def readEmail():
		mailbox = connect();
	
		(response, rawLines, bytes) = mailbox.retr(4);
		rawString = '\n'.join(str(s)[2:-1] for s in rawLines);
		mail = email.message_from_string(rawString);
	
		parts = mail.get_payload()[0]
	
		for part in mail.walk():
			if part.get_content_type() == 'text/plain':
				body = part.get_payload();
	
		return [mail['from'], mail['subject'], body];
	
	def sendEmail(to, subject, body):
		email = MIMEText(body);
		email['subject'] = subject;
		email['from'] = exchangeEmail;
		email['to'] = to;
	
		smtp = smtplib.SMTP('smtp.gmail.com');
		smtp.starttls();
		smtp.login(exchangeEmail, exchangePass);
		smtp.sendmail(exchangeEmail, to, email.as_string());
		smtp.quit();
	
	def main():
		sendEmail('thomasjackdalby@gmail.com', 'testy', 'testuth this email');
	
		email = readEmail();
		print('from: ' + email[0]);
		print('subject: ' + email[1]);
		print('body: ' + email[2]);
