#requires creation of SQL database "TAKESTOCKDB" with a root password of "3141592654"

def wallet_init():
    import MySQLdb
    db = MySQLdb.connect("localhost","root","3141592654","TAKESTOCKDB")
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")
    sql = """CREATE TABLE WALLET (
    USER CHAR(40) NOT NULL,
    AFFILIATION CHAR(20),
    RESETS INT,
    CREDITS FLOAT,
    TESTSHARE INT )"""
    cursor.execute(sql)
    sql = """INSERT INTO EMPLOYEE(USER, AFFILIATION, RESETS, CREDITS, TESTSHARE)
    VALUES ('cdw202@gmail.com', 'dkgfluids', 0, 1000, 1)"""
    cursor.execute(sql)
    db.commit()
    return

def user_add(email):
    import MySQLdb
    db = MySQLdb.connect("localhost","root","3141592654","TAKESTOCKDB")
    cursor = db.cursor()
    sql = """INSERT INTO EMPLOYEE(USER, AFFILIATION, RESETS, CREDITS, TESTSHARE)
    VALUES ('%s', 'default', 0, 1000, 1)""" % (email)
    cursor.execute(sql)
    db.commit()
    return

def db_query()
    import MySQLdb
    db = MySQLdb.connect("localhost","root","3141592654","TAKESTOCKDB")
    cursor = db.cursor()
    results = cursor.fetchall()
    return results

def user_reset(email):
    import MySQLdb
    db = MySQLdb.connect("localhost","christian","3141592654","TAKESTOCKDB")
    cursor = db.cursor()
    cursor.execute("UPDATE WALLET SET RESETS = RESETS + 1 WHERE USER = '%s'" % (email))
    db.commit()
    return

def share_add(shareID):
    import MySQLdb
    db = MySQLdb.connect("localhost","root","3141592654","TAKESTOCKDB")
    cursor = db.cursor()
    cursor.execute("DECLARE CONTINUE handler FOR 1060 BEGIN END")
    cursor.execute("ALTER TABLE WALLET ADD '%s' INT NOT NULL DEFAULT 0" % (shareID))
    db.commit()
    return
