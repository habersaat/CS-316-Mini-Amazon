from flask import current_app as app


class Purchase:
    def __init__(self, id):
        self.id = id
