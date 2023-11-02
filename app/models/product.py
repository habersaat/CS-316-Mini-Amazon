from flask import current_app as app


class Product:
    def __init__(self, id, name, description_short, description_long, rating, image_url, price, available):
        self.id = id
        self.name = name
        self.description_short = description_short
        self.description_long = description_long
        self.rating = rating
        self.image_url = image_url
        self.price = price
        self.available = available

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, name, description_short, description_long, rating, image_url, price, available
FROM Products
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT id, name, description_short, description_long, rating, image_url, price, available
FROM Products
WHERE available = :available
''',
                              available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_k_page_of_n(k, n, available=True):
        k *= n
        rows = app.db.execute('''
SELECT id, name, description_short, description_long, rating, image_url, price, available
FROM Products
WHERE available = :available
OFFSET :k ROWS FETCH NEXT :n ROWS ONLY
''',
                            k=k,
                            n=n,
                            available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_k_page_of_n_price_asc(k, n, available=True):
        k *= n
        rows = app.db.execute('''
SELECT id, name, description_short, description_long, rating, image_url, price, available
FROM Products
WHERE available = :available
ORDER BY price ASC
OFFSET :k ROWS FETCH NEXT :n ROWS ONLY
''',
                            k=k,
                            n=n,
                            available=available)
        return [Product(*row) for row in rows]
    
    @staticmethod
    def get_k_page_of_n_price_desc(k, n, available=True):
        k *= n
        rows = app.db.execute('''
SELECT id, name, description_short, description_long, rating, image_url, price, available
FROM Products
WHERE available = :available
ORDER BY price DESC
OFFSET :k ROWS FETCH NEXT :n ROWS ONLY
''',
                            k=k,
                            n=n,
                            available=available)
        return [Product(*row) for row in rows]
    
    @staticmethod
    def get_k_page_of_n_name_asc(k, n, available=True):
        k *= n
        rows = app.db.execute('''
SELECT id, name, description_short, description_long, rating, image_url, price, available
FROM Products
WHERE available = :available
ORDER BY name ASC
OFFSET :k ROWS FETCH NEXT :n ROWS ONLY
''',
                            k=k,
                            n=n,
                            available=available)
        return [Product(*row) for row in rows]
    
    @staticmethod
    def get_k_page_of_n_name_desc(k, n, available=True):
        k *= n
        rows = app.db.execute('''
SELECT id, name, description_short, description_long, rating, image_url, price, available
FROM Products
WHERE available = :available
ORDER BY name DESC
OFFSET :k ROWS FETCH NEXT :n ROWS ONLY
''',
                            k=k,
                            n=n,
                            available=available)
        return [Product(*row) for row in rows]
    
    @staticmethod
    def get_k_page_of_n_rating_asc(k, n, available=True):
        k *= n
        rows = app.db.execute('''
SELECT id, name, description_short, description_long, rating, image_url, price, available
FROM Products
WHERE available = :available
ORDER BY rating ASC
OFFSET :k ROWS FETCH NEXT :n ROWS ONLY
''',
                            k=k,
                            n=n,
                            available=available)
        return [Product(*row) for row in rows]
    
    @staticmethod
    def get_k_page_of_n_rating_desc(k, n, available=True):
        k *= n
        rows = app.db.execute('''
SELECT id, name, description_short, description_long, rating, image_url, price, available
FROM Products
WHERE available = :available
ORDER BY rating DESC
OFFSET :k ROWS FETCH NEXT :n ROWS ONLY
''',
                            k=k,
                            n=n,
                            available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def k_most_expensive(k):
        rows = app.db.execute('''
SELECT id, name, description_short, description_long, rating, image_url, price, available
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
    
    