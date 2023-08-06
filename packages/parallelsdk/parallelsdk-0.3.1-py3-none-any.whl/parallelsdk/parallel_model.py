from . import optilab_pb2


class ParallelModel:
    def __init__(self, fname):
        self.name = fname

    def get_name(self):
        return self.name

    def on_message(self, proto_message):
        rep_msg = optilab_pb2.OptiLabReplyMessage()
        rep_msg.ParseFromString(proto_message)
        msg_type = rep_msg.type
        if msg_type == optilab_pb2.OptiLabReplyMessage.Metrics:
            met_msg = optilab_pb2.OptimizerMetricsRep()
            if rep_msg.details.Is(optilab_pb2.OptimizerMetricsRep.DESCRIPTOR):
                rep_msg.details.Unpack(met_msg)
            else:
                logging.error(
                    "ParallelModel - OnMessage: invalid metrics type message")
                print("Error on receiving metrics from the back-end")
            print(met_msg.metrics)
        elif msg_type == optilab_pb2.OptiLabReplyMessage.Metadata:
            mtd_msg = optilab_pb2.OptimizerMetadataRep()
            if rep_msg.details.Is(optilab_pb2.OptimizerMetadataRep.DESCRIPTOR):
                rep_msg.details.Unpack(mtd_msg)
            else:
                logging.error(
                    "ParallelModel - OnMessage: invalid metadata type message")
                print("Error on receiving meta-data from the back-end")
            print(mtd_msg.metadata)
        elif msg_type == optilab_pb2.OptiLabReplyMessage.Solution:
            self.on_message_impl(rep_msg)
        else:
            logging.error(
                "ParallelModel - OnMessage: received invalid message type")
            print("Unrecognized message type received from the back-end")

    def on_message_impl(self, optilab_reply_message):
        raise Exception("ParallelModel - OnMessage: requires implementation")
