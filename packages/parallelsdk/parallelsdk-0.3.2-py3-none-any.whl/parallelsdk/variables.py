from . import linear_model_pb2
from . import objects
import string
import sys
from sympy import Symbol


class OptVariable(Symbol):
    """OptiLab variable class"""

    name = ""
    branching_priority = 0
    lower_bound = -sys.float_info.max
    upper_bound = sys.float_info.max
    is_integer = False
    solution_value = -sys.float_info.max
    reduced_cost = -sys.float_info.max
    var_counter = 0
    objective_coefficient = 0.0
    var_index = -1

    def __new__(cls, lb, ub, is_integer, name=""):
        """ defined because sympy.Symbol defines __new__ """
        if not name.strip():
            # Empty name, assign a default name
            name = "_v_" + str(OptVariable.var_counter)
            OptVariable.var_counter += 1
        return Symbol.__new__(cls, name)

    def __init__(self, lb, ub, is_integer, name=""):
        # don't do anything with name b/c it was taken care of in __new__
        self.lower_bound = lb
        self.upper_bound = ub
        self.is_integer = is_integer
        self.objective_coefficient = 0.0

    def set_objective_coefficient(self, val):
        self.objective_coefficient = val

    def get_objective_coefficient(self):
        return self.objective_coefficient

    def set_var_index(self, idx):
        self.var_index = idx

    def get_var_index(self):
        return self.var_index

    def get_name(self):
        return self.name

    def get_lower_bound(self):
        return self.lower_bound

    def get_upper_bound(self):
        return self.upper_bound

    def is_integer(self):
        return self.is_integer

    def set_branching_priority(self, bprior):
        self.branching_priority = bprior

    def get_branching_priority(self):
        return self.branching_priority

    def get_solution_value(self):
        if self.solution_value < self.lower_bound or self.solution_value > self.upper_bound:
            return "N/A"
        return self.solution_value

    def set_solution_value(self, val):
        self.solution_value = val

    def lock_solution_value(self):
        self.lower_bound = self.solution_value
        self.upper_bound = self.solution_value

    def get_reduced_cost(self):
        return self.reduced_cost

    def set_reduced_cost(self, val):
        self.reduced_cost = val

    def to_protobuf(self):
        proto_var = linear_model_pb2.OptVariableProto()
        proto_var.lower_bound = self.lower_bound
        proto_var.upper_bound = self.upper_bound
        proto_var.is_integer = self.is_integer
        proto_var.name = self.name
        proto_var.branching_priority = self.branching_priority
        proto_var.objective_coefficient = self.objective_coefficient
        return proto_var

    def __str__(self):
        var_pp = "var:\n\tname: " + self.name
        var_pp += "\n\tsolution value: " + str(self.get_solution_value())
        var_pp += "\n\tis integer: " + str(self.is_integer)
        if self.is_integer:
            var_pp += "\n\tdomain: [" + str(self.lower_bound) + \
                ", " + str(self.upper_bound) + "]"
        else:
            var_pp += "\n\tdomain: (" + str(self.lower_bound) + \
                ", " + str(self.upper_bound) + ")"
        var_pp += "\n\tbranching priority: " + str(self.branching_priority)
        if self.objective_coefficient != 0.0:
            var_pp += "\n\tobjective coefficient: " + \
                str(self.objective_coefficient)
        return var_pp
