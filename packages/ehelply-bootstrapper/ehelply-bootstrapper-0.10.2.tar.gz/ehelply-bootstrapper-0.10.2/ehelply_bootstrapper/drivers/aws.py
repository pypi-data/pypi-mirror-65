import boto3

from ehelply_bootstrapper.utils.connection_details import ConnectionDetails
from ehelply_bootstrapper.drivers.driver import Driver


class AWS(Driver):

    def __init__(self, connection_details: ConnectionDetails = None, verbosity: int = 0):
        from ehelply_bootstrapper.utils.state import State
        super().__init__(connection_details, verbosity)
        self.aws_access_key_id = State.config.aws.auth.access_key_id
        self.aws_secret_access_key = State.config.aws.auth.access_key

    def make_client(self, name: str, region_name: str = 'ca-central-1'):
        return boto3.client(name, region_name=region_name, aws_access_key_id=self.aws_access_key_id,
                            aws_secret_access_key=self.aws_secret_access_key)

    def make_resource(self, name: str, region_name: str = 'ca-central-1'):
        return boto3.resource(name, region_name=region_name, aws_access_key_id=self.aws_access_key_id,
                              aws_secret_access_key=self.aws_secret_access_key)
