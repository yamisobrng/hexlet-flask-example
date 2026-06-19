import psycopg2
from psycopg2.extras import DictCursor


class UserRepository:
    def __init__(self, conn):
        self.conn = conn


    def find(self, id):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute('SELECT * FROM users WHERE id = %s', (id,))
            row = cur.fetchone()
            return dict(row) if row else None


    def get_content(self):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute('SELECT * FROM users')
            return [dict(row) for row in cur]


    def destroy(self, id):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute('DELETE FROM users WHERE id = %s', (id,))
            self.conn.commit()


    def save(self, user):
        if 'id' in user and user['id']:
            self._update(user)
        else:
            self._create(user)


    def _update(self, user):
        with self.conn.cursor() as cur:
            cur.execute(
                'UPDATE users SET name = %s, email = %s WHERE id = %s',
                (user['name'], user['email'], user['id']),
            )
        self.conn.commit()


    def _create(self, user):
        with self.conn.cursor() as cur:
            cur.execute(
                'INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id',
                (user['name'], user['email']),
            )
            id = cur.fetchone()[0]
            user['id'] = id
        self.conn.commit()