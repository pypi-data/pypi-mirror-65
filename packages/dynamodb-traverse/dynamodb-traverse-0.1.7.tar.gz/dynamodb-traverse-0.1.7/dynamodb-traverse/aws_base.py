import configparser
from os.path import expanduser

from .base import Base


class AWSBase(Base):
    """

    Basic AWS auth info

    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.my_aws_config = configparser.ConfigParser()
        self.my_aws_path = kwargs.pop(
            "my_aws_path", "/".join([expanduser("~"), ".aws/config"])
        )
        self.my_aws_config.read(self.my_aws_path)

        profile = kwargs.pop("profile", "default")
        self.my_aws_access_key_id = self.my_aws_config[profile]["aws_access_key_id"]
        self.my_aws_secret_access_key = self.my_aws_config[profile][
            "aws_secret_access_key"
        ]
        if "region" in self.my_aws_config[profile]:
            self.my_region = self.my_aws_config[profile]["region"]
        else:
            self.my_region = "us-east-1"
