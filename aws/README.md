# AWS

As the name suggests, this part of the repo is meant to manage the deployment
of the lab app on AWS so that it is made globally available to the students.

In order to deploy the app on AWS you will need an AWS authentication key 
which you create using the IAM service available from the AWS console.

You will also need a configuration file that holds all the necessary 
information regarding where you want your app to be deployed (and the secrets
you want to install on the spawned instance). That file is named `.env`, and 
mine looks like so:

```
# API KEYS
export SECRET__GOOGLE_API_KEY=<<use your own secret>>
export SECRET__MISTRAL_API_KEY=<<use your own secret>>
export SECRET__OPENAI_API_KEY=<<use your own secret>>
```

After that, you will need to configure aws to authenticate with your key.
And then, you will be able to deploy a complete instance by runnging the script.


```
uv tool install awscli
uv venv
source .venv/bin/activate

aws config

# everything is configured, all what is left to do now is the following:
python3 deployment.py
```
