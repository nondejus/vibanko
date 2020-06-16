import jsonrpc
import psycopg2
import time
import decimal
import socket

rpc_username = "user"
rpc_password = "password"

bitcoin = jsonrpc.ServiceProxy("http://"+rpc_username+":"+rpc_password+"@127.0.0.1:8332/")

while True:
    try:
        db = psycopg2.connect(database="bitwallet",user="bitwallet",password="903ur092isodj")
        
        transactions = bitcoin.listtransactions("*",1000)
        
        deposits = (t for t in transactions if t['category'] == 'receive' and t['confirmations'] > 4)
        
        for deposit in deposits:
            c = db.cursor()
            
            c.execute("""
            SELECT user_id
            FROM bitcoin_addresses
            WHERE bitcoin_address=%s
            """,(deposit['address'],))
            
            result = c.fetchone()
            
            if result:
                user_id = result[0]
                
                if user_id:
                    try:
                        amount = decimal.Decimal(deposit['amount'])/10**8
                        
                        c.execute("""
                        SELECT deposit_id
                        FROM deposits
                        WHERE bitcoin_address=%s
                        AND transaction_id=%s
                        """,(deposit['address'],deposit['txid']))
                        
                        result = c.fetchone()
                        
                        if result is None:
                            c.execute("""
                            INSERT INTO deposits(amount,bitcoin_address,transaction_id,user_id)
                            VALUES(%s,%s,%s,%s)
                            """,(amount,deposit['address'],deposit['txid'],user_id))
                            
                            c.execute("""
                            UPDATE users
                            SET balance = balance + %s
                            WHERE user_id=%s""",(amount,user_id))
                            
                            db.commit()
                    except psycopg2.IntegrityError:
                        db.rollback()
            c.close()
    except jsonrpc.authproxy.JSONRPCException, e:
        print e.error
    except socket.timeout, e:
        print e.strerror
    except socket.error, e:
        print e.strerror
    except psycopg2.Error, e:
        db.rollback()
    except Exception, e:
        print e.message
    finally:
        db.close()
        time.sleep(1)
