from sqlalchemy import text
from ..database import engine

def run_sql(query):
    with engine.connect() as conn:
        result = conn.execute(text(query))
        return str(result.fetchall())

def execute_sql(query):
    with engine.connect() as conn:
        conn.execute(text(query))
        conn.commit()
    return True

def fetch_one(query):
    with engine.connect() as conn:
        result = conn.execute(text(query))
        return result.fetchone()

def fetch_all(query):
    with engine.connect() as conn:
        result = conn.execute(text(query))
        return result.fetchall()

def insert_and_get_id(query):
    with engine.connect() as conn:
        result = conn.execute(text(query))
        conn.commit()
        return result.lastrowid
def update_and_get_count(query):
    with engine.connect() as conn:
        result = conn.execute(text(query))
        conn.commit()
        return result.rowcount
    
def delete_and_get_count(query):
    with engine.connect() as conn:
        result = conn.execute(text(query))
        conn.commit()
        return result.rowcount
    
def execute_many(queries):
    with engine.connect() as conn:
        for query in queries:
            conn.execute(text(query))
        conn.commit()
    return True

def fetch_column(query, column_index=0):
    with engine.connect() as conn:
        result = conn.execute(text(query))
        return [row[column_index] for row in result.fetchall()]
    
def fetch_dicts(query):
    with engine.connect() as conn:
        result = conn.execute(text(query))
        keys = result.keys()
        return [dict(zip(keys, row)) for row in result.fetchall()]

def execute_transaction(queries):
    with engine.begin() as conn:
        for query in queries:
            conn.execute(text(query))
    return True

