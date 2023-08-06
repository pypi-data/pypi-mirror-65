from enum import Enum
import routing_model_pb2
import logging
import string

# Type of the routing model


class RoutingModelType(Enum):
    VRP = 1
    TSP = 2

# The "RoutingEngineType" sets the type of engine
# to be used to solve a routing model of
# type "RoutingModelType".
# For example, a VRP model can be solved by an
# engine implementing "ACTOR_POLICY_VRP", i.e., using
# an actor executing a policy learned with
# Reinforcement Learning.
# @note not all combinations of model types and engine
# types are valid combinations


class RoutingEngineType(Enum):
    ACTOR_POLICY_VRP = 1


class RoutingModel:
    """OptiLab Routing model solved by back-end optimizers"""

    model_type = None
    engine_type = None
    model_name = ""

    def __init__(self, name, model_type):
        """Generates a new routing model"""
        if not name.strip():
            err_msg = "RoutingModel - empty model name"
            logging.error(err_msg)
            raise Exception(err_msg)
        self.model_name = name
        self.distance_matrix = []
        self.distance_matrix_rows = -1
        self.distance_matrix_cols = -1
        self.distance_matrix_mult = 1

        if not isinstance(model_type, RoutingModelType):
            err_msg = "RoutingModel - invalid model type " + type(model_type)
            logging.error(err_msg)
            raise Exception(err_msg)
        self.model_type = model_type

    def set_engine_type(self, engine_type):
        if not isinstance(model_type, RoutingEngineType):
            err_msg = "RoutingModel - SetEngineType: invalid engine type " + \
                type(engine_type)
            logging.error(err_msg)
            raise Exception(err_msg)
        self.engine_type = engine_type

    def name(self):
        return self.model_name

    def set_distance_matrix(self, dist_matrix, mult_data=1):
        self.distance_matrix = dist_matrix
        self.distance_matrix_mult = mult_data
        rows = len(self.distance_matrix)

        # Check distance matrix:
        # must be a non-empty, square matrix
        if rows == 0:
            err_msg = "RoutingModel - SetDistanceMatrix: invalid matrix (empty)"
            logging.error(err_msg)
            raise Exception(err_msg)
        for idx in range(len(self.distance_matrix)):
            if len(self.distance_matrix[idx]) != rows:
                err_msg = "RoutingModel - SetDistanceMatrix: invalid matrix size " + \
                    str(len(self.distance_matrix[idx]))
                logging.error(err_msg)
                raise Exception(err_msg)

        # Set distance matrix size
        self.distance_matrix_rows = rows
        self.distance_matrix_cols = rows

    def get_distance_matrix(self):
        return self.distance_matrix

    def get_distance_matrixs_rows(self):
        return self.distance_matrix_rows

    def get_distance_matrixs_cols(self):
        return self.distance_matrix_cols

    def serialize(self):
        """Serialization method: to be overriden by derived classes"""
        return self.to_protobuf().SerializeToString()

    def to_protobuf(self):
        """To protocol buffer method: to be overriden by derived classes"""
        raise Exception("RoutingModel - toProtobuf")

        optimizer_model = optimizer_model_pb2.OptimizerModel()
        if self.MPModel is not None:
            optimizer_model.linear_model.CopyFrom(self.MPModel.toProtobuf())
        elif self.MPModel_file_path.strip():
            optimizer_model.linear_model = linear_model_pb2.LinearModelSpecProto()
            optimizer_model.linear_model.model_path = self.MPModel_file_path
        else:
            err_msg = "OptimizerMPModel - Serialize: model not set"
            logging.error(err_msg)
            raise Exception(err_msg)

        # Set model name
        optimizer_model.linear_model.model_id = self.model_name

        # Set model and package type
        if self.model_type is OptimizerModelType.MIP:
            optimizer_model.linear_model.class_type = linear_model_pb2.LinearModelSpecProto.MIP
        elif self.class_type is OptimizerModelType.LP:
            optimizer_model.linear_model.class_type = linear_model_pb2.LinearModelSpecProto.LP
        elif self.class_type is OptimizerModelType.IP:
            optimizer_model.linear_model.class_type = linear_model_pb2.LinearModelSpecProto.IP
        else:
            err_msg = "OptimizerMPModel - Serialize: invalid model class type"
            logging.error(err_msg)
            raise Exception(err_msg)

        if self.package_type is OptimizerPackageType.SCIP:
            optimizer_model.linear_model.package_type = linear_model_pb2.LinearModelSpecProto.SCIP
        elif self.package_type is OptimizerPackageType.GLOP:
            optimizer_model.linear_model.package_type = linear_model_pb2.LinearModelSpecProto.OR_TOOLS_GLOP
        elif self.package_type is OptimizerPackageType.CLP:
            optimizer_model.linear_model.package_type = linear_model_pb2.LinearModelSpecProto.OR_TOOLS_CLP
        elif self.package_type is OptimizerPackageType.GLPK:
            optimizer_model.linear_model.package_type = linear_model_pb2.LinearModelSpecProto.OR_TOOLS_GLPK
        elif self.package_type is OptimizerPackageType.CBC:
            optimizer_model.linear_model.package_type = linear_model_pb2.LinearModelSpecProto.OR_TOOLS_CBC
        elif self.package_type is OptimizerPackageType.BOP:
            optimizer_model.linear_model.package_type = linear_model_pb2.LinearModelSpecProto.OR_TOOLS_BOP
        else:
            err_msg = "OptimizerMPModel - Serialize: invalid package type"
            logging.error(err_msg)
            raise Exception(err_msg)

        # Serialize the string
        return optimizer_model
