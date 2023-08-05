import os
from time import sleep

import sqlite3


def get_db(db_file):
    db = sqlite3.connect(
        str(db_file), detect_types=sqlite3.PARSE_DECLTYPES)
    db.row_factory = sqlite3.Row
    return db


def release_all_locks(db_file):
    db = get_db(db_file)
    db.execute('DELETE FROM locks;')
    db.close()


class SQLiteLock():
    def __init__(self, db_file, lock_name="global", blocking=False,
                 timeout=30, polling_rate=0.4):
        self.db_file = db_file
        self.lock_name = lock_name
        self.lock_acquired = False
        self.acquire(blocking=blocking, timeout=timeout,
                     polling_rate=polling_rate)

    def acquire(self, blocking=False, timeout=30, polling_rate=0.4):
        if self.lock_acquired:
            return

        if not os.path.isfile(self.db_file):
            self.init_db()

        cur_timeout = 0
        while True and not self.lock_acquired:
            db = get_db(self.db_file)
            try:
                db.isolation_level = 'EXCLUSIVE'
                db.execute('BEGIN EXCLUSIVE')
                lock_entry = db.execute(
                    'SELECT * FROM locks WHERE name = ?',
                    (self.lock_name,)).fetchone()
                if lock_entry is None:
                    db.execute(
                        'INSERT INTO locks (name) VALUES (?)',
                        (self.lock_name,))
                    self.lock_acquired = True
                    print(f"Acquired lock {self.lock_name}")
                db.commit()
            except sqlite3.OperationalError as e:
                print(f"Encountering operational error {e}")
            db.close()
            if self.lock_acquired or not blocking:
                break
            cur_timeout += polling_rate
            sleep(polling_rate)

    def init_db(self):
        db = get_db(self.db_file)
        db.executescript('DROP TABLE IF EXISTS locks; '
                         'CREATE TABLE locks (name TEXT NOT NULL);')
        db.close()

    def locked(self):
        return self.lock_acquired

    def __enter__(self):
        return self

    def __exit__(self, *_, **__):
        self.release()

    def release(self):
        if not self.locked():
            return
        while True:
            db = get_db(self.db_file)
            try:
                db.execute(
                    'DELETE FROM locks WHERE name = ?',
                    (self.lock_name,))
                db.commit()
                db.close()
                break
            except sqlite3.OperationalError:
                pass
            db.close()
            sleep(0.4)
        print(f"Released lock {self.lock_name}")
        self.lock_acquired = False
