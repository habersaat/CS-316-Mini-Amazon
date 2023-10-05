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

    @staticmethod
    def reviews_by_product_id(product_id):
        print("The product_id is: ", product_id)
        rows = app.db.execute('''
SELECT review_id, product_id, user_id, rating, comment, timestamp, upvotes
FROM Review
WHERE product_id = :product_id
ORDER BY timestamp DESC
''',
                              product_id=product_id)
        return [Review(*row) for row in rows]
