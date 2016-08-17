#Takestock stock market trading simulator cdw202
#Requires MySQLdb
# 1. Install MySQL using apt-get
# 2. Create SQL database "TAKESTOCKDB"
#Requires yahoo_finance
#Open terminal in run directory
# 1. git clone git://github.com/lukaszbanasiak/yahoo-finance.git
# 2. cd yahoo-finance
# 3. python setup.py install

#Login details
#SQL database
global u
u=""
global p
p=""
#Gmail account
global mu
mu=''
global mp
mp=''
#Admin user email addresses
suemail1=''
suemail2=''

def wallet_init():
    #ready to use
    import MySQLdb
    print 'initialising wallet'
    try:
        db = MySQLdb.connect("localhost",u,p,"TAKESTOCKDB")
        print 'connected to DB'
    except error:
        print 'TAKESTOCKDB not present'
    cursor = db.cursor()
    #Clear tables
    print 'clearing tables'
    cursor.execute("DROP TABLE IF EXISTS WALLET")
    cursor.execute("DROP TABLE IF EXISTS LOG")
    #Recreate tables
    #Wallet
    print 'creating new tables'
    sql = """CREATE TABLE WALLET (
    USER CHAR(40) NOT NULL,
    AFFILIATION CHAR(20),
    RESETS INT,
    CREDITS FLOAT )"""
    cursor.execute(sql)
    db.commit()
    #Log
    sql = """CREATE TABLE LOG (
    ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    USER CHAR(40) NOT NULL,
    COMMAND CHAR(20),
    COMPANY CHAR(20),
    NSHARES INT,
    PRICE FLOAT,
    STATUS CHAR(10) )"""
    cursor.execute(sql)
    db.commit()
    db.close()
    print 'initialisation complete'
    return

def user_add(email):
    #ready to use
    try:
        import MySQLdb
        db = MySQLdb.connect("localhost",u,p,"TAKESTOCKDB")
        cursor = db.cursor()
        sql = """INSERT INTO WALLET(USER, AFFILIATION, RESETS, CREDITS)
        VALUES ('%s', 'default', 0, 1000000)""" % (email)
        cursor.execute(sql)
        db.commit()
        #log entry
        sql = """INSERT INTO LOG(USER, COMMAND, COMPANY, NSHARES, PRICE, STATUS)
        VALUES ('%s', 'user_add', 'null', 0, 0, 'success')""" % (email)
        cursor.execute(sql)
        db.commit()
        db.close()
        print 'success' #add email response
        send_email(email,'new takestock user','Welcome\n\nTakestock uses your' +
                   ' email address as your identity, the email subject' +
                   ' for a command and any other details such as share ticker' +
                   ' and Nshares in the body. You start with 1,000,000 credits' +
                   ' which have the same value as GB pence. \nThe available commands are' +
                   ' "buy", "sell" and "reset". \nThe following command' +
                   ' will buy and sell commands will trade ten Babcock shares e.g.\n' +
                   ' Subject: buy Body: BAB.L 10 \nSubject: sell Body: BAB.L 10 \n\n' +
                   ' "reset" command needs no email body, the query' +
                   ' command returns user information and reset allows the user to ' +
                   ' start again.')
    except error:
        print 'fail' #add email response
    return

def user_reset(user):
    #ready to use
    import MySQLdb
    db = MySQLdb.connect("localhost",u,p,"TAKESTOCKDB")
    cursor = db.cursor()
    #get number of resets before
    sql = """SELECT RESETS FROM WALLET WHERE USER = '%s'""" % (user)
    cursor.execute(sql)
    resets = cursor.fetchone()
    resets = resets[0]+1
    #get affiliation
    sql = """SELECT AFFILIATION FROM WALLET WHERE USER = '%s'""" % (user)
    cursor.execute(sql)
    affiliation = cursor.fetchone()
    affiliation = affiliation[0]
    #delete row
    sql = """DELETE FROM WALLET WHERE USER LIKE '%s'""" % (user)
    cursor.execute(sql)
    db.commit()
    #re-add user, affiliation and reset +1
    sql = """INSERT INTO WALLET(USER, AFFILIATION, RESETS, CREDITS)
    VALUES ('%s', '%s', %d, 1000000)""" % (user,affiliation,resets)
    cursor.execute(sql)
    db.commit()
    #log entry
    sql = """INSERT INTO LOG(USER, COMMAND, COMPANY, NSHARES, PRICE, STATUS)
    VALUES ('%s', 'user_reset', 'null', 0, 0, 'success')""" % (user)
    cursor.execute(sql)
    db.commit()
    db.close()
    print 'user added'
    return

