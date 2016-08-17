from Emailer import *
import random

class Client(object):

	def setup(self):
		#Load password from local file
		f = open('data.xtxt', 'r');
		lines = f.read().split('\n');
		for line in lines:
			for char in '\r\n':
				line.translate(None, char)
	
		self.emailer = Emailer()
		self.emailer.setup(lines[0], lines[1])
		
	def run(self):
		
		stocks = ['HOG', 'RVT']

		#self.emailer.send_command('buy', 'TNE.AX %s' % 14)

		i = 0
		while(i<10):
			amount = random.randint(-5, 5);
			self.emailer.send_command('buy', 'TNE.AX %s' % amount)
			i = i+1

c = Client();
c.setup();
c.run();
