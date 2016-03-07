class Logger:
	def __init__(self, _type):
		self.type = _type;
	
	def Info(self, message):
		print("[" + self.type + "] Info: " + message);

	def Error(self, message):
		print("[" + self.type + "] Error: " + message);

	def Debug(self, message):
		print("[" + self.type + "] Debug: " + message);
