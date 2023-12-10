from app.models.product import Product
from app.models.inventory import Inventory
from app.models.user import User
from app.models.review import Review
from app.models.seller_review import SellerReview
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

        self.price = price
        self.image_url = image_url
        self.save_for_later =  save_for_later


    @staticmethod
    def items_by_uid(uid):
        rows = app.db.execute('''
        SELECT DISTINCT Carts.uid as uid, Carts.pid as pid, Carts.sid as sid, Products.name as name,
        Carts.quantity as quantity, Products.price as price, Products.image_url as image_url, Carts.save_for_later as save_for_later
        FROM Carts, Products, Inventory, Users
        WHERE Carts.uid = :uid AND Carts.pid = Products.id AND Inventory.pid = Products.id AND Carts.sid=Inventory.sid AND Carts.sid=Users.id
        ''',
                              uid=uid)
        return [Cart(*row) for row in rows]
   
   
    @staticmethod
    def add_to_cart(uid, pid, quantity, sid):
        rows = app.db.execute('''
            SELECT quantity
            FROM Carts 
            WHERE uid=:uid AND pid=:pid
        ''',uid=uid,pid=pid)
        if len(rows)==0 or (rows is None):
            action = f'''INSERT INTO Carts(uid, pid, sid, quantity, save_for_later)
                VALUES ({uid}, {pid}, {sid}, {quantity}, False);'''
        else: 
            action = f'''UPDATE Carts SET quantity={int(quantity)+int(rows[0][0])}
                WHERE uid={uid} AND pid={pid} AND sid={sid};'''
        return app.db.execute(action)
   
    @staticmethod
    def delete_from_cart(uid, pid, sid):
        app.db.execute('''
        DELETE from Carts where uid = :uid AND pid = :pid AND sid=:sid''',
        uid = uid,
        pid = pid,
        sid = sid)
        return
   
        return [Cart(*row) for row in rows]
   
   
    @staticmethod
    def add_to_cart(uid, pid, quantity, sid):
        rows = app.db.execute('''
            SELECT quantity
            FROM Carts 
            WHERE uid=:uid AND pid=:pid
        ''',uid=uid,pid=pid)
        if len(rows)==0 or (rows is None):
            action = f'''INSERT INTO Carts(uid, pid, sid, quantity, save_for_later)
                VALUES ({uid}, {pid}, {sid}, {quantity}, False);'''
        else: 
            action = f'''UPDATE Carts SET quantity={int(quantity)+int(rows[0][0])}
                WHERE uid={uid} AND pid={pid} AND sid={sid};'''
        return app.db.execute(action)
   
    @staticmethod
    def delete_from_cart(uid, pid, sid):
        app.db.execute('''
        DELETE from Carts where uid = :uid AND pid = :pid AND sid=:sid''',
        uid = uid,
        pid = pid,
        sid = sid)
        return
   
    @staticmethod
    def decrease_quantity(uid, pid, quantity):
        if (quantity<2): return
        app.db.execute('''
            UPDATE Carts set quantity=:quantity
            WHERE uid=:uid AND pid=:pid''',
            uid=uid,
            pid=pid,
            quantity=quantity-1)
        return
    
    
    def find_invquant(pid):
        invquant = (app.db.execute('''
            SELECT Inventory.quantity
            FROM Inventory, Carts
            WHERE Inventory.pid=Carts.pid AND Inventory.sid=Carts.sid AND Carts.pid=:pid''',
            pid=pid)[0][0])
        return invquant
   
    @staticmethod
    def increase_quantity(uid, pid, quantity):
        invquant = Cart.find_invquant(pid)
        if (quantity >= invquant): quantity = invquant-1
        app.db.execute('''
        UPDATE Carts SET quantity=:quantity
        WHERE uid=:uid AND pid=:pid''',
        uid=uid,
        pid=pid,
        quantity=quantity+1)
        return
    
    def submit_order(uid):
        rows = app.db.execute('''SELECT Carts.id, Carts.pid, Carts.sid, Carts.quantity, 
            Inventory.price, Inventory.sid, Inventory.id, Carts.save_for_later
            FROM Carts, Products, Inventory
            WHERE Carts.sid = Inventory.sid 
            AND Carts.save_for_later = FALSE
            AND Carts.pid = Products.id
            AND Carts.uid = :uid''',
            uid = uid)
        if len(rows)==0 or rows is None:
            return None
        return 
        
    def update_inventory(pid, sid, numsold, curquant):
        app.db.execute('''
        UPDATE Inventory SET quantity=:quantity
        WHERE pid=:pid AND sid=:sid''',
        pid=pid,
        sid=sid,
        quantity=(int(curquant)-int(numsold)))
        return
    
