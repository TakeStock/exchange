# TakeStock

## Welcome :)

Hello and welcome to TakeStock. TakeStock is a stock market simulator, which allows you to have a go at buying and selling, without the risk of losing any real money. It works via an email api, whereby to perform tasks you simply send an email to TakeStockCMD@gmail.com following a specfic format. 

The aim of TakeStock is not fully focused around manually firing off emails after an intensive trawl of the stock data out there, but rather, providing a framework that allows users to script up a client which will trade for them. What algorithm the client uses, is down to you

## Getting Started

As mentioned, if all you want to do is manually buy and sell, the only thing you need is an email account. There is no official "registration" process, the first time you send an email, the server will set you up an account. This account holds no personal information, it is purely a track of the shares you have bought/sold and the email in which to recieve commands/send results.

If you want to take this a step further and script up your approach, included in the repo is client\_template.py

## User Commands

### buy
Allows a broker to buy sum sharze.

```
<ticker> <amount>
 e.g.

RVT 10
BAB.L 1000
```

### sell



```
<ticker> <amount>
 e.g.

RVT 10
BAB.L 1000
```
### reset

## Admin Commands

### init

### kill

## Future Features

As ever, there is always a list of features yet to be implemented. Here they are, and if you have any suggestions, send an email to takestockcmd@gmail.com with the subject 'reset'. ;)

- Time as a column in the server logs.
- New commands.
	- sell/buy all.
	- current wallet value.
- newsletter daily/weekly.
	- biggest grower.
	- best value stock.
	- best portfolio.
- Refuse -ve buys or +ve sell.
- Transaction fee, at a fixed cost of £2.95 per buy/sell.
