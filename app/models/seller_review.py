from flask import current_app as app

class SellerReview:
    def __init__(self, seller_review_id, seller_id, user_id, rating, comment, timestamp, upvotes):
        self.seller_review_id = seller_review_id
        self.seller_id = seller_id
        self.user_id = user_id
        self.rating = rating
        self.comment = comment
        self.timestamp = timestamp
        self.upvotes = upvotes


#modifiers

    @staticmethod
    def create_seller_review(seller_id, user_id, rating, comment):
        # This method will create a new seller review after checking if one doesn't already exist
        existing_seller_review = SellerReview.find_by_user_and_seller(user_id, seller_id)
        if existing_seller_review:
            raise ValueError("User has already reviewed this seller.")
        
        result = app.db.execute('''
INSERT INTO SellerReview (seller_id, user_id, rating, comment)
VALUES (:seller_id, :user_id, :rating, :comment)
RETURNING seller_review_id
''',
                                seller_id=seller_id,
                                user_id=user_id,
                                rating=rating,
                                comment=comment)
        seller_review_id = result[0][0] if result else None
        return seller_review_id

    @staticmethod
    def remove_review(user_id, seller_id):
        rows = app.db.execute('''
DELETE FROM SellerReview
WHERE user_id = :user_id AND seller_id = :seller_id
''',
                              user_id=user_id,
                              seller_id=seller_id)
        return rows

    @staticmethod
    def edit_review(user_id, seller_id, rating, comment):
        rows = app.db.execute('''
UPDATE SellerReview
SET rating = :rating, comment = :comment
WHERE user_id = :user_id AND seller_id = :seller_id
''',
                              user_id=user_id,
                              seller_id=seller_id,
                              rating=rating,
                              comment=comment)
        return rows

#accessors

    @staticmethod
    def count_all_reviews(user_id=None, seller_id=None):
        query = 'SELECT COUNT(*) FROM SellerReview WHERE 1=1'
        params = {}
        if user_id:
            query += ' AND user_id = :user_id'
            params['user_id'] = user_id
        if seller_id:
            query += ' AND seller_id = :seller_id'
            params['seller_id'] = seller_id
        rows = app.db.execute(query, **params)
        return rows[0][0] if rows else 0

    @staticmethod
    def five_most_recent_by_user_id(uid):
        print("The user_id is: ", uid)
        rows = app.db.execute('''
SELECT seller_review_id, seller_id, user_id, rating, comment, timestamp, upvotes
FROM SellerReview
WHERE user_id = :uid
ORDER BY timestamp DESC
LIMIT 5
''',
                              uid=uid)
        return [SellerReview(*row) for row in rows]

    @staticmethod
    def find_by_user_and_seller(user_id, seller_id):
        rows = app.db.execute('''
SELECT seller_review_id
FROM SellerReview
WHERE user_id = :user_id AND seller_id = :seller_id
''',
                              user_id=user_id,
                              seller_id=seller_id)
        print(rows)
        return rows

    @staticmethod
    def has_reviewed(user_id, seller_id):
        rows = app.db.execute('''
SELECT seller_review_id
FROM SellerReview
WHERE user_id = :user_id AND seller_id = :seller_id
''',
                              user_id=user_id,
                              seller_id=seller_id)
        return rows



    @staticmethod
    def get_paginated_reviews(page, per_page=10, user_id=None, seller_id=None):
        offset = (page - 1) * per_page
        query = '''
SELECT seller_review_id, seller_id, user_id, rating, comment, timestamp, upvotes
FROM SellerReview
WHERE 1=1
'''
        params = {
            'per_page': per_page,
            'offset': offset
        }
        if user_id:
            query += 'AND user_id = :user_id\n'
            params['user_id'] = user_id
        if seller_id:
            query += 'AND seller_id = :seller_id\n'
            params['seller_id'] = seller_id
        query += 'ORDER BY timestamp DESC\nLIMIT :per_page OFFSET :offset'
        rows = app.db.execute(query, **params)
        return [SellerReview(*row) for row in rows]

    @staticmethod
    def get_paginated_reviews_by_seller_id(seller_id):
        # Select the top 3 reviews with the highest upvotes
        top_upvoted_rows = app.db.execute('''
SELECT seller_review_id, seller_id, user_id, rating, comment, timestamp, upvotes
FROM SellerReview
WHERE seller_id = :seller_id
ORDER BY upvotes DESC
FETCH FIRST 3 ROWS ONLY
''',
                                          seller_id=seller_id)

        # Select the 7 most recent reviews, excluding the top 3
        recent_rows = app.db.execute('''
SELECT seller_review_id, seller_id, user_id, rating, comment, timestamp, upvotes
FROM SellerReview
WHERE seller_id = :seller_id
  AND seller_review_id NOT IN (SELECT seller_review_id FROM SellerReview WHERE seller_id = :seller_id ORDER BY upvotes DESC FETCH FIRST 3 ROWS ONLY)
ORDER BY timestamp DESC
FETCH FIRST 7 ROWS ONLY
''',
                                      seller_id=seller_id)

        # Combine the top upvoted reviews and the most recent reviews
        rows = top_upvoted_rows + recent_rows

        return [SellerReview(*row) for row in rows]



#unused
    @staticmethod
    def get_all_reviews_by_seller_id(seller_id):
        rows = app.db.execute('''
SELECT seller_review_id, seller_id, user_id, rating, comment, timestamp, upvotes
FROM SellerReview
WHERE seller_id = :seller_id
ORDER BY timestamp DESC
''',
                              seller_id=seller_id)
        return [SellerReview(*row) for row in rows]

    @staticmethod
    def get_all_reviews_by_user_id(user_id):
        rows = app.db.execute('''
SELECT seller_review_id, seller_id, user_id, rating, comment, timestamp, upvotes
FROM SellerReview
WHERE user_id = :user_id
ORDER BY timestamp DESC
''',
                              user_id=user_id)
        return [SellerReview(*row) for row in rows]

    @staticmethod
    def get_all_reviews():
        rows = app.db.execute('''
SELECT seller_review_id, seller_id, user_id, rating, comment, timestamp, upvotes
FROM SellerReview
ORDER BY timestamp DESC
''')
        return [SellerReview(*row) for row in rows]


