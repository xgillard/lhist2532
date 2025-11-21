"""The script to activate / teardown an AWS instance with my streamlit app."""

import boto3
from settings import Settings
from pathlib import Path
import time

import json


def user_data() -> str:
    """Return all the user data we want to use to kickstart the app."""

    return Path("./user_data.sh").open("r", encoding="utf8").read()


def create_secrets(cfg: Settings):
    """Create the secrets"""

    secrets = boto3.client(
        "secretsmanager",
        region_name=cfg.aws_zone,
    )

    for k, v in cfg.aws_secrets.items():
        try:
            secrets.create_secret(Name=k, SecretString=v)
        except Exception as e:
            print(f"{str(e)}")


def create_profile_role(cfg: Settings) -> str:
    iam = boto3.client(
        "iam",
        region_name=cfg.aws_zone,
    )
    ec2 = boto3.client(
        "ec2",
        region_name=cfg.aws_zone,
    )

    # role
    try:
        iam.create_role(
            RoleName=cfg.aws_role_name,
            AssumeRolePolicyDocument=json.dumps(
                {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {"Service": "ec2.amazonaws.com"},
                            "Action": "sts:AssumeRole",
                        }
                    ],
                }
            ),
        )
    except Exception as e:
        print(f"{str(e)}")

    # policy
    try:
        iam.attach_role_policy(
            RoleName=cfg.aws_role_name,
            PolicyArn="arn:aws:iam::aws:policy/SecretsManagerReadWrite",
        )
    except Exception as e:
        print(f"{str(e)}")

    # profile
    try:
        iam.create_instance_profile(
            InstanceProfileName=cfg.aws_profile_name,
        )
    except Exception as e:
        print(f"{str(e)}")

    try:
        iam.add_role_to_instance_profile(
            InstanceProfileName=cfg.aws_profile_name,
            RoleName=cfg.aws_role_name,
        )
    except Exception as e:
        print(f"{str(e)}")
    time.sleep(10)  # Indispensable car IAM est "eventually consistent"

    # 3. Security Group
    sg = ec2.create_security_group(
        GroupName=cfg.aws_security_group_name,
        Description="Streamlit Lab Access",
    )
    sg_id = sg["GroupId"]
    return sg_id


def create_ec2_instance(cfg: Settings, sg_id: str):
    ec2 = boto3.client(
        "ec2",
        region_name=cfg.aws_zone,
    )
    ec2.authorize_security_group_ingress(
        GroupId=sg_id,
        IpPermissions=[
            {
                "IpProtocol": "tcp",
                "FromPort": 80,
                "ToPort": 80,
                "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
            },
        ],
    )
    instances = ec2.run_instances(
        ImageId=cfg.aws_ami_id,
        InstanceType=cfg.aws_instance_type,
        KeyName=cfg.aws_key_name,
        MinCount=1,
        MaxCount=1,
        SecurityGroupIds=[sg_id],
        IamInstanceProfile={"Name": cfg.aws_profile_name},
        UserData=user_data(),
    )
    instance_id = instances["Instances"][0]["InstanceId"]
    waiter = ec2.get_waiter("instance_running")
    waiter.wait(InstanceIds=[instance_id])

    desc = ec2.describe_instances(InstanceIds=[instance_id])
    public_ip = desc["Reservations"][0]["Instances"][0]["PublicIpAddress"]
    print(f"PUBLIC IP http://{public_ip}")


def main():
    cfg = Settings()

    create_secrets(cfg)
    sgid = create_profile_role(cfg)
    create_ec2_instance(cfg, sgid)


if __name__ == "__main__":
    main()
