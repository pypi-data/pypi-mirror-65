from . import linear_model_pb2
from . import variables
import string
import sys


class OptConstraint:
    """OptiLab constraint class"""

    # Constraint's name
    name = ""

    # Constraint counter for creating unique constraint identifiers
    con_counter = 0

    # Flag for lazy constraints
    is_lazy = False

    def __init__(self, lb, ub, name=""):
        # List of variable indices and names of the i-th
        # linear term involved in this constraint
        self.var_index = []
        self.var_name = []

        # List of the coefficient corresponding to the variables in "var_index"
        self.coefficient = []

        if not name.strip():
            # Empty name, assign a default name
            self.name = "_c_" + str(OptConstraint.con_counter)
            OptConstraint.con_counter += 1
        else:
            self.name = name
        self.lower_bound = lb
        self.upper_bound = ub

    def add_scope_variable(self, var, coeff):
        if not isinstance(var, variables.OptVariable):
            err_msg = "OptConstraint - addVariable: invalid type " + type(var)
            logging.error(err_msg)
            raise Exception(err_msg)
        self.var_index.append(var.get_var_index())
        self.var_name.append(var.get_name())
        self.coefficient.append(coeff)

    def get_name(self):
        return self.name

    def get_lower_bound(self):
        return self.lower_bound

    def get_upper_bound(self):
        return self.upper_bound

    def to_protobuf(self):
        proto_con = linear_model_pb2.OptConstraintProto()
        proto_con.lower_bound = self.lower_bound
        proto_con.upper_bound = self.upper_bound
        proto_con.name = self.name
        proto_con.var_index.extend(self.var_index)
        proto_con.coefficient.extend(self.coefficient)
        proto_con.is_lazy = self.is_lazy
        return proto_con

    def __str__(self):
        con_pp = "con:\n\tname: " + self.name
        con_pp += "\n\tbounds: (" + str(self.lower_bound) + \
            ", " + str(self.upper_bound) + ")"
        con_pp += "\n\tscope:"
        con_pp += "\n\t " + str(self.var_name)
        con_pp += "\n\t " + str(self.coefficient)
        return con_pp
