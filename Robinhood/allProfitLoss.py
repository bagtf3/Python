## This script will use the trade_history_helpers to obtain a
## Robinhood accounts past profit and losses on all orders.
## output is a .csv sent to wherever the path variable points.

usr = "username"
psw = "password"
path = 'path/to/files'

rb = Robinhood()
rb.login(usr, psw)

past_orders = get_all_history_orders(rb)
orders = [order_item_info(order, rb) for order in past_orders if order['state'] == 'filled']
keys = ['side', 'symbol', 'shares', 'price', 'date', 'state']

#these dont work.There might be others
bad = ["f20eb7f2-8a1f-41e4-9d50-259f44be1de3", "f2ab5ecc-52dd-400e-8489-d7e342abd211"]
orders = [o for o in orders if not o['symbol'] in bad]

positions = rb.positions()['results']
all_symbols = lookup.keys()
sec = rb.securities_owned()

#get key, values for those still holding
held_lookup = {}
for key, value in lookup.iteritems():
    if value in sec:
        held_lookup[key] = value

#get the orders for securities that are still held
held_orders = [o for o in orders if o['symbol'] in held_lookup.keys()]
held_symbols = list(set(o['symbol'] for o in held_orders))

pl = []

for a in all_symbols:
    #get all positions pertaining to the current symbol, a
    pos = next(p for p in positions if p['instrument'].split("/")[4] == a)
    relevant_orders = [o for o in orders if o['symbol'] == a and o['state'] == 'filled']
    symbol = lookup[a]
    
    #if we are holding this symbol
    if a in held_lookup.keys():
        
        current_price = float(rb.last_trade_price(a))
        quantity = float(pos['quantity'])
        avg_price = float(pos['average_buy_price'])
        
        total_cost = quantity * avg_price
        total_equity = quantity * current_price
        
        unrealizedPL = total_equity - total_cost
        
        total = 0.00
        for r in relevant_orders:
        
            if r['side'] == 'sell':
                total= total + float(str(r['price'])) * float(str(r['shares']))
            
            if r['side'] == 'buy':
                total= total - float(str(r['price'])) * float(str(r['shares']))
        
        totalPL = total + total_equity
        realizedPL = totalPL - unrealizedPL
    
        pl.append({'symbol': symbol , 'realized': round(realizedPL, 3), "unrealized": round(unrealizedPL, 3),\
               "total":round(totalPL,3)})
    
    else:
        
        unrealizedPL = 0.0
    
        total = 0.00
        for r in relevant_orders:
        
            if r['side'] == 'sell':
                total= total + float(str(r['price'])) * float(str(r['shares']))
                
            if r['side'] == 'buy':
                total= total - float(str(r['price'])) * float(str(r['shares']))
        
        realizedPL = total
        totalPL = realizedPL
        
        pl.append({'symbol': symbol , 'realized': round(realizedPL, 3), "unrealized": round(unrealizedPL, 3),\
                   "total":round(totalPL,3)})

#write it out
ff = path + 'all_pl.csv'
keys = ['symbol', 'realized', 'unrealized', 'total']
with open(ff, 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, delimiter = ",", lineterminator = "\n", fieldnames = keys)
    dict_writer.writeheader()
    dict_writer.writerows(pl)
