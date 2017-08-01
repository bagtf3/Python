#These are from https://github.com/Jamonek/Robinhood with slight modifications.

#Trade history and profit loss helper functions.
def fetch_json_by_url(rb_client, url):
    return rb_client.session.get(url).json()

def order_item_info(order, rb_client):
    #We want to extract the hashed symbol from the RH API
    symbol = order['instrument'].split("/")[4]
    
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
##
##
##