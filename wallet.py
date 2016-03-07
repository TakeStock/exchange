#requires creation of SQL database "TAKESTOCKDB" with a root password of "3141592654"

def wallet_init():
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
    CREDITS FLOAT,
    TESTSHARE INT )"""
    cursor.execute(sql)
    sql = """INSERT INTO WALLET(USER, AFFILIATION, RESETS, CREDITS, TESTSHARE)
    VALUES ('cdw202@gmail.com', 'dkgfluids', 0, 1000, 1)"""
    cursor.execute(sql)
    db.commit()
    #Log
    sql = """CREATE TABLE LOG (
    ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    USER CHAR(40) NOT NULL,
    COMMAND CHAR(20),
    COMPANY CHAR(20),
    NSHARES INT,
    STATUS INT )"""
    cursor.execute(sql)
    sql = """INSERT INTO LOG(USER, COMMAND, COMPANY, NSHARES, STATUS)
    VALUES ('cdw202@gmail.com', 'query', 'YHOO', 1, 0)"""
    cursor.execute(sql)
    db.commit()
    db.close()
    return

def user_add(email):
    import MySQLdb
    db = MySQLdb.connect("localhost","root","3141592654","TAKESTOCKDB")
    cursor = db.cursor()
    sql = """INSERT INTO WALLET(USER, AFFILIATION, RESETS, CREDITS, TESTSHARE)
    VALUES ('%s', 'default', 0, 1000, 1)""" % (email)
    cursor.execute(sql)
    db.commit()
    db.close()
    return

def user_query():
    import MySQLdb
    db = MySQLdb.connect("localhost","root","3141592654","TAKESTOCKDB")
    cursor = db.cursor()
    results = cursor.fetchall()
    db.close()
    return results

def user_reset(email):
    import MySQLdb
    db = MySQLdb.connect("localhost","root","3141592654","TAKESTOCKDB")
    cursor = db.cursor()
    cursor.execute("UPDATE WALLET SET RESETS = RESETS + 1 WHERE USER = %s" % (email))
    db.commit()
    db.close()
    return

def share_query():
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
    for char in '@.-':
        shareID = shareID.translate(None,char)
    return shareID

def share_add(shareID):
    import MySQLdb
    db = MySQLdb.connect("localhost","root","3141592654","TAKESTOCKDB")
    cursor = db.cursor()
    #cursor.execute("DECLARE CONTINUE handler FOR 1064 BEGIN END")
    sql = """ALTER TABLE WALLET ADD %s INT NOT NULL DEFAULT 0""" % (shareID)
    cursor.execute(sql)
    db.commit()
    db.close()
    return

def share_sell(user, command, shareID, nsell):
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
        
wallet_init()
user_add('test@test.com')
share_add('TEST2')

