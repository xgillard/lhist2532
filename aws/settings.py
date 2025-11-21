"""Settings for the AWS management scripts."""

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    """Settings of the deployment.

    Attributes:
        aws_zone (str): the deployment zone for our EC2 instance
        aws_instance_type (str): the instance type (I chose a free one, pick
            whatever you want).
        aws_ami_id (str): defaults to Ubuntu. Pick the latest Ubuntu that is
            available and eligible for free tier.
        secret (dict[str, str]): the list of secrets that must be pushed
            to AWS using AWS secrets management.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf8",
        env_nested_delimiter="__",
    )

    aws_key_name: str = "labo-ia-archives-key"
    aws_zone: str = "eu-west-3"
    aws_instance_type: str = "t3.micro"
    aws_ami_id: str = "ami-0ef9bcd5dfb57b968"  # Ubuntu

    aws_role_name: str = "labo-ia-archives-role"
    aws_profile_name: str = "labo-ia-archives-profile"
    aws_security_group_name: str = "labo-ia-archives-sggroup"

    secret: dict[str, str] = dict()

    @property
    def aws_secrets(self) -> dict[str, str]:
        """Create the dictionary of AWS secrets to use."""

        return {k.upper(): v for k, v in self.secret.items()}
