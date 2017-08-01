# The main api library is at https://github.com/Jamonek/Robinhood.
# Most of this script is a modification of trade_history_downloader.py from that github
# This script uses pickles instead of shelves and has a few less elegant feautures to deal with bad
# symbols. output is a .csv of the transaction history suitable for upload to Google Finance or elsewhere.

import json
import csv
import pickle
from Robinhood import Robinhood
import os.path

usr = "username"
psw = "password"
path = 'path/to/files'

rb = Robinhood()
rb.login(usr, psw)

#get old orders
past_orders = get_all_history_orders(rb)
orders = [order_item_info(order, rb) for order in past_orders]

#some keys are bad. You might find more, but these are the ones that gave me issues, so I just left them out.
bad = ["f20eb7f2-8a1f-41e4-9d50-259f44be1de3", "f2ab5ecc-52dd-400e-8489-d7e342abd211"]
orders = [o for o in orders if not o['symbol'] in bad]

#I exclude cancelled, queued or pending orders.
#if you dont want to, just comment this.
orders = [o for o in orders if o['state'] == 'filled']

#dedupe symbols, but still need a list.
symbols = list(set([o['symbol'] for o in orders]))

#RH gives us the symbols in an encrypted form. We have to make calls through the
#API to figure out what the symbols actually are. We can save them locally though, because I 
#do not think they change.

lookup_file = path + "symbol_lookup.pickle"
if os.path.exists(lookup_file): 
    with open(lookup_file, "r") as filename:
        lookup = pickle.load(filename)
        
    #check if we already have those symbol decodings and get them if not
    for s in symbols:
        if not lookup.get(s):
            lookup[s] = rb.symbol(s)
            
#if we cant find a dictionary just make one. This can take a while
else:
    lookup = {s: rb.symbol(s) for s in symbols}

#and either way, save the updated dictionary
with open(lookup_file, "wb") as filename:
    pickle.dump(lookup, filename)
    
#now replace the hashed symbols with their actual names
#also converting shares to integer values
for o in orders:
    o['symbol'] = lookup[o['symbol']]
    o['shares'] = str(int(float(o['shares'])))

#writes out to orders.csv
keys = ['side', 'symbol', 'shares', 'price', 'date', 'state']

ff = path + 'orders.csv'
with open(ff, 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, delimiter = ",", lineterminator = "\n", fieldnames = keys)
    dict_writer.writeheader()
    dict_writer.writerows(orders)