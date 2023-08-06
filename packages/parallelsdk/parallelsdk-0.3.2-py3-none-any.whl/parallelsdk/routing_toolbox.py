from OptimizerRoutingModel import RoutingEngineType
import VRPRoutingModel


def VRPModel(name):
    """Returns a new instance of a routing VRP"""
    mdl = VRPRoutingModel.VRPRoutingModel(name)
    return mdl
