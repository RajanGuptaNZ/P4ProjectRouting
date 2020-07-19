from geocoder import geocoder
from routing import routing
import sqlite3
from sqlite3 import Error
from ORTools import ORTools


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def get_locations(conn):
    cur = conn.cursor()
    cur.execute("""SELECT location_id, user_id, location_name, location_address FROM user_locations ORDER BY user_id""")
    locations = cur.fetchall()
    return locations

def get_distance(src, dest):
    print("%s -> %s:" % (src, dest))
    dist = routing.getDist(src, dest)
    print("dist: ", dist)
    time = routing.getTime(src, dest)
    print("time: ", time)
    print("---")
    return dist

def get_time(src, dest):
    time = routing.getTime(src, dest)
    #print("Get Time")
    return time



def db_save_routes(routesList, locationIDList, costList):
    group_trip_id = 0
    individual_trip_id = 0
    for route in routesList:
        print(route)
        prev_node = 0
        i = 0
        tempCostList = costList[group_trip_id]
        print(tempCostList)
        while i < len(route) - 1 :
            current_location = locationIDList[route[i]]
            next_location = locationIDList[route[i + 1]]
            current_user = db_get_userID(current_location)
            time_cost = tempCostList[i]

            print(str(current_location) + "->" + str(next_location) + ": " + str(time_cost))


            database = r"C:\Users\Skull\PycharmProjects\Routing\carpool_db.db"
            conn = create_connection(database)
            cur = conn.cursor()
            try:
                query = """INSERT INTO route_steps  (
                individual_trip_id,
                group_trip_id,
                user_id,
                departure_location_id,
                arrival_location_id,
                time_cost)
                VALUES (?,?,?,?,?,?);"""
                data_tuple = (individual_trip_id, group_trip_id, current_user, current_location, next_location, time_cost)
                conn.execute(query,data_tuple)
                conn.commit()

            except sqlite3.Error as e:
                print ("SQLite Error: %s" % str(e))
                return None

            i = i + 1
            print(i)
            individual_trip_id = individual_trip_id + 1
        group_trip_id = group_trip_id + 1
        conn.close()

def db_get_locationID(user_id):
    database = r"C:\Users\Skull\PycharmProjects\Routing\carpool_db.db"
    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute("""SELECT location_id FROM user_locations WHERE user_id=?""",(user_id,))
    location_id = cur.fetchone()
    # print("loc %s" % location_id[0])
    conn.close()
    return location_id[0]


def db_get_userID(location_id):
    database = r"C:\Users\Skull\PycharmProjects\Routing\carpool_db.db"
    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute("""SELECT user_id FROM user_locations WHERE location_id=?""", (location_id,))
    user_id = cur.fetchone()
    # print("loc %s" % location_id[0])
    conn.close()
    return user_id[0]


def main():

    locationIDList = []

    database = r"C:\Users\Skull\PycharmProjects\Routing\carpool_db.db"

    conn = create_connection(database)
    times_array = []
    if conn is not None:
        locations = get_locations(conn)
        #print(locations)
        print("Getting arc costs")
        j = 0
        for src in locations:
            temp_array = []
            i = 0
            for dest in locations:
                if src[2] == "University":
                    # Trips from uni cost 0
                    temp_array.insert(i, 0)
                elif src != dest:
                    # Get time from src to dest
                    time = get_time(src[3],dest[3])
                    temp_array.insert(i, time)
                else:
                    # Self loops cost 0
                    temp_array.insert(i, 0)
                i = i + 1
            #print(temp_array)
            times_array.insert(j, temp_array)
            j = j+1
            locationIDList.append(src[0])
        print(times_array)
        numLocations = j
        numVehicles = j - 1
        print(numVehicles)
        print("Solving")
        ORTools.solve(times_array, numVehicles, numLocations)
        routesList = ORTools.get_routes(ORTools)
        costList = ORTools.get_costs(ORTools)
        print("Saving to db")
        db_save_routes(routesList, locationIDList, costList)


        return
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()


addresses = ["139 Bawden Rd, Auckland, New Zealand", "13 Myra Evelyn Grove, Auckland, New Zealand", "41 Nimstedt Ave, Auckland, New Zealand", "78 Sycamore Drive, Auckland, New Zealand", "73 Symonds St, Auckland, New Zealand"]


# for address in addresses:
#     print(address)
#     latLng = geocoder.getLatLng(address)
#     lat = latLng["lat"]
#     lng = latLng["lng"]
#     print("Lat, Lng: %s, %s" % (lat, lng))
#     print("---")
#
#
# src = addresses[0]
# dest = addresses[1]
#
#
# for src in addresses:
#     for dest in addresses:
#         if src != dest:
#             print("%s -> %s:" % (src,dest))
#             dist = routing.getDist(src, dest)
#             print("dist: ", dist)
#             time = routing.getTime(src, dest)
#             print("time: ", time)
#             print("---")