def query(email):
    #get shareID list
    import MySQLdb
    import numpy as np
    db = MySQLdb.connect("localhost",u,p,"TAKESTOCKDB")
    cursor = db.cursor()
    sql="""SELECT COMPANY FROM LOG"""
    cursor.execute(sql)
    tickerdata = cursor.fetchall()
    tickers = []
    for i in range(0,len(tickerdata)):
        tickers.append(tickerdata[i][0])
    tickers = np.unique(tickers).tolist()
    tickers.remove('null')
    #user credits
    cursor = db.cursor()
    sql = """SELECT CREDITS FROM WALLET WHERE USER = '%s'""" % (email)
    cursor.execute(sql)
    ncredits = cursor.fetchall()[0][0]
    body=str(ncredits)+' credits remaining\n\n'
    total=0
    #get email body data
    for ticker in tickers:
        #get nshares
        cursor = db.cursor()
        sql = """SELECT %s FROM WALLET WHERE USER = '%s'""" % (share_defeature(ticker),email)
        cursor.execute(sql)
        nshare = cursor.fetchall()[0][0]
        #get share price
        price = share_price(ticker)
        #add lines with non-zero value
        value = nshare*price
        total=total+value
        if value >0:
            body = body+str(nshare)+' x '+ticker+' @('+str(price)+') = '+str(value)+'\n'
    #add total
    body = body+'\nSub-total of shares = '+str(total)+'\n\nTotal value = '+str(total+ncredits)
    db.close()     
    return body

def share_defeature(shareID):
    #ready to use
    for char in '@.-':
        shareID = shareID.translate(None,char)
    return shareID

def share_add(shareID):
    #ready to use
    import MySQLdb
    db = MySQLdb.connect("localhost",u,p,"TAKESTOCKDB")
    cursor = db.cursor()
    sql = """ALTER TABLE WALLET ADD %s INT NOT NULL DEFAULT 0""" % (share_defeature(shareID))
    cursor.execute(sql)
    db.commit()
    #log entry
    sql = """INSERT INTO LOG(USER, COMMAND, COMPANY, NSHARES, PRICE, STATUS)
    VALUES ('admin', 'add_share', '%s', 0, 0, 'success')""" % (shareID)
    cursor.execute(sql)
    db.commit()
    db.close()
    print shareID+' shareID added'
    return

def share_sell(user, shareID, nsell):
    #ready to use
    try:
        import MySQLdb
        db = MySQLdb.connect("localhost",u,p,"TAKESTOCKDB")
        cursor = db.cursor()
        #get wallet data
        sql = """SELECT %s FROM WALLET WHERE USER = '%s'""" % (share_defeature(shareID),user)
        cursor.execute(sql)
        shares1 = cursor.fetchone()
        shares1=shares1[0]
        sql = """SELECT CREDITS FROM WALLET WHERE USER = '%s'""" %(user)
        cursor.execute(sql)
        credits1 = cursor.fetchone()
        credits1 = credits1[0]
        #get share price
        price = share_price(shareID)
        #valid trade request
        if nsell<=shares1:
            status = 'success'
            credits2 = credits1 + (nsell*price)
            shares2 = shares1 - nsell
            sql = """UPDATE WALLET SET CREDITS=%f, %s=%d WHERE USER = '%s'""" % (credits2,share_defeature(shareID),shares2,user)
            cursor.execute(sql)
            db.commit()
            sql = """INSERT INTO LOG(USER, COMMAND, COMPANY, NSHARES, PRICE, STATUS)
            VALUES ('%s', 'sell', '%s', %d, %f, '%s')""" % (user,shareID,nsell,price,status)
            cursor.execute(sql)
            db.commit()
            db.close()
            subj='Sell success: '+str(nsell)+' '+shareID+' shares'
            body=query(user)
            send_email(user,subj,body)
        else:
            status = 'fail'
            sql = """INSERT INTO LOG(USER, COMMAND, COMPANY, NSHARES, PRICE, STATUS)
            VALUES ('%s', 'sell', '%s', %d, %f, '%s')""" % (user,shareID,nsell,price,status)
            cursor.execute(sql)
            db.commit()
            db.close()
            subj='Sell fail: '+str(nsell)+' '+shareID+' shares'
            body=query(user)
            send_email(user,subj,body)
    except:
        print 'SQL database error'
        send_email(suemail1,'sql problem','from a sell command')
    return

