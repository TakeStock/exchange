#takestock functions
#CDW(cdw202@gmail.com) and TJD2
#last modified 24/2/2016

#module installation
#from run directory
#step1: git clone git://github.com/lukaszbanasiak/yahoo-finance.git
#step2: cd yahoo-finance
#step3: python setup.py install

from yahoo_finance import Share

def trade(ticker, nshares):
    company = Share(ticker)
    price = nshares * float(company.get_price())
    return price

def query_price(ticker):
    company = Share(ticker)
    price = float(company.get_price())
    return price

def query_open(ticker):
    company = Share(ticker)
    price = float(company.get_open())
    return price

def query_change(ticker):
    company = Share(ticker)
    price = float(company.get_open())
    return price

def query_trade_time(ticker):
    company = Share(ticker)
    price = float(company.get_trade_datetime())
    return price

#test = 'MPI.L'
print trade('YHOO',1)
#print query_trade_time(test)


#For stock market trading hours
#http://www.worldtimezone.com/markets24.php

#Other query types    
#get_price()
#get_change()
#get_volume()
#get_prev_close()
#get_open()
#get_avg_daily_volume()
#get_stock_exchange()
#get_market_cap()
#get_book_value()
#get_ebitda()
#get_dividend_share()
#get_dividend_yield()
#get_earnings_share()
#get_days_high()
#get_days_low()
#get_year_high()
#get_year_low()
#get_50day_moving_avg()
#get_200day_moving_avg()
#get_price_earnings_ratio()
#get_price_earnings_growth_ratio()
#get_price_sales()
#get_price_book()
#get_short_ratio()
#get_trade_datetime()
#get_historical(start_date, end_date)
#get_info()
#refresh()
