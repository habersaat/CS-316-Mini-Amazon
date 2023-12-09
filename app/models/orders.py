from flask import current_app as app
from .product import Product

class Order:
    def __init__(self, order_id, seller_id, customer_id, total_amount, recipient_address, order_status, delivery_date):
        self.order_id = order_id
        self.seller_id = seller_id
        self.customer_id = customer_id
        self.total_amount = total_amount
        self.delivery_date = delivery_date
        self.recipient_address = recipient_address
        self.order_status = order_status

    # get the paginated orders of a seller
    @staticmethod
    def get_orders_by_user_id(sid, page=1, per_page=10):
        rows = app.db.execute('''
    SELECT order_id, seller_id, customer_id, total_amount, recipient_address, order_status, delivery_date
    FROM Orders
    WHERE seller_id = :sid
    LIMIT :per_page OFFSET :offset
    ''',
                          sid=sid,
                          per_page=per_page,
                          offset=(page - 1) * per_page)
        return [Orders(*row) for row in rows]