#! /usr/bin/python3

"""
Ce script sert à faire un déploiement (et configuration y compris des
secrets sur AWS sans avoir à passer par le AWS secretmanager qui coute plus
cher que le compute qu'on loue (t3.micro).
"""

import os
import boto3
import time
from botocore.client import ClientError
import paramiko

from settings import Settings
from textwrap import dedent

SETTINGS = Settings()

# --- CONFIGURATION ---
AWS_REGION = SETTINGS.aws_region
AMI_ID = SETTINGS.aws_ami_id
INSTANCE_TYPE = SETTINGS.aws_instance_type
KEY_NAME = SETTINGS.aws_key_name
KEY_PATH = SETTINGS.aws_key_path
REPO_URL = SETTINGS.repo_url

# Vos secrets locaux
SECRETS = SETTINGS.secret

ec2 = boto3.client("ec2", region_name=AWS_REGION)


def manage_ssh_key():
    """
    Crée la clé SSH sur AWS et sauvegarde le fichier .pem localement.
    Gère le cas où la clé existe déjà sur AWS mais qu'on a perdu le fichier local.
    """
    print(f"🔑 Gestion de la clé SSH '{KEY_NAME}'...")

    try:
        # 1. Tentative de création
        key_pair = ec2.create_key_pair(KeyName=KEY_NAME)

        # 2. Si succès, on récupère le contenu (KeyMaterial)
        private_key = key_pair["KeyMaterial"]

        # 3. Sauvegarde locale
        with open(KEY_PATH, "w") as f:
            f.write(private_key)

        # 4. Permissions strictes (Indispensable pour SSH/Paramiko)
        # 0o400 = Lecture seule pour le propriétaire, rien pour les autres
        os.chmod(KEY_PATH, 0o400)

        print(f"   ✅ Clé créée et sauvegardée dans : {KEY_PATH}")

    except ClientError as e:
        if "InvalidKeyPair.Duplicate" in str(e):
            # La clé existe déjà chez AWS
            if os.path.exists(KEY_PATH):
                print("   ℹ️  La clé existe déjà sur AWS et localement. On continue.")
            else:
                # CAS CRITIQUE : AWS a la clé, mais nous on a perdu le fichier .pem
                # Impossible de récupérer la clé privée chez AWS. Il faut détruire et recréer.
                print("   ⚠️  Clé présente sur AWS mais fichier local INTROUVABLE.")
                print("   ♻️  Suppression de l'ancienne clé AWS et recréation...")
                ec2.delete_key_pair(KeyName=KEY_NAME)
                # On rappelle la fonction récursivement pour recréer
                return manage_ssh_key()
        else:
            raise e


def run_ssh_command(ssh, command, description):
    """Exécute une commande et affiche le résultat en temps réel"""
    print(f"🔹 {description}...")
    _, stdout, stderr = ssh.exec_command(command)

    # On attend la fin de la commande et on récupère le code de retour
    exit_status = stdout.channel.recv_exit_status()

    if exit_status != 0:
        error_msg = stderr.read().decode()
        print(f"❌ ERREUR sur : {command}")
        print(error_msg)
        raise Exception(f"Command failed: {description}")
    else:
        print("   ✅ OK")


