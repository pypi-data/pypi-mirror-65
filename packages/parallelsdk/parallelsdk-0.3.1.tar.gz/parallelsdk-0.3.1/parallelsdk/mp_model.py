from . import linear_model_pb2
import logging
from . import constraints
from . import variables
import string
import sys


class OptMPModel():
    """OptiLab mathematical programming model class.

    MP models encapsulates the definition of any
    mathematical programming models including:
    - Linear Programming (LP)
    - Mixed Integer Programming (MIP)
    - Integer Programming (IP)
    """

    # Name of the model
    name = ""

    # Maximization vs minimization problem
    maximize = False

    # Offset on the objective function
    objective_offset = 0.0

    # Objective value set only after solvig the model
    objective_value = sys.float_info.min

    # Variable name to index map
    var_to_idx_map = {}

    # Constraint name to index map
    con_to_idx_map = {}

    def __init__(self, name, maximize=False, objective_offset=0.0):
        # List of variables in the model
        self.variable_list = []

        # List of constraint in the model
        self.constraint_list = []

        self.name = name
        self.maximize = maximize
        self.objective_offset = objective_offset

    def get_model_name(self):
        return self.name

    def clear(self):
        self.variable_list.clear()
        self.constraint_list.clear()

    def set_objective_value(self, val):
        self.objective_value = val

    def get_objective_value(self):
        return self.objective_value

    def get_num_variables(self):
        return len(self.variable_list)

    def add_variable(self, var):
        if not isinstance(var, variables.OptVariable):
            err_msg = "OptMPModel - addVariable: invalid type " + type(var)
            logging.error(err_msg)
            raise Exception(err_msg)
        var.set_var_index(len(self.variable_list))
        self.var_to_idx_map[var.get_name()] = var.get_var_index()
        self.variable_list.append(var)

    def remove_variable(self, var):
        if not isinstance(var, variables.OptVariable):
            err_msg = "OptMPModel - removeVariables: invalid type " + type(var)
            logging.error(err_msg)
            raise Exception(err_msg)
        self.var_to_idx_map.remove(var.get_name())
        self.variable_list.remove(var)
        idx = 0
        for v in self.variable_list:
            v.set_var_index(idx)
            idx += 1

    def get_variable_from_name(self, var_name):
        return self.variable_list[self.var_to_idx_map[var_name]]

    def get_variable(self, idx):
        return self.variable_list[idx]

    def get_num_constraints(self):
        return len(self.constraint_list)

    def get_constraint_from_name(self, con_name):
        return self.constraint_list[self.con_to_idx_map[con_name]]

    def add_constraint(self, con):
        if not isinstance(con, constraints.OptConstraint):
            err_msg = "OptMPModel - addConstraint: invalid type " + type(con)
            logging.error(err_msg)
            raise Exception(err_msg)
        self.con_to_idx_map[con.get_name()] = len(self.constraint_list)
        self.constraint_list.append(con)

    def remove_constraint(self, con):
        if not isinstance(con, constraints.OptConstraint):
            err_msg = "OptMPModel - removeConstraint: invalid type " + \
                type(con)
            logging.error(err_msg)
            raise Exception(err_msg)
        self.con_to_idx_map.remove(con.get_name())
        self.constraint_list.remove(con)

    def get_constraint(self, idx):
        return self.constraint_list[idx]

    def set_objective_direction(self, maximize):
        self.maximize = maximize

    def is_maximization(self):
        return self.maximize

    def set_objective_offset(self, offset):
        self.objective_offset = offset

    def get_objective_offset(self):
        return self.objective_offset

    def to_string(self):
        model_pp = "model:\n\tid: " + self.name + "\n"
        model_pp += "\tmaximize: " + str(self.maximize) + "\n"
        model_pp += "\tnum. variables: " + str(len(self.variable_list)) + "\n"
        model_pp += "\tnum. constraint: " + \
            str(len(self.constraint_list)) + "\n"
        return model_pp

    def to_protobuf(self):
        proto_model_spec = linear_model_pb2.LinearModelSpecProto()
        proto_model = proto_model_spec.model

        # Set model parameters
        proto_model.maximize = self.maximize
        proto_model.objective_offset = self.objective_offset
        proto_model.name = self.name

        # Add variables into the model
        for var in self.variable_list:
            proto_var = proto_model.variable.add()
            proto_var.CopyFrom(var.to_protobuf())

        for con in self.constraint_list:
            proto_con = proto_model.constraint.add()
            proto_con.CopyFrom(con.to_protobuf())

        return proto_model_spec
