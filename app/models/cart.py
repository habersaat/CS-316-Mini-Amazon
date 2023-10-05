from app.models.product import Product
from flask import current_app as app


class Cart:
    def __init__(self, id, uid, pid):
        self.id = id
        self.uid = uid
        self.pid = pid

    @staticmethod
    def items_by_uid(uid):
        print("The uid is: ", uid)
        rows = app.db.execute('''
SELECT Products.id, name, price, available
FROM Products, Carts
WHERE Carts.uid = :uid AND Carts.proid = Products.id
''',
                              uid=uid)
        return [Product(*row) for row in rows]
