import sqlite3


class DBManager:
    def __init__(self, filename='sam.db'):
        self.conn = sqlite3.connect(filename)
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()

    def _do_insert(self, table, data):
        cols = ', '.join(data.keys())
        q_marks = ', '.join(['?'] * len(data))

        query = f'INSERT INTO {table} ({cols}) VALUES ({q_marks})'

        self.c.execute(query, list(data.values()))
        self.conn.commit()
        return self.c.lastrowid

    def new_node(self, node_title):
        return self._do_insert('nodes', {
            'node_title': node_title,
        })

    def new_edge(self, from_node, to_node):
        return self._do_insert('edges', {
            'from_node': from_node,
            'to_node': to_node,
        })

    def get_node(self, node_id):
        query = f'SELECT * FROM nodes WHERE id = ?'
        self.c.execute(query, [node_id])

    def get_edges(self, node, direction):
        assert direction in ['from', 'to']
        query = f'SELECT * FROM edges WHERE {direction}_node = ?'
        self.c.execute(query, [node])


class FamilyManager:
    def __init__(self, db):
        self.db = db  # DBManager

    def get_tree(self, node_id):
        tree = dict()
