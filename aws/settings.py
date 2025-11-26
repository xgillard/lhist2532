"""Settings for the AWS management scripts."""

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    """Settings of the deployment.

    Attributes:
        repo_url (str): url of the repository to clone
        aws_key_name (str): name of the ssh key to use to connect to instance
        aws_key_path (str): path to the local file containing the private key
            required to establish an ssh connection to the instance

        aws_region (str): the deployment zone for our EC2 instance
        aws_instance_type (str): the instance type.
        aws_ami_id (str): defaults to Ubuntu.

        aws_role_name (str): role that will be created for this instance
        aws_profile (str):
        aws_security_group_name (str):

        secret (dict[str, str]): the list of secrets that must be pushed
            to AWS using AWS secrets management.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf8",
        env_nested_delimiter="__",
    )

    repo_url: str = "https://github.com/xgillard/lhist2532.git"
    aws_key_name: str = "labo-ia-archives-key"
    aws_key_path: str = "./labo-ia-archives-key.pem"
    aws_region: str = "eu-west-3"
    aws_instance_type: str = "m5.xlarge"
    aws_ami_id: str = "ami-0ef9bcd5dfb57b968"  # Ubuntu

    aws_role_name: str = "labo-ia-archives-role"
    aws_profile_name: str = "labo-ia-archives-profile"
    aws_security_group_name: str = "labo-ia-archives-sggroup"

    secret: dict[str, str] = dict()

    @property
    def aws_secrets(self) -> dict[str, str]:
        """Create the dictionary of AWS secrets to use."""

        return {k.upper(): v for k, v in self.secret.items()}
