import poplib;
import email.parser;
import string;

def readEmail():
	mailbox = poplib.POP3_SSL('pop.googlemail.com');
	mailbox.user('takeallthestock@gmail.com');
	mailbox.pass_('14142135');
	print('Successfully connected');

	(response, rawLines, bytes) = mailbox.retr(4);
	rawString = '\n'.join(str(s)[2:-1] for s in rawLines);
	mail = email.message_from_string(rawString);

	print("------------");
	print(mail['subject']);
	print(mail['from']);
	parts = mail.get_payload()[0]

	for part in mail.walk():
		if part.get_content_type() == 'text/plain':
			body = part.get_payload();

	print('body >');
	print(body);
readEmail();
