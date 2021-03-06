#These are from https://github.com/Jamonek/Robinhood with slight modifications.

#Trade history and profit loss helper functions.
class security:
    def __init__(self, symbol, rpl, upl, total, div): 
        self.symbol = symbol
        self.rpl = round(rpl, 3)
        self.upl = round(upl, 3)
        self.total = round(total, 3)
        self.div = round(div, 3)
    
    def info(self):
        d = {"symbol": self.symbol, "realized":self.rpl, "unrealized":self.upl, \
        "total": self.total, "div":self.div, 'total_w_div': self.total + self.div}
        
        return d   

def extract_hash(d):
    return d['instrument'].split("/")[4] 

def fetch_json_by_url(rb_client, url):
    return rb_client.session.get(url).json()

def order_item_info(order, rb_client):
    #We want to extract the hashed symbol from the RH API
    symbol = extract_hash(order)
    
    return {
        'side': order['side'],
        'price': order['average_price'],
        'shares': order['cumulative_quantity'],
        'symbol': symbol,
        'date': order['last_transaction_at'],
        'state': order['state']
    }

def get_all_history_orders(rb_client):
    orders = []
    past_orders = rb.order_history()
    orders.extend(past_orders['results'])
    while past_orders['next']:
        print("{} order fetched".format(len(orders)))
        next_url = past_orders['next']
        past_orders = fetch_json_by_url(rb_client, next_url)
        orders.extend(past_orders['results'])
    print("{} order fetched".format(len(orders)))
    return orders

def change_symbol(order, hashed, symbol):
    if order['symbol'] == hashed:
        order['symbol'] = symbol
             
def get_totals(ro):
    total = 0.0
    #loop through the relevant orders and get the totals for buys/sells
    for r in relevant_orders:
        if r['side'] == 'sell':
            total= total + float(str(r['price'])) * float(str(r['shares']))
        
        if r['side'] == 'buy':
            total= total - float(str(r['price'])) * float(str(r['shares']))
    
    return total

##
##
##
