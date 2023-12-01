from flask import current_app as app
from flask_login import current_user

from .user import User
class Product:
    def __init__(self, id, name, description_short, description_long, category, rating, image_url, price, available, low_stock, shipping_speed=None):
        self.id = id
        self.name = name
        self.description_short = description_short
        self.description_long = description_long
        self.category = category
        self.rating = rating
        self.image_url = image_url
        self.price = price
        self.available = available
        self.low_stock = low_stock
        self.shipping_speed = shipping_speed

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, name, description_short, description_long, category, rating, image_url, price, available, low_stock, shipping_speed
FROM Products
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT id, name, description_short, description_long, category, rating, image_url, price, available, low_stock, shipping_speed
FROM Products
WHERE available = :available
''',
                              available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_by_matching_tag(query, available=True):
        rows = app.db.execute('''
SELECT id, name, description_short, description_long, category, rating, image_url, price, available, low_stock, shipping_speed
FROM Products
WHERE id IN (
    SELECT pid
    FROM Tags
    WHERE name = :query
) AND available = :available
''',
                              query=query,
                              available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_k_page_of_n(k, n, ftr=None, ord=None, cat=None, query=None, available=True): 
        # Get list of products that match the query string or are tagged with the query string
        k *= n
        rows = app.db.execute('''
SELECT id, name, description_short, description_long, category, rating, image_url, price, available, low_stock, shipping_speed
FROM Products
''' + (f'WHERE category = :cat AND available = :available' if cat is not None else 'WHERE available = :available') + '''
''' + (f'AND LOWER(name) LIKE LOWER(:query)' if query is not None else '') + '''
UNION
SELECT id, name, description_short, description_long, category, rating, image_url, price, available, low_stock, shipping_speed
FROM Products
WHERE id IN (
    SELECT pid
    FROM Tags
    WHERE LOWER(Tags.name) LIKE LOWER(:query)
) AND available = :available
''' + (f'ORDER BY {ftr} {ord}' if ord is not None else '') + '''
OFFSET :k ROWS FETCH NEXT :n ROWS ONLY
''',
                              cat=cat,
                              query='%' + query + '%' if query is not None else None,
                              available=available,
                              k=k,
                              n=n)
        return [Product(*row) for row in rows]
    
    @staticmethod
    def get_query_length(ftr=None, ord=None, cat=None, query=None, available=True):
        rows = app.db.execute('''
SELECT COUNT(*)
FROM Products
''' + (f'WHERE category = :cat AND available = :available' if cat is not None else 'WHERE available = :available') + '''
''' + (f'AND LOWER(name) LIKE LOWER(:query)' if query is not None else '') + '''
UNION
SELECT COUNT(*)
FROM Products
WHERE id IN (
    SELECT pid
    FROM Tags
    WHERE LOWER(Tags.name) LIKE LOWER(:query)
) AND available = :available
''',
                                cat=cat,
                                query='%' + query + '%' if query is not None else None,
                                available=available)
        if len(rows) == 1:
            return rows[0][0]
        return rows[0][0] + rows[1][0]
    
        
    @staticmethod
    def k_most_expensive(k):
        rows = app.db.execute('''
