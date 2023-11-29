
from flask import current_app as app

class Inventory:
    def __init__(self, id, sid, pid, quantity, available):
        self.id = id
        self.sid = sid
        self.pid = pid
        self.quantity = quantity
        self.available = available

    @staticmethod
    def get_inventory_by_sid(sid, page=1, per_page=10):
        rows = app.db.execute('''
    SELECT id, sid, pid, quantity, available
    FROM Inventory
    WHERE sid = :sid
    LIMIT :per_page OFFSET :offset
    ''',
                          sid=sid,
                          per_page=per_page,
                          offset=(page - 1) * per_page)
        return [Inventory(*row) for row in rows]
    
    @staticmethod
    def get_count_by_sid(sid):
        result = app.db.execute('''
    SELECT COUNT(*)
    FROM Inventory
    WHERE sid = :sid
    ''', sid=sid)
        return result[0][0] 

