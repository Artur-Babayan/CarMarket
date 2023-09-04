import json
from json import JSONEncoder
from models import *

class CarMarketEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, (Buyer, Seller)):
            return o.__dict__
        elif isinstance(o, Car):
            return {
                "model": o.model,
                "price": o.price,
                "sale_date": o.sale_date,
                "returned": o.returned,
                "return_info": o.return_info,
                "buyer": None if o.buyer is None else o.buyer.first_name + " " + o.buyer.last_name,
                "seller": o.seller.first_name + " " + o.seller.last_name
            }
        return super().default(o)