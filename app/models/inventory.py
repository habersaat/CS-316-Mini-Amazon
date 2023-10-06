from flask import current_app as app

class Inventory:
    def __init__(self, id, sellerID, product, quantity):
        self.id = id
        self.sellerID = sellerID
        self.product = product
        self.quantity = quantity

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, sellerID, product, quantity
FROM Inventory
WHERE id = :id
''', id=id)
        return Inventory(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_sellerID(sellerID):
        rows = app.db.execute('''
SELECT id, sellerID, product, quantity
FROM Inventory
WHERE sellerID = :sellerID
ORDER BY product
''', sellerID=sellerID)
        return [Inventory(*row) for row in rows]
