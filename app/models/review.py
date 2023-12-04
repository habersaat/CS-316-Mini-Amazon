from flask import current_app as app

class Review:
    def __init__(self, review_id, product_id, user_id, rating, comment, timestamp, upvotes):
        self.review_id = review_id
        self.product_id = product_id
        self.user_id = user_id
        self.rating = rating
        self.comment = comment
        self.timestamp = timestamp
        self.upvotes = upvotes


#modifiers

    @staticmethod
    def create_review(product_id, user_id, rating, comment):
        # This method will create a new review after checking if one doesn't already exist
        existing_review = Review.find_by_user_and_product(user_id, product_id)
        if existing_review:
            raise ValueError("User has already reviewed this product.")
        
        result = app.db.execute('''
INSERT INTO Review (product_id, user_id, rating, comment)
VALUES (:product_id, :user_id, :rating, :comment)
RETURNING review_id
''',
                                product_id=product_id,
                                user_id=user_id,
                                rating=rating,
                                comment=comment)
        review_id = result[0][0] if result else None  # Extracting the review_id
        return review_id

    
    @staticmethod
    def remove_review(user_id, product_id):
        app.db.execute('''
DELETE FROM Review
WHERE user_id = :user_id AND product_id = :product_id
''',
                    user_id=user_id,
                    product_id=product_id)

    @staticmethod
    def edit_review(user_id, product_id, rating, comment):
        app.db.execute('''
UPDATE Review
SET rating = :rating, comment = :comment
WHERE user_id = :user_id AND product_id = :product_id
''',
                    rating=rating,
                    comment=comment,
                    user_id=user_id,
                    product_id=product_id)

#accessors

    @staticmethod
    def count_reviews(user_id=None, product_id=None):
        query = 'SELECT COUNT(*) FROM Review WHERE 1=1'
        params = {}
        if user_id:
            query += ' AND user_id = :user_id'
            params['user_id'] = user_id
        if product_id:
            query += ' AND product_id = :product_id'
            params['product_id'] = product_id
        rows = app.db.execute(query, **params)
        return rows[0][0] if rows else 0


    @staticmethod
    def five_most_recent_by_user_id(uid):
        print("The user_id is: ", uid)
        rows = app.db.execute('''
SELECT review_id, product_id, user_id, rating, comment, timestamp, upvotes
FROM Review
WHERE user_id = :uid
ORDER BY timestamp DESC
LIMIT 5
''',
                              uid=uid)
        return [Review(*row) for row in rows]


    @staticmethod
    def find_by_user_and_product(user_id, product_id):
        rows = app.db.execute('''
SELECT review_id
FROM Review
WHERE user_id = :user_id AND product_id = :product_id
''',
                              user_id=user_id,
                              product_id=product_id)
        print(rows)  # Add this line for debugging
        return rows


    @staticmethod
    def has_reviewed(user_id, product_id):
        rows = app.db.execute('''
SELECT COUNT(*)
FROM Review
WHERE user_id = :user_id AND product_id = :product_id
''',
                              user_id=user_id,
                              product_id=product_id)
        return rows[0][0] > 0 if rows else False

        
    @staticmethod
    def get_paginated_reviews(page, per_page=10, user_id=None, product_id=None):
        offset = (page - 1) * per_page
        query = '''
SELECT review_id, product_id, user_id, rating, comment, timestamp, upvotes
FROM Review
WHERE 1=1
'''
        params = {
            'per_page': per_page,
            'offset': offset
        }
        if user_id:
            query += 'AND user_id = :user_id\n'
            params['user_id'] = user_id
        if product_id:
            query += 'AND product_id = :product_id\n'
            params['product_id'] = product_id
        query += 'ORDER BY timestamp DESC\nLIMIT :per_page OFFSET :offset'
        rows = app.db.execute(query, **params)
        return [Review(*row) for row in rows]
    

    @staticmethod
    def get_paginated_reviews_by_product_id(product_id):
        # Select the top 3 reviews with the highest upvotes
        top_upvoted_rows = app.db.execute('''
SELECT review_id, product_id, user_id, rating, comment, timestamp, upvotes
FROM Review
WHERE product_id = :product_id
ORDER BY upvotes DESC
FETCH FIRST 3 ROWS ONLY
''',
                                        product_id=product_id)

        # Select the 7 most recent reviews, excluding the top 3
        recent_rows = app.db.execute('''
SELECT review_id, product_id, user_id, rating, comment, timestamp, upvotes
FROM Review
WHERE product_id = :product_id
  AND review_id NOT IN (SELECT review_id FROM Review WHERE product_id = :product_id ORDER BY upvotes DESC FETCH FIRST 3 ROWS ONLY)
ORDER BY timestamp DESC
FETCH FIRST 7 ROWS ONLY
''',
                                    product_id=product_id)

        # Combine the top upvoted reviews and the most recent reviews
        rows = top_upvoted_rows + recent_rows

        return [Review(*row) for row in rows]
