import OptimizerRoutingModel
import routing_model_pb2
import sys


class VRPRoutingModel(OptimizerRoutingModel.RoutingModel):
    """OptiLab VRP routing model solved by back-end optimizers"""

    def __init__(self, name):
        """Generates a new vrp routing model"""
        super().__init__(name, OptimizerRoutingModel.RoutingModelType.VRP)
        self.demand = []
        self.vehicle_capacity = []
        self.num_vehicles = -1
        self.depot = -1

    def set_demand(self, demand):
        """Sets the demand of goods to be delivered for each
        node of the routing network.
        @note the demand list length should be equal to the
        number of nodes in the network, i.e., to the size
        of the distance matrix.
        """
        self.demand = demand

    def get_demand(self):
        return self.demand

    def set_vehicle_capacity(self, vehicle_capacity):
        """Set the load capacity of each vehicle of the
        vehicle routing problem.
        """
        self.vehicle_capacity = vehicle_capacity

    def get_vehicle_capacity(self):
        return self.vehicle_capacity

    def set_num_vehicles(self, num_vehicles):
        """Set the number of vehicles available to satisfy
        demands according to the given capacities.
        """
        if num_vehicles <= 0:
            raise Exception(
                "VRPRoutingModel - SetNumVehicles: invalid number of vehicles " +
                str(num_vehicles))
        self.num_vehicles = num_vehicles

    def get_num_vehicles(self):
        return self.num_vehicles

    def set_depot(self, depot):
        """Set the depot of the VRP on the node network."""
        if depot < 0:
            raise Exception(
                "VRPRoutingModel - SetDepot: invalid depot " +
                str(depot))
        self.depot = depot

    def get_depot(self):
        return self.depot

    def to_protobuf(self):
        # Perform some consistency checks before serializing into protobuf
        # message"""
        if len(self.demand) != super().GetDistanceMatrixsRows():
            err_msg = "VRPRoutingModel - demands " + \
                str(len(self.demand)) + " expected " + str(super().GetDistanceMatrixsRows())
            logging.error(err_msg)
            raise Exception(err_msg)

        if len(self.vehicle_capacity) == 0:
            self.vehicle_capacity = [
                sys.maxsize for x in range(
                    self.num_vehicles)]

        if self.depot >= super().distance_matrix_rows:
            err_msg = "VRPRoutingModel - invalid depot location " + \
                str(self.depot)
            raise Exception(err_msg)

        routing_model = routing_model_pb2.VRPModelProto()
        routing_model.name = super().Name()
        routing_model.demand.extend(self.demand)
        routing_model.capacity.extend(self.vehicle_capacity)
        routing_model.num_vehicle = self.num_vehicles
        routing_model.depot = self.depot
        dmat = routing_model.distance_matrix.add()
        dmat.rows = super().GetDistanceMatrixsRows()
        dmat.cols = super().GetDistanceMatrixsCols()
        for row in super().GetDistanceMatrix():
            for val in row:
                dmat.data.append(int(val * super().distance_matrix_mult))

        return routing_model
