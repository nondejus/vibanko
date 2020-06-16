import jsonrpc
import psycopg2
import time
import socket

rpc_username = "user"
rpc_password = "password"

db = psycopg2.connect(database="bitwallet",user="bitwallet",password="903ur092isodj")

bitcoin = jsonrpc.ServiceProxy("http://"+rpc_username+":"+rpc_password+"@127.0.0.1:8332/")

while True:
    try:
        c = db.cursor()
        c.execute("""
        SELECT COUNT(bitcoin_address)
        FROM bitcoin_addresses
        WHERE user_id IS NULL
        """)
        
        result = c.fetchone()
        
        if result:
            count = result[0]
            
            if count < 1000:
                for x in xrange(1000-count):
                    c.execute("""
                    INSERT INTO bitcoin_addresses(bitcoin_address)
                    VALUES(%s)""",(bitcoin.getnewaddress(),))
                    
                    if x % 100 == 0 or x < 10:
                        db.commit()
                
                db.commit()
            else:
                db.rollback()
        c.close()
    except jsonrpc.authproxy.JSONRPCException, e:
        print e.error
    except socket.timeout, e:
        print e.strerror
    except socket.error, e:
        print e.strerror
    except Exception, e:
        print e.message
    time.sleep(1)
