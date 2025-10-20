#!/usr/bin/env python3
import time
import sqlite3
import functools

query_cache = {}

def with_db_connection(func):
    """
    Decorator that that automatically handles opening and closing database connections.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            # Call wrapped function with conn injected as first argument
            return func(conn, *args, **kwargs)
        finally:
            # Ensure the connection is always closed
            try:
                conn.close()
            except Exception:
                # swallow close errors (optional: log in real code)
                pass
    return wrapper


def cache_query(func):
    """Decorator to cache results of SQL queries"""
    @functools.wraps(func)
    def wrapper(conn, query):
        if query in query_cache:
            print("Using cached result...")
            return query_cache[query]
        else:
            print("Executing query...")
            result = func(conn, query)
            query_cache[query] = result
            return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


if __name__ == "__main__":
    # First call will execute the query and cache the result
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print(users)

    # Second call will use the cached result
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print(users_again)