def install_via_ssh(ip):
    print(f"\n🔌 Connexion SSH à {ip}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Boucle de connexion (car le SSH met du temps à démarrer)
    connected = False
    for i in range(20):
        try:
            ssh.connect(ip, username="ubuntu", key_filename=KEY_PATH, timeout=5)
            connected = True
            break
        except:
            print(f"   ... en attente du SSH ({i + 1}/20)")
            time.sleep(5)

    if not connected:
        raise Exception("Impossible de se connecter en SSH.")

    # 0. Création du Swap (CRUCIAL pour t3.micro)
    print("🧠 Création du Swap (4Go)...")
    swap_cmd = dedent("""
        if [ ! -f /swapfile ]; then
            sudo fallocate -l 4G /swapfile
            sudo chmod 600 /swapfile
            sudo mkswap /swapfile
            sudo swapon /swapfile
        fi
    """).strip()
    run_ssh_command(ssh, swap_cmd, "Activation Swap")

    print("🚀 Début de l'installation...")

    # 1. Mise à jour système et dépendances
    run_ssh_command(
        ssh,
        "sudo apt-get update && sudo apt-get install -y python3-pip python3-venv git nginx",
        "Installation des paquets système",
    )

    # 2. Clonage du Repo (Simple, on est déjà user ubuntu !)
    # Le 'rm -rf' permet de relancer le script plusieurs fois sans erreur
    run_ssh_command(ssh, f"git clone {REPO_URL}", "Clonage du dépôt Git")

    # 3. Injection du .env
    # On construit la string des variables
    env_content = "\n".join([f"{k}={v}" for k, v in SECRETS.items()])
    # On écrit le fichier directement
    sftp = ssh.open_sftp()
    with sftp.file("/home/ubuntu/lhist2532/labo/.env", "w") as f:
        f.write(env_content)
    sftp.close()
    print("   ✅ Secrets injectés (.env)")

    # 4. Installation UV et Environnement Python
    cmd_python = "curl -LsSf https://astral.sh/uv/install.sh | sh "
    run_ssh_command(ssh, cmd_python, "Installation UV")

    # 4bis. Sync de l'environnement.
    cmd_python = dedent("""
        export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH" \
        && cd lhist2532/labo \
        && uv venv \
        && uv sync
    """).strip()
    run_ssh_command(ssh, cmd_python, "Pull dependencies")

    # 5. Configuration Nginx (Avec l'astuce 'sudo tee')
    nginx_conf = dedent("""
        server {
            listen 80;
            server_name _;
            location / {
                proxy_pass http://127.0.0.1:8501;
                proxy_http_version 1.1;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header Host $host;
                proxy_set_header Upgrade $http_upgrade;
                proxy_set_header Connection "upgrade";
            }
        }
    """).strip()
    # On échappe les $ pour le shell python
    nginx_cmd = f"echo '{nginx_conf}' | sudo tee /etc/nginx/conf.d/streamlit.conf"

    run_ssh_command(
        ssh, "sudo rm -f /etc/nginx/sites-enabled/default", "Nettoyage Nginx défaut"
    )
    run_ssh_command(ssh, nginx_cmd, "Configuration Nginx")

    # 6. Configuration Systemd
    service_conf = dedent("""
        [Unit]
        Description=Streamlit App
        After=network.target

        [Service]
        User=ubuntu
        WorkingDirectory=/home/ubuntu/lhist2532/labo
        EnvironmentFile=/home/ubuntu/lhist2532/labo/.env
        ExecStart=/home/ubuntu/lhist2532/labo/.venv/bin/streamlit run app.py
        Restart=always

        [Install]
        WantedBy=multi-user.target
    """).strip()
    service_cmd = (
        f"echo '{service_conf}' | sudo tee /etc/systemd/system/streamlit.service"
    )
    run_ssh_command(ssh, service_cmd, "Création du service Systemd")

    # 7. Démarrage final
    start_cmd = dedent("""
        sudo systemctl daemon-reload \
        && sudo systemctl enable streamlit \
        && sudo systemctl restart streamlit \
        && sudo systemctl restart nginx
    """).strip()
    run_ssh_command(ssh, start_cmd, "Démarrage des services")

    ssh.close()


def deploy():
    print("🏗️  Création de l'infrastructure AWS...")

    manage_ssh_key()

    # 1. Security Group
    try:
        sg = ec2.create_security_group(
            GroupName="Streamlit-SSH-SG", Description="SSH and HTTP"
        )
        sg_id = sg["GroupId"]
        ec2.authorize_security_group_ingress(
            GroupId=sg_id,
            IpPermissions=[
                {
                    "IpProtocol": "tcp",
                    "FromPort": 22,
                    "ToPort": 22,
                    "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
                },
                {
                    "IpProtocol": "tcp",
                    "FromPort": 80,
                    "ToPort": 80,
                    "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
                },
                {
                    "IpProtocol": "tcp",
                    "FromPort": 8501,
                    "ToPort": 8501,
                    "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
                },
            ],
        )
    except Exception:
        # Récupération si existe déjà
        res = ec2.describe_security_groups(GroupNames=["Streamlit-SSH-SG"])
        sg_id = res["SecurityGroups"][0]["GroupId"]

    # 2. Instance (Sans User Data compliqué !)
    print("🚀 Lancement de l'instance...")
    instances = ec2.run_instances(
        ImageId=AMI_ID,
        InstanceType=INSTANCE_TYPE,
        KeyName=KEY_NAME,
        MinCount=1,
        MaxCount=1,
        SecurityGroupIds=[sg_id],
        BlockDeviceMappings=[
            {
                "DeviceName": "/dev/sda1",  # Le nom standard pour Ubuntu
                "Ebs": {
                    "VolumeSize": 30,  # 30 Go (Maximum gratuit du Free Tier)
                    "VolumeType": "gp3",  # Plus performant et moins cher que gp2
                    "DeleteOnTermination": True,
                },
            },
        ],
        InstanceInitiatedShutdownBehavior="terminate",
    )
    instance_id = instances["Instances"][0]["InstanceId"]

    print("⏳ Attente que l'instance soit 'Running'...")
    waiter = ec2.get_waiter("instance_running")
    waiter.wait(InstanceIds=[instance_id])

    desc = ec2.describe_instances(InstanceIds=[instance_id])
    public_ip = desc["Reservations"][0]["Instances"][0]["PublicIpAddress"]

    print(f"✅ Instance prête : {public_ip}")

    # 3. On lance l'installation via SSH
    try:
        install_via_ssh(public_ip)
        print(f"\n🎉 TERMINÉ ! Application visible sur : http://{public_ip}")
    except Exception as e:
        print(f"\n❌ ECHEC de l'installation : {e}")


if __name__ == "__main__":
    deploy()
