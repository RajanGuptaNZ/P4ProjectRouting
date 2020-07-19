import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = r"C:\Users\Skull\PycharmProjects\Routing\carpool_db.db"

    sql_create_group_trips_table =      """CREATE TABLE IF NOT EXISTS "group_trips" (
                                            "group_trip_id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                            "departure_datetime"	TEXT NOT NULL,
                                            "arrival_datetime"	TEXT NOT NULL,
                                            "departure_location_id"	TEXT NOT NULL,
                                            "arrival_location_id"	TEXT NOT NULL
                                        )"""

    sql_create_individual_trips_table = """CREATE TABLE IF NOT EXISTS "individual_trips" (
                                            "individual_trip_id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                            "group_trip_id"	INTEGER NOT NULL,
                                            "user_id"	INTEGER NOT NULL,
                                            "depature_datetime"	TEXT NOT NULL,
                                            "arrival_datetime"	TEXT NOT NULL,
                                            "depature_location_id"	TEXT NOT NULL,
                                            "arrival_location_id"	TEXT NOT NULL,
                                            "individual_trip_cost"	INTEGER NOT NULL,
                                            "trip_confirmation"	INTEGER NOT NULL
                                        )"""

    sql_create_user_accounts_table =    """CREATE TABLE IF NOT EXISTS "user_accounts" (
                                            "user_id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                            "username"	TEXT NOT NULL,
                                            "phone_number"	TEXT NOT NULL,
                                            "email_address"	TEXT NOT NULL UNIQUE,
                                            "encrypted_password"	TEXT NOT NULL
                                        )"""

    sql_create_user_bookings_table =    """CREATE TABLE IF NOT EXISTS "user_bookings" (
                                            "booking_id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                            "user_id"	INTEGER NOT NULL,
                                            "booking_date"	TEXT NOT NULL,
                                            "departure_location"	TEXT NOT NULL,
                                            "arrival_location"	TEXT NOT NULL
                                        )"""
    
    sql_create_user_locations_table =   """CREATE TABLE IF NOT EXISTS "user_locations" (
                                            "location_id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                            "user_id"	INTEGER NOT NULL,
                                            "location_name"	TEXT NOT NULL,
                                            "location_address"	TEXT NOT NULL
                                        )"""

    sql_create_user_timetables_table =  """CREATE TABLE IF NOT EXISTS "user_timetables" (
                                            "event_id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                            "user_id"	INTEGER NOT NULL,
                                            "event_name"	TEXT NOT NULL,
                                            "event_start_datetime"	TEXT NOT NULL,
                                            "event_end_datetime"	TEXT NOT NULL
                                        )"""
    

    # create a database connection
    conn = create_connection(database)
    print("Connected")

    
    if conn is not None:
        # create projects table
        #create_table(conn, sql_create_projects_table)

        # create tasks table
        #create_table(conn, sql_create_tasks_table)
        return
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()