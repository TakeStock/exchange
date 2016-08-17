from Emailer import *

class Client(object):

	def run(self):
		#Load password from local file
		f = open('data.xtxt', 'r');
		lines = f.read().split('\n');
		for line in lines:
			for char in '\r\n':
				line.translate(None, char)
	
		emailer = Emailer()
		emailer.setup(lines[0], lines[1]) 
		emailer.send_command('buy', 'RVT 10') 

c = Client();
c.run();
