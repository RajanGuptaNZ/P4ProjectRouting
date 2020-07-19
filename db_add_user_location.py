import sqlite3
from sqlite3 import Error

from create_db import create_connection


def add(location_id, user_id, location_name, location_address):
    print("Add")
    database = r"C:\Users\Skull\PycharmProjects\Routing\carpool_db.db"
    conn = create_connection(database)
    cur = conn.cursor()
    try:
        # location_id,
        # user_id,
        query = """INSERT INTO user_locations  (
                    location_id,
                    user_id,
                    location_name,
                    location_address)                    
                    VALUES (?,?,?,?);"""
        data_tuple = (location_id, user_id, location_name, location_address)
        conn.execute(query, data_tuple)
        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        print("SQLite Error: %s" % str(e))
        return None


def main():
    print("Main")
    addresses = ["139 Bawden Rd, Auckland, New Zealand", "13 Myra Evelyn Grove, Auckland, New Zealand",
                 "41 Nimstedt Ave, Auckland, New Zealand", "78 Sycamore Drive, Auckland, New Zealand"]

    i = 6
    for address in addresses:
        add(i, i, "Home", address)
        i += 1


if __name__ == "__main__":
    main()