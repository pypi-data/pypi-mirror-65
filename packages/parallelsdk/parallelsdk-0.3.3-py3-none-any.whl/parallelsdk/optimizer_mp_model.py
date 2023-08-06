from enum import Enum
from .import linear_model_pb2
import logging
from . import constraints
from . import optilab_pb2
from . import optimizer_model_pb2
from . import mp_model
from . import variables
from . import parallel_model
import string
import sys

from sympy.core.add import Add
from sympy.core.mul import Mul
from sympy.core.relational import GreaterThan, StrictGreaterThan, LessThan, StrictLessThan


class OptimizerModelType(Enum):
    MIP = 1
    LP = 2
    IP = 3
    UNDEF = 4


class OptimizerPackageType(Enum):
    GLOP = 1
    CLP = 2
    CBC = 3
    SCIP = 4
    GLPK = 5


def infinity():
    return sys.float_info.max


class OptimizerMPModel(parallel_model.ParallelModel):
    """OptiLab Mathematical Programming (MP) model
    solved by back-end optimizers"""

    variable_limit = 100
    constraint_limit = 100
    mp_model = None
    mp_model_file_path = ""
    model_type = None
    package_type = None
    model_name = ""
    model_status = None

    # Model type:
    # - 0b00: default
    # - 0b10: LP (all linear variables)
    # - 0b01: IP (all integer variables)
    # - 0b11: MIP (LP + IP)
    model_user_type = 0b00

    def __init__(self, name=""):
        super().__init__(name)
        """Generates a new model
        If the name is provided, creates a new OptiLab model.
        Otherwise creates an empty model instance and the caller must use
        BuildModel(...) or LoadFromFile(...) to build or load resp. a model.
        """
        self.model_name = name
        if name.strip():
            self.mp_model = mp_model.OptMPModel(name)
        # Default package is SCIP
        self.package_type = OptimizerPackageType.SCIP

    def on_message_impl(self, optilab_reply_message):
        if optilab_reply_message.details.Is(
                optilab_pb2.OptimizerSolutionRep.DESCRIPTOR):
            # JSON solutions are printed verbatim on the screen
            sol_msg = optilab_pb2.OptimizerSolutionRep()
            optilab_reply_message.details.Unpack(sol_msg)
            print(sol_msg.solution)
        elif optilab_reply_message.details.Is(linear_model_pb2.LinearModelSolutionProto.DESCRIPTOR):
            # Capture the protobuf solution
            sol_proto = linear_model_pb2.LinearModelSolutionProto()
            optilab_reply_message.details.Unpack(sol_proto)
            self.upload_proto_solution(sol_proto)

    def get_model_status(self):
        return self.status_to_string(self.model_status)

    def get_objective_value(self):
        return self.mp_model.get_objective_value()

    def status_to_string(self, status):
        if status is None:
            return "SOLVER_UNKNOWN_STATUS"
        else:
            return linear_model_pb2.LinearModelSolutionStatusProto.Name(status)

    def build_model_from_solution(self, linear_model_solution_proto):
        self.mp_model = OptMPModel.OptMPModel(self.model_name)

        # Set the objective value
        self.mp_model.set_objective_value(
            linear_model_solution_proto.objective_value)

        # Set variable values
        if self.model_status == linear_model_pb2.LinearModelSolutionStatusProto.Value('SOLVER_FEASIBLE') or \
            self.model_status == linear_model_pb2.LinearModelSolutionStatusProto.Value('SOLVER_OPTIMAL'):
            for proto_var in linear_model_solution_proto.variable_assign:
                var = self.NumVar(proto_var.var_value[0], proto_var.var_value[0], proto_var.var_name)
                var.set_solution_value(proto_var.var_value[0])

    def upload_proto_solution(self, linear_model_solution_proto):
        # Set the model's status
        self.model_status = linear_model_solution_proto.status

        if self.mp_model is None:
            self.build_model_from_solution(linear_model_solution_proto)
        else:
            # Set the objective value
            self.mp_model.set_objective_value(
                linear_model_solution_proto.objective_value)

            # Set variable values
            if self.model_status == linear_model_pb2.LinearModelSolutionStatusProto.Value('SOLVER_FEASIBLE') or \
                self.model_status == linear_model_pb2.LinearModelSolutionStatusProto.Value('SOLVER_OPTIMAL'):
                for proto_var in linear_model_solution_proto.variable_assign:
                    var = self.mp_model.get_variable_from_name(proto_var.var_name)
                    var.set_solution_value(proto_var.var_value[0])

        # Notify the user about model upload
        print("MIPModel - solution uploaded")

    def set_model_type(self, model_type):
        """Forces the model to be of a specific type"""
        if not isinstance(model_type, OptimizerModelType):
            err_msg = "OptimizerMPModel - SetModelType: invalid model type " + \
                type(model_type)
            logging.error(err_msg)
            raise Exception(err_msg)
        self.model_type = model_type
        if model_type == OptimizerModelType.MIP:
            self.model_user_type = 0b11
        elif model_type == OptimizerModelType.IP:
            self.model_user_type = 0b01
        elif model_type == OptimizerModelType.LP:
            self.model_user_type = 0b10
        else:
            self.model_user_type = 0b00

    def get_model_type(self):
        """Returns the type of this model"""
        if self.model_user_type == 0b11:
            return OptimizerModelType.MIP
        elif self.model_user_type == 0b01:
            return OptimizerModelType.IP
        elif self.model_user_type == 0b10:
            return OptimizerModelType.LP
        else:
            return OptimizerModelType.UNDEF

    def supported_solvers(self):
        if self.model_user_type == 0b11 or self.model_user_type == 0b01:
            # MIP solvers and IP solvers
            return [
                OptimizerPackageType.CBC,
                OptimizerPackageType.SCIP,
                OptimizerPackageType.GLPK]
        elif self.model_user_type == 0b10:
            # LP solvers
            return [
                OptimizerPackageType.GLOP,
                OptimizerPackageType.CLP,
                OptimizerPackageType.GLPK]
        else:
            raise Exception(
                "OptimizerMPModel - SupportedSolvers: undefined model")

    def set_package_type(self, package_type):
        if not isinstance(package_type, OptimizerPackageType):
            err_msg = "OptimizerMPModel - SetPackageType: invalid model type " + \
                type(package_type)
            logging.error(err_msg)
            raise Exception(err_msg)
        self.package_type = package_type

    def set_solver(self, solver_type):
        self.set_package_type(solver_type)

    def build_model(self, name):
        if not name.strip():
            err_msg = "OptimizerMPModel - BuildNewModel: empty model name"
            logging.error(err_msg)
            raise Exception(err_msg)
        self.mp_model_file_path = None
        self.mp_model = OptMPModel.OptMPModel(name)

    def load_model_from_file(self, file_path, name):
        if not name.strip():
            err_msg = "OptimizerMPModel - LoadFromFile: empty model name"
            logging.error(err_msg)
            raise Exception(err_msg)
        self.mp_model = None
        self.mp_model_file_path = file_path

    def clear(self):
        """Clears the model"""
        self.mp_model.clear()

    def num_variables(self):
        """Returns the number of variables in the model"""
        return self.mp_model.get_num_variables()

    def num_constraints(self):
        """Returns the number of constraints in the modelw"""
        return self.mp_model.get_num_constraints()

    def get_variable(self, name):
        """Returns a variable given its name"""
        return self.mp_model.get_variable_from_name(name)

    def BoolVar(self, name=""):
        """Creates, adds to the model, and returns a Boolean variable"""
        if len(self.mp_model.variable_list) >= self.variable_limit:
            raise(OverflowError("maximum variable limit exceeded"))
        var = variables.OptVariable(0.0, 1.0, True, name)
        self.mp_model.add_variable(var)
        self.model_user_type = self.model_user_type | 0b01
        return var

    def IntVar(self, lower_bound, upper_bound, name=""):
        """Creates, adds to the model, and returns an Integer variable"""
        if len(self.mp_model.variable_list) >= self.variable_limit:
            raise(OverflowError("maximum variable limit exceeded"))
        var = variables.OptVariable(lower_bound, upper_bound, True, name)
        var = variables.OptVariable(lower_bound, upper_bound, True, name)
        self.mp_model.add_variable(var)
        self.model_user_type = self.model_user_type | 0b01
        return var

    def NumVar(self, lower_bound, upper_bound, name=""):
        """Creates, adds to the model, and returns a numeric continuous variable"""
        if len(self.mp_model.variable_list) >= self.variable_limit:
            raise(OverflowError("maximum variable limit exceeded"))
        var = variables.OptVariable(lower_bound, upper_bound, False, name)
        self.mp_model.add_variable(var)
        self.model_user_type = self.model_user_type | 0b10
        return var

    def get_constraint(self, name):
        """Returns a constraint given its name"""
        return self.mp_model.get_constraint_from_name(name)

    def Constraint(self, *args, **kwargs):
        """Creates, adds to the model, and returns a constraint
        specified either as an expression, or as follows:
        lower_bound <= varList * coeffList <= upper_bound
        """
        name = kwargs["name"] if "name" in kwargs else ""
        if len(args) == 1:
            # PASSED expr
            expr = args[0]

            # TODO: switch sympy dependency to parser library, to allow
            # for bidirectional inequalities.
            if len(self.mp_model.constraint_list) >= self.constraint_limit:
                raise(OverflowError("maximum constraint limit exceeded"))
            if isinstance(expr, (GreaterThan, StrictGreaterThan)):
                var_expr, bound = expr.args
                con = constraints.OptConstraint(bound, infinity(), name)
            elif isinstance(expr, (LessThan, StrictLessThan)):
                var_expr, bound = expr.args
                con = constraints.OptConstraint(-infinity(), bound, name)
            else:
                raise ValueError("expression must be an inequality")
            for term in var_expr.args:
                if isinstance(term, variables.OptVariable):
                    con.add_scope_variable(term, 1)
                else:
                    coeff, var = term.args
                    con.add_scope_variable(var, coeff)

            self.mp_model.add_constraint(con)
            return con
        elif len(args) <= 4:
            # PASSED var_list AND coeff_list

            # validate argument types and parse from args/kwargs
            var_list, coeff_list = args[0], args[1]
            if len(args) == 2:
                lower_bound = kwargs["lower_bound"] if "lower_bound" in kwargs else -infinity()
                upper_bound = kwargs["upper_bound"] if "upper_bound" in kwargs else infinity(
                )
            elif len(args) == 4:
                lower_bound = args[2]
                upper_bound = args[3]
                if "lower_bound" in kwargs:
                    raise TypeError(
                        "Constraint() got multiple values for argument 'lower_bound'")
                elif "upper_bound" in kwargs:
                    raise TypeError(
                        "Constraint() got multiple values for argument 'upper_bound'")
            else:
                raise TypeError(
                    "Constraint() requires both 'lower_bound' and 'upper_bound' when specified as positional arguments")

            # add constraint
            con = constraints.OptConstraint(lower_bound, upper_bound, name)
            if len(var_list) != len(coeff_list):
                err_msg = "OptimizerMPModel - Constraint: variable and coefficient lists lengths not matching"
                logging.error(err_msg)
                raise Exception(err_msg)
            for idx in range(0, len(var_list)):
                if not isinstance(var_list[idx], variables.OptVariable):
                    err_msg = "OptimizerMPModel - Constraint: invalid type (expected variable) " + type(
                        var_list[idx])
                    logging.error(err_msg)
                    raise Exception(err_msg)
                con.add_scope_variable(var_list[idx], coeff_list[idx])
            self.mp_model.add_constraint(con)
            return con
        else:
            raise TypeError(
                "Constraint() received too many positional arguments")

    def Objective(self, *args, maximize=False):
        """Specifies the objective function either as an expression, or as:
        [maximize | minimize] varList * coeffList
        """
        if len(args) == 1:
            # PASSED expr
            expr = args[0]

            if isinstance(expr, Add):
                for term in expr.args:
                    if isinstance(term, variables.OptVariable):
                        term.set_objective_coefficient(1)
                    else:
                        coeff, var = term.args
                        var.set_objective_coefficient(coeff)
            elif isinstance(expr, Mul):
                coeff, var = term.args
                var.set_objective_coefficient(coeff)
            elif isinstance(expr, variables.OptVariable):
                expr.set_objective_coefficient(1)
            else:
                raise ValueError("expression must be an inequality")
            self.mp_model.set_objective_direction(maximize)
        elif len(args) == 2:
            # PASSED var_list AND coeff_list
            var_list, coeff_list = args
            if len(var_list) != len(coeff_list):
                err_msg = "OptimizerMPModel - Objective: variable and coefficient lists lengths not matching"
                logging.error(errMsg)
                raise Exception(errMsg)
            for idx in range(0, len(var_list)):
                if not isinstance(var_list[idx], variables.OptVariable):
                    err_msg = "OptimizerMPModel - Objective: invalid type (expected variable) " + type(
                        var_list[idx])
                    logging.error(err_msg)
                    raise Exception(err_msg)
                var_list[idx].set_objective_coefficient(coeff_list[idx])
            self.mp_model.set_objective_direction(maximize)
        else:
            raise TypeError(
                "Constraint() received too many positional arguments")

    def Maximize(self, *args):
        self.Objective(*args, maximize=True)

    def Minimize(self, *args):
        self.Objective(*args, maximize=False)

    def serialize(self):
        return self.to_protobuf().SerializeToString()

    def to_protobuf(self):
        optimizer_model = optimizer_model_pb2.OptimizerModel()
        if self.mp_model is not None:
            optimizer_model.linear_model.CopyFrom(self.mp_model.to_protobuf())
        elif self.mp_model_file_path.strip():
            tmp_mdl = linear_model_pb2.LinearModelSpecProto()
            optimizer_model.linear_model.CopyFrom(tmp_mdl);
            optimizer_model.linear_model.model_path = self.mp_model_file_path
        else:
            err_msg = "OptimizerMPModel - Serialize: model not set"
            logging.error(err_msg)
            raise Exception(err_msg)

        # Set model name
        optimizer_model.linear_model.model_id = self.model_name

        # Set model and package type
        m_type = self.get_model_type()
        if m_type is OptimizerModelType.MIP:
            optimizer_model.linear_model.class_type = linear_model_pb2.LinearModelSpecProto.MIP
        elif m_type is OptimizerModelType.LP:
            optimizer_model.linear_model.class_type = linear_model_pb2.LinearModelSpecProto.LP
        elif m_type is OptimizerModelType.IP:
            optimizer_model.linear_model.class_type = linear_model_pb2.LinearModelSpecProto.IP
        else:
            err_msg = "OptimizerMPModel - Serialize: invalid model type"
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
        else:
            err_msg = "OptimizerMPModel - Serialize: invalid package type"
            logging.error(err_msg)
            raise Exception(err_msg)

        # Serialize the string
        return optimizer_model
