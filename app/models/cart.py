from app.models.product import Product
from flask import current_app as app



class Cart:
    def __init__(self, uid, pid, quantity, name, price, image_url):
        #self.id = id
        self.uid = uid
        self.pid = pid
        self.quantity = quantity
        self.name = name
        self.price = price
        self.image_url = image_url

    @staticmethod
    def items_by_uid(uid):
        rows = app.db.execute('''
        SELECT DISTINCT Carts.uid as uid, Carts.pid as pid, Carts.quantity as quantity, Products.name as name, Products.price as price, Products.image_url as image_url
        FROM Carts, Products
        WHERE Carts.uid = :uid AND Carts.pid = Products.id
        ''',
                              uid=uid)
        return [Cart(*row) for row in rows]
    
    
    @staticmethod
    def add_to_cart(uid, pid, quantity):
        app.db.execute('''
        INSERT INTO Carts(uid, pid, quantity)
        VALUES(:uid, :pid, :quantity)
        ''',
        uid=uid,
        pid=pid,
        quantity=quantity)
        return
    
    @staticmethod
    def delete_from_cart(uid, pid):
        app.db.execute('''
        DELETE from Carts where uid = :uid AND pid = :pid''',
        uid = uid,
        pid = pid)
        return
    
    @staticmethod
    def decrease_quantity(uid, pid, quantity):
        app.db.execute('''
        UPDATE Carts set quantity=:quantity
        WHERE uid=:uid AND pid=:pid''',
        uid=uid,
        pid=pid,
        quantity=quantity-1)
        return
    
    @staticmethod
    def increase_quantity(uid, pid, quantity):
        app.db.execute('''
        UPDATE Carts SET quantity=:quantity
        WHERE uid=:uid AND pid=:pid''',
        uid=uid,
        pid=pid,
        quantity=quantity+1)
        return