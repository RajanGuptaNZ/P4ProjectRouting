""""Vehicles Routing Problem (VRP)."""

from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


class ORTools:
    routesList = []
    costList = []

    def create_data_model(times_array, numVehicles, numLocations):
        """Stores the data for the problem."""
        data = {}
        data['distance_matrix'] = times_array
        data['demands'] = ORTools.setup_demands(numLocations)
        data['vehicle_capacities'] = ORTools.setup_capacities(numVehicles)
        data['num_vehicles'] = numVehicles
        data['depot'] = 0
        return data

    def setup_capacities(numVehicles):
        vehicle_capacities = []
        for i in range(0, numVehicles):
            vehicle_capacities.insert(i, 4)
        return vehicle_capacities

    def setup_demands(numLocations):
        demands = []
        demands.insert(0, 0)
        for i in range(1, numLocations):
            demands.insert(i, 1)
        return demands

    def print_solution(data, manager, routing, solution):
        """Prints solution on console."""
        total_distance = 0
        total_load = 0
        for vehicle_id in range(data['num_vehicles']):
            index = routing.Start(vehicle_id)
            plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
            route_distance = 0
            route_load = 0
            while not routing.IsEnd(index):
                node_index = manager.IndexToNode(index)
                route_load += data['demands'][node_index]
                plan_output += ' Node {0} ({1}) -> '.format(node_index, route_load)
                previous_index = index
                index = solution.Value(routing.NextVar(index))
                route_distance += routing.GetArcCostForVehicle(
                    previous_index, index, vehicle_id)
            plan_output += ' Node {0} ({1})\n'.format(manager.IndexToNode(index),
                                                     route_load)
            plan_output += 'Distance of the route: {} mins\n'.format(route_distance)
            plan_output += 'Load of the route: {}\n'.format(route_load)
            print(plan_output)
            total_distance += route_distance
            total_load += route_load
        print('Total distance of all routes: {} mins'.format(total_distance))
        print('Total load of all routes: {}'.format(total_load))

    def save_routes(data, manager, routing, solution):


        total_distance = 0
        total_load = 0
        for vehicle_id in range(data['num_vehicles']):
            tempRouteList = []
            tempCostList = []

            index = routing.Start(vehicle_id)
            plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
            route_distance = 0
            route_load = 0
            while not routing.IsEnd(index):
                node_index = manager.IndexToNode(index)
                route_load += data['demands'][node_index]
                tempRouteList.append(node_index)
                plan_output += ' Node {0} ({1}) -> '.format(node_index, route_load)
                previous_index = index
                index = solution.Value(routing.NextVar(index))
                route_distance += routing.GetArcCostForVehicle(
                    previous_index, index, vehicle_id)
                # Add arc cost to list
                arc_cost = routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
                tempCostList.append(arc_cost)


            plan_output += ' Node {0} ({1})\n'.format(manager.IndexToNode(index),
                                                      route_load)

            #Add next node to list
            node = manager.IndexToNode(index)
            tempRouteList.append(node)
 
            plan_output += 'Distance of the route: {} mins\n'.format(route_distance)
            plan_output += 'Load of the route: {}\n'.format(route_load)
            total_distance += route_distance
            total_load += route_load
            tempRouteList.pop(0)
            tempCostList.pop(0)

            #Only save routes that are used
            if(len(tempRouteList) > 1):
                ORTools.routesList.append(tempRouteList)
                ORTools.costList.append(tempCostList)

    def get_routes(self):
        return (ORTools.routesList)

    def get_costs(self):
        return (ORTools.costList)



    def solve(times_array, numVehicles, numLocations):
        """Solve the CVRP problem."""
        # Instantiate the data problem.
        data = ORTools.create_data_model(times_array, numVehicles, numLocations)

        # Create the routing index manager.
        manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                               data['num_vehicles'], data['depot'])

        # Create Routing Model.
        routing = pywrapcp.RoutingModel(manager)

        # Create and register a transit callback.
        # Returns distances between locations and passes it to the solver
        def distance_callback(from_index, to_index):
            """Returns the distance between the two nodes."""
            # Convert from routing variable Index to distance matrix NodeIndex.
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data['distance_matrix'][from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        # Define cost of each arc.
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        # Add Capacity constraint.
        def demand_callback(from_index):
            """Returns the demand of the node."""
            # Convert from routing variable Index to demands NodeIndex.
            from_node = manager.IndexToNode(from_index)
            return data['demands'][from_node]

        demand_callback_index = routing.RegisterUnaryTransitCallback(
            demand_callback)
        routing.AddDimensionWithVehicleCapacity(
            demand_callback_index,
            0,  # null capacity slack
            data['vehicle_capacities'],  # vehicle maximum capacities
            True,  # start cumul to zero
            'Capacity')

        # Setting first solution heuristic.
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

        # Solve the problem.
        solution = routing.SolveWithParameters(search_parameters)

        # Print solution on console.
        if solution:
            ORTools.print_solution(data, manager, routing, solution)
            ORTools.save_routes(data, manager, routing, solution)
