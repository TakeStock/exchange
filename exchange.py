import sys;
from logging import Logger;

class Exchange(object):
	logger = Logger('Exchange');

	def main(s):
		s.logger.Info('Welcome to the Take Stock Exchange :)');

		args = sys.argv;
		command = args[1];

		option = {
			'test' : s.test, 
			'host' : s.host,
		}[command];

		option(args);

	def test(s, args):
		s.logger.Info('test');

	def host(s, args):
		s.logger.Info('Hosting exchange...');
		
		while(True):
			processEmails();

	def processEmails(s):
		s.logger.Info("Processing emails");		
		# check if any emails are in the queue

	
		
		
e = Exchange();
e.main();
