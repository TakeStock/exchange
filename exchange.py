import sys;
import logger;

class Exchange:
	logger = logger.Logger('Exchange');

	def main(self):
		self.logger.Info('Welcome to the Take Stock Exchange :)');

		args = sys.argv;
		command = args[1];

		option = {
			'test' : self.test, 
			'host' : self.host,
		}[command];

		option(args);

	def test(self, args):
		self.logger.Info('test');

	def host(self, args):
		self.logger.Info('Hosting exchange...');
		
		while(True):
			processEmails();

	def processEmails(self):
		
	
	




Exchange().main();
