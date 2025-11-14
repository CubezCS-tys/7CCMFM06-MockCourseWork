import sqlite3
import math
import os
import numpy as np
import random

def check( id, answer, tol=10**-10, cheat=False):
    """Check whether the answer with the given ID is correct"""
    answer = str(answer)
    
    dbfile = "solns.db"
    if not is_build() and not is_master_project():
        if not os.path.exists(dbfile):
            raise RuntimeError("Database solns.db not found. It must be in the same folder as the notebook.")

    with sqlite3.connect("solns.db") as conn:
        c = conn.cursor()
        c.execute( """
            CREATE TABLE IF NOT EXISTS solutions (
                id text PRIMARY KEY,
                value text NOT NULL
            );""")
        conn.commit()
        if is_build():
            _check_write_mode(conn,id, answer)
        _check_read_mode(conn, id, answer, tol, cheat)
    return

def is_build():
    return os.getenv('IN_BUILD')=="true"

def is_master_project():
    return os.getenv('COCALC_PROJECT_ID')=='a105d69a-2bf1-4215-b693-6c7f15a56199'

def _check_read_mode(conn, id, answer,tol,cheat):
    """Check whether the answer with the given ID is correct"""
    with sqlite3.connect("solns.db") as conn:
        c = conn.cursor()
        c.execute( """
            SELECT value FROM solutions WHERE id=?""",[id])
        row = c.fetchone()
        if not row:
            if is_master_project():
                _check_write_mode(conn,id,answer)
                return
            raise ValueError('Invalid id {}'.format(id))
        value = str(row[0])
        try:
            if abs(float(value)-float(answer))<tol:
                pass
            else:
                if cheat:
                    raise AssertionError('Incorrect answer {}, correct answer is {}'.format(answer, value))
                else:
                    raise AssertionError('Incorrect answer')
        except ValueError:
            if value.strip()!=answer.strip():
                if cheat:
                    print( answer )
                    print( value )
                    raise AssertionError('Incorrect answer >>{}<<, correct answer is >>{}<<'.format(answer,value))
                else:
                    raise AssertionError('Incorrect answer')

def _check_write_mode(conn, id, answer):
    c = conn.cursor()
    c.execute( """
        SELECT * FROM solutions WHERE id=?""", [id]);
    row = c.fetchone()
    if not row:
        c.execute( """
            INSERT INTO solutions( id, value ) VALUES (?,?)""", [id, answer]);
    else:
        c.execute( """
            UPDATE solutions SET value=? WHERE id=?""", [answer,id]);
    conn.commit()

def auto_marking_message( auto_marked = True ):
    if not auto_marked:
        print("Auto marking message: The question above is not automatically marked, you'll have to decide for yourself if you got it right")
        return
    emoji = random.choice(['😊','😀','✔','😺','😻','😍','⭐','🌟','👍','✨','✔️','🏆'])
    print( "Auto marking message: "+emoji+' Correct')