def share_buy(user, shareID, nbuy):
    #check shareID exists
    try:
        try:
            from yahoo_finance import Share
            company = Share(shareID)
            price = float(company.get_price())
        except:
            price=0
        #if share price exists and non-zero then proceed
        if price>0:
            import MySQLdb
            db = MySQLdb.connect("localhost",u,p,"TAKESTOCKDB")
            #get wallet data, add shareID if required
            try:
                cursor = db.cursor()
                sql = """SELECT %s FROM WALLET WHERE USER = '%s'""" % (share_defeature(shareID),user)
                cursor.execute(sql)        
            except:
                db.commit()
                db.close()
                share_add(shareID)
                share_buy(user,shareID,nbuy)
                return
            shares1 = cursor.fetchone()
            shares1 = shares1[0]
            sql = """SELECT CREDITS FROM WALLET WHERE USER = '%s'""" %(user)
            cursor.execute(sql)
            credits1 = cursor.fetchone()
            credits1 = credits1[0]
            #get share price
            price = share_price(shareID)
            #valid trade request
            if nbuy*price<=credits1:
                status = 'success'
                credits2 = credits1 - (nbuy*price)
                shares2 = shares1 + nbuy
                sql = """UPDATE WALLET SET CREDITS=%f, %s=%d WHERE USER = '%s'""" % (credits2,share_defeature(shareID),shares2,user)
                cursor.execute(sql)
                db.commit()
                sql = """INSERT INTO LOG(USER, COMMAND, COMPANY, NSHARES, PRICE, STATUS)
                VALUES ('%s', 'buy', '%s', %d, %f, '%s')""" % (user,shareID,nbuy,price,status)
                cursor.execute(sql)
                db.commit()
                db.close()                
                subj='Purchase success: '+str(nbuy)+' '+shareID+' shares'
                body=query(user)
                send_email(user,subj,body)
            else:
                status = 'fail'
                sql = """INSERT INTO LOG(USER, COMMAND, COMPANY, NSHARES, PRICE, STATUS)
                VALUES ('%s', 'buy', '%s', %d, %f, '%s')""" % (user,shareID,nbuy,price,status)
                cursor.execute(sql)
                db.commit()
                db.close()
                subj='Purchase fail: '+str(nbuy)+' '+shareID+' shares'
                body=query(user)
                send_email(user,subj,body)
        else:
            print 'shareID error'
            send_email(suemail1,'sql problem','from a buy command')
    except:
        user_add(user)
        share_buy(user, shareID, nbuy)
    return

def share_price(ticker):
    from yahoo_finance import Share
    company = Share(ticker)
    price = float(company.get_price())
    return price

def read_emails():
    import imaplib
    import email
    M=imaplib.IMAP4_SSL('imap.gmail.com')
    M.login(mu,mp)
    rv,data=M.select(mailbox="INBOX", readonly=False)
    rv,data=M.search(None, "ALL")
    if rv != 'OK':
        print "No messages found!"
        return
    cmd=[]
    counter=0
    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print "ERROR getting message", num
            return
        msg = email.message_from_string(data[0][1])
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                body = part.get_payload(None, True)
        a = msg['from'][msg['from'].find('<')+1:msg['from'].find('>')]
        b = msg['Subject'].lower()
        c = body[:body.find('\r')]
        if b in ('buy', 'sell', 'reset', 'kill','init'):
            cmd.append(a+' '+b+' '+c)
            move=M.store(num,'+X-GM-LABELS','(log)')
            if move[0]=='OK':
                temp1,temp2=M.store(num,'+FLAGS','\\Deleted')
        else:
            temp1,temp2=M.store(num,'+FLAGS','\\Deleted')
    M.close()
    M.logout()
    return cmd

def send_email(to,subject,body):
    import smtplib
    from email.mime.text import MIMEText
    #construct message
    msg=MIMEText(body)
    msg['Subject']=subject
    msg['From']=mu
    msg['To']=to
    #connect to gmail
    s=smtplib.SMTP('smtp.gmail.com')
    s.starttls()
    s.login(mu,mp)
    #send message
    s.sendmail(mu,to,msg.as_string())
    s.quit()
    return

import time
flag1=0
while True:
    try:
        if flag1==1:
            try:
                send_email(suemail1,'connection error','interrupted internet connetion')
                flag1=0
            except:
                flag1=1
        print 'checking emails'
        cmds=read_emails()
        for i in cmds:
            cmd=i.split()
            print cmd
            if cmd[1]=='buy':
                share_buy(cmd[0],cmd[2],int(cmd[3]))
            elif cmd[1]=='sell':
                share_sell(cmd[0],cmd[2],int(cmd[3]))
            elif cmd[1]=='reset':
                user_reset(cmd[0])
            elif cmd[1]=='init':
                if cmd[0]==suemail1 or cmd[0]==suemail2:
                    print 'wallet initialised'
                    wallet_init()
                else:
                    print 'initialisation abort'
            elif cmd[1]=='kill':
                if cmd[0]==suemail1 or cmd[0]==suemail2:
                    print 'loop killed'
                    break
                else:
                    print 'kill abort'
            else:
                print 'loop error 1'
                send_email(suemail1,'loop error','check while loop')
        time.sleep(10)
    except:
        print 'connection failed'
        time.sleep(20)
        flag1=1
        #send_email(suemail1,'loop error','check while loop')
        #break    


