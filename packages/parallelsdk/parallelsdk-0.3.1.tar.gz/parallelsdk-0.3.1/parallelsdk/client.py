from . import frontend_client_runner
import time

k_opti_lab_socket_port = 8080


class ParallelClient():
    address = ""
    port = -1
    client_runner = None
    use_protobuf = True

    def __init__(self, addr, port=k_opti_lab_socket_port, use_protobuf=True):
        # Set the address
        self.address = addr

        # Set port if defined, otherwise use standard port 8080
        self.port = port

        # Set use of protobuf as communication protocol
        self.use_protobuf = use_protobuf

    def connect(self):
        """Connect Parallel front-end interface to the service"""
        self.client_runner = frontend_client_runner.FrontendClientRunner(
            self.address,
            self.port,
            self.use_protobuf)
        connected = self.client_runner.connect_to_server()
        print('Connecting front-end to Parallel platform...')
        time.sleep(1.5)
        if not connected:
            raise Exception('Cannot connect to the Parallel service.')

    def disconnect(self):
        """Disconnect Parallel front-end interface from the service"""
        self.client_runner.disconnect_from_server()

    def run_optimizer(self, model):
        """Sends the given model to the Parallel back-end service.

        Creates back-end optimizers and run the service on the serialized
        model provided by the caller.
        """
        if self.client_runner is None:
            raise Exception(
                'Parallel is not connected to the service, return.')
        self.client_runner.send_message_to_backend_server(model)
