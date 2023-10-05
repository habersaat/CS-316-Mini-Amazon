from flask import current_app as app


class Cart:
    def __init__(self, uid, purid, proid):
        self.uid = uid
        self.purid = purid
        self.proid = proid

    @staticmethod
    def items_by_uid(uid):
        rows = app.db.execute('''
SELECT Products.name
FROM Products, Carts
WHERE :uid = Carts.uid;
 ''',
                              uid=uid)
        return [Cart(*row) for row in rows]
