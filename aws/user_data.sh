# This script is meant to automate the deployment of the lab on aws.
# For that purpose, you will need to go through the aws console and create
# a t2. or t3 micro which is elligible to the free offering.

# before anything
echo "######## UPDATE AND INSTALL ###########################"
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv git nginx

cd /home/ubuntu

# clone the repo
echo "######## CLONE THE REPO ###############################"
git clone https://github.com/xgillard/lhist2532.git
chown -R ubuntu:ubuntu lhist2532
cd lhist2532


echo "######## CREATE .ENV ##################################"
cat <<EOF > .env
# gemini 2.5
export MODELS__A__NAME=gemini-2.5-flash-lite
export MODELS__A__PROVIDER=google-genai

# mistral large
export MODELS__B__NAME=mistral-large
export MODELS__B__PROVIDER=mistralai

# openai
export MODELS__C__NAME=gpt-oss-20b
export MODELS__C__PROVIDER=openai

EOF

# 1st step: install uv
echo "######## INSTALL UV ##################################"
su - ubuntu -c "curl -LsSf https://astral.sh/uv/install.sh | sh"
su - ubuntu -c "
	export PATH=\$HOME/.cargo/bin:\$PATH
	    cd /home/ubuntu/lhist2532
	    uv venv
	    uv sync
"

cd ..

# configuration du reverse proxy ngnix
# On supprime la config par défaut pour éviter les conflits
echo "######## EDIT CONFIG ##################################"
rm -f /etc/nginx/conf.d/default.conf
rm -f /etc/nginx/sites-enabled/default

# On crée notre config proxy (prod)
cat <<EOF > /etc/nginx/conf.d/streamlit.conf
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header Host \$host;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 86400;
    }
}
EOF

# creation d'un script systemd pour faire démarrer l'appli en mode service
# nécessaire pour la production
cat <<EOF > /etc/systemd/system/streamlit.service
[Unit]
Description=IA et Archives
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/lhist2532
ExecStart=/home/ubuntu/lhist2532/.venv/bin/streamlit run app.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Lancer le service
echo "######## RESTART SYSTEMD ##################################"
sudo systemctl daemon-reload
sudo systemctl enable streamlit
sudo systemctl start streamlit
sudo systemctl enable nginx
sudo systemctl restart nginx

