from app.models.product import Product
from app.models.inventory import Inventory
from flask import current_app as app


class Cart:
    def __init__(self, uid, pid, sid, name, quantity, price, image_url, save_for_later):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.sid = sid
        self.name = name
        self.quantity = quantity
        self.price = price
        self.image_url = image_url
        self.save_for_later =  save_for_later

    @staticmethod
    def items_by_uid(uid):
        rows = app.db.execute('''
        SELECT DISTINCT Carts.uid as uid, Carts.pid as pid, Inventory.sid as sid, Products.name as name, 
        Carts.quantity as quantity, Products.price as price, Products.image_url as image_url
        FROM Carts, Products, Inventory
        WHERE Carts.uid = :uid AND Carts.pid = Products.id AND Inventory.pid = Products.id
        ''',
                              uid=uid)
        return [Product(*row) for row in rows]
    
    #write a sql to add a row to the current cart
    #take in current user ID, add a row in the cart
    @staticmethod
    def add_to_cart(uid, pid):
        app.db.execute('''
        INSERT INTO Carts(uid, pid, quantity)
        VALUES(:uid, :pid, :quantity)
        ''',
        uid=uid,
        pid=pid,
        quantity=1)
        return
    
    @staticmethod
    def delete_from_cart(uid, pid):
        app.db.execute('''
        DELETE from Carts where uid = :uid AND pid = :pid''',
        uid = uid,
        pid = pid)
        return
    
    @staticmethod
    def decrease_quantity(uid, pid, quantity, price):
        if (quantity<1): return
        app.db.execute('''
        UPDATE Carts set quantity=:quantity, price=:price
        WHERE uid=:uid AND pid=:pid''',
        uid=uid,
        pid=pid,
        price = price - 1,
        quantity=quantity-1)
        return
    
    @staticmethod
    def increase_quantity(uid, pid, quantity, price, sid):
        maxQuantity = int(f'''SELECT quantity FROM Inventory WHERE sid = :sid and pid=:pid''')
        print(maxQuantity)
        app.db.execute('''
        UPDATE Carts SET quantity=:quantity, price=:price
        WHERE uid=:uid AND pid=:pid''',
        uid=uid,
        pid=pid,
        sid = sid,
        price = price + 1,
        quantity=quantity+1)
        return