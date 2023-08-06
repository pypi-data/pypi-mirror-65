class OptObject:
    """OptiLab base class for any MP model object"""

    # Constraint's name
    name = ""

    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def to_protobuf(self):
        raise Exception("OptObject - toProtobuf: not implemented")

    def __str__(self):
        raise Exception("OptObject - __str__: not implemented")
