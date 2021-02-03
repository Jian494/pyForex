from websocket import create_connection
import json
import random
import string
import re
from decimal import Decimal
import datetime
import csv

q1 = "qs_" + ''.join(random.choice(string.ascii_letters) for i in range(12))
c1 = "cs_" + ''.join(random.choice(string.ascii_letters) for i in range(12))

Headers = json.dumps({
    'Connection': 'upgrade',
    'Host': 'data.tradingview.com',
    'Origin: https://www.tradingview.com'
    'Cache-Control': 'no-cache',
    'Upgrade': 'websocket',
    'Sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits',    
    'Sec-WebSocket-Key': 'YP5zFMsIgvsATGPH5IrxGw==',
    'Sec-WebSocket-Version': '13',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    })

ws = create_connection('wss://data.tradingview.com/socket.io/websocket',headers=Headers)

ws.send("~m~"+str(len((json.dumps({"m":"set_auth_token","p":["unauthorized_user_token"]}, separators=(',', ':')))))+"~m~"+(json.dumps({"m":"set_auth_token","p":["unauthorized_user_token"]}, separators=(',', ':'))))
ws.send("~m~"+str(len((json.dumps({"m":"chart_create_session","p":[c1,""]}, separators=(',', ':')))))+"~m~"+(json.dumps({"m":"chart_create_session","p":[c1,""]}, separators=(',', ':'))))
ws.send("~m~"+str(len((json.dumps({"m":"quote_create_session","p":[q1]}, separators=(',', ':')))))+"~m~"+(json.dumps({"m":"quote_create_session","p":[q1]}, separators=(',', ':'))))
ws.send("~m~"+str(len((json.dumps({"m":"quote_set_fields","p":[q1,"base-currency-logoid","ch","chp","currency-logoid","currency_code","current_session","description","exchange","format","fractional","is_tradable","language","local_description","logoid","lp","lp_time","minmov","minmove2","original_name","pricescale","pro_name","short_name","type","update_mode","volume"]}, separators=(',', ':')))))+"~m~"+(json.dumps({"m":"quote_set_fields","p":[q1,"base-currency-logoid","ch","chp","currency-logoid","currency_code","current_session","description","exchange","format","fractional","is_tradable","language","local_description","logoid","lp","lp_time","minmov","minmove2","original_name","pricescale","pro_name","short_name","type","update_mode","volume"]}, separators=(',', ':'))))
ws.send("~m~"+str(len((json.dumps({"m":"quote_add_symbols","p":[q1,"FX:GBPUSD",{"flags":["force_permission"]}]}, separators=(',', ':')))))+"~m~"+(json.dumps({"m":"quote_add_symbols","p":[q1,"FX:GBPUSD",{"flags":["force_permission"]}]}, separators=(',', ':'))))
ws.send("~m~"+str(len((json.dumps({"m":"resolve_symbol","p":[c1,"symbol_1","={\"symbol\":\"FX:GBPUSD\",\"adjustment\":\"splits\",\"session\":\"extended\"}"]}, separators=(',', ':')))))+"~m~"+(json.dumps({"m":"resolve_symbol","p":[c1,"symbol_1","={\"symbol\":\"FX:GBPUSD\",\"adjustment\":\"splits\",\"session\":\"extended\"}"]}, separators=(',', ':'))))
ws.send("~m~"+str(len((json.dumps({"m":"create_series","p":[c1,"s1","s1","symbol_1","D",300]}, separators=(',', ':')))))+"~m~"+(json.dumps({"m":"create_series","p":[c1,"s1","s1","symbol_1","D",300]}, separators=(',', ':'))))
ws.send("~m~"+str(len((json.dumps({"m":"quote_fast_symbols","p":[q1,"FX:GBPUSD"]}, separators=(',', ':')))))+"~m~"+(json.dumps({"m":"quote_fast_symbols","p":[q1,"FX:GBPUSD"]}, separators=(',', ':'))))

count = 0
while True:        
    with open('GBPUSD.csv','a', newline='') as data_file:
        employee_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)            
        try:
            t = datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")  
            result = ws.recv()
            pattern = re.compile("~m~\d+~m~~h~\d+$")
            if pattern.match(result):
                ws.recv()
                ws.send(result)
            try:
                x = result.split(",")            
                if x[7] == (''.join(c for c in x[7] if c in '.0123456789')):         
                    print("7")           
                    print(x[7])     
                    employee_writer.writerow([count, t, x[7]])    
                    count += 1                        
                else:
                    if x[13] == (''.join(c for c in x[13] if c in '.0123456789')):
                        print("13")
                        print((x[13]))
                        employee_writer.writerow([count, t, x[13]])    
                        count += 1  
                    else:    
                        if x[11] == (''.join(c for c in x[11] if c in '.0123456789')):     
                            print("11")        
                            print(x[11])
                            employee_writer.writerow([count, t, x[11]])    
                            count += 1  
                        else:   
                            print("x")
                            print(x)
            except:
                pass
        except Exception as e:
            print(e)
            break