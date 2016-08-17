#requires creation of SQL database "TAKESTOCKDB" with a root password of "3141592654"

def wallet_init():
    #ready to use
    import MySQLdb
    db = MySQLdb.connect("localhost","root","3141592654","TAKESTOCKDB")
    cursor = db.cursor()
    #Clear tables
    cursor.execute("DROP TABLE IF EXISTS WALLET")
    cursor.execute("DROP TABLE IF EXISTS LOG")
    #Recreate tables
    #Wallet
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
    return

def user_add(email):
    #ready to use
    import MySQLdb
    db = MySQLdb.connect("localhost","root","3141592654","TAKESTOCKDB")
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
    return

def user_query(email):
    #ready to use
    import MySQLdb
    db = MySQLdb.connect("localhost","root","3141592654","TAKESTOCKDB")
    cursor = db.cursor()
    sql = """SELECT * FROM WALLET WHERE USER = '%s'""" % (email)
    cursor.execute(sql)
    results = cursor.fetchall()
    results = results[0]
    db.close()
    return results

def user_reset(user):
    #ready to use
    import MySQLdb
    db = MySQLdb.connect("localhost","root","3141592654","TAKESTOCKDB")
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
    print 'success' #add email response
    return

def share_query():
    #ready for use
    import MySQLdb
    db = MySQLdb.connect("localhost","root","3141592654","TAKESTOCKDB")
    cursor = db.cursor()
    cursor.execute("""SHOW COLUMNS FROM WALLET""")
    columns = cursor.fetchall()
    results = []
    for i in range(4,len(columns)):
        results.append(columns[i][0])
    db.close()
    return results

def share_defeature(shareID):
    #ready to use
    for char in '@.-':
        shareID = shareID.translate(None,char)
    return shareID

def share_add(shareID):
    #ready to use
    import MySQLdb
    db = MySQLdb.connect("localhost","root","3141592654","TAKESTOCKDB")
    cursor = db.cursor()
    #cursor.execute("DECLARE CONTINUE handler FOR 1064 BEGIN END")
    sql = """ALTER TABLE WALLET ADD %s INT NOT NULL DEFAULT 0""" % (share_defeature(shareID))
    cursor.execute(sql)
    db.commit()
    #log entry
    sql = """INSERT INTO LOG(USER, COMMAND, COMPANY, NSHARES, PRICE, STATUS)
    VALUES ('admin', 'add_share', '%s', 0, 0, 'success')""" % (shareID)
    cursor.execute(sql)
    db.commit()
    db.close()
    return

def share_sell(user, shareID, nsell):
    #ready to use
    import MySQLdb
    db = MySQLdb.connect("localhost","root","3141592654","TAKESTOCKDB")
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
        print 'success' #add email success
    else:
        status = 'fail'
        sql = """INSERT INTO LOG(USER, COMMAND, COMPANY, NSHARES, PRICE, STATUS)
        VALUES ('%s', 'sell', '%s', %d, %f, '%s')""" % (user,shareID,nsell,price,status)
        cursor.execute(sql)
        db.commit()
        db.close()
        print 'error' #add email fail
    return

def share_buy(user, shareID, nbuy):
    #mostly ready - missing email response
    import MySQLdb
    db = MySQLdb.connect("localhost","root","3141592654","TAKESTOCKDB")
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
        print 'success' #change to email response
    else:
        status = 'fail'
        sql = """INSERT INTO LOG(USER, COMMAND, COMPANY, NSHARES, PRICE, STATUS)
        VALUES ('%s', 'buy', '%s', %d, %f, '%s')""" % (user,shareID,nbuy,price,status)
        cursor.execute(sql)
        db.commit()
        db.close()
        print 'error' #change to email response
    return

def share_price(ticker):
    from yahoo_finance import Share
    company = Share(ticker)
    price = float(company.get_price())
    return price
        
wallet_init()
user_add('cdw202@gmail.com')
share_add('BAB.L')
user_add('c.wood@fnc.co.uk')
share_add('YHOO')
share_buy('cdw202@gmail.com','BAB.L',2)
share_buy('cdw202@gmail.com','YHOO',2)
share_sell('cdw202@gmail.com','BAB.L',1)
user_reset('c.wood@fnc.co.uk')