SELECT id, name, description_short, description_long, rating, category, image_url, price, available, low_stock, shipping_speed
FROM Products
ORDER BY price DESC
LIMIT :k
''',
                              k=k)
        return [Product(*row) for row in rows]
    
    @staticmethod
    def get_all_info_by_id(id):
        rows = app.db.execute('''
        SELECT *
        FROM Products
        WHERE id = :id
        ''',
                                id=id)
        return [Product(*row) for row in rows]
    
    @staticmethod
    def update_product_rating(id):

        # Calculate average rating using Reviews table
        rows = app.db.execute('''
        SELECT AVG(rating)
        FROM Review
        WHERE product_id = :id
        ''',
                                id=id)
        
        rating = rows[0][0]
        if rating is None:
            rating = 0

        print(f'Updating product {id} rating to {rating}')

        rows = app.db.execute('''
        UPDATE Products
        SET rating = :rating
        WHERE id = :id
        ''',
                                id=id,
                                rating=rating)
        return rows
    
    @staticmethod
    def product_rating_init():
        print("Initializing product ratings...")

        # calculate average rating for each product and update the rating column in the Products table
        rows = app.db.execute('''
        SELECT id
        FROM Products
        ''')
        for row in rows:
            Product.update_product_rating(row[0])
        return
    
    @staticmethod
    def set_product_low_stock(id, low_stock=True):
        rows = app.db.execute('''
        UPDATE Products
        SET low_stock = :low_stock
        WHERE id = :id
        ''',
                                id=id,
                                low_stock=low_stock)
        return rows
    
    @staticmethod
    def count_product_quantity(id):
        rows = app.db.execute('''
        SELECT SUM(quantity)
        FROM Inventory
        WHERE pid = :id
        ''',
                                id=id)
        return rows[0][0]

    @staticmethod
    def update_product_availability(id, available):
        rows = app.db.execute('''
        UPDATE Products
        SET available = :available
        WHERE id = :id
        ''',
                                id=id,
                                available=available)
        
        # Set product to low stock if quantity is less than or equal to 100
        cnt = Product.count_product_quantity(id)
        if cnt is None or cnt > 100:
            Product.set_product_low_stock(id, False)
        else:
            Product.set_product_low_stock(id, True)

        return rows
    
    @staticmethod
    def update_product_price(id):
        # Update product price based on lowest price in Inventory table
        rows = app.db.execute('''
        SELECT MIN(price)
        FROM Inventory
        WHERE pid = :id
        ''',
                                id=id)
        price = rows[0][0]

        if price is None:
            price = 0
            # Set product to unavailable if no price is found
            Product.update_product_availability(id, False)
        else:
            print(f'Updating product {id} price to {price}')

            # First, get the column of the lowest price in the Inventory table
            rows = app.db.execute('''
            SELECT description_short, description_long, category, image_url
            FROM Inventory
            WHERE price = :price
            ''',
                                    price=price)
            description_short = rows[0][0]
            description_long = rows[0][1]
            category = rows[0][2]
            image_url = rows[0][3]

            # Then, update the price, description_short, description_long, category, and image_url columns in the Products table to match the lowest price in the Inventory table
            rows = app.db.execute('''
            UPDATE Products
            SET price = :price, description_short = :description_short, description_long = :description_long, category = :category, image_url = :image_url
            WHERE id = :id
            ''',
                                    id=id,
                                    price=price,
                                    description_short=description_short,
                                    description_long=description_long,
                                    category=category,
                                    image_url=image_url)
            
            Product.update_product_availability(id, True)
            if current_user.is_authenticated:
                Product.update_shipping_speed(id, current_user.longitude, current_user.latitude)
        return rows

    @staticmethod
    def inventory_init():
        print("Initializing inventory...")
        rows = app.db.execute('''
        SELECT id
        FROM Products
        ''')
        for row in rows:
            Product.update_product_price(row[0])
            # Set product to low stock if quantity is less than or equal to 10
            cnt = Product.count_product_quantity(row[0])
            if cnt is None or cnt > 100:
                Product.set_product_low_stock(row[0], False)
            else:
                Product.set_product_low_stock(row[0], True)
            
        return
    
    @staticmethod
    def get_sid_of_cheapest_product(pid):
        rows = app.db.execute('''
        SELECT sid
        FROM Inventory
        WHERE pid = :pid
        ORDER BY price ASC
        LIMIT 1
        ''',
                                pid=pid)
        if len(rows) == 0:
            return None
        return rows[0][0]
    
    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):
        # Calculate distance between two points using the Haversine formula
        from math import radians, cos, sin, asin, sqrt
        # Convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        
        # Haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        
        # Radius of earth in kilometers is 6371
        km = 6371* c
        return km
    
    @staticmethod
    def get_shipping_speed(pid, lat, lon):
        sid = Product.get_sid_of_cheapest_product(pid)
        loc = User.get_location(sid)
        lat1 = loc[0]
        lon1 = loc[1]
        dist = Product.calculate_distance(lat, lon, lat1, lon1)
        if dist < 6500:
            return "2 days"
        elif dist < 9500:
            return "5 days"
        elif dist < 13500:
            return "7 days"
        else:
            return "10 days"
        
    @staticmethod
    def update_shipping_speed(pid, lon, lat):
        rows = app.db.execute('''
        UPDATE Products
        SET shipping_speed = :shipping_speed
        WHERE id = :id
        ''',
                                id=pid,
                                shipping_speed=Product.get_shipping_speed(pid, lon, lat))
        return rows
        
    @staticmethod
    def shipping_speed_init(lon, lat):
        print("Initializing shipping speed...")
        print("My longitude is: ", lon)
        print("My latitude is: ", lat)
        rows = app.db.execute('''
        SELECT id
        FROM Products
        WHERE available = True
        ''')
        for row in rows:
            Product.update_shipping_speed(row[0], lon, lat)
        return
