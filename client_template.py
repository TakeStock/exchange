import sys
import Emailer
import random
from yahoo_finance import Share

class Client(object):

    def setup(self):
        #Load password from local file
        f = open('data.xtxt', 'r');
        lines = f.read().split('\n');
        for line in lines:
            for char in '\r\n':
                line.translate(None, char)

        self.emailer = Emailer.Emailer()
        self.emailer.setup(lines[0], lines[1])

    def run(self):

        #print self.check_price('BAB.L');

        self.buy('RVT', 0)
        #self.buy('NIOBF', 200)
        #self.buy('RVT', 200)
        #self.buy('HOG', 'max')

    def buy(self, ticker, amount):
        self.emailer.send_command('buy', '%s %s' % (ticker, amount));

    def sell(self, ticker, amount):
        self.emailer.send_command('sell', '%s %s' % (ticker, amount));

    def check_price(self, ticker):
        try:
            company = Share(ticker)
            return float(company.get_price())
        except:
            print 'Failed to check price'
            print sys.exc_info()[0];
            return 0

c = Client();
c.setup();
c.run();
