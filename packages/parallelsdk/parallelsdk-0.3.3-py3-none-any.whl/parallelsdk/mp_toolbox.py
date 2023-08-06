from . import optimizer_mp_model
from .optimizer_mp_model import OptimizerModelType, OptimizerPackageType


def Infinity():
    return optimizer_mp_model.infinity()


def MPModel(model_name, model_type=optimizer_mp_model.OptimizerModelType.UNDEF):
    """Builds and returns a new instance of a Mathematical Programming (MP)
    model. The caller can specify the type of model (e.g., LP, MIP) which is,
    otherwise, inferred from the model itself.
    By default, the model type is undefined.
    """
    if not isinstance(model_type, optimizer_mp_model.OptimizerModelType):
        err_msg = "MPModel - invalid model type " + type(model_type)
        logging.error(err_msg)
        raise Exception(err_msg)
    mdl = optimizer_mp_model.OptimizerMPModel(model_name)
    mdl.set_model_type(optimizer_mp_model.OptimizerModelType.MIP)
    return mdl
