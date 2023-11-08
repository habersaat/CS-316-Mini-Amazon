from flask import current_app as app

class Inventory:
    def __init__(self, id, sid, pid, quantity, available):
        self.id = id
        self.sid = sid
        self.pid = pid
        self.quantity = quantity
        self.available = available

    @staticmethod
    def get_inventory_by_sid(sid):
        rows = app.db.execute('''
SELECT id, sid, pid, quantity, available
FROM Inventory
WHERE sid = :sid
''',
                              sid=sid)
        return [Inventory(*row) for row in rows]