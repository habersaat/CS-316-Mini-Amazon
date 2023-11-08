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
    def five_most_recent_by_user_id(uid):
        print("The product_id is: ", uid)
        rows = app.db.execute('''
SELECT review_id, product_id, user_id, rating, comment, timestamp, upvotes
FROM Review
WHERE user_id = :uid
ORDER BY timestamp DESC
LIMIT 5
''',
                              uid=uid)
        return [Review(*row) for row in rows]
