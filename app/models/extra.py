@staticmethod
    def get_orders_by_user_id(sid):
        rows = app.db.execute('''
    SELECT order_id, seller_id, customer_id, total_amount, recipient_address, order_status, delivery_date
    FROM Orders
    WHERE seller_id = 11
    ''',
                          sid=sid)
        return [Order(*row) for row in rows]