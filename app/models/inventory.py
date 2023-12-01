
from flask import current_app as app
from .product import Product

class Inventory:
    def __init__(self, id, sid, pid, quantity, price, description_short, description_long, category, image_url, available):
        self.id = id
        self.sid = sid
        self.pid = pid
        self.quantity = quantity
        self.price = price
        self.description_short = description_short
        self.description_long = description_long
        self.category = category
        self.image_url = image_url
        self.available = available

    @staticmethod
    def get_inventory_by_sid(sid, page=1, per_page=10):
        rows = app.db.execute('''
    SELECT id, sid, pid, quantity, price, description_short, description_long, category, image_url, available
    FROM Inventory
    WHERE sid = :sid
    LIMIT :per_page OFFSET :offset
    ''',
                          sid=sid,
                          per_page=per_page,
                          offset=(page - 1) * per_page)
        return [Inventory(*row) for row in rows]
    
    @staticmethod
    def get_10_least_expensive_by_product_id(pid):
        rows = app.db.execute('''
    SELECT id, sid, pid, quantity, price, description_short, description_long, category, image_url, available
    FROM Inventory
    WHERE pid = :pid
    ORDER BY price ASC
    LIMIT 10
    ''',
                          pid=pid)
        return [Inventory(*row) for row in rows]

    @staticmethod
    def get_count_by_sid(sid):
        result = app.db.execute('''
    SELECT COUNT(*)
    FROM Inventory
    WHERE sid = :sid
    ''', sid=sid)
        return result[0][0] 
    
    @staticmethod
    def find_pid_by_name(name):
        result = app.db.execute('''
    SELECT id
    FROM Products
    WHERE name = :name
    ''', name=name)
        return result[0][0] if result else None

    @staticmethod
    def create_product(name, description_short, description_long, category, tags, rating, image_url, price, available):
        result = app.db.execute('''
    INSERT INTO Products (name, description_short, description_long, category, rating, image_url, price, available, shipping_speed)
    VALUES (:name, :description_short, :description_long, :category, :rating, :image_url, :price, :available, :shipping_speed)
    RETURNING id
    ''',
                                name=name,
                                description_short=description_short,
                                description_long=description_long,
                                category=category,
                                rating=rating,
                                image_url=image_url,
                                price=price,
                                available=available,
                                shipping_speed="0 days"
                                )
        
        # Add tags
        pid = result[0][0]
        for tag in tags:
            print("Adding tag: " + tag + " to pid: " + str(pid))
            app.db.execute('''
    INSERT INTO Tags (name, pid)
    VALUES (:name, :pid)
    ''',
                            name=tag,
                            pid=pid)

        return pid

    @staticmethod
    def add_product_to_inventory(sid, name, description_short, description_long, category, tags, image_url, price, quantity):
        if sid is None or name is None or description_short is None or description_long is None or category is None or image_url is None or price is None or quantity is None:
            print("ERROR: MISSING PARAMETER")
            return None
        print("ADDING PRODUCT TO INVENTORY")

        if tags is None:
            tags = ["tagless"]
        else:
            tags = tags.split(',')

        pid = Inventory.find_pid_by_name(name)
        print("Found pid: " + str(pid))
        if pid is None:
            # Create new product
            pid = Inventory.create_product(name, description_short, description_long, category, tags, 0, image_url, price, True)
            
        # Add product to inventory
        result = app.db.execute('''
    INSERT INTO Inventory (sid, pid, quantity, price, description_short, description_long, category, image_url, available)
    VALUES (:sid, :pid, :quantity, :price, :description_short, :description_long, :category, :image_url, :available)
    RETURNING id
    ''',
                                sid=sid,
                                pid=pid,
                                quantity=quantity,
                                price=price,
                                description_short=description_short,
                                description_long=description_long,
                                category=category,
                                image_url=image_url,
                                available=True)
        

        Product.update_product_price(pid)

        return 1
    
    @staticmethod
    def update_product_in_inventory(id, sid, name, description_short, description_long, category, tags, image_url, price, quantity):
        if sid is None or name is None or description_short is None or description_long is None or category is None or image_url is None or price is None or quantity is None:
            print("ERROR: MISSING PARAMETER")
            return None
        print("UPDATING PRODUCT IN INVENTORY")

        # Remove old product from inventory
        result = app.db.execute('''
    DELETE FROM Inventory
    WHERE id = :id
    ''',
                                id=id)
        
        # Add new product to inventory
        Inventory.add_product_to_inventory(sid, name, description_short, description_long, category, tags, image_url, price, quantity)
        return 1
    
    @staticmethod
    def delete_product_from_inventory(id):

        # get pid
        rows = app.db.execute('''
    SELECT pid
    FROM Inventory
    WHERE id = :id
    ''',
                                id=id)
        pid = rows[0][0]

        result = app.db.execute('''
    DELETE FROM Inventory
    WHERE id = :id
    ''',
                                id=id)
        
        Product.update_product_price(pid)

        return 1

    @staticmethod
    def get_instance_by_id(id):
        result = app.db.execute('''
    SELECT id, sid, pid, quantity, price, description_short, description_long, category, image_url, available
    FROM Inventory
    WHERE id = :id
    ''', id=id)
        return Inventory(*result[0]) if result else None

