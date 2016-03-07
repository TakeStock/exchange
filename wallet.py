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
    STATUS INT )"""
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
    VALUES ('%s', 'default', 0, 1000)""" % (email)
    cursor.execute(sql)
    db.commit()
    db.close()
    return

def user_query(email):
    #not ready
    import MySQLdb
    db = MySQLdb.connect("localhost","root","3141592654","TAKESTOCKDB")
    cursor = db.cursor()
    results = cursor.fetchall()
    db.close()
    return results

def user_reset(email):
    #not ready
    import MySQLdb
    db = MySQLdb.connect("localhost","root","3141592654","TAKESTOCKDB")
    cursor = db.cursor()
    cursor.execute("UPDATE WALLET SET RESETS = RESETS + 1 WHERE USER = %s" % (email))
    db.commit()
    db.close()
    return

def share_query():
    #not ready
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
    VALUES ('admin', 'add_share', '%s', 0, 0, 0)""" % (shareID)
    cursor.execute(sql)
    db.commit()
    db.close()
    return

def share_sell(user, shareID, nsell):
    #not ready
    import MySQLdb
    db = MySQLdb.connect("localhost","root","3141592654","TAKESTOCKDB")
    cursor = db.cursor()
    sql = "SELECT %s FROM WALLET \ WHERE USER = %s" % (shareID, user)
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        credit = row[3]
        nshares = row[4]

    db.commit()
    db.close()
    return

def share_buy(user, shareID, nbuy):
    #not ready
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
    price = 100
    #valid trade request
    if nbuy*price<=credits1:
        credits2 = credits1 - (nbuy*price)
        shares2 = shares1 + nbuy
        sql = """UPDATE WALLET SET CREDITS=%f, %s=%d WHERE USER = '%s'""" % (credits2,share_defeature(shareID),shares2,user)
        cursor.execute(sql)
        db.commit()
        db.close()
        #log and email success
    else:
        #log email fail
        db.close()
    return
        
wallet_init()
user_add('cdw202@gmail.com')
share_add('BAB.L')
user_add('c.wood@fnc.co.uk')
share_add('YHOO')
share_buy('cdw202@gmail.com','BAB.L',2)
