import jsonrpc
import psycopg2
import time
import socket

rpc_username = "user"
rpc_password = "password"

db = psycopg2.connect(database="bitwallet",user="bitwallet",password="903ur092isodj")

bitcoin = jsonrpc.ServiceProxy("http://"+rpc_username+":"+rpc_password+"@127.0.0.1:8332/")

while True:
    c = db.cursor()
    
    c.execute("""
    SELECT
        withdrawal_request_id,
        withdrawal_amount,
        bitcoin_address
    FROM withdrawal_requests
    WHERE status='PENDING'
    FOR UPDATE
    """)
    
    results = c.fetchall()
    
    if results:
        for result in results:
            reqid,amount,address = result
            
            try:
                scaled_amount = amount * ( 10 ** 8 )
                
                assert(scaled_amount == int(scaled_amount))
                
                scaled_amount = str(int(scaled_amount))
                
                result = bitcoin.sendtoaddress(address,scaled_amount)
                
                c.execute("""
                UPDATE withdrawal_requests
                SET status='SENT'
                WHERE withdrawal_request_id=%s""",(reqid,))
                
                db.commit()
            except jsonrpc.authproxy.JSONRPCException, e:
                print e.error
                db.rollback()
    c.close()
    
    time.sleep(1)
